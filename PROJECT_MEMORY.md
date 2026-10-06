# Project Memory Protocol — independent Hermes adapter experiment

> Canonical operational memory for this experimental branch only.
> Protocol: PMP `0.2.2`
> Canonical path: `PROJECT_MEMORY.md`

## Identity

- Project: PMP public distribution — independent Hermes interoperability track
- Repository: https://github.com/Mad-Max8063/project-memory-protocol-public
- Human authority: Max / Max Devs Solutions
- Branch: `experiment/hermes-pmp-adapter`
- Starting revision: `2d9da5549d802c27b7a47293384d3f0d59b0ff13`
- Last updated: 2026-10-06
- Last actor: Codex (logical participant; no identity attestation)

## Current state

- [VERIFIED] Separate branch/worktree starts from remote-confirmed main.
  Existing Jev, MCP and Artifacts worktrees were not reused or modified.
- [VERIFIED] Core 0.2.2, profile 0.1.1, validators, published replay and existing
  adapters remain unchanged. Branch adds an optional stdlib-only file bridge.
- [VERIFIED] Baseline 57 unit tests, memory/release gates and six-test packaged
  demo passed. Thirteen new bridge tests and full discovery (70) passed.
  See experiments/hermes-pmp/evidence/RESULT.md for commands and boundaries.
- [VERIFIED] Local mock replay records baseline
  `a1b7d1b7bac7456178b694eaadf497d8aa193fa9` and handoff
  `9be68212880c48724228e50879ae2def65326654`: input state, proposal,
  host-run tests, evidence, preserved decisions and exact next action.
- [VERIFIED] A Codex subagent spawned without inherited turns read only the
  result clone and repository evidence, recognized the mock producer, checked
  hashes and reran three tests. Its receipt/memory commit is
  `25e3b504bbc66b64904297a95acc5b27d2623379`. This is observed context
  delivery and local verification, not proof of hidden identity or freshness.
- [VERIFIED] Both saved Git bundles were cloned and independently checked by
  `python experiments/hermes-pmp/verify_archive.py`; bundle digests, lineage,
  change boundaries, host evidence, canonical state and acceptance gates pass.
- [DOCUMENTED, HISTORICAL] Conclusion at the initial experiment commit was B.
  PARTIALLY VALIDATED because actual Hermes/provider execution was unverified.
  The earlier mock/Codex evidence remains unchanged; the live addendum below
  supersedes that checkpoint without rewriting it.
- [VERIFIED] A NEW pinned Hermes minimal Windows CLI runtime now starts locally:
  upstream `e97923c38acba2066aff9c45e35fe1584a2155b2`, Python 3.14.7,
  SDK 2.24.0; CLI tool summary shows 0/28 enabled. No prior track was accessed.
  See experiments/hermes-pmp/evidence/runtime-gate.md for installation failures,
  successful PM-only dependency selection and observed profile/launcher hashes.
- [VERIFIED, HISTORICAL] The Hermes OAuth device flow reported success three times and printed
  “Added openai-codex OAuth credential #1”. However, subsequent read-only
  `auth status openai-codex` reports logged out; `auth list openai-codex` shows
  no entry, and Hermes' read-only credential resolver reports no Codex credentials.
  Only the existing Copilot CLI source is listed. Credential contents were never
  inspected or recorded. The post-login wrapper check still reports CLI 0/28 tools.
  No custom hooks, memories or skills; automatic installs are disabled. Windows USERPROFILE
  is preserved only to make Path.home() work. Wrapper check and 71 tests pass
  (14 bridge tests). At that checkpoint no Hermes inference, purchase, deployment or global PATH
  change occurred; incremental paid cost remains USD 0.
- [DOCUMENTED, HISTORICAL] The OAuth/store
  discrepancy blocks model-catalog and inference checks. Pinned-source inspection
  found a plausible no-insert path for first-time `openai-codex` auth in an empty
  named profile. The Windows wrapper now prepares a separate restricted standalone
  home and verifies Hermes' own auth status after login; see runtime-gate evidence.
  A read-only Hermes path probe confirms `pmp-home` is its own default root with
  no global auth fallback. The final device flow timed out after 15 minutes and
  native `auth status` confirms logged out; `pmp-home/auth.json` is absent.
  At that historical checkpoint, entitlement/quota, live inference and real
  Hermes handoff remained unverified.
  The minimal temporary runtime is not a complete Hermes install
  and may be removed by Windows cleanup; do not silently substitute another.
- [DOCUMENTED] Stable release lifecycle evidence remains in baseline history
  and docs; this experiment neither changes nor re-audits the released lifecycle.
- [VERIFIED] After the earlier failed OAuth/store attempts, one device flow in
  the isolated `pmp-home` completed and Hermes `auth status` confirmed the
  `openai-codex` credential without exposing account data. Its live catalog
  listed `gpt-5.6-luna`; exactly one bounded replay then completed through the
  pinned Hermes CLI `vgit.e97923c` using the existing subscription. No model
  identity or entitlement/quota guarantee is inferred beyond that observed call.
- [VERIFIED] The real replay handoff is archived at
  `experiments/hermes-pmp/evidence/live-replay-20261006/` with report and Git
  bundle. Hermes proposed only the two fixture labels; host ran all three
  acceptance tests and committed the handoff. An independent Codex continuation
  with no inherited turns inspected the fresh clone, reran all three tests,
  checked evidence hashes, and recorded its receipt. This is observed portable
  context recovery, not cryptographic proof of model identity/session freshness.
