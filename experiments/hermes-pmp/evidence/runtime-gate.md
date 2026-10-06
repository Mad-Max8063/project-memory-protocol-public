# Independent Hermes runtime gate — 2026-10-06

This is installation and offline CLI evidence, NOT a live model replay.
The earlier mock/Codex bundles remain unchanged. No previous Hermes/Argon
installation, credentials or components were accessed or reused.

## Observed installation

- Windows 11 Home, build 26300.
- New official source checkout: workspace `work/hermes-pmp-runtime/source`.
- Remote: https://github.com/NousResearch/hermes-agent.git
- Pinned HEAD: `e97923c38acba2066aff9c45e35fe1584a2155b2`.
- Source tracked working tree clean after completing seven missing documentation
  paths with a command-scoped Git `core.longpaths=true`. No upstream code patch.
- Independent runtime/data root: `%TEMP%/pmp-hermes-runtime-20261006`.
- Restricted profile: `<runtime-root>/profiles/pmp`.
- Published launcher: `<runtime-root>/bin/hermes.exe`.
- Actual CLI: `Hermes Agent vgit.e97923c (2026.9.24) · upstream e97923c3`.
- Runtime Python 3.14.7, OpenAI SDK 2.24.0.
- Managed Python successfully imported SSL: `OpenSSL 3.5.8 25 Aug 2026`.
- PM app facts: extras `[]`, environment generation
  `ad045e093651409e97682838a2f06360`, input stamp
  `bf628e92c0d0681df12ff5d577faac6e470b7112dc4a23397be59760146f620d`.
- No source `products`, desktop, setup or gateway stage was run. No global PATH
  change, scheduled job, Windows security change or paid service was made.

These are retained local directories, not portable packaged runtime evidence.
Windows temporary-file cleanup can remove the runtime. Do not replace it with a
different or previous runtime silently; reconstruct a NEW runtime and repeat gates.

## Installation failures and supported alternative

1. Official pinned `scripts/install.ps1 -Stage python-deps` with separate custom
   home/source/store and `-NonInteractive -SkipBrowser -SkipComputerUse` downloaded
   uv and bootstrap Python. Bootstrap SSL import failed with Windows Application
   Control. No security policy or file trust marker was changed.
2. Running `C:/Python314/python.exe -m pm.cli install --without agent-browser
   --without cua-driver` started PM, but the long workspace home failed during
   wheel installation (`REQUESTED`, Windows error 3).
3. A shorter home fixed that step; the still-long tool store failed staging
   FFmpeg, Node and Python (Windows error 3). A short tool store fixed those path
   errors. Node/npm/Python/ripgrep succeeded; FFmpeg execution was rejected by
   Application Control (`WinError 4551`). The top-level command returned 0 despite
   the explicit FFmpeg failure: this was NOT treated as complete installation.
4. `pm.cli install --extra cron` correctly failed because the CLI activation gate
   still requires FFmpeg. No repeated attempt to execute blocked FFmpeg was made.
5. The public PM API supports selecting Python dependencies independently of the
   full tool closure. This succeeded, without raw pip/uv mutation or source edits:

```powershell
# From the NEW pinned Hermes source, all variables process-scoped:
$env:HERMES_HOME = Join-Path $env:TEMP 'pmp-hermes-runtime-20261006'
$env:HERMES_RUNTIME_DIR = Join-Path $env:HERMES_HOME 'tools'
$env:UV_CACHE_DIR = Join-Path $env:HERMES_HOME 'uv-cache'
$env:UV_NO_CONFIG = '1'
& C:\Python314\python.exe -c "import pm; pm.sync_venv([], explicit=True); print('PMP_MINIMAL_DEPENDENCIES_READY')"
```

Observed exit 0, `Installing Python dependencies` successful and the completion
marker above. The official `_launchers.py <runtime-root>/bin` then published
`hermes.exe` and `hermes-acp.exe` without the installer PATH publication stage.
This is a minimal CLI runtime; the default/full Hermes installation remains
incomplete. Multimedia, desktop and other tool use are outside this experiment.

## Offline restrictions actually checked

`windows-runtime.ps1 -Action check` completed with exit 0. Its output included:

```text
Restriction config and empty customization directories verified; no auth read.
Hermes Agent vgit.e97923c (2026.9.24) · upstream e97923c3
CLI  (0/28)
(none enabled)
```

The same tool-summary call was separately launched from the profile directory
using the bridge's minimized environment plus unchanged Windows USERPROFILE.
It also returned exit 0 and zero enabled tools. Config matched `consumer.CONFIG`;
hooks, memories and skills directories were empty; `auth.json` was absent.
The native runtime creates empty data directories and a default SOUL.md; these
were not previous conversation or copied private context. The live call still
uses `--ignore-rules`, disables memory and supplies only the bounded PMP packet.

Without USERPROFILE the actual minimized launcher failed with
`Could not determine home directory`. The bridge now preserves this existing
Windows value only for the Hermes child. No provider API keys are inherited.
The restriction config also explicitly disables `security.allow_lazy_installs`.
None of these controls is an OS sandbox or proof of model behavior.

