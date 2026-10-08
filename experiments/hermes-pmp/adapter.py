"""Non-normative file bridge; unchanged PMP Markdown remains canonical."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

CORE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CORE / 'scripts'))
from markdown_sections import parse_sections
from validate_memory import validate
from validate_release_candidate import SECRET_ASSIGNMENT

INPUT_FILES = ('AGENTS.md', 'PROJECT_MEMORY.md', 'TASK.md', 'fixture.json', 'test_fixture.py')
TEST_COMMAND = ('-I', '-m', 'unittest', 'discover', '-s', '.', '-p', 'test_fixture.py', '-v')
NEXT_ACTION = ('Codex: independently rerun the three acceptance tests, verify evidence '
               'hashes and record a continuation receipt; do not expand scope.')
HANDOFF = '.project-memory/sessions/hermes-handoff.md'
EVIDENCE = 'evidence/host-verification.json'
MAX_BYTES = 65536


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_path(root: Path, relative: str) -> Path:
    """Fixed paths only, reject links/reparse points in every component."""
    root = root.absolute()
    if root.is_symlink() or root.is_junction():
        raise ValueError('linked root rejected')
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('path escapes root')
    path = root
    for part in rel.parts:
        path = path / part
        if path.is_symlink() or path.is_junction():
            raise ValueError('linked path rejected')
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('path escapes root')
    return path


def read(root: Path, relative: str) -> bytes:
    path = safe_path(root, relative)
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('input too large')
    data = path.read_bytes()
    data.decode('utf-8')
    return data


def atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.pmp-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def trusted_seed(root: Path, name: str) -> bool:
    # Git may checkout LF as CRLF on Windows. Trust content, hash actual bytes separately.
    actual = read(root, name).decode('utf-8').replace('\r\n', '\n')
    expected = (Path(__file__).parent / 'seed' / name).read_bytes().decode('utf-8').replace('\r\n', '\n')
    return actual == expected


def read_state(root: Path) -> dict:
    raw = {name: read(root, name) for name in INPUT_FILES}
    if errors := validate(safe_path(root, 'PROJECT_MEMORY.md')):
        raise ValueError('; '.join(errors))
    memory = raw['PROJECT_MEMORY.md'].decode('utf-8')
    if '> Protocol: PMP `0.2.2`' not in memory:
        raise ValueError('this experiment requires explicitly declared PMP 0.2.2')
    sections = {section.name: section.body for section in parse_sections(memory)}
    previous = None
    handoff_path = safe_path(root, HANDOFF)
    if handoff_path.exists():
        previous = read(root, HANDOFF).decode('utf-8')
    actor_match = re.search(r'^- Last actor: (.+)$', sections['Identity'], re.M)
    project_match = re.search(r'^- Project: (.+)$', sections['Identity'], re.M)
    return {
        'protocol': 'PMP 0.2.2', 'canonical_path': 'PROJECT_MEMORY.md',
        'project_identifier': project_match[1] if project_match else sections['Identity'],
        'current_actor': actor_match[1] if actor_match else None,
        'memory_sha256': digest(raw['PROJECT_MEMORY.md']),
        'canonical_memory': memory, 'sections': sections,
        'previous_handoff': previous,
        'input_sha256': {name: digest(data) for name, data in raw.items()},
        'task': raw['TASK.md'].decode('utf-8'),
        'instructions': raw['AGENTS.md'].decode('utf-8'),
        'fixture': json.loads(raw['fixture.json']),
        # Core evidence references stay verbatim. This bridge resolves only its fixed files.
        'relevant_evidence': {'test_definition': raw['test_fixture.py'].decode('utf-8')},
    }


def validate_proposal(packet: dict, proposal: dict, mode: str) -> None:
    fields = {'expected_memory_sha256', 'actor', 'action_attempted', 'result', 'fixture',
              'decisions_proposed', 'unresolved_issues', 'next_action', 'intended_next_actor'}
    if type(proposal) is not dict or set(proposal) != fields:
        raise ValueError('unexpected proposal fields')
    actor = 'mock-hermes' if mode == 'mock' else 'Hermes'
    if proposal['actor'] != actor or proposal['intended_next_actor'] != 'Codex':
        raise ValueError('unexpected logical actor')
    if proposal['expected_memory_sha256'] != packet['memory_sha256']:
        raise ValueError('stale memory digest')
    if proposal['next_action'] != NEXT_ACTION:
        raise ValueError('next action differs from bounded task')
    if proposal['decisions_proposed'] != [] or proposal['unresolved_issues'] != []:
        raise ValueError('unresolved issues/decision changes require human review')
    for name in ('action_attempted', 'result'):
        value = proposal[name]
        if not isinstance(value, str) or not value.strip() or len(value) > 500 or '\n' in value:
            raise ValueError('invalid narrative field')
    expected = copy.deepcopy(packet['fixture'])
    for item in expected['items']:
        item['label'] = ' '.join(item['label'].split())
    if json.dumps(proposal['fixture'], sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError('proposal violates fixture scope')
    if SECRET_ASSIGNMENT.search(json.dumps(proposal)):
        raise ValueError('possible secret assignment')


def create_handoff(root: Path, packet: dict, proposal: dict, mode: str) -> dict:
    """Host verifies, then writes fixed artifacts. Git publication is caller-owned."""
    if mode not in ('mock', 'hermes'):
        raise ValueError('unknown execution mode')
    lock = safe_path(root, '.pmp-bridge.lock')
    lock.open('x').close()
    try:
            current = read_state(root)
            if current['input_sha256'] != packet['input_sha256'] or current != packet:
                raise ValueError('input changed since export')
            validate_proposal(packet, proposal, mode)
            for name in ('AGENTS.md', 'TASK.md', 'test_fixture.py'):
                if not trusted_seed(root, name):
                    raise ValueError('untrusted acceptance code or task')
            outputs = (EVIDENCE, HANDOFF)
            if any(safe_path(root, name).exists() for name in outputs):
                raise ValueError('handoff already exists; append-only history')
            if not trusted_seed(root, 'PROJECT_MEMORY.md'):
                raise ValueError('Writer is limited to this trusted fixture baseline')
            for name in outputs:
                safe_path(root, name)  # fail before changing the fixture
            old_fixture = read(root, 'fixture.json')
            old_memory = read(root, 'PROJECT_MEMORY.md')
            changed = []
            try:
                atomic(safe_path(root, 'fixture.json'), json_bytes(proposal['fixture']))
                check = subprocess.run([sys.executable, *TEST_COMMAND], cwd=root,
                                       capture_output=True, text=True, encoding='utf-8',
                                       timeout=30, check=False, env=clean_env())
                if check.returncode or 'Ran 3 tests' not in check.stderr:
                    raise ValueError('host acceptance tests failed: ' + check.stderr[-1000:])
                record = {
                    'mode': mode, 'logical_actor': proposal['actor'],
                    'observer': 'PMP bridge host', 'timestamp': utc(),
                    'input_sha256': packet['input_sha256'],
                    'fixture_sha256': digest(read(root, 'fixture.json')),
                    'command': ['python', *TEST_COMMAND], 'exit_code': check.returncode,
                    'stdout': check.stdout, 'stderr': check.stderr,
                    'tests_executed_by_model': False,
                    'model_claim': proposal['result'],
                }
                session = (
                    '# Session — bounded Hermes fixture handoff\n\n'
                    f'- Date: {record["timestamp"]}\n- Actor: {proposal["actor"]} (logical label)\n'
                    '- Objective: normalize fixture whitespace only\n'
                    f'- Start memory SHA-256: {packet["memory_sha256"]}\n'
                    '- End revision: supplied by replay Git receipt\n\n'
                    '## Changes made\n\n- fixture.json only; labels normalized, IDs/order preserved.\n'
                    f'- Action attempted (actor report): {proposal["action_attempted"]}\n'
                    f'- Result (actor report, not proof): {proposal["result"]}\n\n'
                    '## Verification\n\n'
                    f'- Host executed `python {" ".join(TEST_COMMAND)}`: three tests passed.\n'
                    f'- Evidence: {EVIDENCE}\n- Fixture SHA-256: {record["fixture_sha256"]}\n'
                    '- Status: [VERIFIED] host acceptance gate; no independent model identity proof.\n\n'
                    '## Decisions and constraints\n\n- No decision proposed/taken; active decisions preserved.\n'
                    '- Intended next actor: Codex. Input memory digest checked before writes.\n\n'
                    '## Risks and blockers\n\n'
                    f'- {"Mock only; real Hermes remains unverified." if mode == "mock" else "Hermes runtime evidence must be reviewed separately."}\n'
                    '- No unresolved fixture issue; no proof of hidden session freshness.\n\n'
                    '## Explicitly not done\n\n- No model terminal/file tools, Core change, purchases or deploy.\n'
                    '- Test commands were host-owned, not executed by the model.\n\n'
                    f'## Next action\n\n{NEXT_ACTION}\n\n## Evidence\n\n- {EVIDENCE}\n'
                )
                sections = dict(packet['sections'])
                sections['Identity'] = re.sub(r'^- Last actor: .+$',
                    f'- Last actor: {proposal["actor"]} (logical participant)',
                    sections['Identity'], flags=re.M)
                sections['Current state'] = (
                    f'- [VERIFIED] Host normalized-fixture acceptance: three tests passed; {EVIDENCE}.\n'
                    f'- [DOCUMENTED] Producer mode: {mode}; no model identity or freshness claim.')
                sections['Next action'] = NEXT_ACTION
                sections['Evidence'] += f'\n- {EVIDENCE}\n- {HANDOFF}'
                memory = '# Portable fixture — canonical project memory\n\n> Protocol: PMP `0.2.2`\n> Canonical path: `PROJECT_MEMORY.md`\n\n'
                memory += '\n\n'.join(f'## {name}\n\n{body}' for name, body in sections.items()) + '\n'
                atomic(safe_path(root, EVIDENCE), json_bytes(record))
                changed.append(EVIDENCE)
                atomic(safe_path(root, HANDOFF), session.encode('utf-8'))
                changed.append(HANDOFF)
                atomic(safe_path(root, 'PROJECT_MEMORY.md'), memory.encode('utf-8'))
                if errors := validate(safe_path(root, 'PROJECT_MEMORY.md')):
                    raise ValueError('; '.join(errors))
                return record
            except BaseException:
                atomic(safe_path(root, 'fixture.json'), old_fixture)
                atomic(safe_path(root, 'PROJECT_MEMORY.md'), old_memory)
                for name in changed:
                    safe_path(root, name).unlink()
                raise
    finally:
        lock.unlink()


def clean_env() -> dict:
    # Keep the existing Windows home path through nested replay subprocesses:
    # the consumer needs it for Path.home() even with its dedicated HERMES_HOME.
    allowed = ('PATH', 'SystemRoot', 'WINDIR', 'TEMP', 'TMP', 'PATHEXT', 'USERPROFILE',
               'LANG', 'LC_ALL', 'COMSPEC')
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    env.update(PYTHONUTF8='1', PYTHONIOENCODING='utf-8', GIT_CONFIG_NOSYSTEM='1',
               GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT='0')
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('read', 'handoff'))
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--packet', type=Path)
    parser.add_argument('--proposal', type=Path)
    parser.add_argument('--mode', choices=('mock', 'hermes'), default='mock')
    args = parser.parse_args()
    try:
        if args.operation == 'read':
            value = read_state(args.root)
        else:
            if not args.packet or not args.proposal:
                parser.error('handoff requires --packet and --proposal')
            if max(args.packet.stat().st_size, args.proposal.stat().st_size) > MAX_BYTES:
                raise ValueError('input too large')
            value = create_handoff(args.root,
                json.loads(args.packet.read_text(encoding='utf-8')),
                json.loads(args.proposal.read_text(encoding='utf-8')), args.mode)
        print(json.dumps(value, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f'BRIDGE REJECTED: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
