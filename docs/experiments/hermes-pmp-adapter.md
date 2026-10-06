# PMP → Hermes → PMP — independent interoperability experiment

## Objective and hypothesis

Test whether a bounded participant can consume portable operational state, make
one fixture proposal and leave enough evidence for a context-free continuation.
PMP stays vendor-neutral; Hermes is an optional actor/runtime, never Core state.
This does not evaluate general autonomy, usefulness or quality of Hermes.

Conclusion to date: **B. PARTIALLY VALIDATED**. The local bridge and mock replay
work; actual Hermes/provider execution remains unverified. See recorded evidence
in experiments/hermes-pmp/evidence/RESULT.md in the repository root.

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

## Optional live Hermes connection — inference NOT YET VERIFIED

On 2026-10-06 a NEW pinned minimal Windows CLI runtime was installed and its
zero-tool profile checked locally. See
[runtime gate evidence](../../experiments/hermes-pmp/evidence/runtime-gate.md).
This is not a real model replay; subscription OAuth is the remaining human gate.
From this experimental repository, the prepared commands are:

```powershell
& ./experiments/hermes-pmp/windows-runtime.ps1 -Action check
& ./experiments/hermes-pmp/windows-runtime.ps1 -Action login
```

`login` checks restrictions, prints the device-login instructions and waits for
human authorization. It makes no model call and restores process environment
afterward. Never paste credentials here. It deliberately uses the NEW runtime
under `%TEMP%/pmp-hermes-runtime-20261006`, not an existing global Hermes runtime.
The temporary runtime can be removed by Windows cleanup; missing runtime is a
hard gate, not permission to reuse the blocked track. No global PATH was changed.
For the later single live replay, after OAuth and covered-model verification:

```powershell
$pmpSavedPath = $env:Path
try {
    $env:Path = (Join-Path $env:TEMP 'pmp-hermes-runtime-20261006/bin') + ';' + $pmpSavedPath
    python experiments/hermes-pmp/replay.py --mode hermes --home (Join-Path $env:TEMP 'pmp-hermes-runtime-20261006/profiles/pmp') --model '<subscription-covered-model>' --archive '<new-empty-evidence-directory>'
} finally {
    $env:Path = $pmpSavedPath
}
```

The full/default source installation failed on blocked FFmpeg. The successful
minimal runtime uses the official PM dependency API with no Python extras.
It does not grant multimedia/tool availability or bypass Windows protection.
The bridge preserves unchanged USERPROFILE for Windows Path.home() and otherwise
keeps the minimized environment. Automatic dependency installation is disabled.

Hermes currently documents --query-file, --oneshot, --ignore-rules,
--format stream-json and one-turn limits in its
[CLI reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands/).
The [provider guide](https://hermes-agent.nousresearch.com/docs/integrations/providers/)
documents `openai-codex` subscription OAuth, but does not fully document plan
eligibility/quota semantics. Availability and no-overage behavior need human
confirmation. Never fall back to a paid API.

After installing independently, create a new dedicated home outside this repo:

```powershell
# Replace the placeholder with a NEW local directory, not any prior Hermes home.
python experiments/hermes-pmp/consumer.py init-home --home '<new-isolated-home>'
$env:HERMES_HOME = '<new-isolated-home>'
hermes auth add openai-codex
```

The human completes subscription OAuth, without copying credentials into Git or
the model packet. Preserve generated config.yaml; no .env, plugins, hooks,
memories or skills may be present. The config explicitly sets platform_toolsets
cli to [], disables memory/title generation, external-login adoption and fallback.
Do not use `--safe-mode`: it ignores this restriction config. Do not rely on
`--toolsets ""`: the currently inspected CLI treats empty strings as defaults.
The live launcher works from the non-code isolated home, with a minimized child
environment, no resume flag and no transcript. This is not an OS sandbox.

Choose a subscription-covered model explicitly, then run one bounded attempt:

```powershell
python experiments/hermes-pmp/replay.py --mode hermes --home '<new-isolated-home>' --model '<subscription-covered-model>'
```

The runner checks runtime/profile/auth availability first. It captures successful
structured completion events and rejects any recorded tool call. This post-run
check is NOT prevention if a Hermes regression enables tools. Verify current
tool-selection semantics on the installed version before authorizing a live run.
Unknown/mismatched CLI versions can fail; do not bypass the guard or enable tools.
The host alone writes the fixture and runs tests. Keep a failed attempt local,
do not retry blindly and do not treat the existence of auth.json as proof of
entitlement. Profile auth is sensitive even though absent from repo evidence.

## Fresh Codex continuation

Start a separate Codex session with only the result repo and this instruction:
"Read AGENTS.md and PROJECT_MEMORY.md; follow the bounded Next action using only
repository evidence. Do not read earlier conversations or other worktrees."

The initial author is this Codex session, not an independently fresh baseline
session. The automatic fresh verifier is Python, not a model. Any separately
observed Codex continuation is recorded in RESULT.md and its own bundle; do not
rewrite the initial report to claim a later check occurred earlier.

## Tests and evidence boundaries

Baseline: 57 original unit tests passed, release hygiene/memory passed, packaged
demo passed six tests. Thirteen new tests cover exact state serialization,
handback/decisions/evidence/next action, stale input, invalid scope/schema, trusted
test boundary, rollback, append-only history/lock, path/link rejection, tamper
rejection, fresh-process reconstruction, CLI completion/tool rejection, missing
runtime fail-closed and backward compatibility. Total: 70 passing unit tests.
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
- Live Hermes may consume subscription quota and its eligibility remains
  unverified. No automatic model download, account activation or paid fallback.

## Result and exact next step

The bridge's transport/storage/continuation mechanism is locally verified. Do
not claim the actual PMP → Hermes → PMP cycle until one real Hermes run and its
runtime evidence are observed. First check whether a NEW independent runtime and
subscription-covered OAuth route are available; if not, leave this harness as
the result. Do not unblock or touch the older Hermes/Argon track.
