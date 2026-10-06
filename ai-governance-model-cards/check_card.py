"""Fail CI when a model card is missing required sections or still has placeholders. Run: python3 check_card.py [card.md]"""
import pathlib, re, sys

REQUIRED = ["Model details", "Intended use", "Training and evaluation data", "Metrics",
            "Risks and limitations", "Safeguards", "EU AI Act classification", "Change log"]
RISK_TIERS = ("unacceptable", "high risk", "high-risk", "limited risk", "minimal risk")


def check(text):
    errors = [f"missing section: {s}" for s in REQUIRED if not re.search(rf"^##\s+{re.escape(s)}\s*$", text, re.M)]
    if not any(t in text.lower() for t in RISK_TIERS):
        errors.append("no EU AI Act risk tier stated")
    if re.search(r"\b(TBD|FIXME|lorem)\b", text, re.I):
        errors.append("placeholder text left in card")
    return errors


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent / "MODEL_CARD.md")
    errs = check(path.read_text())
    print("\n".join(errs) or f"{path.name}: ok")
    sys.exit(1 if errs else 0)
