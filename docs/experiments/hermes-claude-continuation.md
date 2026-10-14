# Hermes → PMP → Claude → PMP → Codex — bounded continuation

Experimental and non-normative, on `experiment/hermes-pmp-adapter`.
PMP Core 0.2.2 and the original Hermes runtime/adapter are unchanged.

## Purpose and scope

Continue the archived real Hermes result with a different runtime using only
repository state. Hermes had normalized two fixture labels. The authorized
Claude follow-up derives `labels.txt` with one `id=label` line per item. The
host imports only that content, runs trusted tests, and records a PMP handoff.
The task is small and deterministic; it is not a quality benchmark or a test
of autonomous code execution.

```text
Archived Hermes handoff d2e225b
  → host dispatch commit (explicit human follow-up scope)
  → PMP packet with nine fixture files
  → Claude Code proposal (no tools)
  → host validation + six tests + evidence + PMP handoff
  → separate Codex continuation from a fresh clone
```

The dispatch changes instructions/current next action in a new Git commit;
it does not pretend that the original Hermes run requested the later Claude
task. Previous fixture data, tests, evidence and historical handoff remain
unchanged. Canonical state remains the target repository's PROJECT_MEMORY.md.

## Components and reproduction

- `experiments/hermes-pmp/claude_replay.py`: thin experimental host runner;
  reuses existing safe-path, hashing, atomic-write, Core parsing/validation,
  Git and original Hermes verification helpers.
- `experiments/hermes-pmp/claude-seed/test_manifest.py`: three trusted tests
  in addition to the original three fixture tests.
- `tests/test_claude_pmp_continuation.py`: offline rejection/environment/chain
  tests. Its synthetic completion is explicitly labelled local mock.
- `experiments/hermes-pmp/evidence/claude-continuation-20261006/`: real report,
  bundle and attempt markers. The later Codex receipt is stored separately.

Requirements: Python 3.12+, Git, and for live execution only, Claude Code
2.1.274 authenticated via the existing `claude.ai` subscription. The runner
refuses another CLI version until its restrictions are reviewed. No install,
new service, server, MCP infrastructure, API key or Core dependency is needed.

From the experimental protocol checkout:

```powershell
python -m unittest discover -s tests -p test_claude_pmp_continuation.py -v
python experiments/hermes-pmp/claude_replay.py prepare --work '<new-absolute-run-directory>'
python experiments/hermes-pmp/claude_replay.py consume --work '<same-run-directory>' --claude '<installed-claude-executable>'
python experiments/hermes-pmp/claude_replay.py finish --work '<same-run-directory>'
```

Use a new directory for each separately authorized run. `consume` creates an
attempt marker, allows one turn and no tools, and never retries automatically.
After diagnosing an unsuccessful invocation, `--retry-once` permits one explicit
second invocation only; it cannot run after accepted output exists. Failures
retain bounded redacted diagnostics. `finish` rejects a changed input snapshot,
wrong/stale proposals, decision changes, or existing output files. On failure,
retain the disposable run for diagnosis; do not treat it as a completed handoff.
No general crash-proof transaction or OS sandbox is claimed.

Verify the archived result without a provider or new model call:

```powershell
git bundle verify experiments/hermes-pmp/evidence/claude-continuation-20261006/claude-replay.bundle
git clone experiments/hermes-pmp/evidence/claude-continuation-20261006/claude-replay.bundle '<new-verification-directory>'
# Run from that new clone:
python -I -m unittest discover -s . -p 'test_*.py' -v
```

Expected handoff HEAD: `1993c0aa4a4b308da690e87bc5f74f6fda514d73`.
Bundle SHA-256: `b9c7e80bdd3c25a4aca67c43dd647fa3325f4340a9f51de5bbc7a61b9f1e03ec`.
The bundle contains the Hermes baseline/history, dispatch, Claude input/output,
host command output, generated manifest, and canonical memory/handoff.
Compare recorded input digests with the dispatch commit; current canonical
memory is expected to differ after the handoff. Never overwrite historical logs.

## Observed execution and limits — 2026-10-06

Local Claude Code reported `2.1.274`, first-party `claude.ai` subscription login
and Pro access. The initial permission review rejected transmission of possibly
private memory. The exact packet was inspected: only nine synthetic fixture,
instruction and evidence files, not the real protocol project's memory or this
conversation. After that review, execution was approved. The packet SHA-256 was
`b8d39b8afc809cf0768129c8cee7e57ec8e7038f1c44a494fb0d1a7cab959646`.

The first CLI invocation exited 1 and its diagnostic output was not retained;
its cause and provider-request count are not established. Read-only `doctor`
reported no installation issues; cached auth status alone was insufficient to
prove a usable live session. Diagnostic capture was corrected. The explicit
second invocation succeeded and the host ran six passing tests. There was no
third invocation and Hermes was not rerun.

The successful runtime receipt reports `claude-sonnet-5`, one agentic turn,
zero enabled tools, and no web requests. Its model-usage data also records
`claude-haiku-4-5-20251001`; the function of that auxiliary usage is not proven
by this receipt. Therefore one agentic turn is not claimed to equal one provider
request. The script used safe/restricted mode, disabled hooks, skills, MCP,
auto-memory and session persistence, and supplied explicit context. API-key and
custom-provider environment variables were not inherited. These controls do
not prove model identity, hidden memory absence, or session freshness.

The successful session's API-equivalent list-price estimate is USD 0.03528,
including auxiliary usage. This is not a bill or an incremental subscription
charge. Existing subscription quota was used; billing/extra-usage settings were
not changed and actual invoice impact was not audited. No credits were bought.
The configured USD 0.50 estimate cap is a guardrail, not a zero-charge guarantee.

At report generation, only the host had verified the result. Accordingly,
`claude-report.json` preserves `fresh_codex_executed=false`. A subsequent
independent Codex receipt must be assessed separately, never retroactively
inserted into that original report.

That separate continuation then completed: six tests passed, fourteen historical
input hashes and both resulting artifacts matched, and fifteen prior files
remained unchanged. The host committed only the verifier's receipt and canonical
memory update at `5e717267e23e39a854347ade7e9efa545269c227`. See
`codex-after-claude.md`, `fresh-codex.json` and `fresh-codex.bundle` in the same
archive. The final bundle SHA-256 is
`1a5eb32bc3cc3c240be4a0533d110d86adf7291240628defc6f9109b45324b25`.
Both bundle checks passed; the repository test suite passed 76 tests, including
four new offline Claude-host checks. Core memory/release gates passed. No remote
CI, push, PR, merge, release or publication occurred.

Conclusion: **A. VALIDATED**, limited to this repository-only fixture chain.
The real model proposes data; the host writes and tests it. It does not establish
that either model independently executed code or will reliably solve arbitrary
tasks. The bounded experiment is complete. Review this evidence before defining
any broader task; no further model calls are needed for its closure.

## Official references checked

- [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Claude Code authentication](https://code.claude.com/docs/en/authentication)

Local `--help` was checked as well. Its `--bare` mode explicitly excludes OAuth,
so this subscription experiment uses safe/restricted mode instead. It is not a
claim that the Hermes runtime's identically named flags share these semantics.
