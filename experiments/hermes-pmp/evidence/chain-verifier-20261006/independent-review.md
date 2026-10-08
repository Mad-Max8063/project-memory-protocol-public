# Independent review — fixed offline chain verifier

Date: 2026-10-06. Reviewer: Codex, logical participant; no identity or hidden-session freshness attestation. Scope: this review snapshot only, repository instructions, canonical PMP memory, CHAIN_TASK.md and linked evidence. No global memory, conversations, credentials, other checkouts, network, provider calls, commit, push or merge were used.

## Result

Changes are required for two P2 boundary findings below. The fixed CLI archive verification succeeds, and all six host-owned acceptance tests pass. The findings concern an altered checkout supplied directly to the exported semantic helper and ancestor links in supplied evidence paths; they do not invalidate the observed successful check of the currently pinned archives.

Reviewed branch: `experiment/hermes-pmp-adapter`.

- HEAD: `d37185b33437c2d30eeee6d424f42e4614acf164`.
- Parent: `966ced18c8ea540ad73ca942531ed7e9f9e64625`.
- Initial tracked/untracked working-tree status: clean.
- `verify_chain.py` SHA256: `b372c61984a833a38b5135dcb0c86fcc14d60773e90ea2b1459bcdb1d7c67f32`.
- `test_pmp_replay_chain.py` SHA256: `3190dac4d42d347f73d655d53365a5da604680b8d5ab33ac660e5d9cc0fc5660`.

These match host-checks.json. The reviewed commit changes only the optional verifier, its tests, task/docs/evidence/session and canonical experiment memory. The Core, existing adapters, profiles and archived bundles are outside its implementation diff.

## Findings

### P2 — Ignored untracked Python modules execute before semantic rejection

Location: `experiments/hermes-pmp/verify_chain.py:100` and `:187`.

The helper checks untracked files with `git ls-files --others --exclude-standard`, which omits ignored files. Its bootstrap then inserts the entire supplied checkout at the front of sys.path. Trusted `test_fixture.py` and `test_manifest.py` import `json`; an ignored untracked `json.py` in that checkout is imported before the Python standard-library module. Pinning the two test modules does not pin their import resolution.

Confirmed in a temporary clone of the pinned final bundle: append `json.py` to that clone's `.git/info/exclude`, create `json.py` containing the following harmless probe, and call `verify_repository(root, *pinned_reports)`:

```python
from pathlib import Path
Path("ignored-code-executed.marker").write_text("executed")
raise RuntimeError("IGNORED_MODULE_EXECUTED")
```

Observed before invocation: the untracked-file gate returns `b''`. Observed after invocation: the marker contains `executed`; the helper raises `ValueError: six acceptance tests did not pass`. Therefore rejection happens after executing the ignored module. Both probe files and the temporary clone were cleaned up. No further payload variants were executed after confirmation.

The exposed helper's contract requires rejection of altered checkouts and execution of only trusted code. Reject all untracked files, including ignored ones, before the bootstrap, or execute the trusted modules from a separate fixed directory whose imports cannot resolve through the supplied checkout. Add a regression that proves the payload never executes. The ordinary `verify_chain` CLI materializes freshly pinned bundles in new temporary clones; this reproduction targets the exported helper supplied an already altered clone.

### P2 — Ancestors of evidence_root are outside link checks

Location: `experiments/hermes-pmp/verify_chain.py:208`, through `adapter.safe_path` at `adapter.py:41-55`.

safe_path checks the root itself and components below it, then compares resolved containment. It does not check ancestors of the absolute root. If an ancestor is a symlink/junction and the final evidence directory is an ordinary directory under that link, both root.resolve() and candidate.resolve() follow the same link and containment still succeeds. This contradicts the task's rejection of symlink/junction paths.

Confirmed by source inspection and a controlled predicate probe: with Path.is_junction returning True only for evidence_root.parent, safe_path(evidence_root, 'live-replay-20261006/replay-report.json') accepts the path. The simulated parent predicate is True, but the helper never consults it. Creating a real Windows junction through PowerShell failed in this sandbox; no real-junction end-to-end success is claimed.

Check every existing absolute ancestor before resolving a supplied evidence/repository root. This can be implemented in the new verifier without changing the existing adapter/Core. Add focused path-boundary coverage. Pinned content digests still reject changed bytes; this finding concerns the promised path boundary, rather than acceptance of an altered bundle.

## Commands and current observations

Executed from the review-snapshot root with TEMP and TMP set to that same absolute directory:

