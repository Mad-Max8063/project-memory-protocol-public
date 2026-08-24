# PMP Evidence-backed Handoff profile

- Profile version: `0.1.1`
- Compatible base: PMP `0.1.1` or `0.2.1`
- Status: stable profile; repository lifecycle state is non-normative
- Profile name: `PMP Evidence-backed Handoff`

This optional profile adds a higher-assurance evidence chain to PMP Reader and
Writer behavior. It does not replace canonical memory and does not make Git
authorship proof of a human or agent identity.

## 1. Intended use

Use this profile when a handoff claim needs more than repository state alone,
for example a public demonstration, security-sensitive change, release gate,
or cross-agent workflow whose execution evidence must remain inspectable.

Do not require this profile for every routine PMP update. Core should remain
small enough for ordinary repositories and fresh participants.

## 2. Required stages

A conforming evidence-backed handoff MUST record these logical stages:

1. **Authority baseline:** the authorized decision, allowed scope, explicit
   exclusions, and starting revision.
2. **Decision handoff:** actionable canonical decisions and their evidence,
   published atomically when either artifact depends on the other.
3. **Implementation handoff:** the actual change, locally observed checks,
   updated canonical memory, and a bounded next action.
4. **Independent review:** a different human, session, or verifier inspects the
   result and discloses the evidence it used and the limits of independence.
5. **External verification:** a persisted runner or equivalent service records
   the declared gates for an exact subject revision.
6. **Evidence closure:** a later record links the external evidence to its
   subject revision without claiming that an unverified documentation revision
   was covered by the earlier run.

The stages MAY be represented by different files or combined where their
atomicity and evidence boundaries remain unambiguous.

## 3. Authority record

When authorization is consequential, the handoff MUST reference an authority
record containing:

- authority name or accountable team;
- date and repository or project identity;
- exact approved decision;
- allowed scope;
- explicit exclusions;
- starting revision or equivalent baseline;
- evidence boundary explaining whether the record proves identity.

Use `templates/AUTHORITY.md` as the default shape. A documentary repository
record MUST NOT be called a digital signature or independent identity proof
unless cryptographic evidence supports that claim.

## 4. External evidence manifest

The handoff MUST reference a manifest containing:

- exact subject revision;
- verifier platform and runner context;
- run identifier and stable URL when available;
- commands or gates actually observed and their conclusions;
- artifact identifier, digest, and retention or expiry when available;
- effective permissions relevant to the verification;
- external states observed separately from the check result;
- evidence boundaries and unresolved limitations;
- the evidence-closure rule used by the project.

Use `templates/EVIDENCE_MANIFEST.md` as the default shape.

## 5. Claim separation

The evidence chain MUST distinguish at least these claims:

- a participant recorded that a local command passed;
- an external runner persisted a successful result for a stated revision;
- an artifact exists and has the stated digest or retention;
- a deployment or promotion succeeded, failed, or was blocked;
- an authority or actor identity was independently verified.

Evidence for one claim MUST NOT be silently reused as proof of another.

## 6. Adjacent findings

Material findings outside the authorized scope MUST be recorded as risks,
blockers, or follow-up items. They MUST NOT be remediated solely because the
verification process exposed them. Any remediation requires its own authority.

## 7. Evidence closure

External evidence commonly exists only after its subject revision is
published. Therefore:

1. a later evidence-only commit MAY record the run;
2. the record MUST name the exact verified subject revision;
3. it MUST NOT state that the earlier run verified the later documentation
   revision;
4. the project MUST define a stopping rule that prevents an endless
   run-record-run cycle;
5. a branch-wide CI exclusion MUST NOT be used as the stopping rule;
6. an evidence-only closure commit does not itself require another persisted
   closure record unless it changes executable code, validation logic,
   workflow/configuration, or a claim that requires new external evidence;
7. an evidence-only path exclusion MAY supplement that terminal rule only when
   its allowlist cannot hide executable, validation, workflow, configuration,
   or other evidence-critical changes.

## 8. Conformance claim

A project using the stable Core MAY claim:

> `PMP 0.2.1 Reader/Writer + Evidence-backed Handoff profile 0.1.1`

A project retaining the frozen `0.1.1` Core MAY instead claim:

> `PMP 0.1.1 Reader/Writer + Evidence-backed Handoff profile 0.1.1`

In either case, the project may make the claim only when all required stages
and records are present and linked from canonical
memory. A released claim additionally requires the separately authorized
stable tag.

The human authority approved `PMP Evidence-backed Handoff` as the profile name.
Profile conformance does not itself prove a tag, GitHub Release, publication,
deployment, or repository visibility state.

The claim does not certify agent identity, session freshness, lack of outside
context, or correctness beyond the declared evidence.

## 9. Validation

Validate the supplied record templates with:

```bash
python scripts/validate_profile_record.py authority profiles/evidence-backed-handoff/templates/AUTHORITY.md
python scripts/validate_profile_record.py evidence profiles/evidence-backed-handoff/templates/EVIDENCE_MANIFEST.md
```

The validator checks structure and obvious secret assignments. It does not
verify identities, signatures, URLs, runs, artifacts, or the truth of claims.

Completed records are intentionally omitted from this clean distribution when
they depend on private repositories or private CI. Use the supplied templates
to create evidence that readers can inspect under the target project's own
access and publication policy.
