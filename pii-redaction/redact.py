"""Regex PII redaction applied before text is sent to a model or written to logs. Run: python3 redact.py"""
import re, sys, unittest

PATTERNS = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}(?: ?[A-Z0-9]{1,4})?\b")),
    ("CARD", re.compile(r"\b\d(?:[ -]?\d){12,15}\b")),
    ("PHONE", re.compile(r"\+\d[\d ()-]{7,}\d")),
]


def luhn(digits):
    s = [int(d) for d in digits][::-1]
    return (sum(s[0::2]) + sum(sum(divmod(2 * d, 10)) for d in s[1::2])) % 10 == 0


def redact(text):
    for label, rx in PATTERNS:
        def sub(m, label=label):
            if label == "CARD" and not luhn(re.sub(r"\D", "", m.group())):
                return m.group()  # order numbers etc. are not cards
            return f"[{label}]"
        text = rx.sub(sub, text)
    return text


class RedactTests(unittest.TestCase):
    def test_email(self):
        self.assertEqual(redact("mail ana.p@example.com now"), "mail [EMAIL] now")

    def test_card_with_valid_luhn(self):
        self.assertEqual(redact("card 4111 1111 1111 1111 ok"), "card [CARD] ok")

    def test_order_number_is_kept(self):
        self.assertEqual(redact("order 1234567890123 shipped"), "order 1234567890123 shipped")

    def test_iban(self):
        self.assertEqual(redact("pay DE89 3704 0044 0532 0130 00"), "pay [IBAN]")

    def test_phone(self):
        self.assertEqual(redact("call +34 600 123 456"), "call [PHONE]")

    def test_idempotent(self):
        once = redact("ana@example.com +34 600 123 456")
        self.assertEqual(redact(once), once)


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
