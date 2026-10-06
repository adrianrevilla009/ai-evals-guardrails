# Model card: orders-assistant

## Model details
- System: customer-support assistant for the Orders domain (classifies requests, drafts replies).
- Underlying model: hosted LLM, version pinned in configuration (example: `stub-1`). Owner: support-platform team.

## Intended use
- Answer order status, shipping, billing and cancellation questions; a human agent reviews anything involving refunds.
- Out of scope: legal or medical advice, credit decisions, employment decisions.

## Training and evaluation data
- Not trained by us. Evaluated on a golden set of labelled support requests (`eval-harness-golden-set`) and calibrated judge scores (`llm-as-judge`).

## Metrics
- Classification accuracy on the golden set, gate 0.85. Judge/human agreement (kappa) gate 0.6.
- Prompt-injection suite must pass with zero canary leaks.

## Risks and limitations
- May hallucinate order details; answers must come from the order API, not from model memory.
- Prompt injection through order notes or retrieved documents.
- Personal data in prompts and traces; mitigated by redaction.

## Safeguards
- PII redaction before model calls and tracing, token and daily cost budgets, GenAI traces for audit.

## EU AI Act classification
- Risk tier: limited risk (a chatbot interacting with people), so the transparency duty applies: tell users they are talking to an AI.
- Not a high-risk use under Annex III as scoped above; re-assess if the scope changes (for example credit scoring).

## Change log
- 2026-10-04: initial version.
