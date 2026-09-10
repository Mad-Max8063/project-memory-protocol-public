# Project Memory Protocol 0.2.2

Status: Core R3 hardening notes; repository lifecycle state is non-normative.
Actual branch, tag, GitHub Release, publication, deployment, and visibility
state is recorded in canonical memory.

## Core R3 hardening

PMP Core `0.2.2` preserves the normative Reader, Writer, and Adapter contract
from `0.2.1` while hardening its executable Markdown-section validation.

- Core and profile validators now use one shared Markdown-section parser.
- Escaped backticks no longer incorrectly open or close code spans.
- Valid multiline code spans remain recognized with LF and CRLF line endings.
- Multiline searches stop at thematic breaks and setext headings, preventing
  hidden HTML-comment content from being counted across paragraph boundaries.
- Focused regression tests exercise the shared parser and run in CI.

The optional Evidence-backed Handoff profile remains at `0.1.1`.

## Known limits

The hardening does not claim complete CommonMark parsing or semantic proof.
Six known limits remain documented:

1. empty human-authority content may pass structural validation;
2. multiple visible next actions may pass structural validation;
3. an invented `[VERIFIED]` claim cannot be disproved mechanically;
4. one secret-scanner evasion remains possible through unsupported formatting;
5. a second secret-scanner evasion remains possible through unsupported formatting;
6. placeholder evidence may satisfy structural presence checks.

Truth, identity, authorization, evidence validity, and complete secret
detection still require additional verification.

## Explicit exclusions

These notes describe protocol contents. Creating a commit, push, pull request,
tag, GitHub Release, deployment, visibility change, or promotional publication
requires separate human authorization.
