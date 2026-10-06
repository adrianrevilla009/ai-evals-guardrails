# pii-redaction

`redact.py` holds a regex-based `redact()` function for emails, IBANs, card numbers and phone numbers, plus six unit tests.

## Goal

Remove personal data from text before it reaches a model, a trace or a log. Standard library only; `redact()` replaces matches with placeholders such as `[EMAIL]`, `[IBAN]`, `[CARD]` and `[PHONE]`.

## Run it

```bash
python3 redact.py
```

Expected output: unittest prints `Ran 6 tests` and `OK`; the exit code is 0 when they pass.

## What it proves

- Card candidates must pass the Luhn checksum, so `order 1234567890123 shipped` is left unchanged while `4111 1111 1111 1111` becomes `[CARD]`.
- Redaction is idempotent: running it on already redacted text returns the same text, so it can be applied at every boundary.
- Each pattern has its own test in `RedactTests`, so a regex change shows its effect immediately.

## Trade-offs

- Regexes miss names, addresses and free-form identifiers; an NER-based tool such as Microsoft Presidio covers more.
- Phone numbers are only detected in international `+` format, to avoid consuming long digit strings.
- Placeholders lose information; reversible tokenisation needs a vault and strict access control.

## When not to use it

- As the only privacy control. It does not make a system GDPR-compliant; minimise data collection and agree data-processing terms with providers as well.
