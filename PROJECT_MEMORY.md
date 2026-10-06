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
  subscription entitlement, profile enforcement and live runtime are unverified.
  Hermes was not found through scoped local availability checks. No model/provider
  call by Hermes, installer, purchase, paid service or deployment occurred.
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

1. Establish whether a NEW independent Hermes runtime and existing-subscription
   OAuth route are available without incremental paid charges.
2. Only after inspecting that version's tool restrictions, run one bounded live
   attempt with the dedicated home, no provider fallback and no chat history.
3. If the route is unavailable, retain this honest partial result; do not expand
   architecture, simulate success or repair the blocked previous track.

## Next action

Human authority: make a NEW independent Hermes runtime available using the
official Windows guide linked in docs/experiments/hermes-pmp-adapter.md.
Do not reuse the blocked track or purchase a service. Then follow the guide's
dedicated-home subscription OAuth procedure and stop if entitlement or tool
restriction cannot be verified; no automatic paid fallback.

## Evidence

- experiments/hermes-pmp/evidence/RESULT.md
- experiments/hermes-pmp/evidence/TESTS.md
- experiments/hermes-pmp/evidence/replay-report.json
- experiments/hermes-pmp/evidence/replay.bundle
- experiments/hermes-pmp/evidence/fresh-codex.json
- experiments/hermes-pmp/evidence/fresh-codex.bundle
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
