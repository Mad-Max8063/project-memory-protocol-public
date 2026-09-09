from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.markdown_sections import parse_sections
from scripts.validate_memory import validate
from scripts.validate_profile_record import validate as validate_profile


ROOT = Path(__file__).resolve().parents[1]
BASE = """# Sample

## Identity
Human authority: Example maintainer
## Current state
[DOCUMENTED] Local test fixture.
## Active decisions
Read the task.
## Constraints
Local only.
## Priorities
Inspect the fixture.
## Next action
Codex: read TASK.md.
## Evidence
TASK.md
## Update rules
Retain observed results.
"""


class MarkdownSectionsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "memory.md"

    def errors(self, text):
        self.path.write_bytes(text.encode("utf-8"))
        return validate(self.path)

    def test_valid_lf_and_crlf(self):
        for text in (BASE, BASE.replace("\n", "\r\n")):
            with self.subTest(text=text):
                self.assertEqual(self.errors(text), [])

    def test_h3_does_not_supply_h2(self):
        self.assertTrue(self.errors(BASE.replace("## Identity", "### Identity")))

    def test_standard_atx_heading_spacing_remains_valid(self):
        for spaces in range(4):
            with self.subTest(spaces=spaces):
                self.assertEqual(self.errors(BASE.replace("## ", " " * spaces + "## ")), [])
        self.assertEqual(self.errors(BASE.replace("## Identity", "## Identity ###")), [])

    def test_heading_name_must_match(self):
        self.assertTrue(self.errors(BASE.replace("## Identity", "## Identity obsolete")))

    def test_inline_reference_is_not_duplicate(self):
        self.assertEqual(self.errors(BASE + "See `## Identity`.\n"), [])

    def test_fenced_documents_are_not_sections(self):
        for fence in ("```", "~~~~", "````"):
            with self.subTest(fence=fence):
                self.assertTrue(self.errors("# Sample\n" + fence + "\n" + BASE + fence + "\n"))

    def test_quoted_document_is_not_root_sections(self):
        self.assertTrue(self.errors("# Sample\n" + "\n".join("> " + line for line in BASE.splitlines())))

    def test_commented_document_is_not_sections(self):
        self.assertTrue(self.errors("# Sample\n<!--\n" + BASE + "-->\n"))

    def test_indented_code_is_not_sections(self):
        self.assertTrue(self.errors("# Sample\n\n" + "\n".join("    " + line for line in BASE.splitlines())))

    def test_fenced_heading_example_is_not_duplicate(self):
        self.assertEqual(self.errors(BASE + "\n```markdown\n## Identity\n```\n"), [])

    def test_commented_heading_example_is_not_duplicate(self):
        self.assertEqual(self.errors(BASE + "\n<!--\n## Identity\n-->\n"), [])

    def test_real_duplicate_is_rejected(self):
        self.assertTrue(self.errors(BASE + "\n## Identity\n"))

    def test_hidden_next_action_is_empty(self):
        self.assertTrue(self.errors(BASE.replace("Codex: read TASK.md.", "<!-- action removed -->")))

    def test_visible_action_formats_remain_valid(self):
        for action in ("`Codex: read TASK.md.`", "> Codex: read TASK.md.",
                       "```text\nCodex: read TASK.md.\n```", "No next action is selected."):
            with self.subTest(action=action):
                self.assertEqual(self.errors(BASE.replace("Codex: read TASK.md.", action)), [])

    def test_empty_fence_does_not_supply_action(self):
        self.assertTrue(self.errors(BASE.replace("Codex: read TASK.md.", "```text\n```")))

    def test_comment_markers_in_code_are_literal(self):
        text = BASE.replace("Inspect the fixture.", "```text\n<!-- literal marker\n```\nInspect the fixture.")
        self.assertEqual(self.errors(text), [])

    def test_fence_inside_comment_does_not_open(self):
        text = BASE.replace("Inspect the fixture.", "<!--\n```text\n-->\nInspect the fixture.")
        self.assertEqual(self.errors(text), [])

    def test_inline_code_comment_marker_is_literal(self):
        text = BASE.replace("Inspect the fixture.", "Inspect `<!--` and continue.")
        self.assertEqual(self.errors(text), [])

    def test_shorter_fence_does_not_close_example(self):
        text = "# Sample\n````markdown\n```\n" + BASE
        self.assertTrue(self.errors(text))

    def test_longer_matching_fence_closes_example(self):
        text = BASE.replace("Inspect the fixture.", "~~~text\n## Identity\n~~~~\nInspect the fixture.")
        self.assertEqual(self.errors(text), [])

    def test_hidden_label_does_not_supply_current_state(self):
        self.assertTrue(self.errors(BASE.replace("[DOCUMENTED]", "<!--[DOCUMENTED]-->")))

    def test_action_is_limited_to_its_section(self):
        sections = {section.name: section for section in parse_sections(BASE)}
        self.assertEqual(sections["Next action"].body, "Codex: read TASK.md.")

    def test_profile_records_cannot_be_fenced_examples(self):
        for kind, name in (("authority", "AUTHORITY.md"), ("evidence", "EVIDENCE_MANIFEST.md")):
            template = (ROOT / "profiles/evidence-backed-handoff/templates" / name).read_text(encoding="utf-8")
            with self.subTest(kind=kind):
                self.path.write_text("# Example\n```markdown\n" + template + "\n```\n", encoding="utf-8")
                self.assertTrue(validate_profile(kind, self.path))

    def test_profile_literal_heading_example_is_not_duplicate(self):
        template = (ROOT / "profiles/evidence-backed-handoff/templates/AUTHORITY.md").read_text(encoding="utf-8")
        self.path.write_text(template + "\n```markdown\n## Identity\n```\n", encoding="utf-8")
        self.assertEqual(validate_profile("authority", self.path), [])

    def test_escaped_backticks_do_not_hide_comment_syntax(self):
        for count in (1, 3):
            tick = chr(92) * count + "`"
            text = BASE.replace("Codex: read TASK.md.", "Codex: read. " + tick + "<!-- Human authority -->" + tick)
            self.assertEqual(self.errors(text), [])
            action = next(section.body for section in parse_sections(text) if section.name == "Next action")
            self.assertNotIn("Human authority", action)

    def test_even_backslashes_allow_a_real_code_span(self):
        text = BASE.replace("Inspect the fixture.", "Inspect " + chr(92) * 2 + "`<!--` and continue.")
        self.assertEqual(self.errors(text), [])

    def test_multiline_code_span_preserves_later_sections(self):
        text = BASE.replace("Inspect the fixture.", "Inspect `literal\nmarker <!--` and continue.")
        for sample in (text, text.replace("\n", "\r\n")):
            self.assertEqual(self.errors(sample), [])

    def test_multiline_code_span_closing_tick_is_not_escaped(self):
        text = BASE.replace("Inspect the fixture.", "Inspect ``literal\nmarker <!--" + chr(92) + "`` and continue.")
        self.assertEqual(self.errors(text), [])

    def test_unmatched_tick_does_not_cross_a_block_boundary(self):
        text = BASE.replace("Inspect the fixture.", "Inspect `unmatched.")
        text = text.replace("Codex: read TASK.md.", "Codex: read. <!-- hidden ` -->")
        self.assertEqual(self.errors(text), [])
        action = next(section.body for section in parse_sections(text) if section.name == "Next action")
        self.assertNotIn("hidden", action)

    def test_thematic_breaks_stop_multiline_code_spans(self):
        for mark in ("*", "-", "_"):
            for separator in (mark * 3, mark * 5, " ".join([mark] * 3), "\t".join([mark] * 3)):
                for indent in range(4):
                    for newline in ("\n", "\r\n"):
                        with self.subTest(separator=separator, indent=indent, newline=newline):
                            action = "Codex: read `example.\n" + " " * indent + separator + " \t\nLater <!-- Human authority ` -->"
                            text = BASE.replace("Codex: read TASK.md.", action).replace("\n", newline)
                            self.assertEqual(self.errors(text), [])
                            body = next(s.body for s in parse_sections(text) if s.name == "Next action")
                            self.assertNotIn("Human authority", body)
                            self.assertIn("Later", body)

    def test_setext_underlines_stop_multiline_code_spans(self):
        for underline in ("=", "===", "-", "--", "   === \t"):
            with self.subTest(underline=underline):
                action = "Codex: read `example.\n" + underline + "\nLater <!-- Human authority ` -->"
                text = BASE.replace("Codex: read TASK.md.", action)
                self.assertEqual(self.errors(text), [])
                body = next(s.body for s in parse_sections(text) if s.name == "Next action")
                self.assertNotIn("Human authority", body)

    def test_non_separators_preserve_multiline_code_spans(self):
        for line in ("**", "__", "*-*", "***text", "___text", "text---", "= =", "    ***", "\t***", r"\***"):
            with self.subTest(line=line):
                action = "Codex: read `example.\n" + line + "\nLater <!-- Human authority ` -->"
                text = BASE.replace("Codex: read TASK.md.", action)
                self.assertEqual(self.errors(text), [])
                body = next(s.body for s in parse_sections(text) if s.name == "Next action")
                self.assertIn("Human authority", body)  # Literal code, not an HTML comment.

    def test_unmatched_tick_does_not_protect_comments(self):
        text = BASE.replace("Inspect the fixture.", "Inspect `unmatched <!-- hidden -->.")
        self.assertEqual(self.errors(text), [])
        priorities = next(section.body for section in parse_sections(text) if section.name == "Priorities")
        self.assertNotIn("hidden", priorities)


if __name__ == "__main__":
    unittest.main()
