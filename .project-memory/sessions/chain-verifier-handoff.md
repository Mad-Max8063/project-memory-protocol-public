# Session — offline replay-chain verifier implementation

- Date: 2026-10-06
- Human authority: Max, accepted bounded next step while connected remotely.
- Start revision: 966ced18c8ea540ad73ca942531ed7e9f9e64625
- Branch: experiment/hermes-pmp-adapter
- Implementing actor: Codex, logical participant.
- Intended next actor: independent Codex reviewer, no inherited conversation.
- Authorized scope: CHAIN_TASK.md; optional verifier, tests, docs and evidence.

The sole Claude invocation used the existing subscription login, no tools and
a selected thirteen-file public-code/evidence/task-memory packet. It timed out
after 300 seconds. No complete proposal or usage receipt was retained. There
was no retry, API fallback, new service or purchase. Codex completed the useful
command locally; Claude implementation success is not claimed.

The host verified the three archived bundle/report pairs, fourteen historical
input hashes, Git lineage/scope, preserved PMP decisions, evidence/handoff links,
final receipt and canonical next action. The six trusted fixture tests passed.
Six acceptance tests cover valid archives, read-only source preservation,
corruption before subprocess execution, missing/linked inputs, altered result,
missing handoff and CLI exit codes. Full discovery: 82 passed in 35.721 seconds.
Core memory/release gates passed; protected-file diff and whitespace checks passed.
Evidence: experiments/hermes-pmp/evidence/chain-verifier-20261006/host-checks.json.

Two execution details are recorded without modifying historical evidence:
the final old Codex receipt paraphrases its canonical next action; Python -I
requires an explicit trusted-module bootstrap for the two named tests.
The initial baseline run hit sandbox TEMP ACL errors; an accessible workspace
TEMP/TMP then passed all 76 baseline tests. The release CLI's relative root
resolved incorrectly in this sandbox; its explicit absolute root passed.

No Core, profile, previous archive or blocked track changed. No remote CI,
push, PR, merge, release or publication. Hashes establish integrity relative to
source pins, not identity, hidden freshness, authenticity or audited billing.

## Next action

Codex: independently verify the offline chain command and tamper rejection tests
from the repository, review scope and record a receipt. Read CHAIN_TASK.md,
docs/experiments/replay-chain-verifier.md and the linked task evidence. The
implementation was completed locally by Codex after the bounded Claude timeout.

## Closure addendum

The separate reviewer reconstructed the task from snapshot d37185b33437c2d30eeee6d424f42e4614acf164
and passed the command plus six original acceptance tests. Its two P2 findings
were corrected locally by the host: reject all untracked/ignored imports and
reject root/ancestor links before path use. Added nonexecution regression and
ancestor predicate checks; seven acceptance tests passed in 27.710s, full
discovery (83) passed in 44.141s. The final CLI -B test passed in 7.884s.
The source snapshot and reviewer receipt remain historical; final-checks.json
records corrected hashes and host verification. No second independent review.

Current next action: Max reviews the guide, independent receipt and final checks.
The bounded implementation is complete. Further model calls or publication need
a new scoped instruction. The planned Claude implementation remains partial;
the offline utility is complete and independently reviewed with host corrections.
