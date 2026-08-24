# Live handoff demo instructions

This repository conforms to PMP `0.1.1`.

Canonical memory: repository-root `PROJECT_MEMORY.md`

Before acting, read `PROJECT_MEMORY.md`, `TASK.md`, and the exact next action. Do not use context from another repository or conversation.

## Phase contract

- If the next action names **ChatGPT**, translate the human-authored requirements into active decisions and evidence. Do not implement `slugify.py`, do not change tests, and do not claim they pass. Create `evidence/01-chatgpt-decision.md`, set `Last actor` to `ChatGPT`, and hand off one exact implementation action to Codex.
- If the next action names **Codex**, implement only the recorded decision, run the tests and `verify_demo.py`, update current state with verified evidence, create `.project-memory/sessions/YYYY-MM-DD-codex-slugify.md`, set `Last actor` to `Codex`, and hand off verification to a human or fresh ChatGPT session.

Source precedence: latest authorized human instruction -> current verified evidence -> `PROJECT_MEMORY.md` -> specialized documentation -> session history -> private model memory.

Never store secrets, credentials, `.env` values, or unnecessary personal data.
