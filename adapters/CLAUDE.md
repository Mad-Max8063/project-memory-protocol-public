## Project Memory Protocol (PMP 0.2.1)

Use the repository-root `PROJECT_MEMORY.md` as the project's canonical operational memory.

- At START, read it before significant work, then verify any branch, revision, test, deployment, or infrastructure state the task relies on.
- DURING, distinguish `[VERIFIED]`, `[DOCUMENTED]`, and `[ASSUMED]` claims and respect active decisions and constraints.
- For bounded work, preserve allowed scope and consequential exclusions; record adjacent findings without silently remediating them.
- At END, update it only if operational state changed. Preserve current truth, add evidence, and move useful history to `.project-memory/sessions/YYYY-MM-DD-topic.md`.
- Never store secrets, credentials, `.env` values, or unnecessary personal data.

Resolve conflicts in this order: latest authorized human instruction -> current verified evidence -> canonical memory -> specialized documentation -> session history -> private model memory. Verify or escalate unresolved same-level conflicts.