```powershell
$env:TEMP = (Get-Location).Path
$env:TMP = (Get-Location).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B experiments/hermes-pmp/verify_chain.py --json
python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v
```

CLI: success; JSON records verified=true, historical_inputs=14, acceptance_tests=6, three bundle SHA256 entries, final_commit=`5e717267e23e39a854347ade7e9efa545269c227`, model_identity_certified=false and session_freshness_certified=false. Its fixed isolated bootstrap ran exactly the six named fixture/manifest tests; test_exit_code=0, `Ran 6 tests in 0.004s`, `OK`.

Host acceptance: exit 0; `Ran 6 tests in 26.800s`, `OK`:

- CLI JSON/usage/failure exit codes.
- Corrupted bundle rejected before subprocess invocation.
- Missing archive and linked-input predicate rejected.
- Modified report rejected before subprocess invocation.
- Real chain and byte-for-byte preservation of the source evidence tree.
- Altered result and missing handoff rejected.

The interpreter emitted `Failed to find real location of C:\Python314\python.exe`, also present in historical receipts; it was nonfatal. These are observations under the available Python 3.14 interpreter, not a Python 3.12 compatibility certification. No full-suite rerun was needed; host-checks.json records the earlier 82-test run as historical host evidence, not an independent rerun here.

Additional inspection commands: `git branch --show-current`, `git rev-parse HEAD`, `git rev-parse HEAD^`, `git status --short --untracked-files=all --ignored`, `git show --stat --oneline HEAD`, `git diff HEAD^ HEAD --name-only`, `git diff --check`, targeted Get-Content/rg reads and Get-FileHash for verifier/tests. Focused probes used `python -I -B -` with in-memory scripts and TemporaryDirectory clones under this snapshot.

The acceptance CLI subprocess omits -B and clean_env drops PYTHONDONTWRITEBYTECODE, creating four ignored bytecode caches for the local adapter/Core imports. Their creation timestamps matched this run. Only those four generated .pyc files were removed by explicit validated paths; no original source/evidence file was removed. All temporary probes cleaned up. Pre-receipt final status, including ignored files, was clean; git diff --check passed. The sole retained review output is this receipt.

## Contract audit and reconstruction

The verifier checks all six fixed archive/report digests before cloning; it copies those verified bytes into temporary files to avoid a second archive read. Three local bundle clones use minimized environments, disabled hooks, core.autocrlf=false and bounded timeouts. No input-derived network URL, command or arbitrary report path is executed. Context managers clean temporary clones and memory-validation files on successful and failing paths. Original evidence bytes remained unchanged in the acceptance check.

The successful path verifies pinned revision labels and parent lineage, exact stage change boundaries, cross-bundle tree equality, tracked working-file bytes, duplicated host receipts, snapshots, five Hermes inputs against baseline and nine Claude inputs against dispatch, proposal memory guards, fixture/manifest bytes, duplicated Claude runtime metadata, historical fresh_codex flags, final two-file diff, Codex receipt and canonical-memory digests. Five historical PMP memories are passed through the unchanged structural validator; active decisions are preserved, next actions are nonempty and stage handoffs link to evidence. Both archived test modules match source hash pins and local trusted test contents before execution. The runner verifies exit status and the actual six-test count. The import boundary has the P2 exception above.

Repository/PMP/evidence were sufficient to recover scope, constraints, implementation authorship and next action. No external conversation or memory was required. The current verifier was implemented locally by Codex after the sole bounded Claude implementation invocation timed out without a retained complete proposal. The older archived task separately records Hermes proposing normalized fixture labels, Claude proposing labels.txt, host execution of acceptance tests, and a later logical Codex continuation receipt committed by the replay host. The current timeout must not be mistaken for a successful Claude implementation handoff, nor for failure of the earlier archived Claude continuation. Usage/request count and billed cost of the timeout remain unestablished.

The CLI's recovered action belongs to the final archived replay memory:

> Max / dispatch host: review .project-memory/sessions/codex-after-claude.md and this canonical update, then close the bounded experiment. No implementation action remains; any further experiment requires a new scoped task.

The current implementation task's canonical action is the independent review of this command and tamper tests. This receipt completes that bounded review against the stated original SHA. The host's authorized next action is to correct the two concrete findings locally, run focused regressions and applicable checks, then incorporate this receipt and current results into task evidence/canonical state. No second independent review, provider retry, publication, main merge or expansion is inferred.

Git and hashes establish consistency/integrity relative to this source snapshot. They do not authenticate logical actors, certify model identity or hidden session freshness, prove general autonomy, independently audit cost, or establish remote CI/deployment/publication. This review has no such claims.
