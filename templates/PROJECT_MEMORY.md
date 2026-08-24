# <Project name> — Project Memory

> Canonical operational memory shared by humans and compatible agents.
> Protocol: PMP `0.2.1`
> Canonical path: `PROJECT_MEMORY.md`

## Identity

- Project: `<name>`
- Repository: `<owner/repository or local identifier>`
- Human authority: `<person or team>`
- Default branch: `<branch>`
- Last updated: `<YYYY-MM-DD>`
- Last actor: `<human, agent, or tool>`

## Current state

- [VERIFIED] `<fact checked during this session, with concise scope>`
- [DOCUMENTED] `<fact inherited from evidence but not revalidated now>`
- [ASSUMED] `<hypothesis that must be checked before consequential action>`

## Active decisions

1. `<current decision and, when useful, who made it and when>`

## Constraints

- `<what must not change or what requires explicit approval>`
- `<for connected systems, consequential adjacent actions that remain unauthorized>`

## Priorities

1. `<highest-priority outcome>`
2. `<next outcome>`

## Next action

`<one exact, executable next action; include the evidence or gate that defines completion>`

## Evidence

- `<commit, PR, issue, test report, runbook, deployment record, or document>`

## Update rules

- Read this file before significant work.
- Update it only when current state, a decision, a constraint, a priority, or the next action changes.
- Keep current truth here; move historical detail to `.project-memory/sessions/`.
- Never store secrets, credentials, tokens, private keys, `.env` values, or unnecessary personal data.
- Use `[VERIFIED]`, `[DOCUMENTED]`, and `[ASSUMED]` exactly as defined by PMP.
- Resolve conflicts using: latest authorized human instruction -> current verified evidence -> this file -> specialized documentation -> session history -> private model memory.
