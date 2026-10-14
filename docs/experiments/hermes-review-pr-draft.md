# Draft PR — ready for human review, not submitted

Source branch: `experiment/hermes-pmp-adapter`

Suggested base: `main`; refresh the actual comparison before submission.
The local base snapshot is not evidence that the current remote main is unchanged.

## Title

experiment: demonstrate repository-based Hermes/Claude/Codex handoffs

## Body

PMP lets an incoming participant recover project state, decisions, evidence and
the next action from the repository. This experimental branch adds a thin
optional file bridge, a small archived Hermes/Claude/Codex fixture replay, and
an offline command for auditing the complete evidence chain.

Hermes proposed normalized fixture labels; Claude proposed a derived manifest.
The host applied these bounded data proposals and ran trusted tests. Separate
Codex continuations reconstructed state from repository evidence without
inherited conversation turns. Models did not execute the fixture tests.

The branch keeps PMP Core 0.2.2, the specification, profiles and existing adapters
unchanged. It introduces no mandatory Hermes/Claude/provider dependency.
Implementation remains experimental and MIT-licensed.

Verification from the checkout root, with Git and Python 3.12+:

```text
python -B experiments/hermes-pmp/verify_chain.py --json
python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v
python -B -m unittest discover -s tests
```

Observed locally on Windows: three bundles, 14 historical inputs and six fixture
tests verified; seven verifier acceptance tests and 83 repository tests passed.
Core memory/release gates passed. Use the temporary-directory setup and package
instructions in `docs/experiments/hermes-review-brief.md` for reproduction.

The independent review identified ignored-import and ancestor-link boundaries
in the initial verifier. The host corrected both and added regression coverage.
The original review and final host checks are preserved separately.

A later, separate Claude implementation attempt timed out after five minutes
without a retained complete proposal. Codex implemented the verifier locally;
that attempted implementation handoff remains partial. The earlier successful
Claude fixture handoff is preserved independently. No retry, purchase or API
fallback occurred for the later attempt; usage and invoice impact are unknown.

Review requested: reproduce the archived result from a new checkout, inspect
the evidence/next action and assess portability and security boundaries. The
offline commands need no AI account, API key or provider access.

Git/JSON integrity is not model identity, session-freshness or autonomy proof.
Comparative savings, external-machine reproduction and remote CI have not been
established. This is a bounded deterministic fixture, not general reliability.

Start with `docs/experiments/hermes-review-brief.md`. Detailed evidence and limits
are in `docs/experiments/replay-chain-verifier.md` and
`experiments/hermes-pmp/evidence/chain-verifier-20261006/`.

## Maintainer note

This is a prepared description, not an existing GitHub PR. Publication and any
merge decision remain separate human actions. No stable tag/release or Core
version change is part of this review package.
