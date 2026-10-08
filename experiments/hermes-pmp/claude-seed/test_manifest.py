"""Trusted host-owned acceptance for the Claude continuation."""
import json
from pathlib import Path
import unittest


class ManifestTests(unittest.TestCase):
    def test_manifest_matches_fixture_in_order(self):
        items = json.loads(Path('fixture.json').read_text(encoding='utf-8'))['items']
        expected = ''.join(f"{item['id']}={item['label']}\n" for item in items)
        self.assertEqual(Path('labels.txt').read_bytes(), expected.encode('utf-8'))

    def test_manifest_has_two_distinct_ids(self):
        lines = Path('labels.txt').read_text(encoding='utf-8').splitlines()
        self.assertEqual([line.split('=', 1)[0] for line in lines], ['pmp', 'handoff'])

    def test_manifest_has_no_blank_lines(self):
        value = Path('labels.txt').read_bytes()
        self.assertTrue(value.endswith(b'\n'))
        self.assertEqual(len(value.splitlines()), 2)
        self.assertNotIn(b'\r', value)


if __name__ == '__main__':
    unittest.main()
