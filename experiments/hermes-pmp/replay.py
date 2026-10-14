"""One bounded local Git replay. Mock and real Hermes are explicitly distinct."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from adapter import EVIDENCE, HANDOFF, INPUT_FILES, TEST_COMMAND, atomic, clean_env, digest, json_bytes, read, read_state, utc, create_handoff

HERE = Path(__file__).resolve().parent


def run(command: list[str], cwd: Path, input_text: str | None = None, timeout=45):
    result = subprocess.run(command, cwd=cwd, env=clean_env(), input=input_text,
                            capture_output=True, text=True, encoding='utf-8', timeout=timeout)
    if result.returncode:
        raise RuntimeError(f'command failed: {command[0]}: {result.stderr[-2000:]}')
    return result


def git(root: Path, *args: str) -> str:
    return run(['git', '-c', f'safe.directory={root.as_posix()}',
                '-c', 'core.longpaths=true', '-c', 'core.autocrlf=false', *args], root).stdout.strip()


def replay(mode='mock', home=None, model=None, archive=None) -> dict:
    # Retained directory, not TemporaryDirectory: do not delete replay evidence.
    work = Path(tempfile.mkdtemp(prefix='pmp-hermes-'))
    root = work / 'repo'
    root.mkdir()
    for name in INPUT_FILES:
        shutil.copyfile(HERE / 'seed' / name, root / name)
    git(root, 'init', '-b', 'replay')
    git(root, 'config', 'user.name', 'PMP Replay Host')
    git(root, 'config', 'user.email', 'pmp-replay@example.invalid')
    git(root, 'add', '--', *INPUT_FILES)
    git(root, 'commit', '-m', 'baseline: bounded portable fixture')
    baseline = git(root, 'rev-parse', 'HEAD')
    before = subprocess.run([sys.executable, *TEST_COMMAND], cwd=root, env=clean_env(),
                            capture_output=True, text=True, encoding='utf-8', timeout=30)
    if before.returncode == 0 or 'Ran 3 tests' not in before.stderr:
        raise ValueError('answer-free seed must fail its three acceptance tests')
    packet = read_state(root)
    atomic(work / 'input-pmp.json', json_bytes(packet))
    consumer_command = [sys.executable, str(HERE / 'consumer.py'), mode]
    if mode == 'hermes':
        if not home or not model:
            raise ValueError('Hermes requires dedicated --home and explicit --model')
        consumer_command += ['--home', str(home.resolve()), '--model', model]
    consumed = json.loads(run(consumer_command, work, json.dumps(packet), timeout=140).stdout)
    atomic(work / 'consumer-output.json', json_bytes(consumed))
    host_record = create_handoff(root, packet, consumed['proposal'], mode)
    # Input, output and receipt are evidence; they are not alternative canonical state.
    for filename in ('input-pmp.json', 'consumer-output.json'):
        atomic(root / 'evidence' / filename, read(work, filename))
    allowed = ['fixture.json', 'PROJECT_MEMORY.md', EVIDENCE, HANDOFF,
               'evidence/input-pmp.json', 'evidence/consumer-output.json']
    git(root, 'add', '--', *allowed)
    git(root, 'commit', '-m', f'handoff: {mode} candidate with host verification and PMP state')
    subject = git(root, 'rev-parse', 'HEAD')
    changed = git(root, 'diff', '--name-only', baseline, subject).splitlines()
    if sorted(changed) != sorted(allowed):
        raise ValueError('unexpected changed files')
    fresh = work / 'fresh-result'
    run(['git', '-c', 'core.longpaths=true', 'clone', '--no-local', str(root), str(fresh)], work)
    # Fresh process sees only new Git clone. No previous chat, packet or response supplied.
    continuation = json.loads(run([sys.executable, str(HERE / 'continuation.py'),
                                   '--root', str(fresh)], work).stdout)
    report = {
        'timestamp': utc(), 'mode': mode,
        'conclusion': 'PARTIALLY VALIDATED' if mode == 'mock' else 'Hermes runtime completed; fresh Codex model review still required',
        'baseline_commit': baseline, 'handoff_commit': subject,
        'input_memory_sha256': packet['memory_sha256'],
        'input_packet_sha256': digest(read(work, 'input-pmp.json')),
        'host_verification': host_record, 'continuation': continuation,
        'changed_files': changed, 'seed_exit_code': before.returncode,
        'seed_stdout': before.stdout,
        'seed_stderr': before.stderr.replace(str(root), '<replay-root>'),
        'log_redaction': 'Only the absolute temporary seed path is replaced by <replay-root>.',
        'core_version': '0.2.2', 'incremental_paid_cost_usd': 0 if mode == 'mock' else None,
        'claims': {'model_identity_certified': False, 'session_freshness_certified': False,
                   'real_hermes_executed': mode == 'hermes', 'fresh_codex_executed': False},
    }
    bundle = work / 'replay.bundle'
    git(root, 'bundle', 'create', str(bundle), '--all')
    report['bundle_sha256'] = digest(bundle.read_bytes())
    atomic(work / 'replay-report.json', json_bytes(report))
    if archive:
        archive.mkdir(parents=True, exist_ok=True)
        for name in ('replay-report.json', 'replay.bundle'):
            destination = archive / name
            if destination.exists():
                raise ValueError('archive already exists; do not overwrite evidence')
            shutil.copyfile(work / name, destination)
    return {'run_directory': str(work), 'fresh_repository': str(fresh), 'report': report}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('mock', 'hermes'), default='mock')
    parser.add_argument('--home', type=Path)
    parser.add_argument('--model')
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(replay(args.mode, args.home, args.model, args.archive), indent=2))
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as error:
        print(f'REPLAY FAILED: {error}', file=sys.stderr)
        raise SystemExit(1)
