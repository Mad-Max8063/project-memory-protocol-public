# Project Memory Protocol — Public Distribution Memory

> Canonical operational memory shared by humans and compatible agents.
> Protocol: PMP `0.2.2`
> Canonical path: `PROJECT_MEMORY.md`

## Identity

- Project: `Project Memory Protocol public distribution`
- Repository: `https://github.com/Mad-Max8063/project-memory-protocol-public` (`PUBLIC`)
- Human authority: `Matías Maximiliano Bernal / Max Devs Solutions`
- Default branch: `main`
- Last updated: `2026-09-12`
- Last actor: `Codex`

## Current state

- [VERIFIED] This public distribution contains only allowlisted protocol,
  validation, documentation, profile-template, and packaged-demo artifacts.
- [VERIFIED] Private operational history, pilot evidence, internal phase
  records, private tag plans, and unrelated repository identifiers are absent.
- [DOCUMENTED] The local Core `0.2.2` release preparation preserves the
  normative Reader, Writer, and Adapter behavior of `0.2.1` while presenting
  the merged Core R3 validator hardening through lifecycle-neutral metadata.
  The Evidence-backed Handoff profile remains at `0.1.1`.
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
- [VERIFIED] PR #2 merged the documentation-only Core R3 post-merge closure
  into `main` through Rebase and merge. The resulting commit is
  `28dfa20970d92ec0b9fb4f129eb31b3e34fb54c5`; its sole parent is
  `c32c4d9cbf5cb239eebcdfad2c184f525bfee61b`.
- [VERIFIED] The PR #2 merge commit and reviewed branch commit
  `1cb86b93f2bad617f8344a5eae542f0bfd93588e` share the exact tree
  `85b3a3a16ee468effff59239cacf35918c4bf3ca` and the same
  `PROJECT_MEMORY.md` blob `91b8e762bf18dbff68f45ee5c701655c15a3e5a6`.
- [VERIFIED] GitHub Actions push run `34420701574` and job `verify`
  `102695248865` completed successfully for the exact PR #2 merge SHA, with
  every reported step passing.
- [VERIFIED] Branch `docs/core-r3-post-merge-closure` remains preserved at
  `1cb86b93f2bad617f8344a5eae542f0bfd93588e`.
- [VERIFIED] Core `0.2.2` release content commit
  `54f95b9ec5e67ab5ad63a54c3532286503f57cb0` is the single child of exact
  `main` `28dfa20970d92ec0b9fb4f129eb31b3e34fb54c5`. It contains exactly 18
  allowlisted paths and tree `ef9343dde4d4423cf6e06eaf601ef035f8f35905`.
- [VERIFIED] All 15 applicable local gates passed for the Core `0.2.2`
  release-content preparation: compilation; six memory validations; two profile
  template validations; 17 profile tests; 33 Markdown parser regressions;
  seven release tests; release metadata, link, size, and secret validation;
  the packaged demo; and the expected-incomplete seed with exit `1`.
- [VERIFIED] The prepared diff contains exactly 18 allowlisted paths: 16
  modified metadata, documentation, memory, adapter, or release-consistency
  files plus two new release documents. Core R3 implementation, memory/profile
  validators, Markdown regression suite, workflow, fixtures, and replay
  history remain unchanged by this preparation.
- [VERIFIED] Branch `release/0.2.2` was published at the exact release content
  commit. Manual GitHub Actions run `34427049413` and job `verify`
  `102714408763` completed successfully for that exact SHA, with every
  reported step passing.
- [VERIFIED] A read-only post-push, pre-PR audit found the repository public with
  `main` unchanged at `28dfa20970d92ec0b9fb4f129eb31b3e34fb54c5`, the
  release branch at the expected content commit, and no pull request, tag,
  GitHub Release, artifact, or deployment.
- [VERIFIED] PR #3 merged the reviewed Core `0.2.2` release scope into `main`
  through Rebase and merge. The resulting linear commits are release content
  `6b98f5d8938707a98d96ce83c1d406c6c2d1edb0`, branch-CI closure
  `9c7a91e367ec4b94e20ab914654b77dcc95edaff`, and final PR closure
  `4cb77f1081138780972147c220852a1164c02bf0`.
- [VERIFIED] The first rebased commit has exact parent
  `28dfa20970d92ec0b9fb4f129eb31b3e34fb54c5` and retains release-content tree
  `ef9343dde4d4423cf6e06eaf601ef035f8f35905`. The final `main` tree
  `e2c2957d976e427a9a110e699126c0899b8d2e87` exactly matches reviewed PR head
  `6e1f8d430248713cf52773618ce0b3974b217908`.
- [VERIFIED] GitHub Actions push run `34553817534` and job `verify`
  `103122086694` completed successfully for exact merged `main`
  `4cb77f1081138780972147c220852a1164c02bf0`, with every reported step
  passing.