- [VERIFIED] Replay initially hit two pre-inference failures because the
  minimized nested Windows environment omitted `USERPROFILE`; the adapter now
  preserves that home path while continuing to exclude provider API keys. A
  regression test covers both conditions. Closure gates pass: 72 tests, PMP
  memory validation, release metadata/links/size/secret scan, and diff checks.
  No remote CI was run.
- [VERIFIED] Authorized Claude extension completed from the real Hermes bundle,
  without rerunning Hermes. Claude Code 2.1.274, existing claude.ai Pro login,
  produced a labels.txt proposal; the host passed six fixture/manifest tests.
  The successful receipt reports claude-sonnet-5, one turn and no tools, with
  auxiliary Haiku usage also recorded. One prior invocation exited 1; its
  provider-request count and cause are unknown. See the dedicated guide.
- [VERIFIED] A separate Codex subagent with no inherited turns read the resulting
  clone, passed all six tests and verified fourteen historical input hashes.
  Its receipt/canonical update is preserved in replay commit
  `5e717267e23e39a854347ade7e9efa545269c227` and a second bundle. Both Claude-stage
  bundles verified; full repository discovery passed 76 tests. The bounded
  chain is A. VALIDATED, without certifying identity, hidden session freshness,
  general autonomy, provider coverage or billing.

## Active decisions

1. Keep PMP canonical and vendor-neutral. Hermes is an optional actor/runtime,
   not Core state or a mandatory dependency.
2. Reuse unchanged Core parser/validator and ordinary Markdown session records.
   Proposal JSON is non-normative transport, not a new PMP schema.
3. Choose the smallest low-risk task: normalize two JSON fixture labels.
   Only the bridge writes fixed paths and executes trusted fixed tests.
4. Separate producer assertions, mock versus live Hermes, host verification and
   Codex continuation. Do not claim identity, freshness or profile conformance.
5. Keep the integration experimental; no additional infrastructure or general
   autonomy claims after this single bounded live replay.
6. Claude receives only the nine-file synthetic fixture packet. Reuse archived
   Hermes evidence, preserve it historically, and give the host fixed write/test
   authority. Further experiments require a new scoped task.

## Constraints

- Do not access, modify, reactivate, repair or depend on the blocked previous
  Hermes/Argon experiment. No Argon, Obsidian, Jev or Cloudflare dependency.
- No Core/spec/version/profile changes, refactor, production credentials,
  destructive changes, deploy, services, credit purchase or subscription activation.
- Target incremental paid cost: USD 0. Existing Codex allowance is not unlimited;
  Hermes provider eligibility/quota semantics are not yet verified.
- No push, PR, main merge, tag, release or publication.
- Generated input snapshots are historical evidence only; current state remains
  solely in each repository's PROJECT_MEMORY.md.
- Bridge lock/atomic file writes are not an OS sandbox or crash-proof multi-file
  transaction. Publish dependent state/evidence together in one Git commit.
- Preserve all six known Core structural-validation limits and evidence boundaries.

## Priorities

1. Preserve the completed Hermes/Claude/Codex chain with replay bundles,
   independent receipt, tests and the local experimental commit.
2. Report the observed result and consumption boundaries; no further live calls,
   subscription purchase, push, PR, merge, release or Hermes/Argon access.

## Next action

Max: review docs/experiments/hermes-claude-continuation.md and the archived Codex
receipt. The bounded experiment is complete; any broader task, additional model
call or publication needs a new scoped instruction.

## Evidence

- experiments/hermes-pmp/evidence/RESULT.md
- experiments/hermes-pmp/evidence/TESTS.md
- experiments/hermes-pmp/evidence/replay-report.json
- experiments/hermes-pmp/evidence/replay.bundle
- experiments/hermes-pmp/evidence/fresh-codex.json
- experiments/hermes-pmp/evidence/fresh-codex.bundle
- experiments/hermes-pmp/evidence/runtime-gate.md
- experiments/hermes-pmp/evidence/live-replay-20261006/replay-report.json
- experiments/hermes-pmp/evidence/live-replay-20261006/replay.bundle
- experiments/hermes-pmp/evidence/live-replay-20261006/codex-continuation.md
- experiments/hermes-pmp/evidence/claude-continuation-20261006/claude-report.json
- experiments/hermes-pmp/evidence/claude-continuation-20261006/fresh-codex.json
- experiments/hermes-pmp/evidence/claude-continuation-20261006/codex-after-claude.md
- experiments/hermes-pmp/evidence/claude-continuation-20261006/claude-replay.bundle
- experiments/hermes-pmp/evidence/claude-continuation-20261006/fresh-codex.bundle
- experiments/hermes-pmp/claude_replay.py
- tests/test_claude_pmp_continuation.py
- docs/experiments/hermes-claude-continuation.md
- experiments/hermes-pmp/windows-runtime.ps1
- experiments/hermes-pmp/verify_archive.py
- experiments/hermes-pmp/README.md
- docs/experiments/hermes-pmp-adapter.md
- tests/test_hermes_pmp_adapter.py
- SPEC.md
- profiles/evidence-backed-handoff/PROFILE.md

## Update rules

- Read this memory and repository instructions before significant work.
- Update state, decisions, evidence and the single next action together.
- Keep detailed results in evidence; never promote mock to live runtime evidence.
- No identity, freshness, autonomy or semantic-truth guarantees from Git.
- Human authority > current evidence > canonical memory > docs > history > chat.
