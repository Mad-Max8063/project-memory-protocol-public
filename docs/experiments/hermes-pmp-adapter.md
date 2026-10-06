# PMP → Hermes → PMP — independent interoperability experiment

## Objective and hypothesis

Test whether a bounded participant can consume portable operational state, make
one fixture proposal and leave enough evidence for a context-free continuation.
PMP stays vendor-neutral; Hermes is an optional actor/runtime, never Core state.
This does not evaluate general autonomy, usefulness or quality of Hermes.

Conclusion: **A. VALIDATED** for one bounded, reproducible PMP → Hermes → PMP
handoff followed by an independent Codex continuation. This does not validate
general autonomy, model identity, session freshness, subscription guarantees,
or the truth of model assertions. See the live replay evidence below.

The later authorized Claude continuation is documented separately in
[Hermes → Claude → Codex](hermes-claude-continuation.md); it reuses the real
Hermes bundle without rerunning Hermes or changing PMP Core.

## Inspection and integration point

Baseline main `2d9da5549d802c27b7a47293384d3f0d59b0ff13` was confirmed through
`git ls-remote` on 2026-10-06. Existing worktrees were not copied or modified.
Core 0.2.2 provides the eight Markdown sections, visible evidence levels, logical
actor in Identity, START/END and session-record semantics. A handoff is a session
record, not a mandatory Core JSON schema. The optional profile 0.1.1 requires
additional external verification; this experiment does NOT claim that profile.

Reused unchanged: scripts/markdown_sections.py, scripts/validate_memory.py,
templates/SESSION.md conventions and existing instruction-surface adapter rules.
The stable branch has no executable MCP server. A file/stdio proposal bridge is
smaller than introducing an MCP service; no server, port, provider SDK or database
is needed. No previous Hermes/Argon component, Obsidian, Jev or Cloudflare track
is imported. The published replay is unchanged.

## Architecture and components

```text
Codex baseline author
  ↓
PMP repository (PROJECT_MEMORY.md + TASK + acceptance definition)
  ↓
Hermes Adapter (derived input packet, exact memory/input hashes)
  ↓
Hermes proposal [or explicit mock, NOT Hermes]
  ↓
Host scope validation + fixed tests + evidence + PMP Handoff
  ↓
Fresh clone / Codex continuation
```

Files under experiments/hermes-pmp:

- adapter.py: `read_state` and `create_handoff`; raw memory plus parser-derived
  state, decisions, constraints, actor, previous handoff, evidence and next action.
- consumer.py: deterministic mock or optional bounded Hermes CLI call.
- replay.py: local baseline Git commit, input/output receipt, host verification,
  single atomic Git handoff commit, fresh clone and separate verifier process.
- continuation.py: recover next action and validate hashes/tests from result repo.
- seed/: JSON fixture, three acceptance tests, task, AGENTS and canonical memory.
- evidence/: observed report, Git bundle and closure/result documentation.

The transport proposal JSON is internal to this experiment, not a PMP schema
change. It supplies actor, action attempted, result, replacement fixture, proposed
decisions, unresolved issues, intended next actor and exact next action. Files
changed, executed commands, timestamp, hashes and verification status come from
the host, not untrusted model assertions. Canonical handoff uses ordinary Markdown.
No numeric confidence score is introduced. Active decisions are not overwritten.

## Requirements and installation

Python 3.12+ (is_junction support) and Git; stdlib only for the local bridge.
The preparation used Windows, Python 3.14 and Git for Windows. No pip/npm install
is required for local tests. Use a normal checkout of this experimental branch.

Real Hermes was not found on PATH, in the known native source-install launcher
directory or as an installed Hermes MSIX package. Docker daemon was unavailable;
WSL listed docker-desktop only. These observations do not prove Hermes exists
nowhere on the machine; no exhaustive scan or previous-track inspection occurred.

