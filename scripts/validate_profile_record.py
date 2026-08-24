#!/usr/bin/env python3
"""Validate the structure of PMP Evidence-backed Handoff profile records."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = {
    "authority": (
        "Identity",
        "Approved decision",
        "Allowed scope",
        "Explicit exclusions",
        "Evidence boundary",
    ),
    "evidence": (
        "Subject",
        "Verification",
        "Artifacts",
        "External state",
        "Evidence boundaries",
        "Closure",
    ),
}

REQUIRED_FIELDS = {
    "authority": {
        "Identity": (
            "Date",
            "Human authority",
            "Repository or project",
            "Starting revision",
        ),
    },
    "evidence": {
        "Subject": (
            "Repository or project",
            "Branch or ref",
            "Verified revision",
            "Recorded at",
        ),
        "Verification": (
            "Platform",
            "Runner context",
            "Run ID",
            "Run URL",
            "Conclusion",
        ),
        "Artifacts": (
            "Artifact ID",
            "Name",
            "Digest",
            "Retention or expiry",
        ),
        "External state": (
            "Effective permissions",
            "Deployment or promotion state",
            "Adjacent findings",
        ),
        "Closure": (
            "Evidence-record location",
            "Stopping rule",
            "Exact next action",
        ),
    },
}

SECRET_ASSIGNMENT = re.compile(
    r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)"
    r"\s*[:=]\s*(?!<)[^\s`]+"
)


def split_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## (.+?)\s*$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[start:end].strip()
    return sections


def field_value(section: str, label: str) -> str | None:
    matches = re.findall(
        rf"^- {re.escape(label)}:[ \t]*(.*)$",
        section,
        flags=re.MULTILINE,
    )
    if len(matches) != 1:
        return None
    value = matches[0].strip()
    return value or None


def nested_list_items(section: str, label: str) -> list[str]:
    lines = section.splitlines()
    field_pattern = re.compile(rf"^- {re.escape(label)}:[ \t]*$")
    occurrence_pattern = re.compile(rf"^- {re.escape(label)}:.*$")
    field_indexes = [
        index for index, line in enumerate(lines) if occurrence_pattern.fullmatch(line)
    ]
    if len(field_indexes) != 1 or not field_pattern.fullmatch(lines[field_indexes[0]]):
        return []

    def indentation_width(prefix: str) -> int:
        width = 0
        for character in prefix:
            if character == "\t":
                width += 4 - (width % 4)
            else:
                width += 1
        return width

    item_pattern = re.compile(r"^([ \t]+)-[ \t]+(\S.*)$")
    items: list[str] = []
    item_width: int | None = None
    for child in lines[field_indexes[0] + 1 :]:
        if not child.strip():
            continue
        if not child.startswith((" ", "\t")):
            break

        match = item_pattern.fullmatch(child)
        child_prefix = child[: len(child) - len(child.lstrip(" \t"))]
        child_width = indentation_width(child_prefix)
        if item_width is None:
            if match is None or child_width < 2:
                return []
            item_width = child_width
            items.append(match.group(2).strip())
            continue

        if child_width < item_width:
            return []
        if match is not None and child_width == item_width:
            items.append(match.group(2).strip())

    return items


def validate(kind: str, path: Path) -> list[str]:
    errors: list[str] = []
    if kind not in REQUIRED_HEADINGS:
        return [f"unknown record type: {kind}"]
    if not path.is_file():
        return [f"file not found: {path}"]

    text = path.read_text(encoding="utf-8")
    headings = re.findall(r"^## (.+?)\s*$", text, flags=re.MULTILINE)
    expected = list(REQUIRED_HEADINGS[kind])
    sections = split_sections(text)

    missing = [heading for heading in expected if heading not in headings]
    if missing:
        errors.append("missing headings: " + ", ".join(missing))

    ordered = [heading for heading in headings if heading in expected]
    if ordered != expected:
        errors.append("required headings are not in the expected order")

    for heading, labels in REQUIRED_FIELDS[kind].items():
        section = sections.get(heading, "")
        for label in labels:
            if field_value(section, label) is None:
                errors.append(f"missing or empty field in {heading}: {label}")

    if kind == "authority":
        decision = sections.get("Approved decision", "")
        if not re.search(r"^>\s+\S", decision, flags=re.MULTILINE):
            errors.append("Approved decision must contain a non-empty blockquote")
        for heading in ("Allowed scope", "Explicit exclusions"):
            if not re.search(r"^-\s+\S", sections.get(heading, ""), flags=re.MULTILINE):
                errors.append(f"{heading} must contain at least one item")
        if not sections.get("Evidence boundary", "").strip():
            errors.append("Evidence boundary must not be empty")

    if kind == "evidence":
        verification = sections.get("Verification", "")
        if not nested_list_items(verification, "Gates observed"):
            errors.append("Verification must contain at least one observed gate")
        boundaries = re.findall(
            r"^-\s+\S.*(?:\n(?: {2,}|\t).*)*",
            sections.get("Evidence boundaries", ""),
            flags=re.MULTILINE,
        )
        if len(boundaries) < 2:
            errors.append("Evidence boundaries must contain at least two items")

    if SECRET_ASSIGNMENT.search(text):
        errors.append("possible secret assignment detected")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: validate_profile_record.py TYPE PATH", file=sys.stderr)
        return 2

    kind, raw_path = argv[1], argv[2]
    errors = validate(kind, Path(raw_path))
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1

    print(f"VALID {kind}: {raw_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
