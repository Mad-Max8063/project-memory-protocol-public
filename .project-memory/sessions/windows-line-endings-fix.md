# Session — Windows Line Endings Portability Fix (.gitattributes)

- Date: 2026-10-13
- Actor: Google Antigravity, logical developer participant, no identity attestation
- Human authority: Max / Max Devs Solutions
- Target branch: `experiment/pmp-windows-line-endings-20261013`
- Base revision: `224a67fd9cac0d5d5b257f15b2c27232b3eaa7fa` (from `docs/antigravity-continuity-20261013`)

## Summary

This session executed Phase 3 of the PMP evaluation: implementing and verifying a minimal, repository-wide Windows portability fix for the LF/CRLF line-ending issue observed during the 2026-10-13 reproduction.

### Phase 1: Empirical Issue Reproduction
- Created an isolated disposable clone configured with Windows default `core.autocrlf=true`.
- Observed failure in `experiments/hermes-pmp/verify_chain.py --json`:
  `ValueError: archive digest mismatch: live-replay-20261006/replay-report.json: expected 7a4e48... got ade854...`
- Observed failure in `test_hermes_pmp_adapter.py`:
  `AssertionError: 'hermes-pmp-fixture\r' != 'hermes-pmp-fixture'` due to regex capture of trailing carriage returns.
- Observed failure in `test_pmp_replay_chain.py` (1 error, 1 failure).

### Phase 2: Minimal Portability Fix
- Added `.gitattributes` at repository root:
  ```gitattributes
  # Project Memory Protocol — repository-wide line ending normalization
  * text=auto eol=lf
  *.bundle binary
  ```
- This configuration instructs Git across all platforms and user configs (including global `core.autocrlf=true`) to check out text files strictly with LF (`\n`) line endings while treating Git bundles as untouched binaries.
- Core 0.2.2, profiles, historical archives, and `verify_chain.py` verification logic remain 100% untouched.

### Phase 3: Regression Suite
- Created `tests/test_line_endings_regression.py` containing 4 regression tests:
  1. `test_gitattributes_configuration_exists_and_enforces_lf`: validates `.gitattributes` presence and rules.
  2. `test_evidence_json_files_have_no_crlf`: validates no CRLF bytes exist in `evidence/**/*.json`.
  3. `test_seed_files_have_no_crlf`: validates no CRLF bytes exist in seed files.
  4. `test_crlf_injection_fails_digest_before_subprocess`: validates that artificial CRLF corruption in evidence JSON is caught by SHA-256 digest checks before any subprocess is invoked.

### Phase 4: Verification Across Configurations
- Verified working tree with `.gitattributes`:
  - `verify_chain.py --json`: Exit code 0 (3 bundles, 14 inputs, 6 fixture tests).
  - `test_pmp_replay_chain.py`: Exit code 0 (7 acceptance tests passing).
  - `test_line_endings_regression.py`: Exit code 0 (4 tests passing).
  - Full suite (`unittest discover -s tests`): Exit code 0 (87 tests passing).
  - Memory validation (`python scripts/validate_memory.py PROJECT_MEMORY.md`): PASS.
  - Release candidate validation (`python scripts/validate_release_candidate.py .`): PASS.
- Tested fresh checkouts under both `core.autocrlf=true` and `core.autocrlf=false`, confirming identical LF checkout and exit code 0.

## Exact Next Action (Handoff to Claude Code)

Claude Code: perform independent verification of `experiment/pmp-windows-line-endings-20261013` from a clean checkout without conversational context. Validate that `.gitattributes` enforces LF checkouts under both `core.autocrlf=true` and `false`. Run offline verifier (`python -B experiments/hermes-pmp/verify_chain.py --json`), acceptance suite (`python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v`), and full test discovery (87 tests, including `tests/test_line_endings_regression.py`). Run memory and release validators. Do not push to remote, merge, or modify PR #8.
