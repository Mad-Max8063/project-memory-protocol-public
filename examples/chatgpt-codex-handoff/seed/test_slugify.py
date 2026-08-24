import unittest

from slugify import slugify


class SlugifyTests(unittest.TestCase):
    def test_lowercases_text(self):
        self.assertEqual(slugify("Project Memory"), "project-memory")

    def test_trims_surrounding_whitespace(self):
        self.assertEqual(slugify("  shared state  "), "shared-state")

    def test_strips_decomposable_diacritics(self):
        self.assertEqual(slugify("Memoria canónica"), "memoria-canonica")

    def test_collapses_separator_runs(self):
        self.assertEqual(slugify("ChatGPT  <->  Codex"), "chatgpt-codex")

    def test_removes_edge_hyphens(self):
        self.assertEqual(slugify("---handoff---"), "handoff")

    def test_empty_input_stays_empty(self):
        self.assertEqual(slugify("   "), "")


if __name__ == "__main__":
    unittest.main()
