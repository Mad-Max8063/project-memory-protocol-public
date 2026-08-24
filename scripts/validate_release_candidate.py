#!/usr/bin/env python3
"""Validate PMP stable-release consistency and repository hygiene."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


CORE_VERSION = "0.2.1"
PROFILE_VERSION = "0.1.1"
MAX_FILE_SIZE = 1024 * 1024

REQUIRED_TEXT = {
    "SPEC.md": (
        f"- Version: `{CORE_VERSION}`",
        "- Status: Stable specification; repository lifecycle state is non-normative",
    ),
    "README.md": (
        f"stable protocol line: Core `{CORE_VERSION}`; Evidence-backed Handoff profile `{PROFILE_VERSION}`",
        "docs/UPGRADING_0.1.1_TO_0.2.1.md",
        "docs/RELEASE_NOTES_0.2.1.md",
        "docs/PROVENANCE.md",
    ),
    "templates/PROJECT_MEMORY.md": (f"> Protocol: PMP `{CORE_VERSION}`",),
    "examples/chatgpt-codex-handoff/README.md": (
        "PMP `0.1.1` compatibility fixture",
        f"Core `{CORE_VERSION}`",
    ),
    "AGENTS.md": (f"PMP `{CORE_VERSION}`",),
    "adapters/AGENTS.md": (f"PMP {CORE_VERSION}",),
    "adapters/CLAUDE.md": (f"PMP {CORE_VERSION}",),
    "adapters/GEMINI.md": (f"PMP {CORE_VERSION}",),
    "adapters/CHATGPT.md": (f"PMP {CORE_VERSION}",),
    "profiles/evidence-backed-handoff/PROFILE.md": (
        f"- Profile version: `{PROFILE_VERSION}`",
        f"- Compatible base: PMP `0.1.1` or `{CORE_VERSION}`",
        "- Status: stable profile; repository lifecycle state is non-normative",
    ),
    "CHANGELOG.md": (f"## {CORE_VERSION} — metadata correction",),
    "docs/RELEASE_NOTES_0.2.1.md": (
        f"# Project Memory Protocol {CORE_VERSION}",
        "Status: stable metadata-correction notes",
    ),
    "docs/PROVENANCE.md": (
        "# Clean distribution provenance",
        f"Protocol Core `{CORE_VERSION}`",
    ),
}

EXCLUDED_DIRECTORIES = {".git", "__pycache__", ".pytest_cache"}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".toml", ".json", ".txt"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)"
    r"\s*[:=]\s*(?![<`])[\"']?[^\s\"'`]+"
)


def repository_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and not any(part in EXCLUDED_DIRECTORIES for part in path.relative_to(root).parts)
    )


def validate_versions(root: Path) -> list[str]:
    errors: list[str] = []
    for relative, required_tokens in REQUIRED_TEXT.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing release file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in required_tokens:
            if token not in text:
                errors.append(f"missing release token in {relative}: {token}")
    return errors


def validate_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in repository_files(root):
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = target.split(maxsplit=1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target or "<" in target or ">" in target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                relative = path.relative_to(root).as_posix()
                errors.append(f"broken relative link in {relative}: {raw_target}")
    return errors


def validate_sizes(root: Path) -> list[str]:
    return [
        f"file exceeds 1 MiB: {path.relative_to(root).as_posix()} ({path.stat().st_size} bytes)"
        for path in repository_files(root)
        if path.stat().st_size > MAX_FILE_SIZE
    ]


def validate_secrets(root: Path) -> list[str]:
    errors: list[str] = []
    for path in repository_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if SECRET_ASSIGNMENT.search(text):
            errors.append(
                f"possible secret assignment in {path.relative_to(root).as_posix()}"
            )
    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_versions(root))
    errors.extend(validate_links(root))
    errors.extend(validate_sizes(root))
    errors.extend(validate_secrets(root))
    return errors


def main(argv: list[str]) -> int:
    if len(argv) > 2:
        print("usage: validate_release_candidate.py [ROOT]", file=sys.stderr)
        return 2
    root = Path(argv[1] if len(argv) == 2 else ".").resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print(
        "VALID release metadata: "
        f"Core {CORE_VERSION}; profile {PROFILE_VERSION}; links, size, and secrets passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
