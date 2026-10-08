"""Independently clone/hash/check saved evidence; no model, no chat history."""
import json
from pathlib import Path
import tempfile

from adapter import EVIDENCE, HANDOFF, INPUT_FILES, TEST_COMMAND, digest, read, validate
from continuation import verify
from replay import git, run
import sys


def verify_archive(evidence: Path) -> dict:
    report = json.loads((evidence / 'replay-report.json').read_text(encoding='utf-8'))
    bundle = (evidence / 'replay.bundle').resolve()
    if digest(bundle.read_bytes()) != report['bundle_sha256']:
        raise ValueError('replay bundle digest mismatch')
    work = Path(tempfile.mkdtemp(prefix='pmp-hermes-archive-'))
    root = work / 'replay'
    run(['git', 'clone', str(bundle), str(root)], work)
    if git(root, 'rev-parse', 'HEAD') != report['handoff_commit']:
        raise ValueError('subject commit mismatch')
    baseline = report['baseline_commit']
    if git(root, 'rev-parse', 'HEAD^') != baseline:
        raise ValueError('baseline lineage mismatch')
    changed = git(root, 'diff', '--name-only', baseline, 'HEAD').splitlines()
    if changed != report['changed_files']:
        raise ValueError('change scope differs from report')
    packet = json.loads(read(root, 'evidence/input-pmp.json'))
    if digest(read(root, 'evidence/input-pmp.json')) != report['input_packet_sha256']:
        raise ValueError('packet digest mismatch')
    observed = json.loads(read(root, EVIDENCE))
    if observed != report['host_verification']:
        raise ValueError('host evidence/report mismatch')
    for name in INPUT_FILES:
        # Git show bytes: do not universal-newline-normalize historical file hashes.
        import subprocess
        from adapter import clean_env
        blob = subprocess.check_output(['git', '-c', f'safe.directory={root.as_posix()}',
                                        'show', f'{baseline}:{name}'], cwd=root,
                                       env=clean_env(), timeout=15)
        if digest(blob) != packet['input_sha256'][name]:
            raise ValueError('baseline input mismatch: ' + name)
    continuation = verify(root)
    for key in ('canonical_memory_sha256', 'handoff_sha256', 'evidence_sha256'):
        if continuation[key] != report['continuation'][key]:
            raise ValueError('fresh verifier differs from persisted evidence')
    result = {'mock_replay_verified': report['mode'] == 'mock', 'host_tests': 3,
              'real_hermes_verified': False, 'fresh_codex_bundle_verified': False}
    manifest = evidence / 'fresh-codex.json'
    if manifest.exists():
        fresh = json.loads(manifest.read_text(encoding='utf-8'))
        fresh_bundle = (evidence / fresh['bundle_file']).resolve()
        if not fresh_bundle.is_relative_to(evidence.resolve()):
            raise ValueError('bundle path escape')
        if digest(fresh_bundle.read_bytes()) != fresh['bundle_sha256']:
            raise ValueError('Codex bundle mismatch')
        clone = work / 'codex'
        run(['git', 'clone', str(fresh_bundle), str(clone)], work)
        if git(clone, 'rev-parse', 'HEAD') != fresh['continuation_commit']:
            raise ValueError('continuation revision mismatch')
        if git(clone, 'rev-parse', 'HEAD^') != report['handoff_commit']:
            raise ValueError('continuation parent mismatch')
        diff = git(clone, 'diff', '--name-only', 'HEAD^', 'HEAD').splitlines()
        if sorted(diff) != ['.project-memory/sessions/codex-continuation.md', 'PROJECT_MEMORY.md']:
            raise ValueError('continuation scope drift')
        if validate(clone / 'PROJECT_MEMORY.md'):
            raise ValueError('continued memory invalid')
        tests = run([sys.executable, *TEST_COMMAND], clone)
        if 'Ran 3 tests' not in tests.stderr:
            raise ValueError('unexpected continued acceptance test count')
        if not (clone / fresh['receipt']).is_file():
            raise ValueError('Codex receipt missing')
        result['fresh_codex_bundle_verified'] = True
        result['next_action'] = 'Max: review completed bounded continuation receipt.'
    return result


if __name__ == '__main__':
    print(json.dumps(verify_archive(Path(__file__).parent / 'evidence'), indent=2))
