# Same-host runtime reproductions — 2026-10-06

Experimental, non-normative evidence. Current project state and task remain
in the outer repository's root `PROJECT_MEMORY.md`.

Both reviewers targeted outer commit
`8c96e926b0d28a182759c45c3a0141fa9a934eba`, not the later documentation tip.
The verifier returns archived fixture commit
`5e717267e23e39a854347ade7e9efa545269c227` and that fixture's historical
`next_action`; neither replaces the outer project's current state.

| Runtime | Reviewer outcome | Verifier exit | Fixture tests | Verifier tests |
| --- | --- | --- | --- | --- |
| [Claude Code](claude-code/20261006T195333Z/REVIEW.md) | PASS, same host | 0 | 6 | 7 in 21.363 s |
| [Google Antigravity](google-antigravity/20261006T203424Z/REVIEW.md) | PASS, same host | 0 | 6 | 7 in 21.391 s |

Each folder contains `REVIEW.md`, `execution.log`, `verifier.json`, and the
separately saved provisional `initial-reconstruction.md`. These are reviewer
records; provider/tool metadata and isolation assertions are not attested.

## Maintainer cross-check, separate from reviewer claims

Max requested verification, then authorized local incorporation and the three
documentation corrections. Read-only host Git checks confirmed both clones'
target SHA and public remote, empty tracked/staged diffs, and only the three
new reviewer report files. Host SHA-256 checks matched both source/test files
and all six archived bundle/report files across the two clones and host repo.
The provisional notes were read from their external work folders.

Host separately reran `python -B experiments/hermes-pmp/verify_chain.py --json`
and `python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v`:
exit 0, 3 bundles, 14 historical inputs, 6 fixture tests, and 7 acceptance tests
in 37.954 s. The host interpreter emitted `Failed to find real location of
C:\Python314\python.exe`; the commands and tests still completed successfully.
This is the preceding verification turn, not a new run attributed to a reviewer.
Current incorporation checks are captured in `host-integration-checks.json`.

## Import provenance and privacy

`import-manifest.json` records original file hashes/sizes/mtimes and imported
file hashes. Imports use UTF-8, LF line endings and one final newline. Local
Windows home paths are represented by `%USERPROFILE%`; Claude's existing
redactions are retained. No results, timings, findings or verdicts are rewritten.
The source files in both reviewer clones and external work folders are untouched.
Digest matching establishes consistency, not independent signatures or provenance.

## Findings and qualifications retained

1. The brief confused archived and current `next_action`; it now distinguishes
   them explicitly, as does the verifier guide and historical review prompt.
2. Temporary-folder instructions differed; the brief now uses outside-clone
   roots on Windows and POSIX. An empty directory itself is not shown by Git
   status: Claude's wording about an untracked empty directory is not endorsed.
3. Claude's first clone hit MSIX/AppData path length; the brief/prompt now
   recommend short Windows paths, without altering global Git settings.
4. Claude's provisional note says approximately 19:56Z, while its observed
   mtime and report/log say 19:54:13Z, before the reported 19:54:43Z verifier
   start. Preserve this discrepancy; neither text nor mutable filesystem
   timestamps independently certifies pre-test authorship or fresh context.
   Antigravity's provisional mtime was 20:36:52Z, before its logged 20:38:10Z
   verifier start; the same non-attestation limitation applies.
5. Antigravity's claim that no live models were queried is too broad for an
   AI-authored review. The offline verification commands do not invoke a
   provider or rerun live agents; reviewer inference/usage is not audited.
   Its fresh/cached-context assertion is self-reported, not proof of absent
   hidden memory. File-level atomic writes are not a crash-proof multi-file
   transaction; its statement about all atomic writes must not imply otherwise.

No code-level failure was reproduced in the bounded commands. The reports
cover different runtimes on the same Windows host, not external-human review,
another machine, general autonomy, model identity or session freshness.
No POSIX execution, full new experiment suite in remote CI, real junction
end-to-end rejection or billing audit is established by this round.
No new services or credits were bought for incorporation; existing tool/model
allowance consumption is not zero by implication and was not measured.

## Historical procedure

See [the pinned prompt](../../../../docs/experiments/hermes-cross-runtime-review-prompt.md)
and [the corrected brief](../../../../docs/experiments/hermes-review-brief.md).
The two fixed commands reproduce stored evidence without an AI account.
Do not repeat this same-host round automatically or reinterpret reviewer
recommendations as publication/contact authority. A future other-machine run
requires its own bounded scope. No push, merge, release or posting occurred
as part of this local incorporation.