Observed SHA-256:

| Artifact | SHA-256 |
| --- | --- |
| Actual profile config bytes | `36c68998b66cf3ceca469eb50d7031d00ad6b87f05ba1c62d2aa620fe3785573` |
| Local generated hermes.exe | `816b5a87ec5079acba2daeba4f255e0abc7e9e7d5ada063c713518da61633059` |
| Source uv.lock | `5f81d0f7057b13bac07a8ee663ee5f501f4f0d743b2bbeefd5ee1d1fd334c85a5` |
| Source pyproject.toml | `3386548996f0b045147b2607aca3adff811997881a245430EEDED04593835725` |

## Verification and remaining gate

- `python -X utf8 -m unittest discover -s tests -v`: 71 tests PASS.
  This includes 14 bridge tests, with an added child-environment regression test.
- Core memory validation, release hygiene (links/size/secrets), Python compileall
  and Git whitespace checks passed after the changes. No remote CI was run.
- Wrapper tested using Windows PowerShell 5.1. Native `python -c` quoting failed
  initially; replaced it with the bridge's `check-home` command. No credentials
  were read while resolving it.
- Runtime startup, tool selection and profile restrictions are observed locally.
  No Hermes inference, real Hermes handoff or new live continuation occurred.
- Installed version is pinned, NOT claimed latest. Its update notice was not acted on.
- Incremental paid cost so far: USD 0. Downloads/disk use are not zero resource use.
- Entitlement and subscription quota treatment remain unverified. Auth existence
  will not be sufficient evidence of coverage; no paid fallback is allowed.

One human action required: complete `windows-runtime.ps1 -Action login` using
the existing ChatGPT/Codex subscription. Do not paste token/credential contents
into the conversation. Then repeat `-Action check`, select a covered model and
run ONE bounded live replay, following the guide. If OAuth/coverage fails, stop.

