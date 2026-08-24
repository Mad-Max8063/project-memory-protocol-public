# Live demo runbook

Goal: produce a screen-recorded and Git-verifiable handoff between independent ChatGPT and Codex sessions, with no human retransmission of project state.

## Isolated repository requirement

- Create a new disposable private repository containing **only** the contents of `seed/`.
- Do not run the claimed blind demo inside this protocol repository: it contains completed fixtures and would expose the expected answer.
- Verify that the seed's first commit contains no `evidence/` files or `.project-memory/sessions/` records.
- Run `python verify_demo.py` and record its expected baseline failure.
- Do not paste ChatGPT's conversation into Codex.

## Recording sequence

### 1. ChatGPT decision

Open a fresh ChatGPT conversation with access only to the isolated repository. Use this prompt:

> Continue the project using only its repository instructions and canonical memory. Complete the exact next action and commit the handoff. Do not implement code.

ChatGPT must translate the human requirements from `TASK.md` into repository memory and evidence only. Commit the canonical memory update and its evidence together as one atomic decision commit; do not expose either half in an intermediate commit. Show:

- the fresh conversation;
- the memory diff;
- the evidence diff in the same commit;
- the commit SHA and timestamp.

### 2. Fresh Codex handoff

Open a new Codex task on the same repository. The only prompt should be:

> Continue the project from its repository instructions and canonical memory. Implement and verify the exact next action, then perform the PMP END handoff. Do not ask me to restate prior context.

Show Codex reading the canonical memory, implementing the function, running tests, updating memory, and creating a session record. Commit the result as a second distinct commit.

### 3. Fresh ChatGPT verification

Open a new ChatGPT conversation with repository access. Ask:

> Based only on the repository and its canonical project memory, tell me what was decided, what Codex completed, what evidence verifies it, and what should happen next.

ChatGPT should recover all four answers without the human restating them.

### 4. Mechanical verification

Run in the isolated repository:

```bash
python verify_demo.py
```

Show the passing output and the Git log containing the baseline, ChatGPT-decision, and Codex-implementation commits.

## Pass criteria

- The Codex prompt contains no hidden decision details.
- The isolated repository contains no completed fixtures or answers in its baseline commit.
- The baseline verifier fails before the handoff.
- Both fresh sessions identify the repository-root `PROJECT_MEMORY.md` as canonical.
- The implementation passes all six tests.
- Canonical memory advances from implementation pending to implementation verified.
- Evidence links to the agent session and test result.
- ChatGPT reconstructs the state and next action from the repository alone.
- Every published commit is internally actionable: no handoff evidence points to canonical decisions that are absent at that commit.
- The final evidence package distinguishes Git-inspectable facts, agent-recorded execution claims, and independently persisted execution evidence.
- A public claim links either a CI run/artifact or an uncut recording that shows the verification commands and results.
- Git author metadata is not presented as proof that a named model acted or that a session was fresh; those limitations are disclosed.
- No production repository, deployment, database, or `main` branch is touched.

## Recording note

Keep the final video around 60–90 seconds. Show the decision, the context-free Codex prompt, the passing verifier, and the fresh ChatGPT recovery. Publish the full Git history and any CI run or artifact beside the video so viewers can inspect the evidence and its limits.
