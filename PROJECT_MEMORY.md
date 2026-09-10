# Project Memory Protocol — Public Distribution Memory

> Canonical operational memory shared by humans and compatible agents.
> Protocol: PMP `0.2.1`
> Canonical path: `PROJECT_MEMORY.md`

## Identity

- Project: `Project Memory Protocol public distribution`
- Repository: `https://github.com/Mad-Max8063/project-memory-protocol-public` (`PUBLIC`)
- Human authority: `Matías Maximiliano Bernal / Max Devs Solutions`
- Default branch: `main`
- Last updated: `2026-09-09`
- Last actor: `Codex`

## Current state

- [VERIFIED] This public distribution contains only allowlisted protocol,
  validation, documentation, profile-template, and packaged-demo artifacts.
- [VERIFIED] Private operational history, pilot evidence, internal phase
  records, private tag plans, and unrelated repository identifiers are absent.
- [DOCUMENTED] Core `0.2.1` and Evidence-backed Handoff profile `0.1.1` preserve
  the accepted protocol behavior while using lifecycle-neutral metadata.
- [VERIFIED] The clean remote was bootstrapped on `main` from the exact
  clean-history root commit `e56aa540ea91d1bb7fd9ed61d3bda8321badea95`.
- [VERIFIED] GitHub Actions run `32764540923` executed for that exact root
  commit after the initial push and completed successfully with every job and
  step passing.
- [DOCUMENTED] The final read-only audit of the root commit passed its
  technical and external-state checks but found one medium documentation
  inconsistency: this memory still claimed that no remote existed and left
  remote creation as the next action. This closure update resolves that
  inconsistency.
- [VERIFIED] The documentation-only bootstrap closure is commit
  `365e48c7b8480f339b622b1f22eb30c8f93a6da8`; GitHub Actions run
  `32765750211` completed successfully for that exact commit.
- [DOCUMENTED] The repository was subsequently made public under explicit
  human authorization. This update resolves the resulting stale `PRIVATE`
  metadata and records the current public state.
- [VERIFIED] The repository and its README, LICENSE, specification, history,
  and CI are anonymously accessible. A post-merge read-only check on
  `2026-09-09` found no tag, GitHub Release, artifact, or deployment.
- [VERIFIED] The public blind replay at
  `Mad-Max8063/pmp-public-replay-01` completed its four-commit
  Human -> ChatGPT -> Codex -> ChatGPT chain at
  `a4e6469a4257f32809b9405946b07fd2ef3e8416`.
- [VERIFIED] Replay CI run `32791128976` completed successfully for that exact
  final commit with seven passing acceptance tests and
  `REPLAY STAGE VERIFIED: chatgpt-verification`.
- [VERIFIED] Local gates pass: Python compilation, six memory validations, two
  profile-template validations, 17 profile tests, seven release tests, release
  metadata/link/size/secret validation, the packaged demo, and the
  expected-incomplete seed.
- [VERIFIED] Targeted privacy scans found no private product or repository
  identifiers, inherited CI URLs or commit SHAs, local user paths, or
  credential-like assignments in the 50-file candidate.
- [VERIFIED] Byte comparison preserved every copied artifact except the
  explicitly reviewed public surfaces: workflow, README, changelog, upgrade
  and release notes, demo script, profile guidance, and release validation.
- [VERIFIED] PR #1 merged the reviewed Core R3 hardening into `main` through
  Rebase and merge. The resulting commit is
  `c32c4d9cbf5cb239eebcdfad2c184f525bfee61b`; its sole parent is
  `0c9b84a28a73b414b0ae8326ad4f4c43cda02ec2`.
- [VERIFIED] The merged commit and reviewed branch commit
  `930082a0be3be1c6b2ab1346d625b8afb4dd7471` share the exact tree
  `8061adf527bfc9cd60bca406327b57d991cc028e`. Both contain the same five-file
  change: 332 insertions and 21 deletions.
- [VERIFIED] GitHub Actions push run `34418092764` and job `verify`
  `102687351177` completed successfully for the exact merged `main` SHA, with
  every reported step passing.
