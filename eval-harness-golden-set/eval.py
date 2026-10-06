"""Golden-set eval harness. The model under test is a deterministic stub so CI needs no API key."""
import json, pathlib, sys

THRESHOLD = 0.85
RULES = [("cancel", ("cancel",)), ("billing", ("charged", "refund", "invoice", "payment", "card")),
         ("shipping", ("where", "parcel", "late", "tracking", "arrived"))]


def classify(text):  # swap for a real LLM call; the harness does not care
    t = text.lower()
    return next((label for label, words in RULES if any(w in t for w in words)), "other")


def run(path):
    rows = [json.loads(l) for l in pathlib.Path(path).read_text().splitlines() if l.strip()]
    results = [(r["id"], r["expected"], classify(r["input"])) for r in rows]
    failures = [x for x in results if x[1] != x[2]]
    return len(results), failures


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    total, failures = run(here / "golden.jsonl")
    acc = (total - len(failures)) / total
    for i, exp, got in failures:
        print(f"FAIL {i}: expected={exp} got={got}")
    print(f"accuracy={acc:.2f} threshold={THRESHOLD} n={total}")
    sys.exit(0 if acc >= THRESHOLD else 1)
