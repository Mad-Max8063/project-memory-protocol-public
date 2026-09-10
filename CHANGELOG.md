# Changelog

All notable protocol changes are documented here.

## 0.2.2 — Core R3 validation hardening

- Added one shared Markdown-section parser for the Core and profile validators.
- Correctly distinguish escaped backticks from code-span delimiters and retain
  valid multiline code spans across LF and CRLF line endings.
- Stop multiline code-span searches at CommonMark paragraph boundaries used by
  thematic breaks and setext headings.
- Added focused regression coverage and an explicit CI gate for the shared
  parser.
- Preserved the normative Reader, Writer, Adapter, and Evidence-backed Handoff
  requirements from `0.2.1`.

## 0.2.1 — metadata correction

- Separated stable protocol and profile status from mutable repository state.
- Preserved every normative Reader, Writer, Adapter, and Evidence-backed
  Handoff requirement from the accepted `0.2.0` line.
- Added lifecycle-neutral release notes, upgrade guidance, validation, and a
  clean distribution boundary.

## 0.2.0 — stable Core and evidence profile

- Added portable repository-native START instructions.
- Added bounded positive and negative scope rules.
- Required deterministic verification for consequential work.
- Added bounded handling of adjacent findings and semantic-terminal evidence
  closure.
- Added the optional Evidence-backed Handoff profile with reusable authority
  and evidence-manifest templates.

## 0.1.1 — release package and evidence clarification

- Added release notes, a reproducible handoff runbook, and explicit evidence
  boundaries.
- Clarified that Git authorship does not prove model identity or session
  freshness.
- Added MIT attribution for Matías Maximiliano Bernal / Max Devs Solutions.

## 0.1.0 — initial protocol

- Defined canonical project memory and Reader, Writer, and Adapter contracts.
- Added evidence labels, conflict precedence, templates, adapters, validators,
  a deterministic handoff fixture, and an answer-free live-demo seed.
