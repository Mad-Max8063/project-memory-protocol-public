"""Bridge tests never install Hermes or call a provider."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1] / 'experiments' / 'hermes-pmp'
sys.path.insert(0, str(HERE))
from adapter import EVIDENCE, HANDOFF, INPUT_FILES, NEXT_ACTION, clean_env, create_handoff, read_state, safe_path
from consumer import CONFIG, extract_stream, hermes_consume, proposal_template
from continuation import verify
from replay import replay
from scripts.validate_memory import validate


class HermesBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pmp-bridge-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in INPUT_FILES:
            shutil.copyfile(HERE / 'seed' / name, self.root / name)
        self.packet = read_state(self.root)
        self.proposal = proposal_template(self.packet, 'mock-hermes')
        for item in self.proposal['fixture']['items']:
            item['label'] = ' '.join(item['label'].split())

    def test_state_serialization_preserves_canonical_bytes_and_sections(self):
        packet = json.loads(json.dumps(self.packet))
        self.assertEqual(packet['canonical_memory'], (self.root / 'PROJECT_MEMORY.md').read_bytes().decode('utf-8'))
        self.assertEqual(packet['project_identifier'], 'hermes-pmp-fixture')
        self.assertEqual(packet['protocol'], 'PMP 0.2.2')
        self.assertIn('Hermes:', packet['sections']['Next action'])
        for section in ('Current state', 'Active decisions', 'Constraints', 'Evidence'):
            self.assertTrue(packet['sections'][section])
        self.assertIsNone(packet['previous_handoff'])

    def test_handoff_preserves_decisions_evidence_and_next_action(self):
        record = create_handoff(self.root, self.packet, self.proposal, 'mock')
        state = read_state(self.root)
        self.assertEqual(state['sections']['Active decisions'], self.packet['sections']['Active decisions'])
        self.assertEqual(state['sections']['Constraints'], self.packet['sections']['Constraints'])
        self.assertEqual(state['sections']['Next action'], NEXT_ACTION)
        self.assertIn(EVIDENCE, state['sections']['Evidence'])
        self.assertIn(EVIDENCE, state['previous_handoff'])
        self.assertFalse(record['tests_executed_by_model'])
        self.assertEqual(validate(self.root / 'PROJECT_MEMORY.md'), [])
        self.assertEqual(verify(self.root)['exit_code'], 0)

    def test_stale_memory_rejected_without_writes(self):
        (self.root / 'PROJECT_MEMORY.md').write_text(self.packet['canonical_memory'] + '\n', encoding='utf-8')
        before = (self.root / 'fixture.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'input changed'):
            create_handoff(self.root, self.packet, self.proposal, 'mock')
        self.assertEqual((self.root / 'fixture.json').read_bytes(), before)
        self.assertFalse((self.root / EVIDENCE).exists())

    def test_invalid_candidate_and_schema_are_rejected(self):
        for mutation in ('path', 'id', 'type', 'next_action', 'actor', 'decision'):
            proposal = copy.deepcopy(self.proposal)
            if mutation == 'path':
                proposal['files_changed'] = ['../../outside']
            elif mutation == 'id':
                proposal['fixture']['items'][0]['id'] = 'changed'
            elif mutation == 'type':
                proposal['fixture']['schema'] = True
            elif mutation == 'next_action':
                proposal['next_action'] = 'Deploy production'
            elif mutation == 'actor':
                proposal['actor'] = 'Hermes'
            else:
                proposal['decisions_proposed'] = ['silently change authority']
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                create_handoff(self.root, self.packet, proposal, 'mock')
        self.assertFalse((self.root / EVIDENCE).exists())

    def test_immutable_tests_cannot_be_replaced_by_a_proposal(self):
        (self.root / 'test_fixture.py').write_text('raise SystemExit(0)\n', encoding='utf-8')
        self.packet = read_state(self.root)
        self.proposal['expected_memory_sha256'] = self.packet['memory_sha256']
        with self.assertRaisesRegex(ValueError, 'untrusted'):
            create_handoff(self.root, self.packet, self.proposal, 'mock')

    def test_host_failure_rolls_back_fixture_and_memory(self):
        before = {name: (self.root / name).read_bytes() for name in INPUT_FILES}
        failure = subprocess.CompletedProcess([], 1, '', 'failure fixture')
        with patch('adapter.subprocess.run', return_value=failure):
            with self.assertRaisesRegex(ValueError, 'tests failed'):
                create_handoff(self.root, self.packet, self.proposal, 'mock')
        for name in INPUT_FILES:
            self.assertEqual((self.root / name).read_bytes(), before[name])
        self.assertFalse((self.root / EVIDENCE).exists())
        self.assertFalse((self.root / '.pmp-bridge.lock').exists())

    def test_append_only_handoff_and_existing_lock(self):
        create_handoff(self.root, self.packet, self.proposal, 'mock')
        newer = read_state(self.root)
        newer_proposal = proposal_template(newer, 'mock-hermes')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            create_handoff(self.root, newer, newer_proposal, 'mock')
        (self.root / '.pmp-bridge.lock').touch()
        with self.assertRaises(FileExistsError):
            create_handoff(self.root, newer, newer_proposal, 'mock')

    def test_traversal_and_linked_paths_are_rejected(self):
        with self.assertRaises(ValueError):
            safe_path(self.root, '../escape')
        with patch.object(Path, 'is_symlink', return_value=True):
            with self.assertRaisesRegex(ValueError, 'linked'):
                safe_path(self.root, 'fixture.json')

    def test_tampered_evidence_cannot_pass_continuation(self):
        create_handoff(self.root, self.packet, self.proposal, 'mock')
        (self.root / 'fixture.json').write_text('{}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            verify(self.root)

    def test_no_history_is_required_by_fresh_process(self):
        create_handoff(self.root, self.packet, self.proposal, 'mock')
        check = subprocess.run([sys.executable, str(HERE / 'continuation.py'), '--root', str(self.root)],
                               capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertEqual(json.loads(check.stdout)['next_action_recovered'], NEXT_ACTION)
        self.assertNotIn('consumer-output', check.stdout)

    def test_real_cli_response_requires_completion_and_no_tools(self):
        response = {'type': 'result', 'exit_code': 0, 'text': json.dumps(self.proposal)}
        self.assertEqual(extract_stream(json.dumps(response))[0], self.proposal)
        with self.assertRaisesRegex(ValueError, 'tool invocation'):
            extract_stream(json.dumps({'type': 'tool_use', 'name': 'terminal'}) + '\n' + json.dumps(response))
        response['exit_code'] = 1
        with self.assertRaisesRegex(ValueError, 'completion'):
            extract_stream(json.dumps(response))

    def test_missing_runtime_fails_without_network_fallback(self):
        with patch('consumer.shutil.which', return_value=None), patch('consumer.subprocess.run') as run:
            with self.assertRaisesRegex(RuntimeError, 'not installed'):
                hermes_consume(self.packet, self.root, 'not-used')
            run.assert_not_called()
        self.assertIn('fallback_providers: []', CONFIG)
        self.assertIn('cli: []', CONFIG)
        self.assertIn('allow_lazy_installs: false', CONFIG)

    def test_minimized_nested_environment_preserves_windows_home_not_secrets(self):
        with patch.dict(os.environ, {'USERPROFILE': r'C:\fixture-user',
                                     'OPENAI_API_KEY': 'test-do-not-inherit'}):
            child_env = clean_env()
        self.assertEqual(child_env.get('USERPROFILE'), r'C:\fixture-user')
        self.assertNotIn('OPENAI_API_KEY', child_env)

    def test_existing_compatibility_fixture_remains_valid(self):
        repo = HERE.parents[1]
        for relative in ('templates/PROJECT_MEMORY.md', 'examples/chatgpt-codex-handoff/fixtures/before/PROJECT_MEMORY.md'):
            self.assertEqual(validate(repo / relative), [])
        for name in INPUT_FILES:
            path = self.root / name
            path.write_bytes(path.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
        self.packet = read_state(self.root)
        self.proposal['expected_memory_sha256'] = self.packet['memory_sha256']
        create_handoff(self.root, self.packet, self.proposal, 'mock')
        self.assertEqual(verify(self.root)['exit_code'], 0)

    def test_runtime_keeps_windows_home_but_not_provider_secrets(self):
        (self.root / 'config.yaml').write_text(CONFIG, encoding='utf-8')
        (self.root / 'auth.json').write_text('{}', encoding='utf-8')
        completion = json.dumps({'type': 'result', 'exit_code': 0,
                                 'text': json.dumps(self.proposal)})
        replies = [subprocess.CompletedProcess([], 0, 'test-runtime', ''),
                   subprocess.CompletedProcess([], 0, completion, '')]
        with patch('consumer.shutil.which', return_value='test-hermes'), \
                patch.dict(os.environ, {'OPENAI_API_KEY': 'test-do-not-inherit'}), \
                patch('consumer.subprocess.run', side_effect=replies) as run:
            hermes_consume(self.packet, self.root, 'test-model')
        child_env = run.call_args.kwargs['env']
        self.assertNotIn('OPENAI_API_KEY', child_env)
        self.assertEqual(child_env['HERMES_HOME'], str(self.root.resolve()))
        if os.name == 'nt' and 'USERPROFILE' in os.environ:
            self.assertEqual(child_env['USERPROFILE'], os.environ['USERPROFILE'])


if __name__ == '__main__':
    unittest.main()
