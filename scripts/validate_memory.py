#!/usr/bin/env python3
"""Validate the version-neutral structural and safety baseline of a PMP memory."""

from __future__ import annotations

import re
import sys
from pathlib import Path


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

    positions: list[int] = []
    for heading in REQUIRED_HEADINGS:
        count = text.count(heading)
        if count != 1:
            errors.append(f"required heading {heading!r} must appear exactly once (found {count})")
        positions.append(text.find(heading))

    present_positions = [position for position in positions if position >= 0]
    if present_positions != sorted(present_positions):
        errors.append("required headings are out of order")

    current_start = text.find("## Current state")
    decisions_start = text.find("## Active decisions")
    if current_start >= 0 and decisions_start > current_start:
        current_state = text[current_start:decisions_start]
        if not EVIDENCE_LABEL.search(current_state):
            errors.append("Current state must include at least one PMP evidence label")

    next_start = text.find("## Next action")
    evidence_start = text.find("## Evidence")
    if next_start >= 0 and evidence_start > next_start:
        body = text[next_start + len("## Next action"):evidence_start].strip()
        if not body:
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
