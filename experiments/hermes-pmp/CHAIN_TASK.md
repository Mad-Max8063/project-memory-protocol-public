# Authorized task — offline Hermes / Claude / Codex archive verifier

Experimental, non-normative. Human authority: Max, 2026-10-06.

Implement one useful command that independently verifies the archived real chain.
Codex supplies this task, Claude proposes implementation, the host runs tests,
and a separate Codex reviewer consumes only the resulting repository and PMP.

## Allowed changes

- Add `experiments/hermes-pmp/verify_chain.py`.
- Host-owned acceptance tests: `tests/test_pmp_replay_chain.py`.
- Task, documentation, new evidence/session record and canonical memory updates.
- Keep existing archives, Core, adapters, profiles and earlier tracks unchanged.

## Contract

Python standard library, Python 3.12+, Git. Reuse `adapter.digest`,
`adapter.clean_env`, `adapter.parse_sections`, `adapter.validate` and the
existing `replay.git` / `replay.run` where useful. No model/provider calls.

Export `verify_chain(evidence_root: Path | None = None) -> dict`. Default root
is the sibling `evidence` directory. Expose `--evidence-root PATH` and `--json`.
Exit 0 on success, 1 on invalid/unavailable evidence, 2 on argparse usage error.
Human output is concise; JSON contains `verified: true`, `historical_inputs: 14`,
`acceptance_tests: 6`, `next_action`, `bundle_sha256` (three entries),
`model_identity_certified: false`, `session_freshness_certified: false`.
Expose `verify_repository(root, hermes_report, claude_report, codex_report)`
as the semantic verification helper after archive integrity checks. It must
reject altered checked-out files, missing handoffs and receipt inconsistencies.

This is a fixed verifier for the archived 2026-10-06 chain, not a generic
archive importer. Pin expected digests in source for the three bundle files and
three JSON manifests supplied in the packet. Check all six before cloning or
executing anything. Pin the five observed Git revisions (baseline, Hermes,
Claude dispatch, Claude result, plus final Codex receipt revision) from reports.
Reject missing files, altered bytes and symlink/junction paths; only fixed
relative paths may be read. Do not derive paths or commands from report input.

Clone verified bundles into `tempfile.TemporaryDirectory`; `core.autocrlf=false`,
disabled Git hooks (`-c core.hooksPath=<empty directory>`), no checkout hooks.
Use a minimized environment, bounded subprocess timeouts, no network, no writes
to original archives. Temporary clones must be cleaned up even on failure.

Check Git parent lineage and exact changed-file boundaries for each stage.
Compare duplicated host receipts to reports, input snapshot digests, proposal
memory guards, fixture/manifest content, runtime metadata and historical inputs:
five Hermes input hashes against the baseline; nine Claude hashes against dispatch.
Validate all relevant PMP memories, preserve active decisions between each
authorized stage, require nonempty next actions and linked stage handoffs.
Check final Codex receipt and canonical memory digests against `fresh-codex.json`;
its recorded two-file diff must be exact. Preserve historical report flags:
Claude report's fresh_codex_executed=false, later Codex manifest=true.

Before running the six fixture tests, compare their contents to trusted local
`seed/test_fixture.py` and `claude-seed/test_manifest.py`; run only these two
named modules using `python -I -B -m unittest test_fixture test_manifest -v`.
No unittest discovery of additional files or untrusted repo commands.
Validate exit status and actual test count (six). Both original trusted test
files' byte hashes are provided in the packet.

Return a structured result only after every check passes. Report integrity and
local test observations; do not promote runtime labels to certified identity,
freshness, reasoning, general autonomy or audited cost. Hashes are integrity
anchors in this source revision, not independent authenticity signatures.

## Handoff

Claude returns code and a structured proposal only; tools disabled.
Do not claim tests were executed. Host imports one fixed file after reviewing it.
Propose no decision changes. Intended next actor: Codex.
Exact next action: Codex: independently verify the offline chain command and
tamper rejection tests from the repository, review scope and record a receipt.

## Stop rule

One Claude implementation invocation and one independent Codex review.
Host may correct concrete review/test findings locally and record authorship.
No new services, API keys, purchases, push, PR, merge, release or publication.

## Observed execution addendum

The one Claude invocation timed out after 300 seconds without a retained complete
proposal. No retry. Codex completed the implementation locally within the same
file/scope and handed it to the independent reviewer. Actual Claude request
count, model usage and invoice impact are unknown for this attempt.

The final Codex receipt in the older archive paraphrases its canonical next
action. Both whole-file hashes are pinned; verify the known historical wording
and recover the exact current action from the archived PROJECT_MEMORY.md.
Python isolated mode removes cwd from sys.path, so the host uses a fixed -I/-B
bootstrap to load exactly the two trusted named test modules. No additional
modules are discovered. These are implementation details, not Core changes.

The independent review against the initial candidate found two P2 issues.
The host corrected ignored-file import execution by rejecting all untracked
files (including ignored ones) before bootstrap, and corrected ancestor link
acceptance with a local root/ancestor guard. Seven acceptance tests and full
discovery (83) passed after these fixes. No second review or provider retry.