- [VERIFIED] Branch `codex/core-r3-integration` remains preserved at the
  reviewed commit. Repository visibility remains public; no existing branch,
  protection setting, tag, Release, artifact, deployment, or replay history
  was changed by the merge closure.
- [DOCUMENTED] Six known validation limits remain: empty authority content,
  multiple actions, invented `[VERIFIED]` claims, two secret-scanner evasions,
  and placeholder evidence. Core R3 does not claim to validate truth, identity,
  authorization, or complete CommonMark semantics.

## Active decisions

1. Keep the private evidence archive separate and unpublished.
2. Keep the public distribution clean-history, self-contained, and separate
   from the private evidence archive.
3. Keep baseline PMP independent of external services; the Evidence-backed
   Handoff profile remains optional.
4. Do not present Git metadata as proof of human or model identity.
5. Treat the public replay as reproducible repository and CI evidence while
   preserving the documented limits around hidden identity and session state.
6. Keep Core `0.2.1` as the current declared version until the human separately
   decides whether to prepare PMP `0.2.2`. This closure is not a version bump,
   tag, GitHub Release, deployment, or promotional publication.

## Constraints

- Do not copy private archive repository names, branches, commits, URLs,
  operational sessions, credentials, local paths, or product-specific details
  here.
- Do not add or change remotes, push additional commits, tag, create a GitHub
  Release, publish, deploy, or change visibility without separate explicit
  human authorization.
- Do not claim that a recording or public companion demo exists until its URL
  and anonymous accessibility have been verified.

## Priorities

1. Keep the public README, canonical memory, replay evidence, and actual
   external state aligned.
2. Require exact-SHA local gates, CI, and read-only audit evidence for each
   authorized lifecycle transition.
3. Let the human decide whether the merged Core R3 hardening should become PMP
   `0.2.2`; perform release preparation only under separate authorization.

## Next action

`Human authority: after this post-merge closure PR and its exact-SHA CI are verified, decide whether to authorize preparation of PMP 0.2.2. No merge of this closure PR, version change, tag, GitHub Release, deployment, branch deletion, protection change, replay change, or promotional publication is implied.`

## Evidence

- `SPEC.md`
- `README.md`
- `docs/PROVENANCE.md`
- `docs/RELEASE_NOTES_0.2.1.md`
- `examples/chatgpt-codex-handoff/README.md`
- PR #1 `https://github.com/Mad-Max8063/project-memory-protocol-public/pull/1`
- Core R3 merge commit `c32c4d9cbf5cb239eebcdfad2c184f525bfee61b`
- Core R3 reviewed commit `930082a0be3be1c6b2ab1346d625b8afb4dd7471`
- Core R3 `main` CI run `34418092764`
- Core R3 `main` CI job `102687351177`
- root commit `e56aa540ea91d1bb7fd9ed61d3bda8321badea95`
- GitHub Actions run `32764540923`
- bootstrap closure commit `365e48c7b8480f339b622b1f22eb30c8f93a6da8`
- bootstrap closure CI run `32765750211`
- public replay `https://github.com/Mad-Max8063/pmp-public-replay-01`
- replay final commit `a4e6469a4257f32809b9405946b07fd2ef3e8416`
- replay final CI run `32791128976`
- `python scripts/validate_release_candidate.py`
- `python examples/chatgpt-codex-handoff/verify_demo.py`

## Update rules

- Read this file before significant work.
- Update it only when current state, a decision, a constraint, a priority, or
  the next action changes.
- Keep current truth here; use session records only when historical detail is
  useful and safe for public distribution.
- Never store secrets, credentials, tokens, private keys, `.env` values,
  private repository identifiers, or unnecessary personal data.
- Use `[VERIFIED]`, `[DOCUMENTED]`, and `[ASSUMED]` exactly as defined by PMP.
- Resolve conflicts using: latest authorized human instruction -> current
  verified evidence -> this file -> specialized documentation -> session
  history -> private model memory.
