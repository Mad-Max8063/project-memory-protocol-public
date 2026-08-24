# Verifiable ChatGPT -> Codex -> ChatGPT handoff

This example demonstrates the protocol boundary without depending on private chat memory.

It remains a PMP `0.1.1` compatibility fixture with preserved evidence. Core `0.2.1`
does not change its canonical headings or executable slugify contract, so the
continues to verify it without rewriting history.

## Scenario

1. ChatGPT records a human-approved behavior for a tiny `slugify` function in canonical memory.
2. A fresh Codex session reads only the repository instructions, memory, and task evidence.
3. Codex implements the function, runs six tests, updates canonical memory, and writes a session record.
4. ChatGPT returns later, reads the repository state, and verifies the handoff without the user restating the decision.

The included repository is in the completed state. `fixtures/before/` and `fixtures/after/` are immutable snapshots used to verify that the operational state changed as claimed.

## Slug behavior scope

The example uses this exact sequence: trim, lowercase, Unicode NFKD normalization, discard remaining non-ASCII code points, collapse separator runs, and trim edge hyphens. It converts Latin letters with decomposable diacritics, such as `ó`, to ASCII. It intentionally does not claim general transliteration for every Latin or non-Latin character.

## Run the deterministic verification

From the protocol repository root:

```bash
python examples/chatgpt-codex-handoff/verify_demo.py
```

The verifier:

- validates both PMP memory snapshots;
- checks that the actor changes from ChatGPT to Codex;
- checks that the next action advances;
- checks the evidence chain;
- executes the final workspace's six tests.

This proves internal consistency and reproducibility of the included artifact. It does **not** prove the identity of an external agent. For a public end-to-end proof with independent agent sessions and Git timestamps, follow [LIVE_DEMO_RUNBOOK.md](LIVE_DEMO_RUNBOOK.md).

## Evidence chain

```text
Human decision
    -> evidence/01-chatgpt-decision.md
    -> fixtures/before/PROJECT_MEMORY.md
    -> fresh Codex implementation
    -> evidence/02-codex-session.md
    -> fixtures/after/PROJECT_MEMORY.md
    -> evidence/03-chatgpt-verification.md
```
