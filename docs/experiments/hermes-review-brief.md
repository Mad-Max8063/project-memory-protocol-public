# Portable agent handoffs, with evidence you can verify offline

An experimental Project Memory Protocol replay involving Hermes, Claude and
Codex. Prepared for external review on October 6, 2026.

## The problem

Switching agents should not require reconstructing project state from a chat
transcript. An incoming participant needs the current state, decisions,
constraints, evidence and next action in a form that belongs to the project.

PMP stores that operational context in the versioned `PROJECT_MEMORY.md`.
This experiment asks whether different runtimes can consume that state and leave
a verifiable handoff for the next participant.

## What was demonstrated

A small repository contains two fixture labels and trusted acceptance tests.
Hermes received a PMP snapshot and proposed normalized labels. The host applied
the bounded proposal, ran three tests and recorded evidence plus a PMP handoff.
Claude then received the repository packet, proposed a derived `labels.txt`
manifest, and the host ran all six fixture/manifest tests. A separate Codex
continuation, launched without inherited conversation turns, reconstructed the
result from the repository and verified its evidence.

```text
PMP state → Hermes proposal → host verification → PMP handoff
          → Claude proposal → host verification → PMP handoff
          → separate Codex continuation from repository evidence
```

The models proposed data with their tools disabled. The host wrote files and
executed tests. The observed result is continuity through portable repository
state for a small deterministic task, not autonomous model execution.

The experiment is optional and non-normative. PMP Core remains 0.2.2; the
existing specification, profile and adapters are unchanged. The bridge uses
Python's standard library and imports existing PMP validation code. Hermes and
Claude are participants, not dependencies of PMP Core. License: MIT.

## Two different outcomes

| Work | Observed result |
| --- | --- |
| Archived Hermes → Claude → Codex fixture handoff | Completed; proposals, host tests, Git commits and continuation receipts preserved |
| Offline verifier for the archived chain | Completed by Codex; 83 repository tests passed after review corrections |
| Later attempt to have Claude implement that verifier | Timed out after 300 seconds; no retained complete proposal; no retry |

The later timeout does not replace the earlier successful Claude fixture
continuation. Its provider-request count, usage and invoice impact are unknown.
The planned Claude implementation handoff remains partially validated.

An independent Codex reviewer found two P2 issues in the initial verifier:
ignored Python imports in an altered checkout, and missing checks for linked
root ancestors. The host corrected both and passed seven acceptance tests and
the full suite (83). The original review and post-fix host verification are
separate records. A real Windows junction probe was unavailable in the sandbox;
ancestor-link regression coverage uses controlled predicates.

## Reproduce without an AI account

Requirements: Git and Python 3.12+. No dependencies to install. Local verification
was performed on Windows with Python 3.14; other environments need external
confirmation. Use a normal directory with no symlink/junction ancestors.
On Windows, use a short parent path and a short clone name; Claude desktop's
MSIX/AppData scratch paths can exceed Git's path-length limit. If cloning fails
with `Filename too long`, retry in a new short destination, preserving any
existing files. Do not change global Git settings or discard changes.

### Public branch: recommended entry point

The experimental branch is being submitted for external review, not merged into
the stable protocol. From a directory where the destination does not exist:

```text
git clone --config core.autocrlf=false --single-branch --branch experiment/hermes-pmp-adapter https://github.com/Mad-Max8063/project-memory-protocol-public.git pmp-hermes-review
cd pmp-hermes-review
git rev-parse HEAD
```

Record that outer source SHA in your review. The branch may receive follow-up
documentation; the three archived replay bundles remain pinned by the verifier.
Continue with the Windows or POSIX verification commands below. Post your
results in the review PR's conversation; do not post credentials or personal paths.

### Offline bundle: alternative transport

The review package contains `pmp-hermes-review.bundle` (source, this brief and
archived evidence), an entry-point README, a draft PR and a SHA-256 manifest.
Choose a new checkout directory. From the extracted
package directory:

```text
git clone --config core.autocrlf=false --branch experiment/hermes-pmp-adapter pmp-hermes-review.bundle pmp-hermes-review
cd pmp-hermes-review
git rev-parse HEAD
```

The checkout SHA must match `source_commit` in the package's `manifest.json`.
The earlier package is a local delivery artifact of its recorded source commit.
It remains independently usable and does not require the public branch or PR.
Review source and the manifest before executing code. Hashes establish
consistency within the delivered package, not independent publisher signatures.

On Windows PowerShell:

