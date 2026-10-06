"""Per-request and per-day token/cost budget enforced before each LLM call. Run: python3 budget.py"""
import sys, unittest

PRICE_PER_1K = {"in": 0.0005, "out": 0.0015}  # illustrative USD prices, not a real rate card


class BudgetExceeded(Exception):
    pass


class Budget:
    def __init__(self, max_request_tokens=2000, max_daily_usd=0.01):
        self.max_request_tokens, self.max_daily_usd, self.spent = max_request_tokens, max_daily_usd, 0.0

    def cost(self, tokens_in, tokens_out):
        return tokens_in / 1000 * PRICE_PER_1K["in"] + tokens_out / 1000 * PRICE_PER_1K["out"]

    def check(self, tokens_in, max_out):
        """Call BEFORE the request, using the worst case (max_out) so the limit cannot be overshot."""
        if tokens_in + max_out > self.max_request_tokens:
            raise BudgetExceeded("request too large")
        if self.spent + self.cost(tokens_in, max_out) > self.max_daily_usd:
            raise BudgetExceeded("daily budget exhausted")

    def record(self, tokens_in, tokens_out):
        self.spent += self.cost(tokens_in, tokens_out)


class BudgetTests(unittest.TestCase):
    def test_oversized_request_rejected(self):
        with self.assertRaises(BudgetExceeded):
            Budget().check(1900, 500)

    def test_daily_limit_stops_the_loop(self):
        b, calls = Budget(), 0
        try:
            while True:
                b.check(1000, 500)
                b.record(1000, 500)  # 0.00125 USD each
                calls += 1
        except BudgetExceeded as e:
            self.assertEqual(str(e), "daily budget exhausted")
        self.assertEqual(calls, 8)

    def test_spend_never_exceeds_limit(self):
        b = Budget()
        for _ in range(50):
            try:
                b.check(1000, 500)
                b.record(1000, 500)
            except BudgetExceeded:
                break
        self.assertLessEqual(b.spent, b.max_daily_usd)


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
