# Hermes PMP bridge — experimental, non-normative

Read the full experiment guide at docs/experiments/hermes-pmp-adapter.md in the
protocol repository. `adapter.py` imports existing Core code without modifying
it. `PROJECT_MEMORY.md` is always the canonical state in each target repository.

For the English external-review introduction, offline reproduction commands
and evidence boundaries, start with
[the review brief](../../docs/experiments/hermes-review-brief.md).

Local mock replay, from the protocol repo root:

```powershell
python experiments/hermes-pmp/replay.py --mode mock
python -m unittest -v tests/test_hermes_pmp_adapter.py
python experiments/hermes-pmp/verify_archive.py
```

The command prints its retained temporary run directory and fresh clone. It does
not install anything, connect to a model, publish or delete the result. The seed
intentionally fails two of its three acceptance checks before normalization.

Verify the saved historical replay without a provider:

```powershell
# Choose a NEW destination; never overwrite an existing checkout.
git clone experiments/hermes-pmp/evidence/replay.bundle <new-result-directory>
python experiments/hermes-pmp/continuation.py --root <new-result-directory>
```

The bundle stores baseline, input packet, output, test evidence, handoff and
canonical state in real local commits. The report labels producer mode `mock`.
Neither a fresh verifier process nor a successful mock proves real Hermes ran.

Live mode is optional and gated on a separately installed Hermes, an isolated
home, human subscription OAuth and an explicit human-selected model. See the
guide. No automatic install, paid API fallback, credit purchase or existing
Hermes profile reuse is performed. Do not run this against production.
