"""Emit one OTLP/JSON trace for an LLM call using OpenTelemetry GenAI semantic-convention attributes.
Stdlib only. Without OTLP_ENDPOINT it validates and prints the payload; with it, it POSTs to /v1/traces."""
import json, os, secrets, sys, time, urllib.request

REQUIRED = {"gen_ai.operation.name", "gen_ai.system", "gen_ai.request.model",
            "gen_ai.usage.input_tokens", "gen_ai.usage.output_tokens"}


def attr(k, v):
    return {"key": k, "value": {"intValue": str(v)} if isinstance(v, int) else {"stringValue": v}}


def build_span(prompt_tokens=120, completion_tokens=40):
    start = time.time_ns()
    attrs = {"gen_ai.operation.name": "chat", "gen_ai.system": "stub-provider", "gen_ai.request.model": "stub-1",
             "gen_ai.usage.input_tokens": prompt_tokens, "gen_ai.usage.output_tokens": completion_tokens,
             "app.order.id": "1001"}
    span = {"traceId": secrets.token_hex(16), "spanId": secrets.token_hex(8), "name": "chat stub-1", "kind": 3,
            "startTimeUnixNano": str(start), "endTimeUnixNano": str(start + 250_000_000),
            "attributes": [attr(k, v) for k, v in attrs.items()]}
    return {"resourceSpans": [{"resource": {"attributes": [attr("service.name", "orders-assistant")]},
                               "scopeSpans": [{"scope": {"name": "ai-evals-guardrails"}, "spans": [span]}]}]}


def validate(payload):
    span = payload["resourceSpans"][0]["scopeSpans"][0]["spans"][0]
    missing = REQUIRED - {a["key"] for a in span["attributes"]}
    if missing:
        raise SystemExit(f"missing GenAI attributes: {sorted(missing)}")


if __name__ == "__main__":
    payload = build_span()
    validate(payload)
    endpoint = os.environ.get("OTLP_ENDPOINT")  # e.g. http://localhost:4318
    if not endpoint:
        print(json.dumps(payload)[:300] + "...\nvalid GenAI span (dry run; set OTLP_ENDPOINT to send)")
        sys.exit(0)
    req = urllib.request.Request(endpoint + "/v1/traces", json.dumps(payload).encode(), {"Content-Type": "application/json"})
    print("sent, status", urllib.request.urlopen(req, timeout=5).status)
