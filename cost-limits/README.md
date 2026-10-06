# cost-limits

A `Budget` class in `budget.py` that enforces a per-request token cap and a daily spend cap, with three unit tests.

## Goal

Stop an LLM caller from overspending. `Budget.check()` runs before each request and uses the worst case (input tokens plus maximum output tokens), so spend cannot overshoot the limit. Prices in `PRICE_PER_1K` are illustrative, not a real rate card.

## Run it

```bash
python3 budget.py
```

Expected output: unittest prints `Ran 3 tests` and `OK`; the exit code is 0 when they pass.

## What it proves

- A request of 1900 input plus 500 output tokens exceeds the 2000-token cap and raises `BudgetExceeded("request too large")` before any spend.
- A loop of 1000-in, 500-out calls is stopped with "daily budget exhausted" after exactly 8 calls at the demo prices and the 0.01 USD limit.
- Recorded spend never exceeds `max_daily_usd`, even over 50 attempts.

## Trade-offs

- State is in memory; a real service needs a shared store (for example Redis) and per-user or per-tenant keys.
- Worst-case reservation is conservative and rejects some requests that would have fit.
- Token counts come from the caller; in practice use the provider's tokenizer or response usage fields.

## When not to use it

- As a replacement for provider-side spend limits and billing alerts; set those as a second layer.
