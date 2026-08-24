# Repository instructions

This repository conforms to PMP `0.2.1` as both Reader and Writer.
Operational tag, release, publication, and visibility state is recorded only
in canonical memory.

Canonical memory: `PROJECT_MEMORY.md` in the repository root

Before significant analysis or changes, read the canonical memory and relevant repository evidence. Verify claims marked `[DOCUMENTED]` or `[ASSUMED]` before relying on them for consequential actions.

For bounded work, state the allowed scope and preserve consequential exclusions
for merge, release, deployment, infrastructure, database, credentials,
environment, visibility, or publication until the human authority changes them.
Do not remediate adjacent findings without separate authority.

When work changes current state, a decision, a constraint, a priority, or the next action, update canonical memory and add a session record when historical detail is useful. Never store secrets, credentials, `.env` values, or unnecessary personal data.

Source precedence: latest authorized human instruction -> current verified evidence -> canonical memory -> specialized documentation -> session history -> private model memory. Verify or escalate unresolved same-level conflicts.

Keep the protocol vendor-neutral. Adapters may describe tool-specific instruction surfaces, but MUST NOT duplicate current project state.
