# Reproducibility review — PMP Hermes/Claude/Codex archived chain

- Runtime label: `claude-code`
- Run ID: `20261006T195333Z` (UTC start of the run)
- Classification: **separate-runtime reproduction on the same host**. This ran
  on the project maintainer's own Windows computer, in a new Claude Code session.
  It is not a reproduction on another machine and not a human external review.
- Verdict: **PASS** for the bounded scope (archived-evidence verification and
  context recovery). See "Verdict" for limits.

## 1. Runtime and environment

| Item | Observed value |
| --- | --- |
| Tool / runtime | Claude Code `2.1.274` (desktop app, Code tab), driving Git Bash (MINGW64) |
| Model (tool-reported metadata, not certified identity) | `claude-opus-5-5` ("Opus 5.5"), as named in the session's system prompt |
| OS | Windows 11 Home, build 10.0.26300, x86_64 |
| Git | `2.53.0.windows.2` |
| Python | `3.14.3` (`python`; `python3` resolves to the Microsoft Store alias and is not a real interpreter) |
| Repository | https://github.com/Mad-Max8063/project-memory-protocol-public, branch `experiment/hermes-pmp-adapter` |
| Exact commit reviewed (outer HEAD) | `8c96e926b0d28a182759c45c3a0141fa9a934eba` |
| Branch tip at clone time | `2e08ae15586955e76655f110fe424b85f1c8b121` (one later commit, "docs: save cross-runtime reproduction prompt"; pinned commit is its ancestor) |
| Archived replay final commit (inside the bundles) | `5e717267e23e39a854347ade7e9efa545269c227` |

The outer HEAD (`8c96e92`) is the repository revision under review. The
`final_commit` (`5e71726`) is the last commit inside the archived
`fresh-codex.bundle`, i.e. the end of the historical fixture chain. They are
different repositories/histories and must not be conflated.

## 2. Known context and isolation limits

- New Claude Code session; no earlier conversation was imported. No subagents were used.
- Automatically loaded context that I know about (none of it was used as project evidence):
  - The maintainer's global user instruction file (working style, a map of the
    maintainer's other projects, Windows/Git Bash gotchas). It does not describe
    PMP or this experiment.
  - A hook asking chat replies to be in Argentine Spanish (reports are in English as required).
  - A list of recently used local project folders, the user's account e-mail,
    and the names of connected tools/MCP servers. None of these were opened for this review.
  - A per-session auto-memory directory exists for this scratch session; its index
    was not shown in context and I did not read it.
- I cannot certify that no other hidden context (provider-side memory, model
  training data about this repo) influenced me; I make no claim that it is absent.
- The same Claude Code version (2.1.274) and the same host appear in the
  archived experiment's own evidence, so this is not runtime-independent in the
  strong sense.
- I did not consult any other reviewer's report from this round. I did not
  access the earlier Hermes/Argon experiment, credentials, private profiles or
  other projects.

## 3. Initial reconstruction (before running anything)

Saved outside the clone at
`%USERPROFILE%/pmp-reviews/work-claude-code-20261006T195333Z/initial-reconstruction.md`
(file mtime 19:54:13Z; verifier started 19:54:43Z). Summary, from AGENTS.md and
PROJECT_MEMORY.md only:

- **Objective:** show that PMP canonical memory plus Git evidence lets
  different runtimes (Hermes, Claude Code, Codex) hand off a small task
  portably; current goal is external reproduction of the archived chain via PR #8.
- **Current state (claimed):** live Hermes replay → Claude continuation →
  separate Codex continuation archived as bundles and declared "A. VALIDATED"
  within limits; offline verifier `verify_chain.py` written by Codex after a
  Claude implementation attempt timed out (300 s, no proposal retained); one
  independent Codex review found two P2 issues, host fixed them; 7 acceptance
  tests and 83 full-suite tests passed (host-reported). CI run 37495814502
  passed but only for existing Core checks on an earlier pushed commit.
- **Decisions/constraints:** PMP stays vendor-neutral; Hermes optional; no
  Core/spec/profile change; no merge/release/deploy/social posting; USD 0 cost;
  no identity/freshness/autonomy claims.
- **Exact next action (canonical, outer repo):** Max reviews the social drafts
  and manually shares the reproduction request linking PR #8; next success
  criterion is an external reviewer report.
- **Not verified at that point:** every hash, test, bundle and claim.

## 4. Code inspection before execution

Read `docs/experiments/hermes-review-brief.md`,
`docs/experiments/replay-chain-verifier.md`,
`experiments/hermes-pmp/verify_chain.py`, `tests/test_pmp_replay_chain.py`
and the helpers it imports from `adapter.py` (`clean_env`, `digest`,
`safe_path`, `validate`, `parse_sections`).

