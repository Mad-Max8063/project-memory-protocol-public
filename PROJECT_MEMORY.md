# Project Memory Protocol — Public Distribution Memory

> Canonical operational memory shared by humans and compatible agents.
> Protocol: PMP `0.2.1`
> Canonical path: `PROJECT_MEMORY.md`

## Identity

- Project: `Project Memory Protocol public distribution`
- Repository: `local clean-history candidate; no remote configured`
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
- [VERIFIED] No remote, public repository, tag, GitHub Release, deployment, or
  publication has been created from this clean candidate.
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

- Do not copy private repository names, branches, commits, URLs, operational
  sessions, credentials, local paths, or product-specific details here.
- Do not configure a remote, push, tag, create a GitHub Release, publish,
  deploy, or change visibility without separate explicit human authorization.
- Do not claim that a recording or public companion demo exists until its URL
  and anonymous accessibility have been verified.

## Priorities

1. Pass all protocol, release, privacy, link, and packaged-demo gates locally.
2. Review the exact clean-history manifest and initial commit before any remote
   repository is created.
3. Prepare a separately reviewed public evidence path for the live demo.

## Next action

`Human authority: review the locally committed clean-history candidate and its audit results, then explicitly approve or reject creating a new private remote for pre-publication CI. No public visibility, tag, GitHub Release, post, video, or deployment is implied.`

## Evidence

- `SPEC.md`
- `README.md`
- `docs/PROVENANCE.md`
- `docs/RELEASE_NOTES_0.2.1.md`
- `examples/chatgpt-codex-handoff/README.md`
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