Official references: [Windows installation](https://hermes-agent.nousresearch.com/docs/user-guide/windows-native/),
[PM API](https://hermes-agent.nousresearch.com/docs/reference/package-management/),
[subscription provider](https://hermes-agent.nousresearch.com/docs/integrations/providers/).

## OAuth checkpoint — 2026-10-06

The human completed device authorization remotely. The isolated runtime's
`auth add openai-codex --no-browser --timeout 180` command reported an added
OAuth credential and exited 0. No credential contents, device codes or account
identifiers are included here; credentials were not read by the verifier.

After authorization, `windows-runtime.ps1 -Action check` exited 0 and again
reported the pinned upstream version, matching restriction config, empty
customization directories and `CLI (0/28)` / `(none enabled)`.

This supersedes the earlier pending-OAuth next action, not the historical
installation observations. Model selection and actual subscription coverage
remain pending. No model inference, new live replay, purchase or paid API
fallback occurred. Conclusion remains B. PARTIALLY VALIDATED.

## OAuth store discrepancy — 2026-10-06

After the above checkpoint, a read-only account-catalog probe using Hermes'
credential resolver returned `No Codex credentials stored`. The first Hermes
`auth status openai-codex` call also reported logged out; `auth list` showed only
the pre-existing Copilot CLI source and no OpenAI Codex entry.

A second device authorization completed and the CLI printed
`Added openai-codex OAuth credential #1`. Immediately afterward, the CLI again
reported `logged out`, and `auth list openai-codex` listed no credential. These
commands did not display or read token contents. The auth file's path/size/time
were checked as filesystem metadata only. No account catalog became available;
no model call or replay was attempted.

### Pinned-source diagnosis and isolated-home workaround

Three OAuth device authorizations reported success in total. The latest used
both the runtime root in `HERMES_HOME` and explicit `-p pmp`; Hermes still
reported logged out. The profile `auth.json` metadata remained 698 bytes with
its earlier modification time; its contents were never opened. Focused source
inspection of pinned upstream `e97923c38acba2066aff9c45e35fe1584a2155b2`
identified a path consistent with these observations:

1. The launcher set `HERMES_HOME` to the named path `<runtime-root>/profiles/pmp`.
   `get_default_hermes_root()` consequently treats `<runtime-root>` as the
   global root, while the profile's `auth.json` has no locally owned Codex pool
   rows.
2. `CredentialPool.add_entry()` calls `_persist()` when no borrowed root rows
   were loaded. `persist_pool_entries()` special-cases the single-use-refresh
   `openai-codex` provider and routes a profile with no local rows to
   `_update_root_pool_rows()`.
3. That helper is explicitly update-only: it updates root rows with matching
   existing IDs and does not insert the newly added credential. The caller can
   still print `Added ...` because it does not verify a successful disk write.

This source path explains the observed message/store mismatch; it is not a claim
that every Hermes profile or provider has this behavior. We did not inspect
credential contents, patch upstream Hermes, or rerun OAuth during diagnosis.

The PMP runtime wrapper now provisions a separate restricted `pmp-home` outside
the named-profile hierarchy. It uses that directory as its own `HERMES_HOME`,
checks the zero-tool restriction before login, and verifies Hermes' own
`auth status` afterward without printing account details. The existing
`profiles/pmp` directory and all other Hermes tracks are left untouched.

The standalone home initially lacked Hermes' managed Python dependency
environment; its first CLI tool-summary check failed on missing `ruamel.yaml`.
Using the official PM API with `extras=[]`, the isolated home and existing
temporary tool/cache directories, minimal dependencies completed successfully.
The wrapper's offline check then passed: Hermes `vgit.e97923c`, OpenAI SDK
2.24.0, and CLI `0/28` tools. No auth contents were read.

After allowing only its temporary fixture paths, PMP bridge tests passed (14/14),
`validate_memory.py PROJECT_MEMORY.md` passed, `validate_release_candidate.py`
passed (Core 0.2.2/profile 0.1.1, links, size and secret scan), and
`git diff --check` passed. A prior sandbox-only test invocation failed on temp
directory ACLs; it is superseded by the successful 14/14 run above. The focused
upstream Hermes auth tests remain unrun because the base Python lacks `ruamel.yaml`.

One final device authorization was started in this standalone home after those
checks passed. Hermes timed out after 15 minutes with exit 1; the wrapper stopped
without retrying. A follow-up native `auth status openai-codex` reports logged
out and no Codex credentials. The device code is intentionally not recorded. No
model catalog request or inference has occurred.

### Current Hermes store resolution — read-only probe

Using the pinned `hermes_constants` path resolvers with `HERMES_HOME` switched
in-process (no auth files opened), the old and corrected paths resolve as:

| Mode | `HERMES_HOME` / default root | Active `auth.json` | Global fallback |
| --- | --- | --- | --- |
| Old named profile | `<runtime-root>/profiles/pmp` / `<runtime-root>` | `<runtime-root>/profiles/pmp/auth.json` | `<runtime-root>/auth.json` |
| New standalone home | `<runtime-root>/pmp-home` / `<runtime-root>/pmp-home` | `<runtime-root>/pmp-home/auth.json` | none |

A separate filesystem metadata check found `pmp-home/auth.json` absent after
the flow timed out. This confirms no credential persisted to the new home; it
does not invalidate the path-resolution fix. Do not start another device flow
without a fresh human decision to complete OAuth.

The focused pinned-Hermes pytest checks were attempted but could not collect
because the available `C:\Python314` environment lacks `ruamel.yaml`; the
source-level diagnosis above is code-path analysis corroborated by the observed
CLI/store metadata, not a passing upstream regression test. The earlier offline
check passed; its final authorization timed out. This historical checkpoint is
superseded by the live replay checkpoint below.

## Live subscription replay — 2026-10-06

After Max explicitly authorized one retry, the device flow completed in the
standalone `pmp-home`; Hermes' read-only auth status confirmed `openai-codex`.
The provider's authenticated model catalog listed `gpt-5.6-luna`. Exactly one
bounded inference call succeeded with the existing subscription. No account
details, OAuth material, device codes, or API keys were read into or saved from
the credential store. This confirms the one observed call only, not future
eligibility, quota limits, or no-overage terms.

Two replay attempts before that call failed at the runtime-version preflight,
before model invocation: the replay's nested minimized Windows environment had
omitted `USERPROFILE`. `hermes --version` worked when that variable was present.
The adapter's allowlist now carries the existing `USERPROFILE` for Hermes'
`Path.home()` resolution while excluding `OPENAI_API_KEY`. A regression test
asserts both. After this correction the single live replay completed; the report
shows the Hermes proposal, host verification, handoff commit, and Python
continuation. A later separate Codex process/agent independently reran the three
fixture tests and verified hashes; see
`live-replay-20261006/codex-continuation.md`.

Archived report: `live-replay-20261006/replay-report.json`.
Baseline: `4488a97dc68b7b614365d0f274edbf665e679f41`.
Handoff: `d2e225b61857be0e0b79c5d28116ae6a9800f7c7`.
Input PMP memory SHA-256:
`9d22adc0cd8eb1adc1f1bc83c09c8e1fc4d37e57ce6c3f29555257452e5ea199`.
Input packet SHA-256:
`76e6c6ce5989a96aeefb5266db704e83063fc2afb25f6b39a93c00ac64d269ff`.
Git bundle SHA-256:
`b729b7f2220f5e639ad9e43f205314c45055d69eab966689b0438f178398de17`.
The report's immediate continuation field correctly says Python (not Codex) and
`fresh_codex_executed=false`; the later Codex result is separate evidence and
does not retroactively alter that timestamped report.

The run used the already available Codex subscription and may have consumed
allowance. Exact metering was unavailable; incremental purchase/API charges
observed: USD 0. No further model calls are authorized or needed for this
bounded replay. No previous Hermes/Argon track was accessed or changed.
