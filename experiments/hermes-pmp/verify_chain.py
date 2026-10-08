"""Offline integrity and semantic verification of the fixed 2026-10-06 chain."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from adapter import clean_env, digest, parse_sections, safe_path, validate

HERE = Path(__file__).absolute().parent
PINNED = {
    'live-replay-20261006/replay.bundle': 'b729b7f2220f5e639ad9e43f205314c45055d69eab966689b0438f178398de17',
    'live-replay-20261006/replay-report.json': 'ade8546d585305fdccbb3061da91898e5a3ab991b8178815106faa36de134c7d',
    'claude-continuation-20261006/claude-replay.bundle': 'b9c7e80bdd3c25a4aca67c43dd647fa3325f4340a9f51de5bbc7a61b9f1e03ec',
    'claude-continuation-20261006/claude-report.json': '45d6b507ffa1af8df119f2e49d34c1d84f80896df939d1e2de3f2dca01f65adc',
    'claude-continuation-20261006/fresh-codex.bundle': '1a5eb32bc3cc3c240be4a0533d110d86adf7291240628defc6f9109b45324b25',
    'claude-continuation-20261006/fresh-codex.json': '939cb81062e442b9bb4ef0a0960dfc37c986702d25163291c39539bd2f3c589b',
}
BASELINE = '4488a97dc68b7b614365d0f274edbf665e679f41'
HERMES = 'd2e225b61857be0e0b79c5d28116ae6a9800f7c7'
DISPATCH = 'ff595d4a4e4296c5171d10b996201755900c0cbb'
CLAUDE = '1993c0aa4a4b308da690e87bc5f74f6fda514d73'
CODEX = '5e717267e23e39a854347ade7e9efa545269c227'
HERMES_INPUTS = ('AGENTS.md', 'PROJECT_MEMORY.md', 'TASK.md', 'fixture.json', 'test_fixture.py')
CLAUDE_INPUTS = (*HERMES_INPUTS, 'CLAUDE_TASK.md', 'test_manifest.py',
                 'evidence/host-verification.json', '.project-memory/sessions/hermes-handoff.md')
TEST_HASHES = {'test_fixture.py': '90a355a2777d5f82610cd18cc90ec2de45a81054bbc23e6d4aaa9367bd5147e1',
               'test_manifest.py': 'ab84cb813d37faf36952d8f5b44a8a6ef1d4dcdf1a3aa33d0a50ca02f91625fc'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unlinked_root(root: Path) -> Path:
    root = root.absolute()
    # A plain leaf under a junction/symlink still redirects the archive root.
    for component in (root, *root.parents):
        require(not component.is_symlink() and not component.is_junction(),
                'linked root or ancestor rejected')
    return root


def git_bytes(root: Path, *args: str) -> bytes:
    # Built-in commands only, minimized env, no input-derived options or hooks.
    result = subprocess.run(['git', '-c', f'safe.directory={root.as_posix()}',
                             '-c', 'core.autocrlf=false', '-c', 'core.hooksPath=' + str(HERE / '.no-hooks'),
                             *args], cwd=root, env=clean_env(), capture_output=True, timeout=30)
    require(result.returncode == 0, 'Git verification failed: ' + args[0])
    return result.stdout


def blob(root: Path, revision: str, name: str) -> bytes:
    return git_bytes(root, 'show', f'{revision}:{name}')


def read_file(root: Path, name: str) -> bytes:
    path = safe_path(root, name)
    require(path.is_file() and path.stat().st_size <= 1024 * 1024, 'missing/oversized evidence: ' + name)
    return path.read_bytes()


def load(root: Path, name: str):
    return json.loads(read_file(root, name))


def sections(raw: bytes) -> dict:
    return {section.name: section.body for section in parse_sections(raw.decode('utf-8'))}


def stage(root, parent, revision, expected):
    require(git_bytes(root, 'rev-parse', revision + '^').decode().strip() == parent, 'lineage mismatch')
    changed = git_bytes(root, 'diff', '--name-only', parent, revision).decode().splitlines()
    require(sorted(changed) == sorted(expected), 'stage change scope mismatch')


def verify_repository(root: Path, hermes_report: dict, claude_report: dict, codex_report: dict) -> dict:
    """Semantic helper; archive authentication is the caller's responsibility."""
    root = unlinked_root(root)
    require(git_bytes(root, 'rev-parse', 'HEAD').decode().strip() == CODEX, 'final revision mismatch')
    require(hermes_report['baseline_commit'] == BASELINE and hermes_report['handoff_commit'] == HERMES,
            'Hermes report revision mismatch')
    require(claude_report['source_hermes_commit'] == HERMES and claude_report['dispatch_commit'] == DISPATCH
            and claude_report['claude_handoff_commit'] == CLAUDE, 'Claude report revision mismatch')
    require(codex_report['input_revision'] == CLAUDE and codex_report['receipt_commit'] == CODEX,
            'Codex report revision mismatch')
    hermes_scope = ('fixture.json', 'PROJECT_MEMORY.md', 'evidence/host-verification.json',
                    '.project-memory/sessions/hermes-handoff.md', 'evidence/input-pmp.json',
                    'evidence/consumer-output.json')
    claude_scope = ('labels.txt', 'PROJECT_MEMORY.md', 'evidence/claude-host-verification.json',
                    '.project-memory/sessions/claude-handoff.md', 'evidence/claude-input.json',
                    'evidence/claude-output.json')
    final_scope = ('PROJECT_MEMORY.md', '.project-memory/sessions/codex-after-claude.md')
    stage(root, BASELINE, HERMES, hermes_scope)
    stage(root, HERMES, DISPATCH, ('AGENTS.md', 'CLAUDE_TASK.md', 'test_manifest.py', 'PROJECT_MEMORY.md'))
    stage(root, DISPATCH, CLAUDE, claude_scope)
    stage(root, CLAUDE, CODEX, final_scope)
    require(sorted(hermes_report['changed_files']) == sorted(hermes_scope), 'reported Hermes scope mismatch')
    require(sorted(codex_report['changed_files']) == sorted(final_scope), 'reported Codex scope mismatch')
    # Compare every tracked working file to its Git blob, including test code.
    names = git_bytes(root, 'ls-files', '-z').decode().split('\0')
    for name in filter(None, names):
        require(read_file(root, name) == blob(root, CODEX, name), 'changed checked-out file: ' + name)
    # Ignored files can shadow stdlib or trusted modules too. Reject them
    # before putting the clone on the isolated test process's import path.
    require(git_bytes(root, 'ls-files', '--others', '-z') == b'', 'untracked or ignored result files')
    hi = load(root, 'evidence/input-pmp.json')
    ci = load(root, 'evidence/claude-input.json')
    ho = load(root, 'evidence/consumer-output.json')
    co = load(root, 'evidence/claude-output.json')
    he = load(root, 'evidence/host-verification.json')
    ce = load(root, 'evidence/claude-host-verification.json')
    require(he == hermes_report['host_verification'] and ce == claude_report['host_verification'],
            'host receipt/report mismatch')
    require(he['exit_code'] == ce['exit_code'] == 0 and he['mode'] == 'hermes'
            and he['logical_actor'] == 'Hermes' and ce['logical_actor'] == 'Claude', 'unsupported host result')
    require(he['tests_executed_by_model'] is False and ce['tests_executed_by_model'] is False,
            'unsupported model test claim')
    require(digest(read_file(root, 'evidence/input-pmp.json')) == hermes_report['input_packet_sha256'],
            'Hermes snapshot hash mismatch')
    checked = 0
    for revision, receipt, snapshot, inputs in ((BASELINE, he, hi, HERMES_INPUTS),
                                               (DISPATCH, ce, ci, CLAUDE_INPUTS)):
        require(set(receipt['input_sha256']) == set(inputs), 'unexpected historical input map')
        require(receipt['input_sha256'] == snapshot['input_sha256'], 'input map mismatch')
        for name in inputs:
            require(digest(blob(root, revision, name)) == receipt['input_sha256'][name],
                    'historical input hash mismatch: ' + name)
            checked += 1
    require(hi['canonical_memory'].encode() == blob(root, BASELINE, 'PROJECT_MEMORY.md'),
            'Hermes canonical snapshot mismatch')
    require(hi['memory_sha256'] == digest(hi['canonical_memory'].encode()) == hermes_report['input_memory_sha256'],
            'Hermes memory hash mismatch')
    require(set(ci['files']) == set(CLAUDE_INPUTS), 'Claude embedded input scope mismatch')
    for name, content in ci['files'].items():
        require(content.encode() == blob(root, DISPATCH, name), 'Claude embedded input mismatch: ' + name)
    require(ho['proposal']['expected_memory_sha256'] == hi['memory_sha256']
            and co['proposal']['expected_memory_sha256'] == ci['input_sha256']['PROJECT_MEMORY.md'],
            'proposal memory guard mismatch')
    require(json.loads(read_file(root, 'fixture.json')) == ho['proposal']['fixture']
            and digest(read_file(root, 'fixture.json')) == he['fixture_sha256'], 'fixture proposal mismatch')
    require(read_file(root, 'labels.txt') == co['proposal']['labels_text'].encode()
            and digest(read_file(root, 'labels.txt')) == ce['labels_sha256'], 'labels proposal mismatch')
    require(ci['source_hermes_commit'] == ce['source_hermes_commit'] == HERMES
            and co['runtime'] == ce['runtime'], 'source/runtime metadata mismatch')
    require(claude_report['fresh_codex_executed'] is False and codex_report['fresh_codex_executed'] is True,
            'historical flags changed')
    require(codex_report['exit_code'] == 0 and codex_report['tests_passed'] == 6
            and codex_report['historical_input_hashes_checked'] == 14, 'Codex verification claim mismatch')
    require(digest(read_file(root, '.project-memory/sessions/codex-after-claude.md')) == codex_report['receipt_sha256'],
            'Codex receipt digest mismatch')
    require(digest(read_file(root, 'PROJECT_MEMORY.md')) == codex_report['memory_sha256'],
            'final memory digest mismatch')
    # Validate historical PMP through unchanged Core validator using temporary files.
    memories = [blob(root, revision, 'PROJECT_MEMORY.md') for revision in (BASELINE, HERMES, DISPATCH, CLAUDE, CODEX)]
    with tempfile.TemporaryDirectory(prefix='pmp-chain-memory-') as directory:
        memory = Path(directory) / 'PROJECT_MEMORY.md'
        for raw in memories:
            memory.write_bytes(raw)
            require(not validate(memory), 'invalid historical PMP memory')
    states = [sections(raw) for raw in memories]
    require(all(state['Active decisions'] == states[0]['Active decisions'] for state in states),
            'active decisions not preserved')
    require(all(state['Next action'].strip() for state in states), 'empty next action')
    for revision, record, evidence in ((HERMES, '.project-memory/sessions/hermes-handoff.md', 'evidence/host-verification.json'),
                                      (CLAUDE, '.project-memory/sessions/claude-handoff.md', 'evidence/claude-host-verification.json'),
                                      (CODEX, '.project-memory/sessions/codex-after-claude.md', 'evidence/claude-host-verification.json')):
        handoff = read_file(root, record).decode()
        state = sections(blob(root, revision, 'PROJECT_MEMORY.md'))
        require(record in state['Evidence'] and evidence in handoff, 'handoff/evidence link missing')
        if revision != CODEX:
            require(state['Next action'].strip() in handoff, 'handoff next action differs from canonical memory')
        else:
            # Historical Codex receipt paraphrases its canonical next action.
            # Both full files are independently pinned; do not rewrite history.
            require(state['Next action'] == 'Max / dispatch host: review .project-memory/sessions/codex-after-claude.md and this canonical update, then close the bounded experiment. No implementation action remains; any further experiment requires a new scoped task.',
                    'unexpected final canonical next action')
            require('Next action: Max / dispatch host reviews this receipt and the canonical-memory update, then closes the bounded experiment.' in handoff,
                    'final receipt continuation mismatch')
    require(digest(blob(root, HERMES, '.project-memory/sessions/hermes-handoff.md'))
            == hermes_report['continuation']['handoff_sha256'], 'Hermes handoff digest mismatch')
    require(digest(blob(root, HERMES, 'PROJECT_MEMORY.md'))
            == hermes_report['continuation']['canonical_memory_sha256'], 'Hermes result memory mismatch')
    # Only known, locally anchored test modules may execute.
    for name, local in (('test_fixture.py', HERE / 'seed/test_fixture.py'),
                        ('test_manifest.py', HERE / 'claude-seed/test_manifest.py')):
        source = read_file(root, name)
        require(digest(source) == TEST_HASHES[name], 'untrusted archived test module')
        require(source.decode().replace('\r\n', '\n') == local.read_text(encoding='utf-8'),
                'local trusted test differs')
    # -I removes cwd from sys.path. Explicitly enable only the verified clone
    # for these two named modules, with no discovery of additional tests.
    bootstrap = ('import os,sys,unittest; sys.path.insert(0,os.getcwd()); '
                 'suite=unittest.defaultTestLoader.loadTestsFromNames(["test_fixture","test_manifest"]); '
                 'result=unittest.TextTestRunner(verbosity=2).run(suite); '
                 'sys.exit(0 if result.wasSuccessful() else 1)')
    command = [sys.executable, '-I', '-B', '-c', bootstrap]
    result = subprocess.run(command, cwd=root, env=clean_env(), capture_output=True, text=True,
                            encoding='utf-8', timeout=30)
    require(result.returncode == 0 and re.search(r'^Ran 6 tests in ', result.stderr, re.M)
            and re.search(r'^OK$', result.stderr, re.M), 'six acceptance tests did not pass')
    return {'verified': True, 'historical_inputs': checked, 'acceptance_tests': 6,
            'next_action': states[-1]['Next action'], 'final_commit': CODEX,
            'model_identity_certified': False, 'session_freshness_certified': False,
            'test_command': ['python', *command[1:]], 'test_exit_code': result.returncode,
            'test_stdout': result.stdout, 'test_stderr': result.stderr}


