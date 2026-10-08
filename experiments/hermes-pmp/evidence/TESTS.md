# Local test record — 2026-10-06

Observed by Codex host on Windows/Python 3.14; no CI or live Hermes claim.
This record describes the working tree prepared for the single experiment commit.
It does not claim that a remote runner covered that commit.

## Experiment unit tests

Command: `python -m unittest -v tests/test_hermes_pmp_adapter.py`
Result: Ran 13 tests; OK; exit code 0.

Every test below passed:

- test_state_serialization_preserves_canonical_bytes_and_sections — PASS
- test_handoff_preserves_decisions_evidence_and_next_action — PASS
- test_stale_memory_rejected_without_writes — PASS
- test_invalid_candidate_and_schema_are_rejected — PASS
- test_immutable_tests_cannot_be_replaced_by_a_proposal — PASS
- test_host_failure_rolls_back_fixture_and_memory — PASS
- test_append_only_handoff_and_existing_lock — PASS
- test_traversal_and_linked_paths_are_rejected — PASS
- test_tampered_evidence_cannot_pass_continuation — PASS
- test_no_history_is_required_by_fresh_process — PASS
- test_real_cli_response_requires_completion_and_no_tools — PASS (synthetic stream, NOT Hermes)
- test_missing_runtime_fails_without_network_fallback — PASS
- test_existing_compatibility_fixture_remains_valid — PASS

## Existing gates / compatibility

- Baseline `python -m unittest discover -s tests -v`: 57 existing tests PASS.
- Final full discovery: 70 tests PASS; original 57 + new 13.
- `python -m compileall -q scripts examples tests experiments/hermes-pmp`: PASS.
- `python scripts/validate_memory.py PROJECT_MEMORY.md`: PASS.
- Seed memory validation with the same unchanged validator: PASS.
- Both original authority/evidence profile template validations: PASS.
- `python scripts/validate_release_candidate.py`: PASS (metadata/links/size/secret checks).
- `python examples/chatgpt-codex-handoff/verify_demo.py`: PASS, six original demo tests.
- `git diff --check`: PASS.

## Replay acceptance

Exact command: `python -I -m unittest discover -s . -p test_fixture.py -v`

- test_shape_and_ids — PASS before and after normalization.
- test_normalized_labels — expected FAIL in seed; PASS after import.
- test_whitespace_contract — expected FAIL in seed; PASS after import.
- Fresh Python verifier: all three PASS.
- Separate context-free Codex continuation: all three PASS, baseline/current hashes MATCH.
- `python experiments/hermes-pmp/verify_archive.py`: both bundle digests/lineages,
  scoped changes, input/evidence hashes and rerun acceptance PASS.

Original seed failures and host/fresh-process successful output are saved in
replay-report.json. Codex continuation's exact checks are in its committed receipt
inside fresh-codex.bundle. Synthetic CLI/consumer tests do not prove real Hermes
profile enforcement, provider eligibility or operational compatibility.
