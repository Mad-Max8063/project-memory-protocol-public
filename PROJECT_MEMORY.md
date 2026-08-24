# Project Memory Protocol — Public Distribution Memory

> Canonical operational memory shared by humans and compatible agents.
> Protocol: PMP `0.2.1`
> Canonical path: `PROJECT_MEMORY.md`

## Identity

- Project: `Project Memory Protocol public distribution`
- Repository: `https://github.com/Mad-Max8063/project-memory-protocol-public` (`PRIVATE`)
- Human authority: `Matías Maximiliano Bernal / Max Devs Solutions`
- Default branch: `main`
- Last updated: `2026-08-24`
- Last actor: `Codex`

## Current state

- [VERIFIED] This local candidate contains only allowlisted protocol,
  validation, documentation, profile-template, and packaged-demo artifacts.
- [VERIFIED] Private operational history, pilot evidence, internal phase
  records, private tag plans, and unrelated repository identifiers are absent.
- [DOCUMENTED] Core `0.2.1` and Evidence-backed Handoff profile `0.1.1` preserve
  the accepted protocol behavior while using lifecycle-neutral metadata.
- [VERIFIED] The private remote was bootstrapped on `main` from the exact
  clean-history root commit `e56aa540ea91d1bb7fd9ed61d3bda8321badea95`.
- [VERIFIED] GitHub Actions run `32764540923` executed for that exact root
  commit after the initial push and completed successfully with every job and
  step passing.
- [DOCUMENTED] The final read-only audit of the root commit passed its
  technical and external-state checks but found one medium documentation
  inconsistency: this memory still claimed that no remote existed and left
  remote creation as the next action. This closure update resolves that
  inconsistency.
- [VERIFIED] The repository remains private, with no tags, GitHub Releases,
  pull requests, artifacts, deployments, public visibility, or publication.
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

## Active decisions

1. Keep the private evidence archive separate and unpublished.
2. Publish only a clean-history, self-contained distribution after a separate
   human authorization for the exact candidate revision.
3. Keep baseline PMP independent of external services; the Evidence-backed
   Handoff profile remains optional.
4. Do not present Git metadata as proof of human or model identity.

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

1. Keep the remote private and preserve the verified clean-history provenance.
2. Require exact-SHA local gates, CI, and read-only audit evidence for each
   authorized lifecycle transition.
3. Prepare a separately reviewed public evidence path for the live demo.

## Next action

`Human authority: review the private closure commit and its exact CI and audit evidence, then explicitly approve or reject the next lifecycle action. No tag, GitHub Release, public visibility, publication, post, video, or deployment is authorized.`

## Evidence

- `SPEC.md`
- `README.md`
- `docs/PROVENANCE.md`
- `docs/RELEASE_NOTES_0.2.1.md`
- `examples/chatgpt-codex-handoff/README.md`
- root commit `e56aa540ea91d1bb7fd9ed61d3bda8321badea95`
- GitHub Actions run `32764540923`
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
