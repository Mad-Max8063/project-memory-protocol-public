# Capability-Aware Handoff

- Status: exploratory proposal; non-normative
- Stable Core impact: none
- Profile version: unassigned
- Compatibility target: PMP Reader, Writer, and Adapter model

This document explores an optional PMP profile for handing work between
participants that have different execution capabilities. It is not part of
PMP Core `0.2.2`, is not a released profile, and does not create a conformance
claim.

## 1. Problem

A participant can understand the task and still be unable to execute it. A
remote or sandboxed environment may lack a required filesystem root, operating
system feature, tool, network route, credential scope, or hydrated artifact.

Without an explicit handoff, that limitation is often buried in chat history.
The next participant must rediscover the blocker, requested artifacts,
constraints, and intended result.

Capability-Aware Handoff would let a PMP Writer record the mismatch as current
operational state and leave a bounded next action for a compatible participant.

## 2. Intended scope

The profile would describe:

- capabilities required by the next action;
- capabilities observed or declared in the current environment;
- unavailable capabilities and the resulting blocker;
- logical artifact references, digests, media types, sizes, and access classes;
- the participant or environment class that can resume the work;
- constraints that remain in force after the handoff;
- outputs and verification evidence produced by the receiving participant.

The vocabulary must remain vendor-neutral. An Adapter may translate local tool
or platform details into the shared record without duplicating canonical
project state.

## 3. Non-goals

The proposed profile would not:

- grant permissions or bypass a sandbox;
- mount a filesystem or transfer an artifact;
- distribute credentials, secrets, or private paths;
- prove that a capability declaration is truthful;
- select an executor as a substitute for human authorization;
- prove human or agent identity, intent, or session freshness;
- turn an inaccessible artifact into verified evidence;
- require an orchestration service or hosted PMP component.

Artifact transport, credential brokerage, and executor scheduling remain
external concerns. PMP would record the state needed to perform and verify the
handoff.

## 4. Candidate record

The exact file shape remains open. A future profile could add a dedicated
record or embed equivalent fields in canonical memory and session evidence.
The following vocabulary is illustrative, not normative:

```markdown
## Execution environment

- Environment class: `remote-sandbox`
- Platform: `linux`
- Subject revision: `<exact repository revision>`
- Observation timestamp: `<UTC timestamp>`
- Observed capabilities: `repository-read`, `repository-write`
- Missing capability: `local-artifact-read`

## Required artifacts

- Artifact ID: `source-media-01`
- Locator: `artifact://source-media-01`
- Media type: `video/mp4`
- Size: `<known size or pending>`
- Digest: `sha256:<known digest or pending>`
- Access class: `local-only`

## Handoff reason

- [DOCUMENTED] The current environment cannot resolve the artifact locator.
- Required receiver capability: `local-artifact-read`

## Constraints preserved

- Treat source artifacts as read-only.
- Write outputs only to the authorized destination.
- Do not publish or contact third parties.

## Next action

`Local-capable participant: resolve artifact://source-media-01 through an
authorized Adapter, verify the observed size and digest when readable, perform
the bounded task, and record the output digest and actual checks.`
```

When the current participant cannot read an artifact, its size or digest must
remain unknown or documented rather than invented. The receiving participant
should verify those fields after resolving the artifact.

## 5. Candidate flow

1. **START:** compare the next action's required capabilities with the current
   environment's observed capabilities.
2. **READY:** continue under normal PMP Reader and Writer behavior when the
   requirements are satisfied.
3. **CAPABILITY_MISMATCH:** stop before unsupported execution, record the
   missing capability and preserve all active constraints.
4. **HANDOFF:** identify a compatible environment class and one exact next
   action. Reference artifacts by logical identifier and safe metadata.
5. **RESUME:** the receiving participant revalidates the current revision,
   authority, relevant capabilities, permissions, and authorized artifact
   metadata before performing only the bounded action.
6. **END:** record actual outputs, digests, checks, remaining limits, and the
   next participant.

`CAPABILITY_MISMATCH` must remain distinct from task rejection and execution
failure. An unsupported environment is not evidence that the requested work is
invalid.

## 6. Artifact and locator rules under consideration

- Prefer repository paths or logical `artifact://` identifiers over absolute
  machine paths in portable or public records.
- Store an absolute local path only when the repository's privacy policy and
  human authority explicitly permit it.
- Label whether metadata was declared, observed, or externally verified.
- Bind an artifact to a digest when it is readable and the digest is useful.
- Never claim a pending digest or inaccessible artifact was verified.
- Keep transfer credentials and signed URLs outside canonical memory.
- Treat locator resolution as Adapter behavior, not Core behavior.

## 7. Security and authority boundaries

A capability record is evidence about an environment only to the level stated
by its evidence label. Self-reported tools, paths, and permissions are not
independent verification.

Routing also does not authorize execution. The receiving participant must
still apply PMP source precedence and the latest human-authorized scope. A
handoff may narrow existing authority but may not expand it.

Public examples must use disposable artifacts, synthetic identifiers, and
sanitized paths. Private credentials, tokens, personal data, and unnecessary
local filesystem details must not enter repository history.

## 8. Relationship to existing PMP layers

- **Core:** remains unchanged and continues to define canonical state,
  precedence, Reader/Writer behavior, and Adapter boundaries.
- **Evidence-backed Handoff:** may supply authority and external evidence when
  higher assurance is required, but would not become mandatory.
- **Capability-Aware Handoff:** would describe why the current executor cannot
  proceed and what a compatible executor needs to resume safely.

Projects could adopt either optional profile or both. No compatibility or
conformance wording should be finalized before a disposable prototype and
adversarial review pass.

## 9. Prototype acceptance criteria

A future isolated prototype should demonstrate that:

1. an incompatible participant stops with `CAPABILITY_MISMATCH` rather than a
   false success or ordinary task rejection;
2. the handoff records one exact next action, required capabilities, preserved
   constraints, and safe artifact metadata;
3. a compatible participant can resume without relying on the previous chat;
4. readable input and produced output artifacts are bound to observed digests;
5. stale digests, missing artifacts, unsupported tools, and denied permissions
   remain distinguishable failure cases;
6. public fixtures contain no secrets, credentials, personal data, or real
   private paths;
7. an exact-revision verifier can reproduce the declared structural results.

## 10. Open decisions

- Whether capability data belongs in one profile record, canonical memory, or
  both.
- Which capability vocabulary is small enough to remain interoperable.
- How Adapters resolve logical artifact identifiers without leaking locators.
- Which declarations require external evidence in higher-assurance workflows.
- Whether routing remains advisory or gains an optional orchestrator binding.
- What minimum negative-test matrix is required before assigning a profile
  version.

The next step is a disposable, cross-environment pilot. Until that evidence
exists, this document remains a design proposal rather than released PMP
behavior.