```powershell
git --version
python --version
$pmpReviewParent = Split-Path -Parent (Get-Location).Path
$pmpReviewTemp = Join-Path $pmpReviewParent ('pmp-review-tmp-' + [guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $pmpReviewTemp | Out-Null
$env:TEMP = $pmpReviewTemp
$env:TMP = $pmpReviewTemp
python -B experiments/hermes-pmp/verify_chain.py --json
```

On a POSIX shell (instructions supplied for external validation):

```sh
git --version
python3 --version
pmp_review_parent=$(cd .. && pwd -P)
export TMPDIR=$(mktemp -d "$pmp_review_parent/pmp-review-tmp.XXXXXX")
export TEMP="$TMPDIR"
export TMP="$TMPDIR"
python3 -B experiments/hermes-pmp/verify_chain.py --json
```

The temporary-directory settings apply to that shell. Keep this temporary root
outside the clone, with no symlink/junction ancestors, consistent with the
cross-runtime review prompt. The verifier cleans its temporary clones; the
empty external root may remain. These settings avoid inaccessible or linked
system-temp paths. For a repeat run, reuse the same external directory.

Success: exit code 0 and JSON with `verified: true`, `historical_inputs: 14`,
`acceptance_tests: 6`, three `bundle_sha256` entries and a nonempty `next_action`.
`final_commit` is `5e717267e23e39a854347ade7e9efa545269c227`: the archived fixture
continuation, distinct from the outer review package's source commit.
Likewise, JSON `next_action` belongs to that archived fixture repository at
`final_commit`, not to the current protocol repository. For today's task,
read the outer checkout's root `PROJECT_MEMORY.md`; do not apply the archived
action to it or treat a historical snapshot as current state.

The verifier checks three pinned bundle/report pairs, Git lineage and change
scope, historical inputs, proposals, host receipts, PMP decisions and handoffs.
It runs only the two trusted fixture test modules. Exit code 1 means invalid or
unavailable evidence; exit code 2 means invalid command usage.

Optional checks from the checkout root (use `python3` on POSIX):

```text
python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v
python -B -m unittest discover -s tests
```

Expected: seven verifier acceptance tests; 83 full repository tests. These
commands do not invoke Hermes, Claude, model APIs, OAuth or paid services.
Do not run live replay/provider commands to reproduce the archived evidence.

## Evidence to inspect

- [Verifier guide](replay-chain-verifier.md)
- [Original Hermes bridge](hermes-pmp-adapter.md)
- [Successful Claude continuation](hermes-claude-continuation.md)
- [Independent verifier review](../../experiments/hermes-pmp/evidence/chain-verifier-20261006/independent-review.md)
- [Post-review host checks](../../experiments/hermes-pmp/evidence/chain-verifier-20261006/final-checks.json)
- [Later Claude timeout](../../experiments/hermes-pmp/evidence/chain-verifier-20261006/claude-timeout.json)
- [Same-host runtime reproductions and maintainer assessment](../../experiments/hermes-pmp/evidence/reproductions/README.md)

The three archived bundles retain actual commits, snapshots, proposals and
receipts. Current state stays in each repository's `PROJECT_MEMORY.md`;
snapshots are historical evidence, not competing sources of current state.

## What the evidence does not establish

Git and hashes do not prove model identity, hidden session freshness, private
reasoning or the absence of hidden provider memory. This is a single small
task, not a reliability benchmark or a measurement of time/token savings.
Actual billing was not audited. No new services or credits were purchased.
The offline verification commands require no provider calls; existing live
results used available subscriptions. Remote CI and another machine's
reproduction are not established by the local evidence.

## External review request

For a unified copy/paste prompt for fresh Claude Code and Google Antigravity
sessions, see
[`hermes-cross-runtime-review-prompt.md`](hermes-cross-runtime-review-prompt.md).

Can you reproduce the archived result in a new checkout without receiving the
original chat history or configuring an AI account? Please report:

1. Source commit, operating system, Python and Git versions.
2. Exact command, exit code and verifier JSON (redact unrelated personal paths).
3. Whether the three bundles, 14 inputs and six fixture tests verified.
4. Whether the repository explains what happened, who proposed versus verified
   it, and what the next action is.
5. Any failure, confusing instruction or security finding.

Claude Code and Google Antigravity subsequently reported PASS from separate
clones of `8c96e926b0d28a182759c45c3a0141fa9a934eba` on the maintainer's Windows
machine. Both recorded exit 0, three bundles, fourteen inputs, six fixture tests
and seven verifier acceptance tests. The maintainer checked the clones and
digests and separately reran the bounded commands. Their original reports and
the assessment above retain the scope limits and documentation findings.
Reproduction on another machine remains the next success criterion; these
reports are not external-human review or certification of hidden freshness.
