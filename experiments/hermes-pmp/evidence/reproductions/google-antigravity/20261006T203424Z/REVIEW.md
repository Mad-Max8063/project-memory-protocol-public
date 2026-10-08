# Reproducibility Review Report — Project Memory Protocol (PMP)

## 1. Runtime, Environment, and Exact Commit

- **Runtime / Reviewer**: `google-antigravity`
- **Observed Model (tool-reported metadata)**: Gemini 3.8 Flash (High) *(metadata only; not certified identity)*
- **Operating System**: Microsoft Windows NT 10.0.26300.0 (Windows 11)
- **Git Version**: git version 2.53.0.windows.2
- **Python Version**: Python 3.14.3
- **Repository Clone Directory**: `%USERPROFILE%\.gemini\antigravity\scratch\pmp-review-google-antigravity-20261006T203424Z`
- **Target Remote Branch**: `experiment/hermes-pmp-adapter`
- **Pinned Commit (Review Target)**: `8c96e926b0d28a182759c45c3a0141fa9a934eba`
- **Archived Replay Final Commit**: `5e717267e23e39a854347ade7e9efa545269c227`
- **Run ID**: `20261006T203424Z`
- **Review PR**: https://github.com/Mad-Max8063/project-memory-protocol-public/pull/8

---

## 2. Known Context and Isolation Limits

