# PMP live handoff demo — Project Memory

> Canonical operational memory for an isolated live demonstration.
> Protocol: PMP `0.1.1`
> Canonical path: `PROJECT_MEMORY.md`

## Identity

- Project: `pmp-live-handoff-demo`
- Repository: `<set after disposable repository creation>`
- Human authority: Max / demo operator
- Default branch: `main`
- Last updated: `2026-08-22`
- Last actor: `demo operator`

## Current state

- [VERIFIED] `TASK.md` contains the human-authored behavior for `slugify`.
- [VERIFIED] `test_slugify.py` contains six executable acceptance tests.
- [VERIFIED] `slugify.py` is intentionally unimplemented and the test suite fails with `NotImplementedError`.
- [VERIFIED] No ChatGPT decision evidence or Codex session record exists in this seed.

## Active decisions

1. ChatGPT must convert the requirements in `TASK.md` into active project decisions before implementation begins.
2. The ChatGPT phase is documentation-only; Codex owns the implementation phase.

## Constraints

- Do not paste prior conversation context into either agent session.
- Do not modify `slugify.py` or the tests during the ChatGPT phase.
- Do not weaken or replace the human-authored acceptance tests.
- Use only the Python standard library.

## Priorities

1. Record the human requirements as canonical active decisions.
2. Produce a context-free handoff to a fresh Codex session.

## Next action

`ChatGPT: read TASK.md, record its requirements as active decisions in PROJECT_MEMORY.md, create evidence/01-chatgpt-decision.md, and hand off one exact implementation action to Codex. Do not implement code.`

## Evidence

- `TASK.md`
- `test_slugify.py`
- baseline command: `python verify_demo.py` fails before either handoff

## Update rules

- Read this file before significant work.
- Update it only when current state, a decision, a constraint, a priority, or the next action changes.
- Keep historical detail in `.project-memory/sessions/`.
- Never store secrets or unnecessary personal data.
- Use `[VERIFIED]`, `[DOCUMENTED]`, and `[ASSUMED]` as defined by PMP.
- Apply PMP source precedence.
