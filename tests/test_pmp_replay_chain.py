"""Offline acceptance for the useful archive verifier; no provider calls."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).absolute().parents[1] / 'experiments/hermes-pmp'
sys.path.insert(0, str(HERE))
import verify_chain as chain
from adapter import clean_env, digest

EVIDENCE = HERE / 'evidence'
CLAUDE = EVIDENCE / 'claude-continuation-20261006'


class ChainAcceptanceTests(unittest.TestCase):
    def reports(self):
        return tuple(json.loads(path.read_text(encoding='utf-8')) for path in (
            EVIDENCE / 'live-replay-20261006/replay-report.json',
            CLAUDE / 'claude-report.json', CLAUDE / 'fresh-codex.json'))

    def clone_result(self, directory):
        root = Path(directory) / 'result'
        subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.hooksPath=' + directory,
                        'clone', str(CLAUDE / 'fresh-codex.bundle'), str(root)],
                       env=clean_env(), check=True, capture_output=True, timeout=30)
        return root

    def test_real_archive_chain_and_readonly_boundary(self):
        before = {str(p): digest(p.read_bytes()) for p in EVIDENCE.rglob('*') if p.is_file()}
        result = chain.verify_chain(EVIDENCE)
        self.assertIs(result['verified'], True)
        self.assertEqual(result['historical_inputs'], 14)
        self.assertEqual(result['acceptance_tests'], 6)
        self.assertEqual(len(result['bundle_sha256']), 3)
        self.assertTrue(result['next_action'].strip())
        self.assertIs(result['model_identity_certified'], False)
        self.assertIs(result['session_freshness_certified'], False)
        after = {str(p): digest(p.read_bytes()) for p in EVIDENCE.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_corrupted_bundle_rejected_before_git(self):
        with tempfile.TemporaryDirectory(prefix='pmp-chain-corrupt-') as directory:
            target = Path(directory) / 'evidence'
            shutil.copytree(EVIDENCE, target)
            bundle = target / 'claude-continuation-20261006/fresh-codex.bundle'
            bundle.write_bytes(bundle.read_bytes() + b'corruption')
            with patch('subprocess.run', side_effect=AssertionError('must reject before subprocess')):
                with self.assertRaises(ValueError):
                    chain.verify_chain(target)

    def test_modified_report_rejected_before_git(self):
        with tempfile.TemporaryDirectory(prefix='pmp-chain-report-') as directory:
            target = Path(directory) / 'evidence'
            shutil.copytree(EVIDENCE, target)
            report = target / 'claude-continuation-20261006/fresh-codex.json'
            data = json.loads(report.read_text(encoding='utf-8'))
            data['tests_passed'] = 600
            report.write_text(json.dumps(data), encoding='utf-8')
            with patch('subprocess.run', side_effect=AssertionError('must reject before subprocess')):
                with self.assertRaises(ValueError):
                    chain.verify_chain(target)

    def test_semantic_verifier_rejects_changed_result_and_missing_handoff(self):
        with tempfile.TemporaryDirectory(prefix='pmp-chain-semantic-') as directory:
            root = self.clone_result(directory)
            reports = self.reports()
            self.assertIs(chain.verify_repository(root, *reports)['verified'], True)
            labels = root / 'labels.txt'
            original = labels.read_bytes()
            labels.write_bytes(b'pmp=Wrong result\nhandoff=Evidence chain\n')
            with self.assertRaises(ValueError):
                chain.verify_repository(root, *reports)
            labels.write_bytes(original)
            (root / '.project-memory/sessions/claude-handoff.md').unlink()
            with self.assertRaises(ValueError):
                chain.verify_repository(root, *reports)

    def test_missing_archive_and_linked_inputs_rejected(self):
        with tempfile.TemporaryDirectory(prefix='pmp-chain-missing-') as directory:
            with self.assertRaises((ValueError, OSError)):
                chain.verify_chain(Path(directory))
        with patch.object(Path, 'is_symlink', return_value=True):
            with self.assertRaises(ValueError):
                chain.verify_chain(EVIDENCE)
        # Only an ancestor is linked; the root and file leaves are plain.
        for method in ('is_symlink', 'is_junction'):
            with self.subTest(method=method), patch.object(Path, method, autospec=True,
                    side_effect=lambda path: path == EVIDENCE.parent):
                with self.assertRaisesRegex(ValueError, 'ancestor'):
                    chain.verify_chain(EVIDENCE)

    def test_ignored_import_payload_rejected_without_execution(self):
        with tempfile.TemporaryDirectory(prefix='pmp-chain-ignored-') as directory:
            root = self.clone_result(directory)
            (root / '.git/info/exclude').write_text('json.py\n', encoding='utf-8')
            (root / 'json.py').write_text(
                "open('ignored-code-executed.marker', 'w').write('executed')\n"
                "raise RuntimeError('unexpected ignored module')\n", encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'ignored result files'):
                chain.verify_repository(root, *self.reports())
            self.assertFalse((root / 'ignored-code-executed.marker').exists())

    def test_cli_json_usage_and_failure_exit_codes(self):
        command = [sys.executable, '-B', str(HERE / 'verify_chain.py')]
        result = subprocess.run([*command, '--json'], cwd=HERE.parents[1], env=clean_env(),
                                capture_output=True, text=True, encoding='utf-8', timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['verified'])
        bad_usage = subprocess.run([*command, '--unknown'], env=clean_env(), capture_output=True, timeout=15)
        self.assertEqual(bad_usage.returncode, 2)
        with tempfile.TemporaryDirectory(prefix='pmp-chain-cli-') as directory:
            missing = subprocess.run([*command, '--evidence-root', directory, '--json'],
                                     env=clean_env(), capture_output=True, timeout=15)
            self.assertEqual(missing.returncode, 1)


if __name__ == '__main__':
    unittest.main()
