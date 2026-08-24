## Project Memory Protocol (PMP 0.2.1)

Canonical memory: `PROJECT_MEMORY.md` in the repository root

Before significant analysis or changes:

1. Read the canonical memory and relevant repository instructions.
2. Verify branch, revision, worktree, and external state when the task depends on them.
3. Treat `[DOCUMENTED]` and `[ASSUMED]` claims as unverified.
4. Surface conflicts with active constraints before acting.
5. Confirm the allowed scope and consequential exclusions for bounded work.

When work changes current state, a decision, a constraint, a priority, or the next action:

1. Update canonical memory to current truth only.
2. Add evidence; never promote a hypothesis to `[VERIFIED]` without checking it.
3. Add `.project-memory/sessions/YYYY-MM-DD-topic.md` when historical detail helps the next participant.
4. Never store secrets, credentials, `.env` values, or unnecessary personal data.
5. Record adjacent findings without treating them as authorization to expand scope.

Source precedence: latest authorized human instruction -> current verified evidence -> canonical memory -> specialized documentation -> session history -> private model memory. Verify or escalate same-level conflicts; do not guess.