def verify_chain(evidence_root: Path | None = None) -> dict:
    evidence = unlinked_root(evidence_root if evidence_root is not None else HERE / 'evidence')
    # Do not follow links before checking original fixed-path components.
    verified = {}
    for name, expected in PINNED.items():
        data = read_file(evidence, name)
        require(digest(data) == expected, 'archive digest mismatch: ' + name)
        verified[name] = data
    hr = json.loads(verified['live-replay-20261006/replay-report.json'])
    cr = json.loads(verified['claude-continuation-20261006/claude-report.json'])
    fr = json.loads(verified['claude-continuation-20261006/fresh-codex.json'])
    bundles = {name: PINNED[name] for name in PINNED if name.endswith('.bundle')}
    require(hr['bundle_sha256'] == bundles['live-replay-20261006/replay.bundle']
            and cr['bundle_sha256'] == bundles['claude-continuation-20261006/claude-replay.bundle']
            and fr['bundle_sha256'] == bundles['claude-continuation-20261006/fresh-codex.bundle'],
            'bundle/report digest mismatch')
    with tempfile.TemporaryDirectory(prefix='pmp-chain-') as directory:
        work = Path(directory)
        hooks = work / 'empty-hooks'
        hooks.mkdir()
        clones = []
        for index, (name, revision) in enumerate((('live-replay-20261006/replay.bundle', HERMES),
                          ('claude-continuation-20261006/claude-replay.bundle', CLAUDE),
                          ('claude-continuation-20261006/fresh-codex.bundle', CODEX))):
            # Materialize the already-verified bytes to avoid hash/read TOCTOU.
            bundle = work / f'archive-{index}.bundle'
            bundle.write_bytes(verified[name])
            root = work / f'repo-{index}'
            result = subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.hooksPath=' + str(hooks),
                                     'clone', str(bundle), str(root)], cwd=work, env=clean_env(),
                                    capture_output=True, timeout=30)
            require(result.returncode == 0, 'verified bundle could not be cloned')
            require(git_bytes(root, 'rev-parse', 'HEAD').decode().strip() == revision, 'bundle revision mismatch')
            clones.append(root)
        # Same commits must contain identical files across the saved stages.
        for older, newer, revision in ((clones[0], clones[2], HERMES), (clones[1], clones[2], CLAUDE)):
            require(git_bytes(older, 'rev-parse', revision + '^{tree}')
                    == git_bytes(newer, 'rev-parse', revision + '^{tree}'), 'cross-bundle tree mismatch')
        result = verify_repository(clones[-1], hr, cr, fr)
        result['bundle_sha256'] = bundles
        result['scope'] = 'fixed archived chain; offline integrity and local test verification'
        return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-root', type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = verify_chain(args.evidence_root)
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        if args.json:
            print(json.dumps({'verified': False, 'error': str(error)}))
        else:
            print('CHAIN REJECTED: ' + str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2) if args.json else
          'VERIFIED: three bundles, fourteen historical inputs, six acceptance tests; canonical next action recovered.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
