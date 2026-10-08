# Observed result — 2026-10-06

Conclusion: **B. PARTIALLY VALIDATED**.

## What actually ran

1. Codex prepared an independent worktree from remote-confirmed main
   `2d9da5549d802c27b7a47293384d3f0d59b0ff13`.
2. Baseline tests: 57 passed; memory/release validators passed; packaged demo six
   tests passed. No other experimental code was included.
3. Bridge tests: all 13 passed; full discovery 70 passed. Exact test methods and
   assertions are in tests/test_hermes_pmp_adapter.py in the protocol repository.
4. One actual local mock run on 2026-10-06T11:37:15Z generated Git baseline
   `a1b7d1b7bac7456178b694eaadf497d8aa193fa9` and handoff
   `9be68212880c48724228e50879ae2def65326654`. Two seed acceptance tests failed
   as expected; three passed after host import and again in the fresh verifier.
5. A separate Codex agent received only the fresh clone path and the instruction
   to follow PMP, spawned with fork_turns=none. It read repository artifacts,
   recognized the MOCK producer, reran three tests, checked baseline/current
   hashes and recorded continuation commit
   `25e3b504bbc66b64904297a95acc5b27d2623379`. Only canonical memory and its
   receipt changed; fixture, task, tests, instructions and previous evidence did not.

## Persisted artifacts

- replay-report.json: observed test outputs, timestamps, hashes, revisions and
  explicit mock/fresh-Python-process claim separation. Absolute temporary seed
  paths in failing tracebacks are replaced by <replay-root>; no other log content
  was changed. The original run directory was retained, not deleted.
- replay.bundle: full baseline/handoff Git history with PMP snapshot, model-shaped
  mock proposal, host evidence and session record. SHA-256
  `1b2604abddecc8a40cc6998d800f194287312edf6d210fff7977fc1967ac489d`.
- fresh-codex.json and fresh-codex.bundle: separately observed continuation,
  not retroactively claimed by the original report. Bundle SHA-256
  `c76cd1f0100916802ae66af9d7f83dd265c824af67f92ea97ee0ed7d55aa2c57`.
- Receipt inside Codex bundle: .project-memory/sessions/codex-continuation.md.
  It preserves exact commands and results. A harmless Python executable-location
  warning is disclosed; commands returned zero. Untracked pycache was not committed.

Independent reproduction from protocol repository root:

```powershell
python experiments/hermes-pmp/verify_archive.py
python -m unittest -v tests/test_hermes_pmp_adapter.py
python experiments/hermes-pmp/replay.py --mode mock
```

## What this does not show

Actual Hermes was not executed, installed or authenticated. Current native
Hermes CLI docs/source support isolated profile/query-file/structured result,
but those integration assumptions were not tested against a runtime here.
There was no Nous Portal, provider API, new credit purchase, model download,
server, deploy, Argon, Obsidian, previous Hermes/Argon reuse, push, PR or merge.
The initial Codex author already had this conversation; only the continuation
was spawned without inherited turns. This is not proof of hidden model identity,
session freshness or semantic reliability. Local command receipts are not CI or
the complete optional Evidence-backed Handoff profile.

Incremental paid cost observed: USD 0. Codex used existing task/subscription
allowance. A Hermes subscription provider's actual entitlement/quota treatment
remains unverified; do not infer free/covered inference from documentation alone.

## Problems resolved without expanding scope

- Source checkout had different filesystem ownership: Git safe.directory was
  set only per command, never globally; existing dirty worktrees stayed intact.
- Isolated Python `-I -m unittest -v test_fixture.py` cannot import the local
  test module. Switched to explicit unittest discovery; recorded three actual
  tests, not merely a zero exit code.
- Inspection found an empty CLI --toolsets string selects defaults, not zero
  tools. Prepared a dedicated restricted profile instead; its real runtime
  enforcement remains a live gate, not a tested security claim.

## Stop rule / next action

No more mock variants or architecture are needed. Check availability of a NEW
independent Hermes runtime and subscription-covered OAuth route. If available,
review tool restriction on that exact version, then run one bounded live replay
using the documented dedicated home; if unavailable, keep this partial result.

## Addendum — live Hermes and Codex continuation, 2026-10-06

This addendum supersedes the historical “not executed” checkpoint above; the
original mock report and its claims remain unchanged. A new isolated Hermes
runtime `vgit.e97923c` authenticated through the existing OpenAI Codex
subscription. Its account-scoped catalog listed `gpt-5.6-luna`, and one bounded
real inference replay completed with no enabled tools or provider fallback.
The host validated and imported the fixture proposal, ran three acceptance
tests, and archived a PMP handoff.

A separate Codex continuation with no inherited turns read only the result
clone, reran all three tests, checked the recorded hashes, and wrote a receipt.
This validates one bounded PMP → Hermes → PMP → separate Codex continuation;
it does not prove model identity, session freshness, general autonomy, semantic
truth, or plan quota/no-overage terms. The historical replay report correctly
records Python as its immediate continuation and `fresh_codex_executed=false`;
the later Codex receipt is separate evidence.

See `live-replay-20261006/replay-report.json`, `replay.bundle`,
`codex-continuation.md`, and `../runtime-gate.md`. The report's bundle SHA-256 is
`b729b7f2220f5e639ad9e43f205314c45055d69eab966689b0438f178398de17`.
The direct `git bundle verify` check passed. Two pre-inference attempts failed
at runtime preflight because nested process environment lacked `USERPROFILE`;
the adapter now preserves it while excluding provider API keys, with a test.
The full repository suite now has 72 passing tests. Exact subscription usage
cost was unavailable; an existing allowance was used, no credits/API key were
purchased or used, and no separate charge was observed.

Final bounded-track category: **A. VALIDATED** under the user's defined
criterion. This applies only to this reproducible fixture replay. Do not make
additional model calls, or push, open a PR, merge, tag, release, or publish.
Never reopen or repair the blocked previous Hermes/Argon experiment.
