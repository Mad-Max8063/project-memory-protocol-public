"""Bounded Claude continuation of the archived real Hermes handoff; no Core changes."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from adapter import atomic, clean_env, digest, json_bytes, parse_sections, read, safe_path, utc, validate
from continuation import verify as verify_hermes
from replay import git, run

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'evidence/live-replay-20261006/replay.bundle'
SOURCE_SHA256 = 'b729b7f2220f5e639ad9e43f205314c45055d69eab966689b0438f178398de17'
HERMES_HEAD = 'd2e225b61857be0e0b79c5d28116ae6a9800f7c7'
NEXT = 'Codex: independently run all six acceptance tests, verify Claude and Hermes evidence hashes, and record a continuation receipt; do not expand scope.'
FILES = ('AGENTS.md', 'PROJECT_MEMORY.md', 'TASK.md', 'CLAUDE_TASK.md', 'fixture.json',
         'test_fixture.py', 'test_manifest.py', 'evidence/host-verification.json',
         '.project-memory/sessions/hermes-handoff.md')
TESTS = ('-I', '-m', 'unittest', 'discover', '-s', '.', '-p', 'test_*.py', '-v')
EVIDENCE = 'evidence/claude-host-verification.json'
HANDOFF = '.project-memory/sessions/claude-handoff.md'
TASK = '''# Authorized Claude continuation

The human authorizes Claude to continue from the completed Hermes task.
The earlier TASK.md describes that completed task; do not repeat it.
Read canonical PROJECT_MEMORY.md, fixture.json and the linked Hermes evidence.
Derive labels.txt: one id=label line per fixture item, in the existing order,
UTF-8 with LF and one final newline. Preserve fixture, previous decisions and evidence.
Return a JSON proposal only. The host writes fixed paths and executes the six
trusted acceptance tests. Do not claim that you ran tools/tests yourself.
Propose no decision changes. After host verification, hand off to Codex:
''' + NEXT + '\n'


def set_memory(root: Path, changes: dict) -> None:
    sections = {s.name: s.body for s in parse_sections(read(root, 'PROJECT_MEMORY.md').decode())}
    sections.update(changes)
    content = '# Portable fixture — canonical project memory\n\n> Protocol: PMP `0.2.2`\n> Canonical path: `PROJECT_MEMORY.md`\n\n'
    content += '\n\n'.join(f'## {key}\n\n{value}' for key, value in sections.items()) + '\n'
    atomic(root / 'PROJECT_MEMORY.md', content.encode())
    if errors := validate(root / 'PROJECT_MEMORY.md'):
        raise ValueError('; '.join(errors))


def packet(root: Path) -> dict:
    files = {name: read(root, name).decode('utf-8') for name in FILES}
    return {'source_hermes_commit': HERMES_HEAD, 'files': files,
            'input_sha256': {name: digest(value.encode()) for name, value in files.items()}}


def prepare(work: Path) -> dict:
    if digest(SOURCE.read_bytes()) != SOURCE_SHA256:
        raise ValueError('archived Hermes bundle digest mismatch')
    work.mkdir(parents=True, exist_ok=False)
    root = work / 'repo'
    run(['git', '-c', 'core.autocrlf=false', 'clone', str(SOURCE), str(root)], work)
    if git(root, 'rev-parse', 'HEAD') != HERMES_HEAD:
        raise ValueError('unexpected Hermes handoff revision')
    previous = verify_hermes(root)
    git(root, 'config', 'user.name', 'PMP Replay Host')
    git(root, 'config', 'user.email', 'pmp-replay@example.invalid')
    git(root, 'switch', '-c', 'claude-continuation')
    atomic(root / 'AGENTS.md', read(root, 'AGENTS.md') +
           b'\nAuthorized follow-up: CLAUDE_TASK.md supersedes the completed fixture-only\n'
           b'task. Claude proposes labels.txt only; the host records evidence and PMP.\n')
    atomic(root / 'CLAUDE_TASK.md', TASK.encode())
    atomic(root / 'test_manifest.py', (HERE / 'claude-seed/test_manifest.py').read_bytes())
    sections = {s.name: s.body for s in parse_sections(read(root, 'PROJECT_MEMORY.md').decode())}
    set_memory(root, {
        'Identity': sections['Identity'].replace('Hermes (logical participant)', 'Codex dispatch host (logical participant)'),
        'Constraints': sections['Constraints'] + '\n- Authorized follow-up: Claude may propose labels.txt via the host; all previous fixture/evidence remains unchanged.',
        'Priorities': '- Continue the verified Hermes result with the authorized derived-label manifest task.',
        'Next action': 'Claude: read CLAUDE_TASK.md, recover the verified Hermes result from PMP, and propose labels.txt. The host verifies and hands off to Codex.',
        'Evidence': sections['Evidence'] + '\n- CLAUDE_TASK.md\n- test_manifest.py (trusted acceptance definition, not a passing run)'
    })
    git(root, 'add', '--', 'AGENTS.md', 'CLAUDE_TASK.md', 'test_manifest.py', 'PROJECT_MEMORY.md')
    git(root, 'commit', '-m', 'dispatch: authorize bounded Claude continuation of Hermes result')
    data = packet(root)
    atomic(work / 'input-pmp.json', json_bytes(data))
    atomic(work / 'dispatch.json', json_bytes({'timestamp': utc(), 'dispatch_commit': git(root, 'rev-parse', 'HEAD'),
           'source_bundle_sha256': SOURCE_SHA256, 'prior_host_check': previous}))
    return {'work': str(work), 'dispatch_commit': git(root, 'rev-parse', 'HEAD')}


def claude_env() -> dict:
    env = clean_env()
    for key in ('APPDATA', 'LOCALAPPDATA'):
        if key in os.environ:
            env[key] = os.environ[key]
    return env


def extract(raw: str) -> dict:
    events = [json.loads(line) for line in raw.splitlines() if line.strip()]
    initial = [e for e in events if e.get('type') == 'system' and e.get('subtype') == 'init']
    results = [e for e in events if e.get('type') == 'result']
    if len(initial) != 1 or len(results) != 1 or initial[0].get('tools') != []:
        raise ValueError('missing runtime receipt or unexpected enabled tools')
    for event in events:
        for block in event.get('message', {}).get('content', []):
            if isinstance(block, dict) and block.get('type') in ('tool_use', 'tool_result'):
                raise ValueError('unexpected model tool event')
    result = results[0]
    if result.get('is_error') or result.get('subtype') != 'success':
        raise ValueError('Claude did not complete successfully')
    text = result.get('result', '').strip()
    if text.startswith('```json\n') and text.endswith('\n```'):
        text = text[8:-4]
    proposal = json.loads(text)
    return {'proposal': proposal, 'runtime': {
        'model_reported': initial[0].get('model'), 'tools': [],
        'version_reported': initial[0].get('claude_code_version'),
        'session_id': initial[0].get('session_id'),
        'num_turns': result.get('num_turns'), 'usage': result.get('usage'),
        'model_usage': result.get('modelUsage'),
        'estimated_api_equivalent_usd_not_a_bill': result.get('total_cost_usd'),
        'exit_code': 0, 'identity_or_freshness_certified': False}}


def consume(work: Path, executable: Path, retry_once: bool = False) -> dict:
    env = claude_env()
    version = subprocess.run([str(executable), '--version'], env=env, cwd=work,
                             capture_output=True, text=True, timeout=15)
    if version.returncode or version.stdout.strip() != '2.1.274 (Claude Code)':
        raise ValueError('recheck restriction semantics before using a different Claude CLI version')
    # Attempt markers bound invocations: one initial call and one explicit retry.
    if retry_once and (not (work / 'claude-attempt.json').exists() or (work / 'claude-output.json').exists()):
        raise ValueError('retry requires a previous attempt with no accepted output')
    attempt = 'claude-retry.json' if retry_once else 'claude-attempt.json'
    with (work / attempt).open('x', encoding='utf-8') as stream:
        json.dump({'timestamp': utc(), 'max_turns': 1, 'model_alias': 'sonnet'}, stream)
    auth = subprocess.run([str(executable), 'auth', 'status', '--json'], env=env,
                          cwd=work, capture_output=True, text=True, timeout=30)
    status = json.loads(auth.stdout)
    if auth.returncode or not status.get('loggedIn') or status.get('authMethod') != 'claude.ai':
        raise ValueError('existing Claude subscription login required; no API fallback')
    fields = {'actor': 'Claude', 'previous_actor': 'Hermes',
              'expected_memory_sha256': '<digest from packet>', 'labels_text': '<derived text>',
              'action_attempted': '<short description>', 'result': '<proposal, not executed tests>',
              'tests_executed_by_model': False, 'decisions_proposed': [], 'unresolved_issues': [],
              'intended_next_actor': 'Codex', 'next_action': NEXT}
    prompt = ('You are the Claude participant in a bounded PMP handoff. Use only the repository packet below. '
              'Follow canonical PROJECT_MEMORY.md and CLAUDE_TASK.md. Do not use tools. '
              'Return exactly one JSON object with these fields; no markdown: ' + json.dumps(fields) +
              '\nRepository packet:\n' + read(work, 'input-pmp.json').decode())
    cmd = [str(executable), '--print', '--safe-mode', '--restricted', '--setting-sources', '',
           '--settings', '{"disableAllHooks":true,"autoMemoryEnabled":false}',
           '--tools', '', '--strict-mcp-config', '--disable-slash-commands', '--no-chrome',
           '--no-session-persistence', '--permission-mode', 'dontAsk', '--model', 'sonnet',
           '--max-turns', '1', '--max-budget-usd', '0.50', '--output-format', 'stream-json', '--verbose',
           '--system-prompt', 'Consume only the supplied PMP repository packet. Produce the bounded JSON proposal. No tools or conversational history.']
    result = subprocess.run(cmd, input=prompt, cwd=work, env=env, capture_output=True,
                            text=True, encoding='utf-8', timeout=180)
    if result.returncode:
        # Retain bounded diagnostics, redacting URLs, email addresses, long IDs
        # and credential-shaped strings. Never retain auth-status account fields.
        detail = result.stderr + '\n' + result.stdout
        detail = re.sub(r'https?://\S+|[\w.+-]+@[\w.-]+|[A-Za-z0-9_./+=-]{24,}', '<redacted>', detail)
        detail = re.sub(r'(?i)(bearer|token|secret|api.key)\s*[:=]\s*\S+', r'\1=<redacted>', detail)
        failure = {'timestamp': utc(), 'exit_code': result.returncode,
                   'diagnostic_redacted': detail[-2500:], 'provider_request_count': 'not established'}
        atomic(work / ('claude-retry-failure.json' if retry_once else 'claude-failure.json'), json_bytes(failure))
        raise ValueError(json.dumps(failure))
    received = extract(result.stdout)
    received['runtime']['auth_method'] = status['authMethod']
    received['runtime']['prompt_sha256'] = digest(prompt.encode())
    atomic(work / 'claude-output.json', json_bytes(received))
    return received['runtime']


def validate_candidate(data: dict, proposal: dict) -> str:
    fields = {'actor', 'previous_actor', 'expected_memory_sha256', 'labels_text', 'action_attempted',
              'result', 'tests_executed_by_model', 'decisions_proposed', 'unresolved_issues', 'intended_next_actor', 'next_action'}
    if not isinstance(proposal, dict) or set(proposal) != fields:
        raise ValueError('invalid proposal schema')
    if (proposal['actor'], proposal['previous_actor'], proposal['intended_next_actor']) != ('Claude', 'Hermes', 'Codex'):
        raise ValueError('actor chain mismatch')
    if proposal['expected_memory_sha256'] != data['input_sha256']['PROJECT_MEMORY.md']:
        raise ValueError('stale memory')
    if proposal['tests_executed_by_model'] is not False or proposal['decisions_proposed'] != [] or proposal['unresolved_issues'] != [] or proposal['next_action'] != NEXT:
        raise ValueError('unsupported claim, decision change or next action')
    expected = ''.join(f"{item['id']}={item['label']}\n" for item in json.loads(data['files']['fixture.json'])['items'])
    if proposal['labels_text'] != expected:
        raise ValueError('manifest does not match portable fixture')
    for field in ('action_attempted', 'result'):
        if not isinstance(proposal[field], str) or not proposal[field].strip() or len(proposal[field]) > 500 or '\n' in proposal[field]:
            raise ValueError('invalid narrative')
    return expected


def finish(work: Path) -> dict:
    root = work / 'repo'
    data = json.loads(read(work, 'input-pmp.json'))
    response = json.loads(read(work, 'claude-output.json'))
    if packet(root) != data:
        raise ValueError('repository changed after export')
    content = validate_candidate(data, response['proposal'])
    outputs = ('labels.txt', EVIDENCE, HANDOFF, 'evidence/claude-input.json', 'evidence/claude-output.json')
    for name in outputs:
        if safe_path(root, name).exists():
            raise ValueError('append-only output already exists')
    for name in ('test_fixture.py',):
        if read(root, name).decode().replace('\r\n', '\n') != (HERE / 'seed' / name).read_text(encoding='utf-8'):
            raise ValueError('untrusted acceptance code')
    if read(root, 'test_manifest.py') != (HERE / 'claude-seed/test_manifest.py').read_bytes():
        raise ValueError('untrusted manifest acceptance code')
    atomic(root / 'labels.txt', content.encode())
    check = run([sys.executable, *TESTS], root)
    if 'Ran 6 tests' not in check.stderr:
        raise ValueError('all six acceptance tests must run')
    evidence = {'timestamp': utc(), 'logical_actor': 'Claude', 'input_sha256': data['input_sha256'],
                'labels_sha256': digest(read(root, 'labels.txt')), 'command': ['python', *TESTS],
                'exit_code': check.returncode, 'stdout': check.stdout, 'stderr': check.stderr,
                'tests_executed_by_model': False, 'source_hermes_commit': HERMES_HEAD,
                'runtime': response['runtime']}
    atomic(root / EVIDENCE, json_bytes(evidence))
    atomic(root / 'evidence/claude-input.json', read(work, 'input-pmp.json'))
    atomic(root / 'evidence/claude-output.json', read(work, 'claude-output.json'))
    atomic(root / HANDOFF, ('# Session — Claude continuation of Hermes\n\n'
        f'- Actor: Claude (logical label)\n- Timestamp: {evidence["timestamp"]}\n'
        f'- Start memory SHA-256: {data["input_sha256"]["PROJECT_MEMORY.md"]}\n'
        '- Result: labels.txt proposed by Claude, imported and tested by the host.\n'
        '- Verification: six acceptance tests passed; model did not run tests.\n'
        '- Decisions: existing decisions preserved; none proposed.\n'
        '- Unresolved issues: none within this fixture. Identity/freshness not certified.\n'
        f'- Evidence: {EVIDENCE}\n- Labels SHA-256: {evidence["labels_sha256"]}\n\n'
        f'## Next action\n\n{NEXT}\n').encode())
    sections = {s.name: s.body for s in parse_sections(read(root, 'PROJECT_MEMORY.md').decode())}
    set_memory(root, {'Identity': re.sub(r'^- Last actor: .+$', '- Last actor: Claude (logical participant)', sections['Identity'], flags=re.M),
        'Current state': sections['Current state'] + '\n- [VERIFIED] Host accepted Claude labels.txt and passed six tests; evidence/claude-host-verification.json.',
        'Next action': NEXT, 'Evidence': sections['Evidence'] + f'\n- labels.txt\n- {EVIDENCE}\n- {HANDOFF}\n- evidence/claude-input.json\n- evidence/claude-output.json'})
    changed = (*outputs, 'PROJECT_MEMORY.md')
    git(root, 'add', '--', *changed)
    git(root, 'commit', '-m', 'handoff: Claude manifest proposal with host verification and PMP state')
    atomic(work / 'host-verification.json', json_bytes(evidence))
    git(root, 'bundle', 'create', str(work / 'claude-replay.bundle'), '--all')
    report = {'timestamp': utc(), 'source_hermes_commit': HERMES_HEAD,
              'dispatch_commit': json.loads(read(work, 'dispatch.json'))['dispatch_commit'],
              'claude_handoff_commit': git(root, 'rev-parse', 'HEAD'),
              'bundle_sha256': digest((work / 'claude-replay.bundle').read_bytes()),
              'host_verification': evidence, 'fresh_codex_executed': False,
              'model_identity_certified': False, 'session_freshness_certified': False}
    atomic(work / 'claude-report.json', json_bytes(report))
    run(['git', '-c', 'core.autocrlf=false', 'clone', str(work / 'claude-replay.bundle'), str(work / 'fresh-result')], work)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('prepare', 'consume', 'finish'))
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--claude', type=Path)
    parser.add_argument('--retry-once', action='store_true', help='Explicit second invocation after a failed attempt; never automatic')
    args = parser.parse_args()
    work = args.work.resolve()
    if args.phase == 'consume' and not args.claude:
        parser.error('--claude executable path required')
    try:
        result = prepare(work) if args.phase == 'prepare' else consume(work, args.claude.resolve(), args.retry_once) if args.phase == 'consume' else finish(work)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f'CLAUDE REPLAY STOPPED: {exc}', file=sys.stderr)
        raise SystemExit(1)