- **Evaluation Category**: Separate-runtime reproduction on the same host (executed on the author's local workstation environment, not on a physically distinct remote host or by an independent external human).
- **Session Isolation**: Performed in a fresh, isolated session with no prior conversation turns or cached agent states imported.
- **Repository Isolation**: Cloned directly into an empty, separate directory (`scratch/pmp-review-google-antigravity-20261006T203424Z`) via `--config core.autocrlf=false --single-branch --branch experiment/hermes-pmp-adapter`.
- **Temporary Directory Isolation**: A dedicated external temporary directory was created strictly outside the clone (`%USERPROFILE%\.gemini\antigravity\scratch\tmp-pmp-review-20261006T203424Z`). All path components were verified to have no symlinks or reparse points (`IsReparsePoint: False`). `$env:TEMP` and `$env:TMP` were set to this path. No `.review-tmp` directory was created inside the clone.
- **Subagent & External Tool Restrictions**: No subagents were invoked or delegated to.
- **Evidence Boundaries**:
  - No LLM provider APIs, paid services, OAuth credentials, or live models were queried or executed during this review.
  - Verification is purely offline, exercising Git integrity, cryptographic SHA-256 hashes, and deterministic standard library tests.
  - Commits and JSON reports establish historical integrity and reproducible context preservation across handoffs, but do not cryptographically certify remote model identity, freshness of private model sessions, or general model autonomy.

---

## 3. Initial Reconstruction (Before Running Tests)

Prior to test execution, repository instructions (`AGENTS.md`) and canonical memory (`PROJECT_MEMORY.md`) were read, and an initial reconstruction was provisionally recorded outside the clone:

- **Objective**: Bounded, offline reproducibility check of the PMP repository from a fresh clone, reconstructing state and verifying archived multi-agent handoff evidence without live inference.
- **Current State**:
  - Experimental branch `experiment/hermes-pmp-adapter` published with review PR #8 open against `main`.
  - Core 0.2.2 and profile 0.1.1 unchanged; minimal stdlib file bridge added for Hermes adapter interoperability.
  - Archived chain: Hermes proposed label whitespace normalization (host wrote files and verified 3 fixture tests; bundle preserved); Claude proposed manifest `labels.txt` (host wrote file and verified 6 fixture/manifest tests; bundle preserved); Codex performed clean continuation (bundle preserved).
  - Verifier tool `experiments/hermes-pmp/verify_chain.py` was created by Codex after a single Claude implementation invocation timed out at 300s.
  - Earlier independent Codex review found two P2 boundaries (ignored imports, linked ancestors), which were addressed by host fixes with 7 unit tests passing.
- **Decisions & Constraints**:
  - Vendor-neutral protocol: `PROJECT_MEMORY.md` remains canonical; proposals are non-normative transport.
  - Offline review only: no live inference, no credential inspection, no credit purchases ($0 incremental cost).
  - No modifications to tracked files, tests, hashes, or canonical memory.
- **Available Evidence**:
  - Pinned bundles and reports: `replay.bundle`, `claude-replay.bundle`, `fresh-codex.bundle`.
  - Verifier script and acceptance tests: `verify_chain.py`, `test_pmp_replay_chain.py`.
- **Exact Next Action**:
  - Per canonical memory: Max to review social drafts and manually share reproduction request linking PR #8.
  - Immediate reviewer task: run offline verifier and unit test suite, document outputs, and record reproduction results.
- **Claims vs Unverified Status**:
  - Repository claimed 3 bundles, 14 historical inputs, and 6 fixture tests verify offline with exit code 0, and 7 unit tests pass.
  - At reconstruction time, no tests had yet been executed; code had not yet been inspected for safety; provider authenticity remained uncertified.

---

## 4. Actual Commands and Results

### Command 1: Offline Chain Verifier
- **Command**:
  ```powershell
  $env:TEMP = "%USERPROFILE%\.gemini\antigravity\scratch\tmp-pmp-review-20261006T203424Z"
  $env:TMP = "%USERPROFILE%\.gemini\antigravity\scratch\tmp-pmp-review-20261006T203424Z"
  python -B experiments/hermes-pmp/verify_chain.py --json
  ```
- **Exit Code**: `0`
- **Stdout**:
  ```json
  {
    "verified": true,
    "historical_inputs": 14,
    "acceptance_tests": 6,
    "next_action": "Max / dispatch host: review .project-memory/sessions/codex-after-claude.md and this canonical update, then close the bounded experiment. No implementation action remains; any further experiment requires a new scoped task.",
    "final_commit": "5e717267e23e39a854347ade7e9efa545269c227",
    "model_identity_certified": false,
    "session_freshness_certified": false,
    "test_command": [
      "python",
      "-I",
      "-B",
      "-c",
      "import os,sys,unittest; sys.path.insert(0,os.getcwd()); suite=unittest.defaultTestLoader.loadTestsFromNames([\"test_fixture\",\"test_manifest\"]); result=unittest.TextTestRunner(verbosity=2).run(suite); sys.exit(0 if result.wasSuccessful() else 1)"
    ],
    "test_exit_code": 0,
    "test_stdout": "",
    "test_stderr": "test_normalized_labels (test_fixture.FixtureTests.test_normalized_labels) ... ok\ntest_shape_and_ids (test_fixture.FixtureTests.test_shape_and_ids) ... ok\ntest_whitespace_contract (test_fixture.FixtureTests.test_whitespace_contract) ... ok\ntest_manifest_has_no_blank_lines (test_manifest.ManifestTests.test_manifest_has_no_blank_lines) ... ok\ntest_manifest_has_two_distinct_ids (test_manifest.ManifestTests.test_manifest_has_two_distinct_ids) ... ok\ntest_manifest_matches_fixture_in_order (test_manifest.ManifestTests.test_manifest_matches_fixture_in_order) ... ok\n\n----------------------------------------------------------------------\nRan 6 tests in 0.002s\n\nOK\n",
    "bundle_sha256": {
      "live-replay-20261006/replay.bundle": "b729b7f2220f5e639ad9e43f205314c45055d69eab966689b0438f178398de17",
      "claude-continuation-20261006/claude-replay.bundle": "b9c7e80bdd3c25a4aca67c43dd647fa3325f4340a9f51de5bbc7a61b9f1e03ec",
      "claude-continuation-20261006/fresh-codex.bundle": "1a5eb32bc3cc3c240be4a0533d110d86adf7291240628defc6f9109b45324b25"
    },
    "scope": "fixed archived chain; offline integrity and local test verification"
  }
  ```
- **Stderr**: *(empty)*

### Command 2: Verifier Acceptance Unit Tests
- **Command**:
  ```powershell
  $env:TEMP = "%USERPROFILE%\.gemini\antigravity\scratch\tmp-pmp-review-20261006T203424Z"
  $env:TMP = "%USERPROFILE%\.gemini\antigravity\scratch\tmp-pmp-review-20261006T203424Z"
  python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v
  ```
- **Exit Code**: `0`
- **Stdout**: *(empty)*
- **Stderr**:
  ```text
  test_cli_json_usage_and_failure_exit_codes (test_pmp_replay_chain.ChainAcceptanceTests.test_cli_json_usage_and_failure_exit_codes) ... ok
  test_corrupted_bundle_rejected_before_git (test_pmp_replay_chain.ChainAcceptanceTests.test_corrupted_bundle_rejected_before_git) ... ok
  test_ignored_import_payload_rejected_without_execution (test_pmp_replay_chain.ChainAcceptanceTests.test_ignored_import_payload_rejected_without_execution) ... ok
  test_missing_archive_and_linked_inputs_rejected (test_pmp_replay_chain.ChainAcceptanceTests.test_missing_archive_and_linked_inputs_rejected) ... ok
  test_modified_report_rejected_before_git (test_pmp_replay_chain.ChainAcceptanceTests.test_modified_report_rejected_before_git) ... ok
  test_real_archive_chain_and_readonly_boundary (test_pmp_replay_chain.ChainAcceptanceTests.test_real_archive_chain_and_readonly_boundary) ... ok
  test_semantic_verifier_rejects_changed_result_and_missing_handoff (test_pmp_replay_chain.ChainAcceptanceTests.test_semantic_verifier_rejects_changed_result_and_missing_handoff) ... ok

  ----------------------------------------------------------------------
  Ran 7 tests in 21.391s

  OK
  ```

---

## 5. Evidence Supporting Conclusions

1. **Replay Integrity**:
   - `verify_chain.py --json` validated the 3 archived Git bundles against their pinned SHA-256 digests.
   - All 14 historical input snapshots matched their expected digests.
   - The 6 fixture acceptance tests (`test_fixture.py` and `test_manifest.py`) executed within an isolated, trusted bootstrap and passed with exit code 0.
   - The archived replay final commit was identified as `5e717267e23e39a854347ade7e9efa545269c227`, distinct from the outer repository HEAD commit `8c96e926b0d28a182759c45c3a0141fa9a934eba`.
2. **Defensive Boundaries**:
   - All 7 acceptance tests passed in `test_pmp_replay_chain.py`.
   - Defensive checks confirmed: corrupted bundles rejected before Git execution, modified JSON reports rejected before Git execution, missing archives or symlink/junction ancestors rejected, untracked/ignored file payloads rejected before inclusion in sys.path, and invalid proposals or missing handoffs rejected.
3. **Clarity of Roles and Actions**:
   - **Who proposed changes**: Hermes proposed fixture JSON label modifications; Claude proposed `labels.txt`; Codex proposed verifier implementation.
   - **Who wrote files**: The bridge/host process performed all disk writes atomically after schema/digest validation.
   - **Who ran tests**: The host executed all test suites (`tests_executed_by_model: false`).
   - **Pending items**: External-machine / external-reviewer reproduction.
   - **Exact next action**: Explicitly documented in canonical memory and recovered by the verifier.

---

## 6. Failures, Ambiguities, and Risks

1. **Documentation Ambiguity Regarding Temporary Directory Location**:
   - In `docs/experiments/hermes-review-brief.md` (lines 106-107), example commands show `$pmpReviewTemp = Join-Path (Get-Location).Path '.review-tmp'`. However, reviewer instructions strictly require creating the temporary folder *outside* the clone to guarantee zero untracked file pollution and avoid repo-internal reparse points. When using an external path for `$env:TEMP` / `$env:TMP`, execution completed without issues.
2. **Host Environment Boundary**:
   - This reproduction ran on the author's local workstation environment under Windows 11. While conducted in a clean clone and independent process tree, it represents a "separate-runtime reproduction on the same host" rather than an external third-party machine run.
3. **Claude Verifier Implementation Scope**:
   - The repository transparently documents that Claude's attempt to implement `verify_chain.py` timed out after 300 seconds without producing code, and Codex implemented it locally. The verified chain covers the earlier fixture continuation, not Claude-authored verifier implementation.

---

## 7. Detected Checkout Changes

- Prior to generating the review reproduction report:
  - `git diff --exit-code`: exit code 0 (no diff)
  - `git diff --cached --exit-code`: exit code 0 (no staged diff)
  - `git status --porcelain`: clean (0 modified or untracked files)
- Following the generation of reproduction evidence, the only changes in the working tree are the newly added files under:
  `experiments/hermes-pmp/evidence/reproductions/google-antigravity/20261006T203424Z/`

---

## 8. What Was Not Tested

- Live LLM model inference or external provider API connectivity (Claude, OpenAI, Hermes).
- Authentication workflows, token quotas, or billing validation.
- The broader repository test suite beyond the verifier scope (the full 83-test suite was not rerun).
- Kernel-level NTFS reparse point / junction bypassing (reliance was on standard Python / Win32 path attribute APIs).

---

## 9. Verdict

**PASS** (Separate-runtime reproduction on the same host)

**Reasons**:
- The fresh clone checked out cleanly and pinned the exact target commit (`8c96e926b0d28a182759c45c3a0141fa9a934eba`).
- The offline verifier executed with exit code 0, validating all 3 bundles, 14 historical inputs, 6 fixture tests, and recovering canonical memory state.
- All 7 verifier acceptance tests passed cleanly with exit code 0.
- Repository documentation and evidence explicitly and accurately distinguish model proposals, host writes, test executions, and historical timeouts.
- The working tree remained unpolluted and zero tracked files were modified.

---

## 10. Recommended Next Action

Per canonical memory in `PROJECT_MEMORY.md`:
> "Max: review docs/experiments/hermes-review-social-drafts.md and manually share the reproduction request linking PR #8 when ready. The next experimental success criterion is an external reviewer report identifying source commit, environment, commands, exit code, verifier JSON and any failures. No merge/release is authorized."
