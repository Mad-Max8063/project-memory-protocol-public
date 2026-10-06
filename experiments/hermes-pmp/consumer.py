"""Explicit mock consumer, or bounded Hermes CLI invocation with a dedicated home."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

from adapter import NEXT_ACTION, atomic, clean_env, json_bytes

CONFIG = '''platform_toolsets:
  cli: []
fallback_providers: []
mcp_servers: {}
memory:
  memory_enabled: false
  user_profile_enabled: false
skills:
  auto_load: []
auxiliary:
  title_generation:
    enabled: false
    model_upgrade_enabled: false
auth:
  adopt_external_logins: false
agent:
  max_turns: 1
  disabled_toolsets: [terminal, file, web, browser, memory, session_search, skills, delegation, cronjob]
'''


def proposal_template(packet: dict, actor: str) -> dict:
    return {
        'expected_memory_sha256': packet['memory_sha256'], 'actor': actor,
        'action_attempted': 'Normalize the authorized fixture labels only.',
        'result': 'Replacement proposed; host tests have not been run by the model.',
        'fixture': copy.deepcopy(packet['fixture']), 'decisions_proposed': [],
        'unresolved_issues': [], 'next_action': NEXT_ACTION,
        'intended_next_actor': 'Codex',
    }


def prompt(packet: dict) -> str:
    return (
        'PMP Reader/Writer bounded task. Use only the provided repository packet. '
        'No prior conversation, tools, terminal, files, web or model memory. '
        'Read canonical_memory, constraints, decisions, evidence and next action. '
        'Perform the fixture transformation specified by TASK, returning ONLY one JSON object '
        'with the exact proposal_template keys. Replace fixture with your result. '
        'Do not claim to have run tests: the host runs them. No new decisions.\n'
        + json.dumps({'packet': packet, 'proposal_template': proposal_template(packet, 'Hermes')},
                     ensure_ascii=False, indent=2)
    )


def extract_stream(text: str) -> tuple[dict, list[dict]]:
    events = [json.loads(line) for line in text.splitlines() if line.strip()]
    if any(event.get('type') in ('tool_use', 'tool_result') for event in events):
        raise ValueError('tool invocation rejected; this fixture run is tool-free')
    finals = [event for event in events if event.get('type') == 'result']
    if len(finals) != 1 or finals[0].get('exit_code') != 0:
        raise ValueError('Hermes did not produce one successful completion')
    return json.loads(finals[0]['text']), events


def hermes_consume(packet: dict, home: Path, model: str) -> tuple[dict, dict]:
    executable = shutil.which('hermes')
    if not executable:
        raise RuntimeError('Hermes not installed/on PATH; no paid fallback attempted')
    if not home.is_dir() or home.is_symlink() or home.is_junction():
        raise RuntimeError('dedicated isolated home required')
    if (home / 'config.yaml').read_text(encoding='utf-8') != CONFIG:
        raise RuntimeError('profile restriction config changed; inspect manually')
    if not (home / 'auth.json').is_file():
        raise RuntimeError('human subscription OAuth login required in the isolated home')
    for name in ('.env', 'plugins', 'hooks', 'memories', 'skills'):
        target = home / name
        if target.exists() and (target.is_file() and target.stat().st_size or
                                target.is_dir() and any(target.iterdir())):
            raise RuntimeError('isolated home must not contain secrets/customizations/context')
    env = clean_env()
    env['HERMES_HOME'] = str(home.resolve())
    # Do not inherit provider keys, previous session IDs or external auth/home settings.
    command = [executable, 'chat', '--oneshot', '--query-file', '-', '--ignore-rules',
               '--provider', 'openai-codex', '--model', model, '--max-turns', '1',
               '--format', 'stream-json']
    version = subprocess.run([executable, '--version'], cwd=home, env=env,
                             capture_output=True, text=True, encoding='utf-8', timeout=15)
    if version.returncode:
        raise RuntimeError('Hermes version check failed')
    result = subprocess.run(command, input=prompt(packet), cwd=home, env=env,
                            capture_output=True, text=True, encoding='utf-8', timeout=120)
    if result.returncode or len(result.stdout.encode('utf-8')) > 262144:
        raise RuntimeError('Hermes run failed; no retry or provider fallback')
    proposal, events = extract_stream(result.stdout)
    # Do not persist raw diagnostics/provider auth info. Session IDs are observable labels only.
    return proposal, {'runtime_version': version.stdout.strip(), 'events': events,
                      'exit_code': result.returncode, 'tools': [], 'query_sha256_only_in_receipt': True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('mock', 'hermes', 'init-home'))
    parser.add_argument('--home', type=Path)
    parser.add_argument('--model')
    args = parser.parse_args()
    try:
        if args.mode == 'init-home':
            if not args.home:
                parser.error('--home required')
            args.home.mkdir(parents=True, exist_ok=False)
            atomic(args.home / 'config.yaml', CONFIG.encode('utf-8'))
            print('Dedicated home created; no credentials or model calls made.')
            return 0
        packet = json.loads(sys.stdin.read(65537))
        if args.mode == 'mock':
            proposal = proposal_template(packet, 'mock-hermes')
            for item in proposal['fixture']['items']:
                item['label'] = ' '.join(item['label'].split())
            receipt = {'runtime': 'deterministic mock; NOT Hermes', 'tools': [], 'exit_code': 0}
        else:
            if not args.home or not args.model:
                parser.error('Hermes requires --home and --model selected by the human')
            proposal, receipt = hermes_consume(packet, args.home, args.model)
        print(json.dumps({'proposal': proposal, 'runtime_receipt': receipt}, ensure_ascii=False))
        return 0
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f'CONSUMER FAILED: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