- [VERIFIED] Branch `release/0.2.2` remains preserved at reviewed head
  `6e1f8d430248713cf52773618ce0b3974b217908`. The post-merge audit found the
  repository public with no tag, GitHub Release, artifact, or deployment.
- [VERIFIED] PR #4 merged the one-file Core `0.2.2` post-merge closure through
  Rebase and merge. Resulting commit
  `53f3daac4da79e5e1ed8a581a1108f7940c49a83` has exact parent
  `4cb77f1081138780972147c220852a1164c02bf0` and tree
  `c01668ecd1451ea5bb88f1a7092790fc649e3808`, identical to reviewed head
  `18b804c0258d7775c24d633e4a2c2df7c263a0e9`.
- [VERIFIED] GitHub Actions push run `34555094139` and job `verify`
  `103125951065` completed successfully for exact PR #4 merge commit
  `53f3daac4da79e5e1ed8a581a1108f7940c49a83`, with every reported step
  passing. Branch `docs/pmp-0.2.2-post-merge-closure` remains preserved at its
  reviewed head.
- [VERIFIED] A strict read-only tag-readiness audit of that exact merge commit
  passed lineage, tree, version metadata, CI, branch protection, anonymous
  access, visibility, branch preservation, and zero-tag, zero-Release,
  zero-artifact, zero-deployment, and zero-open-PR checks.
- [DOCUMENTED] The same audit found one blocking documentation inconsistency:
  canonical memory still described PR #4 as pending and treated its parent as
  current `main`. This lifecycle-neutral closure resolves that inconsistency
  without predicting the SHA that a future protected merge may create.
- [DOCUMENTED] Six known validation limits remain: empty authority content,
  multiple actions, invented `[VERIFIED]` claims, two secret-scanner evasions,
  and placeholder evidence. Core R3 does not claim to validate truth, identity,
  authorization, or complete CommonMark semantics.
- [VERIFIED] PR #5 merged the one-file lifecycle-neutral tag-readiness closure
  through Rebase and merge. Resulting `main` commit
  `0597ac7fd428e5c693d50caffb8686f8319b9fa4` has exact parent
  `53f3daac4da79e5e1ed8a581a1108f7940c49a83` and tree
  `6ea52ffdc714b8fd3952a66ae1ed8b8504db3a2b`, identical to reviewed head
  `2395f617acf9145711f1e4fc777072651140109a`.
- [VERIFIED] GitHub Actions push run `34556398091` and job `verify`
  `103129875345` completed successfully for that exact `main` commit.
- [VERIFIED] Annotated tag `v0.2.2` has tag-object
  `1bda566198a1e5c6cc4564c0984b42b7744575e7` and peels to exact commit
  `0597ac7fd428e5c693d50caffb8686f8319b9fa4`. Its approved tagger is
  `Matías Maximiliano Bernal <179927943+Mad-Max8063@users.noreply.github.com>`;
  the tag is unsigned as explicitly accepted by the human authority.
- [VERIFIED] GitHub Release `386759221`, titled
  `Project Memory Protocol v0.2.2`, is public, stable, non-draft,
  non-prerelease, and marked `Latest`. Its published body matches
  `docs/RELEASE_NOTES_0.2.2.md`; anonymous access to the Release and automatic
  ZIP/TAR source archives returned HTTP `200`.
- [VERIFIED] The post-Release audit on `2026-09-11` found the repository public
  with all six branches preserved, one tag, one Release, no uploaded Release
  assets, no Actions artifacts, no deployments, and no open pull requests.
- [DOCUMENTED] A new `Capability-Aware Handoff` document records an exploratory,
  non-normative design for transferring bounded work between environments with
  different observable capabilities. It does not change Core `0.2.2`, profile
  `0.1.1`, the published tag, or the stable GitHub Release.

## Active decisions

1. Keep the private evidence archive separate and unpublished.
2. Keep the public distribution clean-history, self-contained, and separate
   from the private evidence archive.
3. Keep baseline PMP independent of external services; the Evidence-backed
   Handoff profile remains optional.
4. Do not present Git metadata as proof of human or model identity.
5. Treat the public replay as reproducible repository and CI evidence while
   preserving the documented limits around hidden identity and session state.
6. Preserve published Core `0.2.2`, its normative contract, profile `0.1.1`,
   annotated tag-object `1bda566198a1e5c6cc4564c0984b42b7744575e7`, exact
   target `0597ac7fd428e5c693d50caffb8686f8319b9fa4`, and stable GitHub Release.
   Treat any tag or Release modification, deployment, visibility or protection
   change, replay change, and promotional publication as separate human
   decisions.
7. Treat `Capability-Aware Handoff` only as an exploratory optional-profile
   proposal until a disposable cross-environment pilot and adversarial review
   provide evidence for a separate human decision.

## Constraints

