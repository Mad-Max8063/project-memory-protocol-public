# Same-host runtime reproductions — 2026-10-06

Experimental, non-normative evidence. Current project state and task remain
in the outer repository's root `PROJECT_MEMORY.md`.

Later evidence: [Max's other-machine Windows reproduction](acer-windows-20261007/REPORT.md)
at pinned source `1f56483e472c518d2954d7af15cfa59f1e5cf58e`. This is a
maintainer-supplied console report, separate from the same-host runtime round
below; it is not independent third-party review or a directly observed host run.

Both reviewers targeted outer commit
`8c96e926b0d28a182759c45c3a0141fa9a934eba`, not the later documentation tip.
The verifier returns archived fixture commit
`5e717267e23e39a854347ade7e9efa545269c227` and that fixture's historical
`next_action`; neither replaces the outer project's current state.

| Runtime | Reviewer outcome | Verifier exit | Fixture tests | Verifier tests |
| --- | --- | --- | --- | --- |
| [Claude Code](claude-code/20261006T195333Z/REVIEW.md) | PASS, same host | 0 | 6 | 7 in 21.363 s |
| [Google Antigravity](google-antigravity/20261006T203424Z/REVIEW.md) | PASS, same host | 0 | 6 | 7 in 21.391 s |
| [Google Antigravity](google-antigravity/20261013T215241Z/REVIEW.md) | PASS, same host (post-LF recovery) | 0 | 6 | 7 in 26.413 s |
| [Claude Code](claude-code/20261014T021522Z/REVIEW.md) | PASS, same host (Windows LF fix review) | 0 | 6 | 7 in 23.264 s (87/87 suite) |

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

## Round 2026-10-13 (ChatGPT → Google Antigravity Continuity)

A follow-up independent evaluation on 2026-10-13 tested cross-runtime continuity
from `c974baf015b58e867e5fccb335a3c5df67d75089`. The initial run revealed an
integrity failure in `verify_chain.py` caused by Windows default `core.autocrlf=true`
converting text evidence files (`.json`) to CRLF, altering their SHA-256 byte digest.
Binary `.bundle` archives were unaffected. Following the documented requirement of
`core.autocrlf=false`, the files were restored to match Git's LF blobs, after which
all 3 bundles, 14 historical inputs, 6 fixture tests, and 7 verifier acceptance tests
passed (exit code 0). See [google-antigravity/20261013T215241Z/REVIEW.md](google-antigravity/20261013T215241Z/REVIEW.md)
and [crlf-issue-proposal.md](google-antigravity/20261013T215241Z/crlf-issue-proposal.md).

## Round 2026-10-14 (Windows Line Endings Portability Fix Review)

An independent evaluation by Claude Code (Opus 5.5) on 2026-10-13/2026-10-14 reviewed
commit `dbb55f5c9dbfab15bdc708d160d5285a41ca2435` on branch `experiment/pmp-windows-line-endings-20261013`
from repository state only without prior chat history:

- Verified that `.gitattributes` enforces LF checkouts in fresh clones under both
  `core.autocrlf=true` and `core.autocrlf=false`.
- Both fresh clone configurations passed all validation gates: memory, release candidate,
  offline verifier (exit code 0), 7 acceptance tests, 4 regression tests, and all 87 tests
  across the full suite.
- Re-tested parent commit `224a67fd9cac0d5d5b257f15b2c27232b3eaa7fa` under `core.autocrlf=true`,
  confirming exact failure reproduction (archive digest mismatch in `verify_chain.py` and carriage
  return mismatch in `test_hermes_pmp_adapter.py`).
- Identified that pre-existing worktrees previously checked out with CRLF can continue failing
  after checking out `dbb55f5` because Git does not rewrite unchanged files in an existing worktree,
  even with clean `git status`. The recommended recovery path is a fresh clean clone, avoiding manual
  index manipulation.
- Critical analysis of tests noted that test 4 (`test_crlf_injection_fails_digest_before_subprocess`)
  tests evidence tampering rejection rather than the `.gitattributes` rule itself, and noted that
  future files requiring CRLF (such as `.bat` or `.cmd`) will require explicit exceptions in `.gitattributes`.
- Same-host evaluation boundary: independent model and session, but executed on the same Windows host.
  See [claude-code/20261014T021522Z/REVIEW.md](claude-code/20261014T021522Z/REVIEW.md).


