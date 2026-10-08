# Provisional Initial Reconstruction — Project Memory Protocol Review

- Runtime: Google Antigravity
- Host OS: Microsoft Windows NT 10.0.26300.0
- Run ID: 20261006T203424Z
- Pinned Commit: 8c96e926b0d28a182759c45c3a0141fa9a934eba
- Branch: experiment/hermes-pmp-adapter
- Repository: https://github.com/Mad-Max8063/project-memory-protocol-public

## 1. Objective
Perform a bounded, offline reproducibility review of the Project Memory Protocol (PMP) repository from a fresh, isolated clone. Reconstruct project state and verify evidence integrity solely from the committed files in the repository, specifically evaluating the Hermes/Claude/Codex chain verification logic without performing live LLM calls, provider integrations, or environment alterations.

## 2. Current State (per canonical memory PROJECT_MEMORY.md)
- Branch `experiment/hermes-pmp-adapter` is published and draft PR #8 is open against `main`.
- Starting revision: `2d9da5549d802c27b7a47293384d3f0d59b0ff13`; pinned commit under review: `8c96e926b0d28a182759c45c3a0141fa9a934eba`.
- Prior chain events:
  - Bounded Hermes live replay executed and committed (`experiments/hermes-pmp/evidence/live-replay-20261006/`).
  - Claude continuation executed from the Hermes bundle, verified by host, followed by a separate Codex continuation (`experiments/hermes-pmp/evidence/claude-continuation-20261006/`).
  - Follow-up offline verification script `experiments/hermes-pmp/verify_chain.py` created by Codex after a single Claude implementation invocation timed out at 300s.
  - Previous Codex review noted two P2 boundaries (ignored imports in semantic helper, linked ancestors), which were addressed by host fixes with 7 unit tests passing.
  - Public review materials and English social drafts prepared (`docs/experiments/hermes-review-social-drafts.md`).

## 3. Decisions & Constraints
- Vendor-neutral protocol: PMP canonical memory (`PROJECT_MEMORY.md`) is the sole authoritative state tracker; adapters must not duplicate or fork state.
- No live inference, no credential inspection, no paid services, no modifications to tracked files, tests, hashes, or canonical memory.
- Bounded evaluation: offline execution of `verify_chain.py` and `test_pmp_replay_chain.py`.
- No claim of certified model identity, cryptographic freshness, or general autonomy based solely on Git commits or JSON reports.
- Reproduction classification: separate-runtime reproduction on the same host (same machine as author).

## 4. Available Evidence
- `PROJECT_MEMORY.md` and session files in `.project-memory/sessions/`.
- Three archived Git bundles and reports:
  1. `experiments/hermes-pmp/evidence/live-replay-20261006/replay.bundle` & `replay-report.json`
  2. `experiments/hermes-pmp/evidence/claude-continuation-20261006/claude-replay.bundle` & `claude-report.json`
  3. `experiments/hermes-pmp/evidence/claude-continuation-20261006/fresh-codex.bundle` & `fresh-codex.json`
- Prior chain verifier checks in `experiments/hermes-pmp/evidence/chain-verifier-20261006/`.
- Verification code and tests: `experiments/hermes-pmp/verify_chain.py`, `tests/test_pmp_replay_chain.py`.
- Documentation in `docs/experiments/hermes-review-brief.md` and `docs/experiments/replay-chain-verifier.md`.

## 5. Exact Next Action (per canonical memory)
"Max: review docs/experiments/hermes-review-social-drafts.md and manually share the reproduction request linking PR #8 when ready. The next experimental success criterion is an external reviewer report identifying source commit, environment, commands, exit code, verifier JSON and any failures. No merge/release is authorized."
Immediate reviewer task action: execute the offline verifier and unit test suite, document all commands, stdout, stderr, and exit codes, and generate reproduction evidence in `experiments/hermes-pmp/evidence/reproductions/google-antigravity/20261006T203424Z/`.

## 6. What the Repository Claims
- Claims that an end-to-end multi-agent chain across Hermes, Claude, and Codex was successfully captured and verified via portable Git bundles.
- Claims that `verify_chain.py` validates three bundles, 14 historical input snapshots, 6 fixture tests, lineage, and handoff integrity.
- Claims that 7 acceptance tests in `test_pmp_replay_chain.py` pass without external network access or credentials.
- Claims that all operations are repeatable offline from repository contents alone.

## 7. What Has NOT Been Verified Yet (at this reconstruction point)
- Actual execution and exit status of `experiments/hermes-pmp/verify_chain.py --json`.
- Actual execution and results of `tests/test_pmp_replay_chain.py`.
- Source code safety of `verify_chain.py` (not yet inspected).
- Authenticity or provenance of remote provider executions claimed in archived bundles (cannot be cryptographically certified from Git history).
- Independent external host execution (running on same host machine).
