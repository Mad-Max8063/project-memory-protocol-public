# Provisional initial reconstruction (written before running any verifier/test)

Written: 2026-10-06 ~19:56Z, after reading only AGENTS.md and PROJECT_MEMORY.md at
commit 8c96e926b0d28a182759c45c3a0141fa9a934eba.

## Objective
Experimental branch `experiment/hermes-pmp-adapter` of the PMP public repo tests
whether PMP canonical memory (PROJECT_MEMORY.md) plus Git evidence lets different
runtimes (Hermes, Claude Code, Codex) hand off work portably. Current objective:
get an external reproduction of the archived chain evidence via review PR #8.

## Current state (as claimed)
- Draft PR #8 open against main; branch published (initial pushed source 6ae8b85).
- Live Hermes replay (pinned CLI vgit.e97923c, model listed gpt-5.6-luna) archived in
  evidence/live-replay-20261006/; Claude Code continuation (claude-sonnet-5 reported)
  archived in evidence/claude-continuation-20261006/; Codex fresh continuations
  verified. Chain declared "A. VALIDATED" within stated limits.
- Offline verifier verify_chain.py: Claude implementation attempt timed out (300 s,
  no proposal retained); Codex implemented it; independent Codex review found two P2
  issues, host fixed them; 7 acceptance tests, full suite 83 passed (host-reported).
- CI run 37495814502 passed for 6ae8b85 but only existing Core checks.

## Decisions / constraints
- PMP stays vendor-neutral; Hermes optional. Proposal JSON is non-normative.
- No Core/spec/profile changes, no merge/tag/release/deploy/social posting, USD 0 cost.
- Do not touch the previous Hermes/Argon experiment.
- No identity/freshness/autonomy claims from Git evidence.

## Available evidence (claimed)
Bundles + reports under experiments/hermes-pmp/evidence/ (replay.bundle,
fresh-codex.bundle, live-replay-20261006/replay.bundle,
claude-continuation-20261006/{claude-replay,fresh-codex}.bundle), chain-verifier
evidence (host-checks.json, final-checks.json, claude-timeout.json,
independent-review.md), session records under .project-memory/sessions/.

## Exact next action (as stated)
Max: review hermes-review-social-drafts.md and manually share the reproduction request
linking PR #8. Next success criterion: an external reviewer report with source commit,
environment, commands, exit code, verifier JSON and failures. No merge/release.

## What the repo claims vs. what I have not verified
Claims: verify_chain.py verifies three bundle SHA-256 pins, 14 historical inputs,
lineage, PMP/handoff integrity; 7 acceptance tests pass.
Not yet verified by me: any hash, any test, bundle contents, whether bundle count is
"three" (memory lists more bundle files than three - need to check which three are pinned),
CI result, PR state, live runs (out of scope, will not be verified).
Observation: branch tip at clone time was 2e08ae1 ("docs: save cross-runtime
reproduction prompt"), one commit ahead of the pinned commit; I review the pinned one.
