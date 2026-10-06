# ai-governance-model-cards

A model card for the example orders assistant (`MODEL_CARD.md`) and `check_card.py`, which lints it.

## Goal

Keep a model card in git next to the code and check it in CI. The card covers model details, intended use, data, metrics, risks, safeguards, an EU AI Act classification and a change log.

## Run it

```bash
python3 check_card.py            # checks MODEL_CARD.md
python3 check_card.py other.md   # checks another file
```

Expected output: `MODEL_CARD.md: ok` and exit code 0. Otherwise each problem is printed, for example `missing section: Metrics`, and the exit code is 1.

## What it proves

- The checker requires eight `##` sections, a stated risk tier (such as limited risk) and no `TBD`, `FIXME` or `lorem` text.
- The Metrics section cites the gates in the other folders (accuracy 0.85, kappa 0.6, zero canary leaks), so claims point to evidence.
- The card classifies the assistant as limited risk (transparency duty) and notes that Annex III uses would be high risk.

## Trade-offs

- The check verifies structure, not truth; a reviewer must still read the card.
- The risk classification is an informal awareness note, not legal advice.
- Cards go stale unless a change to the model or prompt forces a card update in the same pull request.

## When not to use it

- For regulated high-risk systems, which need a full conformity assessment, technical documentation and legal review rather than a one-page card.
