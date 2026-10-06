# eval-harness-golden-set

A golden set of eight labelled support requests (`golden.jsonl`) and a harness (`eval.py`) that scores a stub classifier against it.

## Goal

Run inputs with expected labels through a model and fail the build when accuracy drops below a threshold. The model is a rule-based stub in `classify()`, so the harness runs offline; replace it with a real LLM call to evaluate a prompt.

## Run it

```bash
python3 eval.py
```

Expected output:

```
accuracy=1.00 threshold=0.85 n=8
```

The exit code is 0 when accuracy is at least 0.85 and 1 otherwise. Failing cases are printed as `FAIL <id>: expected=... got=...`.

## What it proves

- A golden set in git acts as a regression test: all 8 cases in `golden.jsonl` pass with the current rules.
- The gate is a plain exit code, so any CI system can enforce it.
- Failures print the case id, expected label and actual label, enough to start debugging.

## Trade-offs

- Eight cases is a demo; real sets need hundreds, including edge cases.
- Exact-match labels only work for classification; free text needs a judge (see `llm-as-judge`).
- A fixed threshold ignores run-to-run noise from real, non-deterministic models.
- The stub is deterministic, so this does not show how a real model behaves. Nothing here calls an LLM.

## When not to use it

- When outputs are open-ended and cannot be reduced to labels.
- When there is no trusted ground truth yet; collect and label production samples first.
