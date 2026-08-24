# PMP handoff demo — Project Memory

> Canonical operational memory snapshot after the Codex handoff.
> Protocol: PMP `0.1.1`

## Identity

- Project: `pmp-handoff-demo`
- Repository: `local demo fixture`
- Human authority: demo operator
- Default branch: `demo`
- Last updated: `2026-08-22`
- Last actor: `Codex`

## Current state

- [VERIFIED] `workspace/slugify.py` implements the six human-approved normalization rules, including the explicitly limited NFKD-decomposable Latin-diacritic behavior.
- [VERIFIED] `python -m unittest -v test_slugify.py` completed with six passing tests.
- [VERIFIED] No third-party runtime dependency was added.

## Active decisions

1. The six normalization rules recorded in `../../evidence/01-chatgpt-decision.md` remain active.
2. Keep the demo dependency-free.

## Constraints

- Do not weaken the tests or change the recorded behavior without a new human decision.
- Do not treat this reference fixture as proof of an external agent's identity; use the live runbook for that evidence.

## Priorities

1. Have a human review the completed demo artifact.
2. Record a live independent-session demo with Git timestamps.

## Next action

`Human: review the passing artifact, then execute LIVE_DEMO_RUNBOOK.md on a disposable branch to capture independent-session evidence.`

## Evidence

- `../../evidence/01-chatgpt-decision.md`
- `../../evidence/02-codex-session.md`
- `../../workspace/.project-memory/sessions/2026-08-22-codex-slugify.md`
- executable check: `python examples/chatgpt-codex-handoff/verify_demo.py`

## Update rules

- Read this file before significant work.
- Update it only when operational state, a decision, a constraint, a priority, or the next action changes.
- Keep history outside canonical memory.
- Never store secrets or unnecessary personal data.
- Apply PMP source precedence.
