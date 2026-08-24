#!/usr/bin/env python3
"""Verify the live handoff repository after both independent agent phases."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
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


def main() -> int:
    errors: list[str] = []
    memory_path = ROOT / "PROJECT_MEMORY.md"
    memory = memory_path.read_text(encoding="utf-8")

    positions = [memory.find(heading) for heading in REQUIRED_HEADINGS]
    if any(position < 0 for position in positions):
        errors.append("canonical memory is missing required PMP headings")
    elif positions != sorted(positions):
        errors.append("canonical memory headings are out of order")

    if "Last actor: `Codex`" not in memory:
        errors.append("canonical memory does not record the Codex handoff")
    if "[VERIFIED]" not in memory:
        errors.append("canonical memory has no verified state")

    chatgpt_evidence = ROOT / "evidence" / "01-chatgpt-decision.md"
    if not chatgpt_evidence.is_file():
        errors.append("missing ChatGPT decision evidence")

    session_dir = ROOT / ".project-memory" / "sessions"
    codex_sessions = list(session_dir.glob("*-codex-slugify.md")) if session_dir.is_dir() else []
    if len(codex_sessions) != 1:
        errors.append("expected exactly one Codex slugify session record")

    test_run = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_slugify.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = test_run.stdout + test_run.stderr
    if test_run.returncode != 0 or "Ran 6 tests" not in output or "OK" not in output:
        errors.append("six-test acceptance suite is not passing")

    if errors:
        print("LIVE DEMO NOT COMPLETE")
        for error in errors:
            print(f"- {error}")
        return 1

    print("LIVE DEMO VERIFIED")
    print("- canonical memory records the Codex handoff")
    print("- ChatGPT decision evidence exists")
    print("- one Codex session record exists")
    print("- 6 acceptance tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
