"""Local deterministic checks; never invoke Claude or a provider."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1] / 'experiments/hermes-pmp'
sys.path.insert(0, str(HERE))
from claude_replay import NEXT, claude_env, extract, finish, prepare, validate_candidate
from adapter import atomic, json_bytes, validate


class ClaudeContinuationTests(unittest.TestCase):
    def setUp(self):
        self.data = {'input_sha256': {'PROJECT_MEMORY.md': 'memory-digest'},
                     'files': {'fixture.json': json.dumps({'items': [{'id': 'pmp', 'label': 'Portable memory'},
                                                                    {'id': 'handoff', 'label': 'Evidence chain'}]})}}
        self.proposal = {'actor': 'Claude', 'previous_actor': 'Hermes', 'expected_memory_sha256': 'memory-digest',
                         'labels_text': 'pmp=Portable memory\nhandoff=Evidence chain\n',
                         'action_attempted': 'Derive labels manifest.', 'result': 'Proposal only; no tests run.',
                         'tests_executed_by_model': False, 'decisions_proposed': [], 'unresolved_issues': [],
                         'intended_next_actor': 'Codex', 'next_action': NEXT}

    def test_bad_or_stale_proposal_rejected(self):
        for key, value in [('labels_text', 'wrong\n'), ('expected_memory_sha256', 'stale'),
                           ('tests_executed_by_model', True), ('decisions_proposed', ['change scope']),
                           ('next_action', 'deploy'), ('previous_actor', 'unknown')]:
            with self.subTest(key=key):
                bad = copy.deepcopy(self.proposal)
                bad[key] = value
                with self.assertRaises(ValueError):
                    validate_candidate(self.data, bad)
        self.assertEqual(validate_candidate(self.data, self.proposal), self.proposal['labels_text'])

    def test_runtime_tools_or_failed_completion_rejected(self):
        events = [{'type': 'system', 'subtype': 'init', 'tools': [], 'model': 'local-test'},
                  {'type': 'result', 'subtype': 'success', 'is_error': False, 'result': json.dumps(self.proposal)}]
        encode = lambda value: '\n'.join(json.dumps(event) for event in value)
        self.assertEqual(extract(encode(events))['proposal'], self.proposal)
        events[0]['tools'] = ['Bash']
        with self.assertRaises(ValueError):
            extract(encode(events))
        events[0]['tools'] = []
        events[1]['subtype'] = 'error_max_turns'
        with self.assertRaises(ValueError):
            extract(encode(events))

    def test_auth_environment_does_not_inherit_api_keys(self):
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-value', 'ANTHROPIC_AUTH_TOKEN': 'test-value',
                                     'ANTHROPIC_BASE_URL': 'https://invalid.example', 'USERPROFILE': r'C:\fixture-user'}):
            env = claude_env()
        self.assertNotIn('ANTHROPIC_API_KEY', env)
        self.assertNotIn('ANTHROPIC_AUTH_TOKEN', env)
        self.assertNotIn('ANTHROPIC_BASE_URL', env)
        self.assertEqual(env['USERPROFILE'], r'C:\fixture-user')

    def test_local_host_chain_preserves_hermes_and_next_action(self):
        with tempfile.TemporaryDirectory(prefix='pmp-claude-test-') as temp:
            work = Path(temp) / 'run'
            prepare(work)
            data = json.loads((work / 'input-pmp.json').read_text(encoding='utf-8'))
            proposal = copy.deepcopy(self.proposal)
            proposal['expected_memory_sha256'] = data['input_sha256']['PROJECT_MEMORY.md']
            atomic(work / 'claude-output.json', json_bytes({'proposal': proposal,
                   'runtime': {'mode': 'local mock; NOT real Claude', 'tools': []}}))
            report = finish(work)
            self.assertEqual(report['host_verification']['exit_code'], 0)
            self.assertIn('Ran 6 tests', report['host_verification']['stderr'])
            self.assertFalse(report['fresh_codex_executed'])
            root = work / 'fresh-result'
            self.assertEqual(validate(root / 'PROJECT_MEMORY.md'), [])
            self.assertIn(NEXT, (root / 'PROJECT_MEMORY.md').read_text(encoding='utf-8'))
            for name in ('fixture.json', 'evidence/host-verification.json', '.project-memory/sessions/hermes-handoff.md'):
                self.assertEqual((root / name).read_bytes().decode(), data['files'][name])
            with self.assertRaises(ValueError):
                finish(work)


if __name__ == '__main__':
    unittest.main()
