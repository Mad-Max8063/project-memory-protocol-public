from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from scripts.validate_profile_record import REQUIRED_FIELDS, validate


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_TEMPLATE = (
    ROOT / "profiles/evidence-backed-handoff/templates/AUTHORITY.md"
)
EVIDENCE_TEMPLATE = (
    ROOT / "profiles/evidence-backed-handoff/templates/EVIDENCE_MANIFEST.md"
)


class ValidateProfileRecordTests(unittest.TestCase):
    def temporary_record(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "record.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_authority_template_is_valid(self) -> None:
        self.assertEqual(validate("authority", AUTHORITY_TEMPLATE), [])

    def test_evidence_template_is_valid(self) -> None:
        self.assertEqual(validate("evidence", EVIDENCE_TEMPLATE), [])

    def test_unknown_record_type_is_rejected(self) -> None:
        self.assertIn("unknown record type", validate("unknown", AUTHORITY_TEMPLATE)[0])

    def test_authority_with_only_headings_is_rejected(self) -> None:
        text = "\n".join(
            [
                "# Authority",
                "## Identity",
                "## Approved decision",
                "## Allowed scope",
                "## Explicit exclusions",
                "## Evidence boundary",
            ]
        )
        errors = validate("authority", self.temporary_record(text))
        self.assertTrue(any("missing or empty field" in error for error in errors))
        self.assertIn("Approved decision must contain a non-empty blockquote", errors)

    def test_evidence_with_only_headings_is_rejected(self) -> None:
        text = "\n".join(
            [
                "# Evidence",
                "## Subject",
                "## Verification",
                "## Artifacts",
                "## External state",
                "## Evidence boundaries",
                "## Closure",
            ]
        )
        errors = validate("evidence", self.temporary_record(text))
        self.assertTrue(any("missing or empty field" in error for error in errors))
        self.assertIn("Verification must contain at least one observed gate", errors)

    def test_missing_required_field_is_rejected(self) -> None:
        text = AUTHORITY_TEMPLATE.read_text(encoding="utf-8").replace(
            "- Starting revision: `<commit, tag, or immutable baseline>`\n", ""
        )
        errors = validate("authority", self.temporary_record(text))
        self.assertIn("missing or empty field in Identity: Starting revision", errors)

    def test_every_required_scalar_field_rejects_an_empty_value(self) -> None:
        templates = {
            "authority": AUTHORITY_TEMPLATE.read_text(encoding="utf-8"),
            "evidence": EVIDENCE_TEMPLATE.read_text(encoding="utf-8"),
        }

        for kind, sections in REQUIRED_FIELDS.items():
            for heading, labels in sections.items():
                for label in labels:
                    with self.subTest(kind=kind, heading=heading, label=label):
                        text, replacements = re.subn(
                            rf"^- {re.escape(label)}:[^\r\n]*$",
                            f"- {label}:",
                            templates[kind],
                            count=1,
                            flags=re.MULTILINE,
                        )
                        self.assertEqual(replacements, 1)
                        errors = validate(kind, self.temporary_record(text))
                        self.assertIn(
                            f"missing or empty field in {heading}: {label}",
                            errors,
                        )

    def test_every_required_scalar_field_rejects_a_duplicate(self) -> None:
        templates = {
            "authority": AUTHORITY_TEMPLATE.read_text(encoding="utf-8"),
            "evidence": EVIDENCE_TEMPLATE.read_text(encoding="utf-8"),
        }

        for kind, sections in REQUIRED_FIELDS.items():
            for heading, labels in sections.items():
                for label in labels:
                    with self.subTest(kind=kind, heading=heading, label=label):
                        text, replacements = re.subn(
                            rf"(^- {re.escape(label)}:[^\r\n]*$)",
                            rf"\1\n- {label}:",
                            templates[kind],
                            count=1,
                            flags=re.MULTILINE,
                        )
                        self.assertEqual(replacements, 1)
                        errors = validate(kind, self.temporary_record(text))
                        self.assertIn(
                            f"missing or empty field in {heading}: {label}",
                            errors,
                        )

    def test_evidence_requires_a_nested_observed_gate(self) -> None:
        text = EVIDENCE_TEMPLATE.read_text(encoding="utf-8").replace(
            "  - `<command or gate>` -> `<observed result>`\n", ""
        )
        errors = validate("evidence", self.temporary_record(text))
        self.assertIn("Verification must contain at least one observed gate", errors)

    def test_evidence_rejects_an_unrelated_indented_bullet_without_gate_field(
        self,
    ) -> None:
        text = EVIDENCE_TEMPLATE.read_text(encoding="utf-8").replace(
            "- Gates observed:\n", ""
        )
        errors = validate("evidence", self.temporary_record(text))
        self.assertIn("Verification must contain at least one observed gate", errors)

    def test_evidence_rejects_an_empty_gate_field_with_a_decoy_nested_elsewhere(
        self,
    ) -> None:
        text = EVIDENCE_TEMPLATE.read_text(encoding="utf-8").replace(
            "- Gates observed:\n"
            "  - `<command or gate>` -> `<observed result>`\n",
            "- Gates observed:\n"
            "- Notes:\n"
            "  - `<unrelated indented bullet>`\n",
        )
        errors = validate("evidence", self.temporary_record(text))
        self.assertIn("Verification must contain at least one observed gate", errors)

    def test_evidence_rejects_duplicate_gate_fields_in_either_order(self) -> None:
        template = EVIDENCE_TEMPLATE.read_text(encoding="utf-8")
        valid_then_empty = template.replace(
            "  - `<command or gate>` -> `<observed result>`\n",
            "  - `<command or gate>` -> `<observed result>`\n"
            "- Gates observed:\n",
        )
        empty_then_valid = template.replace(
            "- Gates observed:\n",
            "- Gates observed:\n- Gates observed:\n",
        )

        for text in (valid_then_empty, empty_then_valid):
            with self.subTest(order=text.index("  - `<command or gate>`")):
                errors = validate("evidence", self.temporary_record(text))
                self.assertIn(
                    "Verification must contain at least one observed gate",
                    errors,
                )

    def test_evidence_rejects_one_space_gate_indentation(self) -> None:
        text = EVIDENCE_TEMPLATE.read_text(encoding="utf-8").replace(
            "  - `<command or gate>` -> `<observed result>`\n",
            " - `<command or gate>` -> `<observed result>`\n",
        )
        errors = validate("evidence", self.temporary_record(text))
        self.assertIn("Verification must contain at least one observed gate", errors)

    def test_evidence_rejects_a_deep_bullet_without_a_direct_gate(self) -> None:
        text = EVIDENCE_TEMPLATE.read_text(encoding="utf-8").replace(
            "  - `<command or gate>` -> `<observed result>`\n",
            "  continuation without a direct gate\n"
            "    - `<deep bullet without parent>`\n",
        )
        errors = validate("evidence", self.temporary_record(text))
        self.assertIn("Verification must contain at least one observed gate", errors)

    def test_evidence_accepts_supported_direct_gate_indentation(self) -> None:
        template = EVIDENCE_TEMPLATE.read_text(encoding="utf-8")
        for indentation in ("  ", "    ", "\t"):
            with self.subTest(indentation=repr(indentation)):
                text = template.replace(
                    "  - `<command or gate>` -> `<observed result>`\n",
                    f"{indentation}- `<command or gate>` -> `<observed result>`\n",
                )
                self.assertEqual(validate("evidence", self.temporary_record(text)), [])

    def test_wrong_heading_order_is_rejected(self) -> None:
        text = AUTHORITY_TEMPLATE.read_text(encoding="utf-8").replace(
            "## Allowed scope", "## TEMP", 1
        ).replace("## Explicit exclusions", "## Allowed scope", 1).replace(
            "## TEMP", "## Explicit exclusions", 1
        )
        errors = validate("authority", self.temporary_record(text))
        self.assertIn("required headings are not in the expected order", errors)

    def test_secret_assignment_is_rejected(self) -> None:
        secret_assignment = '\npass' + 'word = "not-a-real-secret"\n'
        text = AUTHORITY_TEMPLATE.read_text(encoding="utf-8") + secret_assignment
        errors = validate("authority", self.temporary_record(text))
        self.assertIn("possible secret assignment detected", errors)


if __name__ == "__main__":
    unittest.main()
