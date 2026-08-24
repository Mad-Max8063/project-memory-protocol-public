# PMP handoff demo — Project Memory

> Canonical operational memory for the completed reference workspace.
> Protocol: PMP `0.1.1`

## Identity

- Project: `pmp-handoff-demo`
- Repository: `local demo workspace`
- Human authority: demo operator
- Default branch: `demo`
- Last updated: `2026-08-22`
- Last actor: `Codex`

## Current state

- [VERIFIED] `slugify.py` implements the six human-approved normalization rules, including the explicitly limited NFKD-decomposable Latin-diacritic behavior.
- [VERIFIED] `python -m unittest -v test_slugify.py` completed with six passing tests.
- [VERIFIED] No third-party runtime dependency was added.

## Active decisions

1. The six normalization rules in `../evidence/01-chatgpt-decision.md` remain active.
2. Keep the demo dependency-free.

## Constraints

- Do not weaken tests or change recorded behavior without a new human decision.
- Use the live runbook for independent agent-identity evidence.

## Priorities

1. Human review.
2. Live independent-session recording.

## Next action

`Human: review the passing artifact, then execute ../LIVE_DEMO_RUNBOOK.md on a disposable branch.`

## Evidence

- `../evidence/01-chatgpt-decision.md`
- `../evidence/02-codex-session.md`
- `.project-memory/sessions/2026-08-22-codex-slugify.md`
- `python ../verify_demo.py`

## Update rules

- Read this file before significant work.
- Update it only when operational state, a decision, a constraint, a priority, or the next action changes.
- Keep history in `.project-memory/sessions/`.
- Never store secrets or unnecessary personal data.
- Apply PMP source precedence.