No unsafe operation found for the prescribed commands:
- No network, provider, OAuth or Hermes/Claude invocation on these code paths.
- Evidence is hash-checked before any Git call; bundles are cloned into a
  `tempfile.TemporaryDirectory` with an empty hooks path, `GIT_CONFIG_GLOBAL`
  set to devnull, system config disabled, terminal prompts off and a minimized env.
- The only code executed from the archive is `test_fixture.py` and
  `test_manifest.py`, after their SHA-256 and their text are matched against
  trusted local seed copies, run with `python -I -B`.
- The unit tests write only to temporary directories (corrupted copies of the
  evidence, a harmless marker-file probe that the test asserts is never executed).

## 5. Commands and results

Full verbatim output is in `execution.log`; the verifier stdout is saved
byte-for-byte as `verifier.json`. TEMP/TMP/TMPDIR pointed to a new folder
outside the clone (`%USERPROFILE%\pmp-reviews\work-claude-code-20261006T195333Z\tmp`);
the folder and all ancestors (and the clone root and its ancestors) were checked:
no symlinks or junctions. No `.review-tmp` was created in the clone.

| Step | Command | Exit | Result |
| --- | --- | --- | --- |
| Clone (attempt 1) | `git clone ...` into the session scratch workspace | non-zero | `Filename too long` (long MSIX-virtualized AppData path); nothing left behind |
| Clone (attempt 2) | `git clone --config core.autocrlf=false --single-branch --branch experiment/hermes-pmp-adapter <url> pmp-review-claude-code-20261006T195333Z` in a new `%USERPROFILE%/pmp-reviews` | 0 | clean (`git status --porcelain` empty) |
| Pin | `git switch --detach 8c96e926…` ; `git rev-parse HEAD` | 0 | `8c96e926b0d28a182759c45c3a0141fa9a934eba`, still clean |
| Verifier | `python -B experiments/hermes-pmp/verify_chain.py --json` | **0** | `verified: true`, `historical_inputs: 14`, `acceptance_tests: 6`, 3 `bundle_sha256` entries, nonempty `next_action`, `final_commit: 5e717267…`, `model_identity_certified: false`, `session_freshness_certified: false`; stderr empty; ~23 s |
| Acceptance tests | `python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v` | **0** | `Ran 7 tests in 21.363s` / `OK`; all 7 named tests `ok` |

Expected-vs-actual checklist: exit 0 ✔; `verified=true` ✔; three
`bundle_sha256` entries ✔; `historical_inputs=14` ✔; `acceptance_tests=6` ✔;
nonempty `next_action` ✔; 7 tests ✔.

## 6. Evidence supporting the conclusions

- **Independent digest cross-check** (`sha256sum`, outside the verifier): the
  three bundles and three reports on disk match the six `PINNED` values in
  `verify_chain.py`, and the three bundle digests match the verifier's JSON output.
- **Source identity of the verifier:** `sha256(verify_chain.py) = 5a4f25d0…f044`
  and `sha256(test_pmp_replay_chain.py) = 72c70f7d…6c18` equal `verifier_sha256`
  and `acceptance_source_sha256` in
  `experiments/hermes-pmp/evidence/chain-verifier-20261006/final-checks.json`,
  so I ran the same post-review code the host recorded.
