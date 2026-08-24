from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_release_candidate import (
    CORE_VERSION,
    MAX_FILE_SIZE,
    PROFILE_VERSION,
    REQUIRED_TEXT,
    validate,
    validate_links,
    validate_secrets,
    validate_sizes,
    validate_versions,
)


ROOT = Path(__file__).resolve().parents[1]


class ValidateReleaseCandidateTests(unittest.TestCase):
    def temporary_root(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return Path(directory.name)

    def complete_version_fixture(self) -> Path:
        root = self.temporary_root()
        for relative, tokens in REQUIRED_TEXT.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(tokens), encoding="utf-8")
        return root

    def test_repository_release_candidate_is_valid(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_stable_versions_are_explicit(self) -> None:
        self.assertEqual(CORE_VERSION, "0.2.1")
        self.assertEqual(PROFILE_VERSION, "0.1.1")
        self.assertIn("docs/RELEASE_NOTES_0.2.1.md", REQUIRED_TEXT)
        self.assertIn("docs/PROVENANCE.md", REQUIRED_TEXT)

    def test_version_contract_rejects_a_missing_token(self) -> None:
        root = self.complete_version_fixture()
        path = root / "SPEC.md"
        path.write_text("candidate without version", encoding="utf-8")
        errors = validate_versions(root)
        self.assertTrue(any("SPEC.md" in error for error in errors))

    def test_relative_link_checker_accepts_existing_target(self) -> None:
        root = self.temporary_root()
        (root / "target.md").write_text("# Target\n", encoding="utf-8")
        (root / "source.md").write_text("[target](target.md)\n", encoding="utf-8")
        self.assertEqual(validate_links(root), [])

    def test_relative_link_checker_rejects_missing_target(self) -> None:
        root = self.temporary_root()
        (root / "source.md").write_text("[missing](missing.md)\n", encoding="utf-8")
        self.assertTrue(validate_links(root))

    def test_size_checker_rejects_file_over_limit(self) -> None:
        root = self.temporary_root()
        (root / "large.bin").write_bytes(b"x" * (MAX_FILE_SIZE + 1))
        self.assertTrue(validate_sizes(root))

    def test_secret_checker_rejects_assignment(self) -> None:
        root = self.temporary_root()
        secret_text = "api_" + 'key = "not-a-real-secret"\n'
        (root / "unsafe.txt").write_text(secret_text, encoding="utf-8")
        self.assertTrue(validate_secrets(root))


if __name__ == "__main__":
    unittest.main()
