# PMP live handoff seed

This directory is the complete starting state for an isolated live demonstration. Copy **only its contents** into a new disposable repository. Do not copy the completed fixtures or evidence from the parent PMP repository.

The seed intentionally contains:

- human-authored requirements;
- six executable tests;
- an unimplemented function;
- initial canonical project memory;
- repository instructions for the ChatGPT and Codex phases;
- a verifier that cannot pass until both handoffs are complete.

It intentionally does not contain:

- the implementation;
- ChatGPT decision evidence;
- a Codex session record;
- expected final memory;
- completed before/after fixtures.

The behavior in `TASK.md` deliberately limits accent handling to Unicode NFKD normalization followed by removal of remaining non-ASCII code points. It is not a general transliteration requirement.

## Baseline check

At the initial commit, this command MUST fail because the function is unimplemented and the two handoff artifacts do not exist:

```bash
python verify_demo.py
```

That failure is evidence that the answer was not packaged into the seed.
