#!/usr/bin/env python3
"""Validate the version-neutral structural and safety baseline of a PMP memory."""

from __future__ import annotations

import re
import sys
from pathlib import Path

if __package__:
    from .markdown_sections import parse_sections
else:
    from markdown_sections import parse_sections


REQUIRED_HEADINGS = [
    "## Identity",
    "## Current state",
    "## Active decisions",
    "## Constraints",
    "## Priorities",
    "## Next action",
    "## Evidence",
    "## Update rules",
]

EVIDENCE_LABEL = re.compile(r"\[(VERIFIED|DOCUMENTED|ASSUMED)\]")
SECRET_ASSIGNMENT = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:[A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)|"
    r"(?:api[_-]?key|access[_-]?token|client[_-]?secret|password))\s*[:=]\s*"
    r"(?!<|redacted|none|not set)(\S+)"
)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read UTF-8 Markdown: {exc}"]

    if not text.startswith("# "):
        errors.append("file must start with a level-one project title")

    sections = parse_sections(text)
    headings = ["## " + section.name for section in sections]
    positions: list[int] = []
    for heading in REQUIRED_HEADINGS:
        count = headings.count(heading)
        if count != 1:
            errors.append(f"required heading {heading!r} must appear exactly once (found {count})")
        positions.append(headings.index(heading) if count else -1)

    present_positions = [position for position in positions if position >= 0]
    if present_positions != sorted(present_positions):
        errors.append("required headings are out of order")

    for section in sections:
        if section.name == "Current state" and not EVIDENCE_LABEL.search(section.prose):
            errors.append("Current state must include at least one PMP evidence label")
        if section.name == "Next action" and not section.body:
            errors.append("Next action must not be empty")

    if SECRET_ASSIGNMENT.search(text):
        errors.append("possible secret assignment detected")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_memory.py PATH", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    errors = validate(path)
    if errors:
        print(f"INVALID: {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALID: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
