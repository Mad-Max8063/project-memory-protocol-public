#!/usr/bin/env python3
"""Verify the packaged PMP handoff example end to end."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


DEMO_DIR = Path(__file__).resolve().parent
REPO_ROOT = DEMO_DIR.parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_memory import validate  # noqa: E402


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    before_path = DEMO_DIR / "fixtures" / "before" / "PROJECT_MEMORY.md"
    after_path = DEMO_DIR / "fixtures" / "after" / "PROJECT_MEMORY.md"
    workspace_memory = DEMO_DIR / "workspace" / "PROJECT_MEMORY.md"

    for path in (before_path, after_path, workspace_memory):
        for error in validate(path):
            errors.append(f"{path.relative_to(REPO_ROOT)}: {error}")

    before = before_path.read_text(encoding="utf-8")
    after = after_path.read_text(encoding="utf-8")
    require("Last actor: `ChatGPT`" in before, "before snapshot must identify ChatGPT", errors)
    require("Last actor: `Codex`" in after, "after snapshot must identify Codex", errors)
    require("did not implement" in before, "before snapshot must keep implementation pending", errors)
    require("six passing tests" in after, "after snapshot must record test evidence", errors)
    require("02-codex-session.md" in after, "after snapshot must link Codex evidence", errors)
    require("LIVE_DEMO_RUNBOOK.md" in after, "after snapshot must advance the next action", errors)

    evidence_files = [
        DEMO_DIR / "evidence" / "01-chatgpt-decision.md",
        DEMO_DIR / "evidence" / "02-codex-session.md",
        DEMO_DIR / "evidence" / "03-chatgpt-verification.md",
        DEMO_DIR / "workspace" / ".project-memory" / "sessions" / "2026-08-22-codex-slugify.md",
    ]
    for path in evidence_files:
        require(path.is_file(), f"missing evidence: {path.relative_to(REPO_ROOT)}", errors)

    test_run = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_slugify.py"],
        cwd=DEMO_DIR / "workspace",
        text=True,
        capture_output=True,
        check=False,
    )
    combined_output = test_run.stdout + test_run.stderr
    require(test_run.returncode == 0, "workspace tests failed", errors)
    require("Ran 6 tests" in combined_output, "expected exactly six executed tests", errors)
    require("OK" in combined_output, "test suite did not report OK", errors)

    if errors:
        print("DEMO INVALID")
        for error in errors:
            print(f"- {error}")
        if test_run.returncode != 0:
            print(combined_output)
        return 1

    print("DEMO VERIFIED")
    print("- before memory: valid; actor ChatGPT; implementation pending")
    print("- after memory: valid; actor Codex; implementation verified")
    print("- evidence chain: complete")
    print("- executable result: 6 tests passed")
    print("- next action: live independent-session recording")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
