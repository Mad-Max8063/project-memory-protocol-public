# PMP v0.2.1 — 90-second demo script

> Draft recording script. Do not publish until the human approves the final cut and repository visibility change.

## Recording setup

- Use a clean browser profile or clearly fresh conversations.
- Create a disposable repository using only
  `examples/chatgpt-codex-handoff/seed/` during the claimed blind handoff.
- Keep the repository history, canonical memory, prompts, commands, and outputs readable on screen.
- Record one continuous take when practical; disclose every cut.
- Do not display tokens, credentials, private tabs, notifications, or unrelated repositories.

## Shot list and narration

### 0–10 seconds — The problem

**Screen:** Start with the isolated repository at its baseline commit and open `TASK.md` plus `PROJECT_MEMORY.md`.

**Narration:**

> A fresh AI session usually loses the decisions that existed in another tool. Project Memory Protocol keeps the current operational state in Git so a different agent can continue without receiving the old chat.

### 10–28 seconds — ChatGPT records the decision

**Screen:** Show the fresh ChatGPT conversation, the decision-only prompt, and
atomic commit `<CHATGPT_DECISION_SHA>` changing only `PROJECT_MEMORY.md` and
`evidence/01-chatgpt-decision.md`.

**Narration:**

> ChatGPT reads the human task and records the active decisions and exact next action. It does not implement the function. Memory and evidence land atomically in one commit.

### 28–52 seconds — Codex continues from Git

**Screen:** Show the fresh Codex prompt without hidden requirements, Codex
reading `PROJECT_MEMORY.md`, and commit `<CODEX_IMPLEMENTATION_SHA>`.

**Narration:**

> A fresh Codex task receives no restated decision. It reads the repository, implements only the authorized work, runs the six tests, and updates the canonical memory and session evidence.

### 52–68 seconds — Mechanical verification

**Screen:** Run `python -m unittest -v test_slugify.py` and `python verify_demo.py`, then show the successful GitHub Actions run.

**Narration:**

> The unchanged acceptance suite passes, the handoff verifier prints LIVE DEMO VERIFIED, and GitHub Actions preserves independent execution logs.

### 68–82 seconds — ChatGPT recovers the state

**Screen:** Show a new ChatGPT conversation reconstructing the human decision, Codex work, evidence, and next action using repository access only.

**Narration:**

> Another fresh ChatGPT session reconstructs what was decided, what Codex completed, what evidence exists, and what should happen next—without the user retelling the project history.

### 82–90 seconds — Claim and call to action

**Screen:** Return to the PMP README and show `PROJECT_MEMORY.md`, `SPEC.md`, the Evidence-backed Handoff profile, and the `v0.2.1` tag.

**Narration:**

> PMP is an open, model-agnostic protocol for shared operational project state. Core 0.2.1, the optional Evidence-backed Handoff profile, templates, adapters, demo, and evidence are available in the repository.

## Required on-screen disclosures

- The completed fixture proves reproducibility, not external agent identity.
- Git authorship does not prove that a named model acted or that a session was fresh.
- The blind-handoff claim depends on the isolated baseline, visible prompts, repository history, and persisted execution evidence together.
- The slug example covers NFKD-decomposable Latin diacritics, not general transliteration.
- The Evidence-backed Handoff profile is optional; baseline PMP does not require external services.

## Final-cut acceptance criteria

- Duration is 60–90 seconds, excluding an optional long-form appendix.
- Baseline, atomic ChatGPT commit, Codex commit, verification output, and return recovery are all visible.
- Commit SHAs and the successful CI URL are readable or linked in the description.
- No narration claims hidden-memory synchronization, universal interoperability, or independently proven model identity.
- A reviewer who follows `LIVE_DEMO_RUNBOOK.md` can reproduce the mechanical checks.
