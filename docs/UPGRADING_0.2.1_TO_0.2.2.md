# Upgrading from PMP 0.2.1 to 0.2.2

Status: stable compatibility guidance. Repository lifecycle state is tracked in
`PROJECT_MEMORY.md`.

## Compatibility

PMP `0.2.1` projects remain valid. Core `0.2.2` preserves the same canonical
path, eight required headings, evidence labels, source precedence, and
Reader/Writer/Adapter requirements.

The change is limited to executable validation hardening. It aligns Core and
profile section parsing and fixes edge cases involving escaped backticks,
multiline code spans, thematic breaks, setext headings, and LF/CRLF endings.
No canonical heading or data migration is required.

The optional Evidence-backed Handoff profile remains at `0.1.1` and is
compatible with Core `0.2.2`.

## Adoption

1. Update the protocol qualifier in canonical memory, templates, and adapters
   to `0.2.2`.
2. Replace the Core and profile validators together so both use the same
   Markdown-section parser.
3. Include the shared parser regressions in the project verification gate.
4. Keep any project-specific evidence and current operational state in that
   project's canonical memory.

## Preserved limits

Core `0.2.2` remains a bounded structural validator. It does not prove the
truth of `[VERIFIED]` claims, participant identity, human authorization,
external evidence validity, complete secret detection, or full CommonMark
semantics. See the release notes for the six known validation limits.

## Not authorized by this guide

This document describes compatibility only. Committing, pushing, opening or
merging a pull request, tagging, creating a GitHub Release, publishing,
deploying, or changing repository visibility remain separate operational
decisions.
