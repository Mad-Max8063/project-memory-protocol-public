"""Regression tests for Windows LF/CRLF portability in PMP evidence and seed files."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'experiments' / 'hermes-pmp'
sys_path = str(HERE)
import sys
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

import verify_chain as chain


class LineEndingsRegressionTests(unittest.TestCase):
    def test_gitattributes_configuration_exists_and_enforces_lf(self):
        gitattributes = ROOT / '.gitattributes'
        self.assertTrue(gitattributes.is_file(), '.gitattributes file must exist at repository root')
        content = gitattributes.read_text(encoding='utf-8')
        self.assertIn('* text=auto eol=lf', content, 'Must enforce eol=lf for text files')
        self.assertIn('*.bundle binary', content, 'Must declare bundles as binary')

    def test_evidence_json_files_have_no_crlf(self):
        evidence_dir = HERE / 'evidence'
        for json_path in evidence_dir.rglob('*.json'):
            raw = json_path.read_bytes()
            self.assertNotIn(b'\r\n', raw, f'Evidence JSON file must not contain CRLF: {json_path.relative_to(ROOT)}')

    def test_seed_files_have_no_crlf(self):
        for seed_dir in (HERE / 'seed', HERE / 'claude-seed'):
            if seed_dir.is_dir():
                for seed_file in seed_dir.rglob('*'):
                    if seed_file.is_file() and not seed_file.name.endswith('.pyc'):
                        raw = seed_file.read_bytes()
                        self.assertNotIn(b'\r\n', raw, f'Seed file must not contain CRLF: {seed_file.relative_to(ROOT)}')

    def test_crlf_injection_fails_digest_before_subprocess(self):
        with tempfile.TemporaryDirectory(prefix='pmp-crlf-test-') as directory:
            target = Path(directory) / 'evidence'
            shutil.copytree(HERE / 'evidence', target)
            report = target / 'live-replay-20261006' / 'replay-report.json'
            original = report.read_bytes()
            crlf_bytes = original.replace(b'\n', b'\r\n')
            report.write_bytes(crlf_bytes)
            with patch('subprocess.run', side_effect=AssertionError('must reject before subprocess')):
                with self.assertRaises(ValueError) as ctx:
                    chain.verify_chain(target)
                self.assertIn('archive digest mismatch', str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
