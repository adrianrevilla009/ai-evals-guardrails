# langfuse-otel-genai

`trace.py` builds an OTLP/JSON span with GenAI attributes; `compose.yaml` and `otel-collector.yaml` run a collector that forwards it to Langfuse.

## Goal

Send GenAI traces (model, token usage, latency) using OpenTelemetry GenAI semantic-convention attributes, through an OpenTelemetry Collector, to Langfuse's OTLP endpoint. `trace.py` uses only the standard library.

## Run it

Offline check, validates the required `gen_ai.*` attributes and prints the payload:

```bash
python3 trace.py
```

Expected output: the start of the JSON payload, then `valid GenAI span (dry run; set OTLP_ENDPOINT to send)`.

Full path, needs Docker and a Langfuse project (Langfuse Cloud free tier is enough):

```bash
cp .env.example .env            # set LANGFUSE_HOST and LANGFUSE_BASIC_AUTH; never commit .env
docker compose up -d
OTLP_ENDPOINT=http://localhost:4318 python3 trace.py
docker compose down -v          # destroy step
```

Not run end to end: the collector, the POST and delivery to Langfuse were not executed; only the offline dry run was. Langfuse itself is not bundled, because its self-hosted stack (Postgres, ClickHouse, Redis, S3) is too large for this folder; use Langfuse Cloud or its official compose file.

## What it proves

- The span carries `gen_ai.operation.name`, `gen_ai.request.model` and `gen_ai.usage.input_tokens`/`output_tokens`, and `validate()` fails if one is missing.
- `otel-collector.yaml` takes OTLP/HTTP on port 4318 and exports to `${LANGFUSE_HOST}/api/public/otel` plus a debug exporter.
- Credentials come from `.env` (template in `.env.example`) into the collector, not into application code.

## Trade-offs

- GenAI semantic conventions are still experimental; attribute names may change.
- Hand-built OTLP JSON is for learning; use the OpenTelemetry SDK in real services.
- Prompts and completions in traces are sensitive; combine with `pii-redaction`.

## When not to use it

- If a vendor SDK already gives you traces.
- If traffic is too low to justify running a collector.
