# Project instruction — Project Memory Protocol (PMP 0.2.1)

When repository access is available, use the repository-root `PROJECT_MEMORY.md` as the canonical operational state for this project.

Before giving state-dependent advice or proposing significant changes:

1. Read canonical memory.
2. Inspect only the evidence relevant to the request.
3. Revalidate task-critical technical or external state when possible.
4. Clearly label anything still documented or assumed rather than verified.
5. Preserve allowed scope and consequential exclusions for bounded work.

After an authorized decision or repository-visible action changes operational state, update canonical memory if repository writes are available. Otherwise, produce an exact proposed memory patch for the human or repository agent to apply. Keep useful history in `.project-memory/sessions/` and never store secrets or unnecessary personal data.

Record adjacent findings as risks or follow-up evidence. Do not remediate them
unless the authorized scope separately permits it.

Conflict precedence: latest authorized human instruction -> current verified evidence -> canonical memory -> specialized documentation -> session history -> conversational memory. Do not silently resolve same-level contradictions.
