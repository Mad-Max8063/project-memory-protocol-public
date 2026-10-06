"""Fresh process verifier; reads only the result repo, never consumer input/history."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from adapter import EVIDENCE, HANDOFF, NEXT_ACTION, TEST_COMMAND, clean_env, digest, read, read_state, trusted_seed


def verify(root: Path) -> dict:
    state = read_state(root)
    record = json.loads(read(root, EVIDENCE))
    if state['sections']['Next action'] != NEXT_ACTION:
        raise ValueError('next action not preserved')
    if not state['previous_handoff'] or EVIDENCE not in state['previous_handoff']:
        raise ValueError('handoff evidence missing')
    if record['exit_code'] != 0 or record['tests_executed_by_model'] is not False:
        raise ValueError('unsupported verification claim')
    for name in ('AGENTS.md', 'TASK.md', 'test_fixture.py'):
        if digest(read(root, name)) != record['input_sha256'][name]:
            raise ValueError('instruction/test boundary changed')
        if not trusted_seed(root, name):
            raise ValueError('untrusted continuation code/task')
    if digest(read(root, 'fixture.json')) != record['fixture_sha256']:
        raise ValueError('fixture evidence digest mismatch')
    tests = subprocess.run([sys.executable, *TEST_COMMAND], cwd=root, env=clean_env(),
                           capture_output=True, text=True, encoding='utf-8', timeout=30)
    if tests.returncode or 'Ran 3 tests' not in tests.stderr:
        raise ValueError('continuation acceptance tests failed')
    return {'verifier': 'fresh Python process, NOT a Codex model session',
            'mode': record['mode'], 'logical_previous_actor': record['logical_actor'],
            'canonical_memory_sha256': state['memory_sha256'],
            'next_action_recovered': state['sections']['Next action'],
            'handoff_sha256': digest(read(root, HANDOFF)),
            'evidence_sha256': digest(read(root, EVIDENCE)),
            'command': ['python', *TEST_COMMAND], 'exit_code': tests.returncode,
            'stdout': tests.stdout, 'stderr': tests.stderr}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root), indent=2))
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f'CONTINUATION REJECTED: {error}', file=sys.stderr)
        raise SystemExit(1)
