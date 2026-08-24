# Upgrading from PMP 0.1.1 to 0.2.1

Status: stable compatibility guidance. Repository lifecycle state is tracked in
`PROJECT_MEMORY.md`.

## Compatibility

PMP `0.1.1` projects remain valid. Core `0.2.1` keeps the same canonical
path, eight required headings, evidence labels, source precedence, and basic
Reader/Writer/Adapter roles.

Core `0.2.1` has the same normative behavior as Core `0.2.0`. The patch
separates protocol status from mutable branch, merge, tag, release,
publication, deployment, and visibility state.

The optional `PMP Evidence-backed Handoff` profile `0.1.1` likewise retains
the behavior of profile `0.1.0` and corrects lifecycle metadata only.

## Adoption

1. Keep one versioned canonical memory and repository instructions that locate it.
2. Update the protocol qualifier in the memory template and adapters to `0.2.1`.
3. Apply the bounded-scope, deterministic-verification, and adjacent-finding
   rules described in `SPEC.md`.
4. Adopt profile `0.1.1` only when higher-assurance evidence is needed.
5. Track operational repository state in canonical memory rather than in
   timeless specification or profile status fields.

No canonical heading migration or data conversion is required.

## Historical versions

The compatibility statements refer to protocol versions, not to the Git
history of this clean distribution. Private operational tag history is not
reproduced here; see [PROVENANCE.md](PROVENANCE.md).

## Not authorized by this guide

This document describes compatibility only. Tagging, GitHub Releases,
publication, deployment, and visibility are separate operational decisions.