- Do not copy private archive repository names, branches, commits, URLs,
  operational sessions, credentials, local paths, or product-specific details
  here.
- Do not add or change remotes, modify tags or GitHub Releases, publish
  promotional material, deploy, or change visibility without separate explicit
  human authorization.
- Each remaining lifecycle transition MUST be separately and explicitly
  human-authorized. In particular, this documentation closure does not imply
  merge, tag, GitHub Release, deployment, branch deletion, visibility change,
  protection change, replay change, or promotional publication authority.
- Do not claim that a recording or public companion demo exists until its URL
  and anonymous accessibility have been verified.
- Do not place private paths, credentials, signed artifact URLs, or unnecessary
  personal data in public capability records or fixtures.

## Priorities

1. Keep the public README, canonical memory, replay evidence, and actual
   external state aligned.
2. Require exact-SHA local gates, CI, and read-only audit evidence for each
   authorized lifecycle transition.
3. Keep the published `v0.2.2` tag, Release notes, canonical memory, and actual
   external state aligned; let the human decide whether to authorize
   promotional publication.
4. Review the `Capability-Aware Handoff` proposal and decide whether to prepare
   a disposable, non-production cross-environment prototype.

## Next action

`Human authority: review the non-normative Capability-Aware Handoff proposal and decide whether to authorize an isolated, disposable cross-environment prototype and adversarial test matrix. No Core or stable-profile change, commit, push, pull request, tag or GitHub Release modification, deployment, branch deletion, visibility or protection change, replay change, artifact transfer, credential access, or promotional publication is implied by this proposal.`

## Evidence

- `SPEC.md`
- `README.md`
- `docs/PROVENANCE.md`
- `docs/RELEASE_NOTES_0.2.1.md`
- `docs/RELEASE_NOTES_0.2.2.md`
- `docs/UPGRADING_0.2.1_TO_0.2.2.md`
- `docs/proposals/CAPABILITY_AWARE_HANDOFF.md`
- `examples/chatgpt-codex-handoff/README.md`
- PR #1 `https://github.com/Mad-Max8063/project-memory-protocol-public/pull/1`
- Core R3 merge commit `c32c4d9cbf5cb239eebcdfad2c184f525bfee61b`
- Core R3 reviewed commit `930082a0be3be1c6b2ab1346d625b8afb4dd7471`
- Core R3 `main` CI run `34418092764`
- Core R3 `main` CI job `102687351177`
- PR #2 `https://github.com/Mad-Max8063/project-memory-protocol-public/pull/2`
- PR #2 merge commit `28dfa20970d92ec0b9fb4f129eb31b3e34fb54c5`
- PR #2 reviewed commit `1cb86b93f2bad617f8344a5eae542f0bfd93588e`
- PR #2 merge CI run `34420701574`
- PR #2 merge CI job `102695248865`
- Core `0.2.2` release content commit `54f95b9ec5e67ab5ad63a54c3532286503f57cb0`
- Core `0.2.2` release content CI run `34427049413`
- Core `0.2.2` release content CI job `102714408763`
- PR #3 `https://github.com/Mad-Max8063/project-memory-protocol-public/pull/3`
- PR #3 initial head `a341d3c8482ff32e52702cca6c41454dc55aa60a`
- PR #3 initial CI run `34428284113`
- PR #3 initial CI job `102718094144`
- PR #3 reviewed head `6e1f8d430248713cf52773618ce0b3974b217908`
- PR #3 reviewed-head CI run `34552366066`
- PR #3 reviewed-head CI job `103117747308`
- PR #3 merged `main` commit `4cb77f1081138780972147c220852a1164c02bf0`
- PR #3 merged `main` CI run `34553817534`
- PR #3 merged `main` CI job `103122086694`
- PR #4 `https://github.com/Mad-Max8063/project-memory-protocol-public/pull/4`
- PR #4 reviewed head `18b804c0258d7775c24d633e4a2c2df7c263a0e9`
- PR #4 pull-request CI run `34554752425`
- PR #4 pull-request CI job `103124919674`
- PR #4 merged commit `53f3daac4da79e5e1ed8a581a1108f7940c49a83`
- PR #4 merged `main` CI run `34555094139`
- PR #4 merged `main` CI job `103125951065`
- PR #5 `https://github.com/Mad-Max8063/project-memory-protocol-public/pull/5`
- PR #5 reviewed head `2395f617acf9145711f1e4fc777072651140109a`
- PR #5 merged `main` commit `0597ac7fd428e5c693d50caffb8686f8319b9fa4`
- PR #5 merged `main` CI run `34556398091`
- PR #5 merged `main` CI job `103129875345`
- annotated tag `v0.2.2` object `1bda566198a1e5c6cc4564c0984b42b7744575e7`
- GitHub Release `https://github.com/Mad-Max8063/project-memory-protocol-public/releases/tag/v0.2.2`
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
