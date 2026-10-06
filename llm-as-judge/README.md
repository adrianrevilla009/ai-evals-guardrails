# llm-as-judge

Ten human-labelled question and answer pairs (`labeled.jsonl`) and `judge.py`, which compares a stub judge with those labels.

## Goal

Show that an automatic judge must be calibrated against human labels before it is trusted. `judge.py` scores each answer pass or fail and reports raw agreement and Cohen's kappa. The judge is a keyword-overlap stub so it runs offline; swap `judge()` for an LLM call with a rubric prompt.

## Run it

```bash
python3 judge.py
```

Expected output:

```
agreement=1.00 kappa=1.00 min_kappa=0.6
```

The exit code is 0 when kappa is at least 0.6 and 1 otherwise. Each mismatch is printed as `DISAGREE <id>: human=... judge=...`.

## What it proves

- On the 10 labelled items the stub judge agrees with the human labels on all 10 (kappa 1.00), so the gate passes.
- `kappa()` corrects agreement for chance, so a judge that always answers "pass" would score a kappa near zero.
- Disagreements are listed per case id, so the rubric or the labels can be fixed.

## Trade-offs

- Ten items is far too few for a stable kappa; aim for 100 or more and several annotators.
- The stub is lexical. A real LLM judge adds cost, latency and its own biases, such as position and verbosity.
- Kappa on skewed labels can be misleadingly low; also look at the confusion matrix, which this folder does not compute.
- No real LLM judge was run; only the stub is exercised.

## When not to use it

- When a deterministic check works (exact match, schema validation, regex).
- When there are no human labels to calibrate against; an uncalibrated judge gives false confidence.
