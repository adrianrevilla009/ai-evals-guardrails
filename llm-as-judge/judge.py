"""LLM-as-judge calibration: compare judge verdicts with human labels using agreement and Cohen's kappa."""
import json, pathlib, sys

MIN_KAPPA = 0.6


def judge(question, answer):  # stub judge; replace with an LLM call that returns "pass" or "fail"
    words = {w.strip("?.,!").lower() for w in question.split() if len(w) > 3}
    hits = sum(w in answer.lower() for w in words)
    return "pass" if hits >= max(1, len(words) // 2) else "fail"


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in set(a) | set(b))
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


if __name__ == "__main__":
    rows = [json.loads(l) for l in (pathlib.Path(__file__).parent / "labeled.jsonl").read_text().splitlines() if l.strip()]
    human = [r["human"] for r in rows]
    model = [judge(r["question"], r["answer"]) for r in rows]
    agree = sum(h == m for h, m in zip(human, model)) / len(rows)
    k = kappa(human, model)
    for r, m in zip(rows, model):
        if r["human"] != m:
            print(f"DISAGREE {r['id']}: human={r['human']} judge={m}")
    print(f"agreement={agree:.2f} kappa={k:.2f} min_kappa={MIN_KAPPA}")
    sys.exit(0 if k >= MIN_KAPPA else 1)
