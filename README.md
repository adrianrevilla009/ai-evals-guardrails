# ai-evals-guardrails

Small, offline examples of how to test and guard an LLM feature: golden-set evals, judge calibration, injection tests, PII redaction, cost limits, GenAI tracing and a model card check. They use a tiny Orders support assistant as the shared example, and the models are deterministic stubs, so no API key is needed.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`eval-harness-golden-set`](./eval-harness-golden-set) | Golden set run with an accuracy gate (exit code) | `python3 eval.py` |
| [`llm-as-judge`](./llm-as-judge) | Judge verdicts compared with human labels (agreement, Cohen's kappa) | `python3 judge.py` |
| [`prompt-injection-tests`](./prompt-injection-tests) | Direct and document-borne injection tests with input and output guards | `python3 injection_test.py` |
| [`pii-redaction`](./pii-redaction) | Regex redaction of emails, IBANs, cards (Luhn) and phones | `python3 redact.py` |
| [`cost-limits`](./cost-limits) | Per-request token cap and daily spend cap checked before each call | `python3 budget.py` |
| [`langfuse-otel-genai`](./langfuse-otel-genai) | OTLP span with GenAI attributes, collector config forwarding to Langfuse | `python3 trace.py` |
| [`ai-governance-model-cards`](./ai-governance-model-cards) | Model card in git, checked for required sections and a risk tier | `python3 check_card.py` |

## Prerequisites

- Python 3 (standard library only) for every folder.
- Docker with Compose, plus a Langfuse project (Cloud free tier is enough), only for the optional full path in `langfuse-otel-genai`.

## How to read it

Start with `eval-harness-golden-set`, then `llm-as-judge`; the other folders are independent. `ai-governance-model-cards` refers to the gates in the others.
