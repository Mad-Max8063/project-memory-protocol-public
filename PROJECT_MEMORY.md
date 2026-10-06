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
- [DOCUMENTED] Conclusion: B. PARTIALLY VALIDATED. Actual Hermes installation,
  subscription entitlement and live inference were unverified at the initial
  experiment commit. The earlier mock/Codex evidence remains unchanged.
- [VERIFIED] A NEW pinned Hermes minimal Windows CLI runtime now starts locally:
  upstream `e97923c38acba2066aff9c45e35fe1584a2155b2`, Python 3.14.7,
  SDK 2.24.0; CLI tool summary shows 0/28 enabled. No prior track was accessed.
  See experiments/hermes-pmp/evidence/runtime-gate.md for installation failures,
  successful PM-only dependency selection and observed profile/launcher hashes.
- [VERIFIED] The Hermes OAuth device flow reported success three times and printed
  “Added openai-codex OAuth credential #1”. However, subsequent read-only
  `auth status openai-codex` reports logged out; `auth list openai-codex` shows
  no entry, and Hermes' read-only credential resolver reports no Codex credentials.
  Only the existing Copilot CLI source is listed. Credential contents were never
  inspected or recorded. The post-login wrapper check still reports CLI 0/28 tools.
  No custom hooks, memories or skills; automatic installs are disabled. Windows USERPROFILE
  is preserved only to make Path.home() work. Wrapper check and 71 tests pass
  (14 bridge tests). No Hermes inference, purchase, deployment or global PATH
  change occurred; incremental paid cost remains USD 0.
- [DOCUMENTED] Conclusion remains B. PARTIALLY VALIDATED. The OAuth/store
  discrepancy blocks model-catalog and inference checks. Pinned-source inspection
  found a plausible no-insert path for first-time `openai-codex` auth in an empty
  named profile. The Windows wrapper now prepares a separate restricted standalone
  home and verifies Hermes' own auth status after login; see runtime-gate evidence.
  Entitlement, quota,
  actual zero-tool model execution and real Hermes handoff remain unverified.
  The minimal temporary runtime is not a complete Hermes install
  and may be removed by Windows cleanup; do not silently substitute another.
- [DOCUMENTED] Stable release lifecycle evidence remains in baseline history
  and docs; this experiment neither changes nor re-audits the released lifecycle.

## Active decisions

1. Keep PMP canonical and vendor-neutral. Hermes is an optional actor/runtime,
   not Core state or a mandatory dependency.
2. Reuse unchanged Core parser/validator and ordinary Markdown session records.
   Proposal JSON is non-normative transport, not a new PMP schema.
3. Choose the smallest low-risk task: normalize two JSON fixture labels.
   Only the bridge writes fixed paths and executes trusted fixed tests.
4. Separate producer assertions, host verification, mock process, actual Codex
   continuation and missing real-Hermes evidence. Do not claim profile conformance.
5. No additional mock cases or infrastructure until the runtime gate is resolved.

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

1. Complete the one final subscription OAuth currently pending in the new
   standalone `pmp-home`; the wrapper checks Hermes `auth status` and stops if it
   is still logged out. Offline check passed with CLI 0/28.
2. If Hermes confirms storage, check the actual account-scoped Luna catalog and
   only then run one bounded replay. Otherwise retain this partial result; no more
   OAuth, paid API, simulated success or Hermes/Argon access.

## Next action

Codex: finish the one pending device authorization in the new standalone home.
Require Hermes' read-only auth status to confirm it before checking Luna or
attempting the single live replay. If that gate fails, stop and retain the partial
validation. No paid fallback or previous Hermes/Argon runtime.

## Evidence

- experiments/hermes-pmp/evidence/RESULT.md
- experiments/hermes-pmp/evidence/TESTS.md
- experiments/hermes-pmp/evidence/replay-report.json
- experiments/hermes-pmp/evidence/replay.bundle
- experiments/hermes-pmp/evidence/fresh-codex.json
- experiments/hermes-pmp/evidence/fresh-codex.bundle
- experiments/hermes-pmp/evidence/runtime-gate.md
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