If a live run is desired, install a NEW independent Hermes runtime via its
[official Windows instructions](https://hermes-agent.nousresearch.com/docs/user-guide/windows-native/).
Do not reuse a previous experiment/profile, run its installer blindly, choose
Nous Portal or purchase credits. Installation/provider login were not attempted.

## Local execution and reproduction

From the protocol repo root:

```powershell
python -m unittest discover -s tests -v
python scripts/validate_memory.py PROJECT_MEMORY.md
python scripts/validate_release_candidate.py
python experiments/hermes-pmp/replay.py --mode mock
```

Replay prints a new retained run directory. Read its fresh-result/PROJECT_MEMORY.md
and `.project-memory/sessions/hermes-handoff.md`. The producer is explicitly
`mock-hermes`. input-pmp.json and consumer-output.json are immutable historical
evidence, not live state or chat memory. Host tests run with isolated Python:

```powershell
python -I -m unittest discover -s . -p test_fixture.py -v
```

To verify the archived run, clone its bundle to a new directory and invoke
continuation.py, as in experiments/hermes-pmp/README.md. A new generated run has
new commits/timestamps; successful gates, not identical SHAs, are the invariant.
Pass `--archive <new-empty-directory>` to retain its report and bundle elsewhere.

## Live Hermes replay — 2026-10-06

A fresh device OAuth flow completed in the isolated `pmp-home`; Hermes' native
read-only auth status confirmed the credential. The authenticated account
catalog listed `gpt-5.6-luna`; this is evidence of one usable catalog entry, not
a general quota/no-overage guarantee. Exactly one bounded real inference ran
using the pinned minimal Hermes CLI `vgit.e97923c` (2026.9.24), OpenAI SDK 2.24.0,
one turn, no enabled tools, no fallback, and the existing subscription. No API
key, credential, device code, or account detail was stored in the repository.

The agent proposed normalized fixture labels only. The host validated scope,
updated the fixture, ran its three acceptance tests, wrote evidence and PMP
handoff, and committed the result. A separate Codex continuation with no
inherited turns opened the result clone, independently reran the three tests,
verified recorded hashes, and wrote a continuation receipt. It used the PMP
state/evidence in that clone, not the parent conversation.

Replay archive: `experiments/hermes-pmp/evidence/live-replay-20261006/`.
`replay-report.json` records baseline `4488a97dc68b7b614365d0f274edbf665e679f41`,
handoff `d2e225b61857be0e0b79c5d28116ae6a9800f7c7`, input memory and packet hashes,
host command and output, timestamps, changed files, and explicit non-claims.
The bundle SHA-256 is
`b729b7f2220f5e639ad9e43f205314c45055d69eab966689b0438f178398de17`.
The separate Codex receipt is `codex-continuation.md`.

Two earlier replay invocations failed before inference because the minimized
nested Windows environment omitted `USERPROFILE`, which Hermes needs for
`Path.home()`. The bridge now preserves that path while excluding provider API
keys; a regression test protects both properties. These failures consumed no
inference. The archived successful report is not rewritten to imply that the
later Codex continuation had already happened.

The minimal runtime used the official PM API without Python extras; the default
installation hit an FFmpeg environment blocker. The restricted profile had
zero enabled CLI tools, disabled memory/title generation and dependency installs.
These are runtime/profile checks, not an OS sandbox or proof of model behavior.
The temporary runtime may be removed by Windows cleanup. No other Hermes track
was accessed or modified.

## Fresh Codex continuation

The observed separate Codex continuation is recorded at
`experiments/hermes-pmp/evidence/live-replay-20261006/codex-continuation.md`.
It used only the result clone, whose instruction was:
"Read AGENTS.md and PROJECT_MEMORY.md; follow the bounded Next action using only
repository evidence. Do not read earlier conversations or other worktrees."

The Hermes replay report correctly records that its immediate continuation was
Python and that fresh Codex was still required at that timestamp. The later
Codex result is a separate receipt. Git evidence cannot certify the identity of
either model or true session freshness.

## Tests and evidence boundaries

Baseline: 57 original unit tests passed, release hygiene/memory passed, packaged
demo passed six tests. Thirteen new tests cover exact state serialization,
handback/decisions/evidence/next action, stale input, invalid scope/schema, trusted
test boundary, rollback, append-only history/lock, path/link rejection, tamper
rejection, fresh-process reconstruction, CLI completion/tool rejection, missing
runtime fail-closed, backward compatibility, and Windows home preservation
without provider API key inheritance. Total after the fix: 72 passing unit tests.
The three fixture acceptance tests are separate; before task two fail as expected,
after host import all three pass and a fresh verifier repeats them successfully.

Tests do not validate a real Hermes CLI, a real provider, model understanding,
autonomy or absence of private model memory. Structural PMP validation cannot
establish truth, identity, authorization, real evidence content or complete secret
detection. All six known Core limits remain unchanged. No external CI ran.

## Security, failure paths and costs

- Only JSON data is accepted. No model code/shell/path is executed. The fixed
  acceptance code and instruction/task content must match the trusted seed;
  LF/CRLF are equivalent for this allowlist only. Evidence hashes always bind
  the actual bytes, not a newline-normalized claim.
- READ can inspect valid declared 0.2.2 memories; WRITE deliberately supports
  only this trusted fixture baseline. It is not a general-purpose PMP editor:
  the baseline check prevents lossy rewriting of arbitrary Markdown by the
  experiment's section-derived renderer. Another task needs separate scope/tests.
- Input hashes are checked before writes; cooperating bridges use an exclusive
  lock. Existing evidence/handoff cannot be silently overwritten.
- Individual files use same-directory write/rename; rollback handles ordinary
  exceptions. An OS crash can interrupt multi-file updates: publication is the
  caller's single Git commit, not a filesystem-wide transaction. Do not consume
  partial uncommitted state. External writers/TOCTOU are not fully excluded.
- Reject traversal, symlinks and junctions on root/fixed paths. This is scoped
  local validation, not a multi-tenant or hostile-host security boundary.
- No production credentials, server, database, MCP gateway, deploy or destructive
  cleanup. Temporary replay dirs are retained intentionally. Delete them only
  with separately scoped human authorization after retaining required evidence.
- Real incremental paid cost so far: USD 0. The mock makes no model call. A Codex
  continuation consumes existing subscription allowance; no new credits purchased.
- The one live `gpt-5.6-luna` inference used the existing subscription. It may
  have consumed its allowance; exact quota/cost accounting is unavailable here.
  No API-key fallback or credit purchase occurred. Do not infer ongoing quota
  or no-overage guarantees from this single successful call.

## Result and exact next step

The bounded PMP → Hermes → PMP cycle and separate evidence-based Codex
continuation were observed and archived. The success claim is limited to this
fixture and this run: it does not establish identity, freshness, general
interoperability, autonomy, truthfulness, or long-term provider coverage. Next,
finish local validation and commit this scoped evidence. Do not make more model
calls or unblock/touch the older Hermes/Argon track.
