import json
import unittest
from pathlib import Path


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.value = json.loads(Path('fixture.json').read_text(encoding='utf-8'))

    def test_shape_and_ids(self):
        self.assertEqual(set(self.value), {'schema', 'items'})
        self.assertEqual(self.value['schema'], 1)
        self.assertEqual([x['id'] for x in self.value['items']], ['pmp', 'handoff'])
        self.assertTrue(all(set(x) == {'id', 'label'} for x in self.value['items']))

    def test_normalized_labels(self):
        self.assertEqual([x['label'] for x in self.value['items']],
                         ['Portable memory', 'Evidence chain'])

    def test_whitespace_contract(self):
        for item in self.value['items']:
            self.assertEqual(item['label'], ' '.join(item['label'].split()))


if __name__ == '__main__':
    unittest.main()
