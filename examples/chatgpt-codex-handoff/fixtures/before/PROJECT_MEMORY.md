# PMP handoff demo — Project Memory

> Canonical operational memory snapshot before the Codex handoff.
> Protocol: PMP `0.1.1`

## Identity

- Project: `pmp-handoff-demo`
- Repository: `local demo fixture`
- Human authority: demo operator
- Default branch: `demo`
- Last updated: `2026-08-22`
- Last actor: `ChatGPT`

## Current state

- [VERIFIED] The human-approved slug behavior is recorded in `../../evidence/01-chatgpt-decision.md`.
- [VERIFIED] ChatGPT did not implement `slugify.py`.
- [DOCUMENTED] The test file defines six expected behaviors and has not yet been run against an implementation.

## Active decisions

1. Implement the six normalization rules exactly as recorded in the decision evidence.
2. Keep the demo dependency-free.

## Constraints

- Do not change the test expectations to make an implementation pass.
- Do not use third-party packages.
- Do not ask the human to restate the prior ChatGPT conversation.

## Priorities

1. Implement `slugify.py` from canonical memory and linked evidence.
2. Run all tests and record evidence.

## Next action

`Codex: implement workspace/slugify.py, run python -m unittest -v test_slugify.py from workspace/, then perform the PMP END update.`

## Evidence

- `../../evidence/01-chatgpt-decision.md`
- `../../workspace/TASK.md`
- `../../workspace/test_slugify.py`

## Update rules

- Read this file before significant work.
- Update it only when operational state, a decision, a constraint, a priority, or the next action changes.
- Keep history outside canonical memory.
- Never store secrets or unnecessary personal data.
- Apply PMP source precedence.
