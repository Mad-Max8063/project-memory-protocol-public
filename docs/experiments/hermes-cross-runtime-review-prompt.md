# Independent runtime review prompt

Use this same prompt in a new Claude Code session and a new Google Antigravity
session. Each runtime should work from its own fresh clone. Do not give either
reviewer this conversation or the other reviewer's report.

```text
Act as a reproducibility reviewer for Project Memory Protocol (PMP).

OBJECTIVE

From a fresh checkout, reconstruct the experiment state and verify its evidence
using only the repository. This is a bounded check of archived evidence and
context recovery. Do not implement an integration or rerun live Hermes/Claude.

REPOSITORY

https://github.com/Mad-Max8063/project-memory-protocol-public

Branch: experiment/hermes-pmp-adapter
Exact commit: 8c96e926b0d28a182759c45c3a0141fa9a934eba
Review PR: https://github.com/Mad-Max8063/project-memory-protocol-public/pull/8

ISOLATION

- Use a new session with no imported earlier conversation.
- Create a separate fresh clone in a new folder. Do not reuse the author's
  checkout or another reviewer's clone.
- Do not consult this round's other review report. Historical evidence committed
  before the pinned commit is in scope.
- Do not rely on personal memory as project evidence. Record any automatically
  loaded context you know about; do not claim hidden context is absent.
- Do not delegate to subagents.

SCOPE AND SAFETY

You may clone the public repository, read it, run the commands below, create
temporary files, and write the final report in the authorized folder.

Do not modify tracked files, PROJECT_MEMORY.md, code, tests, instructions,
hashes or prior evidence. Do not commit, push, open/update a PR, merge, deploy
or post. Do not inspect credentials, private profiles or other projects. Do
not access or depend on the earlier Hermes/Argon experiment. Do not install
tools/dependencies, buy credits, activate services, or run live replay modes.

Use only currently available tools/access. Budget: about 15 minutes, one bounded
evaluation. If Git, Python, access or permissions are unavailable, document the
blocker; do not invent results or alter the experiment to make it pass.

PROCEDURE

1. Record runtime/tool and observable version, OS, Git and Python versions.
   Record the model only if visible, as tool-reported metadata, not certified
   identity.

2. Clone to a new folder. Replace the example destination below with a unique
   runtime name and UTC run ID, for example
   pmp-review-claude-code-20261006T170000Z:

   git clone --config core.autocrlf=false --single-branch --branch experiment/hermes-pmp-adapter https://github.com/Mad-Max8063/project-memory-protocol-public.git <NEW_DIRECTORY>

3. In the clone, confirm it starts clean; pin the exact commit:

   git status --porcelain
   git switch --detach 8c96e926b0d28a182759c45c3a0141fa9a934eba
   git rev-parse HEAD

   If the initial checkout is dirty or the SHA differs, stop and explain.
   Do not discard changes automatically.

4. Read AGENTS.md and PROJECT_MEMORY.md first. Before running tests, save
   your initial reconstruction provisionally OUTSIDE the clone:
   objective, current state, decisions/constraints, available evidence, exact
   next action, what the repository claims, and what you have not verified.

5. Read applicable experiment instructions. Review these before execution:

   docs/experiments/hermes-review-brief.md
   docs/experiments/replay-chain-verifier.md
   experiments/hermes-pmp/verify_chain.py

   Inspect the code first. If you find an unsafe operation, document it and
   do not run it.

6. Prepare a new writable temporary folder OUTSIDE the clone. Use paths with
   no symlink/junction ancestors. Set TEMP and TMP to that folder; on POSIX
   also set TMPDIR. Do not create .review-tmp inside the clone. Use Python
   3.12+. If unavailable, report BLOCKED and do not install it.

7. From the clone root, run once and preserve the exact command, stdout, stderr
   and exit code:

   python -B experiments/hermes-pmp/verify_chain.py --json

   Use python3 where appropriate. Check exit 0, verified=true, three
   bundle_sha256 entries, historical_inputs=14, acceptance_tests=6 and a
   nonempty next_action. Distinguish the outer repository HEAD from the
   archived replay's final_commit.

8. Run once:

   python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v

   Seven tests are expected. Record actual output and exit code, including
   failures. The full 83-test suite need not be repeated.

9. Compare the initial reconstruction with executed evidence. Assess whether
   the repository makes clear what happened, who proposed changes, who wrote
   files, who ran tests, what remains pending and the exact next action.

10. Before saving final reports, run:

    git diff --exit-code
    git diff --cached --exit-code
    git status --porcelain

    Do not delete or revert unexpected differences; document them.

REPORTS IN THE REPOSITORY

Only after completing the checks, create this folder in your clone:

experiments/hermes-pmp/evidence/reproductions/<runtime>/<run-id>/

Use runtime claude-code or google-antigravity, and a unique UTC timestamp for
run-id. Save:

- REVIEW.md
- verifier.json, only if valid JSON was produced;
- execution.log

Do not fabricate JSON. Keep captured output in execution.log. REVIEW.md must be
in English and include runtime/environment/exact commit; known context and
isolation limits; initial reconstruction; actual commands/results; evidence
supporting conclusions; failures/ambiguities/risks; detected checkout changes;
what was not tested; verdict PASS, PARTIAL, FAIL or BLOCKED with reasons; and
one recommended next action.

Redact credentials or unnecessary personal data if they unexpectedly appear;
state which category was redacted. Never invent or alter results.

FINAL CHECK

- git diff and git diff --cached must remain empty.
- git status may show only your new reports folder.
- Explain any other difference.
- Do not commit or push.
- Report the exact absolute folder containing your reports.
- Do not delete the clone or results. The project maintainer will review and
  incorporate the reports into the public branch later.

EVIDENCE LIMITS

This checks archived evidence and context recovery. It does not demonstrate a
new live model execution, general autonomy, certified model identity or the
absence of hidden memory.

If this runs on the author's computer, call the result “separate-runtime
reproduction on the same host,” not reproduction on another machine or human
external review.

A model assertion is not a substitute for a command actually executed. Failures
are useful evidence; do not force PASS.
```
