# prompt-injection-tests

`injection_test.py` attacks a toy support agent that holds a canary secret, with and without input and output guards.

## Goal

Treat prompt injection as a regression test suite. The agent is a stub with a canary string in its pretend system prompt. It is attacked with direct and document-borne injections; the guarded variant must never leak the canary while benign requests still work.

## Run it

```bash
python3 injection_test.py
```

Expected output: unittest prints `Ran 5 tests` and `OK`; the exit code is 0 when they pass.

## What it proves

- `naive_agent` leaks the canary on the first attack, so the attack corpus in `ATTACKS` is real and the other tests mean something.
- `guarded_agent` combines an input guard (regex, also applied to `retrieved_doc`) with an output guard that redacts the canary. A test forces a leaking model to show the output guard working alone.
- Retrieved documents are treated as untrusted input and are blocked by the same guard.

## Trade-offs

- Regex guards are easy to bypass (paraphrase, encoding, other languages); real systems add classifiers, privilege separation and least-privilege tools.
- The agent is a stub, so this tests the test pattern, not the robustness of a real model.
- Canary checks detect leaks of known secrets only, not harmful actions.

## When not to use it

- As the only defence. If an agent has powerful tools, rely on architecture (sandboxing, human approval) rather than string matching.
- When the agent has no secrets and no tools; the risk is smaller and the suite adds little.
