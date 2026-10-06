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

**Blocker:** Hermes' login-success message does not match the read-only provider
status and pool listing for the isolated profile. The next step is to diagnose
profile/auth-store resolution in the pinned Hermes source before requesting any
further human authorization. Do not run another login, infer, refresh tokens,
read auth-store contents or change the incomplete install in the meantime.