- My verifier result (`next_action`, `final_commit`, counts) matches
  `final_chain_result` in `final-checks.json`. One difference: the archived host
  run's `test_stderr` starts with `Failed to find real location of
  C:\Python314\python.exe` (a host-interpreter warning); my run has no such line.
- **Actors are recorded explicitly**: archived host receipts carry
  `logical_actor` (`Hermes`, `Claude`) and `tests_executed_by_model: false`;
  `claude-timeout.json` records the timed-out Claude attempt with
  `implementation_author: "Codex after timeout"` and
  `claude_implementation_validated: false`; `independent-review.md` records the
  two P2 findings with reproduction details.

## 7. Comparison: initial reconstruction vs executed evidence

The reconstruction from AGENTS.md + PROJECT_MEMORY.md alone was accurate for
everything the bounded commands can check: three pinned bundles (my provisional
note flagged that more bundle files are listed in memory; the verifier pins
exactly the two 2026-10-06 stages' three bundles, while the earlier mock-replay
bundles are checked by a different script, `verify_archive.py`, which I did not
run), 14 historical inputs, six fixture tests, seven acceptance tests, and the
statement that models proposed while the host wrote files and ran tests.

Assessment of clarity:
- **What happened:** clear. PROJECT_MEMORY.md separates mock vs live, success
  vs timeout, historical vs current, and the brief has a two-outcome table.
- **Who proposed changes:** clear (Hermes: fixture labels; Claude: `labels.txt`;
  Claude did *not* deliver the verifier; Codex wrote it after the timeout).
- **Who wrote files / ran tests:** clear at the logical level ("host" wrote
  files and ran tests; `tests_executed_by_model: false`). Git authorship is a
  placeholder (`PMP Experiment Host <pmp-experiment@example.invalid>` on the
  verifier commit), so Git itself does not attribute work to a person or model.
- **What remains pending:** clear (external-machine reproduction; real Windows
  junction end-to-end probe; full new suite in CI).
- **Exact next action:** clear in PROJECT_MEMORY.md, but see ambiguity A1.

## 8. Failures, ambiguities and risks

- **A1 — two "next actions".** The verifier returns the *archived* fixture
  repository's next action ("Max / dispatch host: review … then close the bounded
  experiment"), while the outer canonical memory's next action is "Max: review
  the social drafts and manually share the reproduction request linking PR #8".
  Both are correct in their own repository, but a reader who only sees the
  verifier JSON could take the archived one as the project's current next action.
  The brief mentions that `final_commit` differs from the outer commit, but does
  not say the same about `next_action`.
- **A2 — temp-folder instructions differ.** The brief tells reviewers to create
  `.review-tmp` *inside* the checkout; this round's reproduction prompt says to
  keep it *outside*. Both work; the brief's version leaves an untracked
  directory in `git status`.
- **A3 — Windows path length.** A clone under a long path (e.g. the Claude
  desktop scratch workspace under AppData, which is virtualized to
  `AppData\Local\Packages\…\LocalCache`) fails with `Filename too long`. The
  brief only says "use a normal directory with no symlink/junction ancestors";
  a short-path note would help Windows reviewers.
- **A4 — `python3` on Windows** is the Store alias stub; the brief's Windows
  block already uses `python`, so this is only a note.
- **R1 — trust anchor.** As the docs state, the pins live in the same
  repository as the evidence; matching digests prove internal consistency
  relative to this commit, not independent provenance.
- **R2 — same host, same Claude Code version** as the original experiment.
- No failures occurred in the prescribed commands.

## 9. Detected checkout changes

- Before writing reports: `git diff --exit-code` (exit 0, empty),
  `git diff --cached --exit-code` (exit 0, empty), `git status --porcelain`
  (empty), `git status --porcelain --ignored` (empty; `-B` left no `__pycache__`).
- After writing reports: only the new untracked folder
  `experiments/hermes-pmp/evidence/reproductions/claude-code/20261006T195333Z/`
  (see section 13).

## 10. Not tested

- Full 83-test suite (not required), `verify_archive.py`, PMP memory/release
  validators.
- Remote CI, PR #8 state, the offline Git-bundle/ZIP package and its manifest.
- POSIX/macOS/Linux, another machine, a different Python minor version.
- Real Windows junction/symlink end-to-end rejection (only the unit test's
  patched predicates ran).
- Any live Hermes/Claude/Codex/provider execution, billing, model identity,
  session freshness or absence of hidden memory.

## 11. Verdict

**PASS** — within the bounded scope. From a fresh clone pinned to
`8c96e926b0d28a182759c45c3a0141fa9a934eba`, the offline verifier exited 0 with
every expected field, the 7 acceptance tests passed, the six pinned digests and
the verifier/test source digests were independently confirmed, the checkout
stayed clean, and PROJECT_MEMORY.md alone was sufficient to reconstruct the
objective, state, actors, constraints and next action before running anything.
This is a separate-runtime reproduction on the same host; it does not satisfy
the "another installation / external reviewer" criterion.

## 12. Recommended next action

Have a reviewer on a different machine (ideally Linux/macOS, without Claude
Code 2.1.274) run the same two commands from a fresh clone of `8c96e92`, and
meanwhile add one sentence to the brief stating that the verifier's
`next_action` belongs to the archived fixture repository, not to the outer
project (A1).

## 13. Redactions and post-report checks

Redacted category: the local Windows account name in absolute paths (replaced by
`%USERPROFILE%` / `<user>`) and the machine hostname. No credentials appeared.
`verifier.json` contains no paths and is unmodified.

Post-report check results (run after these files were written):

```text
$ git rev-parse HEAD
8c96e926b0d28a182759c45c3a0141fa9a934eba
$ git diff --exit-code
exit 0
$ git diff --cached --exit-code
exit 0
$ git status --porcelain --untracked-files=all
?? experiments/hermes-pmp/evidence/reproductions/claude-code/20261006T195333Z/REVIEW.md
?? experiments/hermes-pmp/evidence/reproductions/claude-code/20261006T195333Z/execution.log
?? experiments/hermes-pmp/evidence/reproductions/claude-code/20261006T195333Z/verifier.json
```
