# Project Memory Protocol Specification

- Version: `0.2.1`
- Status: Stable specification; repository lifecycle state is non-normative
- Canonical default path: `PROJECT_MEMORY.md` in the repository root

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** describe normative requirements.

## 1. Purpose

PMP defines a repository-native contract that lets humans and heterogeneous AI agents share current project state without sharing private conversational or model memory.

Git provides transport, authorship, ordering, and history. The canonical memory provides a compact snapshot of what is operationally true now.

## 2. Non-goals

PMP does not standardize:

- model internals, chat history, embeddings, or vector databases;
- task execution or agent orchestration;
- issue tracking, architecture records, or release management;
- automatic trust in unverified agent output;
- a specific vendor, model, repository host, or instruction filename.

## 3. Terms

- **Canonical memory:** the single current-state Markdown file all adapters reference.
- **Session record:** an optional immutable or append-only historical handoff.
- **Evidence:** a verifiable artifact supporting a memory claim, such as a commit, test result, issue, PR, runbook, or deployment record.
- **Human authority:** the person or group authorized to make product or operational decisions.
- **Reader:** a participant that consumes canonical memory.
- **Writer:** a participant authorized to update canonical memory.
- **Adapter:** a thin instruction that connects a tool or agent to the canonical memory.
- **Bounded handoff:** a task whose authorized outcome, change surface, or completion gate is explicitly limited.
- **Connected system:** a repository-linked service or resource whose state can be changed by project commands, credentials, automation, or configuration.
- **Consequential action:** an action that is persistent, externally visible, security-sensitive, destructive, costly, or difficult to reverse.
- **Consequential exclusion:** an explicit statement that a consequential action or connected system remains outside the current authority.
- **Material finding:** an observed fact outside the active task that could affect safety, correctness, authorization, or a later decision.
- **Actionable finding:** a material finding that still requires a decision, mitigation, verification, or bounded follow-up after the current session.

## 4. Repository layout

The default layout is:

```text
PROJECT_MEMORY.md
.project-memory/
`-- sessions/
    `-- YYYY-MM-DD-topic.md
```

A project MAY use another path. If it does, every adapter and relevant repository instruction MUST identify exactly the same canonical path. A project MUST NOT maintain multiple files that each claim to be canonical.

## 5. Canonical memory contract

The canonical memory MUST be UTF-8 Markdown and MUST contain these level-two headings exactly:

1. `## Identity`
2. `## Current state`
3. `## Active decisions`
4. `## Constraints`
5. `## Priorities`
6. `## Next action`
7. `## Evidence`
8. `## Update rules`

It SHOULD begin with a level-one project title and a short statement that it is canonical operational memory.

### 5.1 Content rules

The canonical memory:

- MUST describe current, actionable state rather than reproduce conversation history;
- MUST distinguish verified facts from documented but unverified claims and assumptions;
- MUST identify the human authority or decision owner;
- MUST contain one concrete next action, or explicitly state that no next action is selected;
- MUST link or point to evidence for claims about commits, tests, deployments, migrations, or production state;
- MUST identify the command or procedure actually observed when making a verification claim;
- MUST NOT contain secrets, credentials, private keys, access tokens, `.env` values, or unnecessary personal data;
- SHOULD remain short enough to read at session start;
- SHOULD replace superseded state instead of accumulating contradictory statements;
- MAY link to session records, issues, PRs, ADRs, runbooks, or technical reports.

Tests that mutate process-global or external state SHOULD isolate, serialize,
and restore that state. Time-dependent tests SHOULD use fixed instants when
incidental clock boundaries could change the result. These requirements govern
evidence quality without selecting a language, framework, runner, or provider.

### 5.2 Evidence labels

Claims about technical or external state MUST use one of these labels:

- `[VERIFIED]`: checked against current evidence during the stated session or timestamp.
- `[DOCUMENTED]`: copied from a trusted project artifact but not revalidated in the current session.
- `[ASSUMED]`: a working hypothesis that requires verification before a consequential action.

`[VERIFIED]` is scoped to the stated verifier, evidence, and time. By itself it does not mean the evidence is independent, third-party, CI-backed, durably archived, or proof of agent identity. When any of those properties matters, the memory MUST state it explicitly and link the supporting artifact.

An adapter or writer MAY use equivalent machine-readable metadata in a future version, but v0.1 requires the visible labels above.

## 6. Source precedence

When sources conflict, a conforming participant MUST apply this order:

1. latest explicit instruction from the authorized human;
2. current verified technical evidence;
3. canonical memory;
4. current specialized documentation;
5. historical session records and handoffs;
6. private model memory or conversational recollection.

Two conflicting sources at the same level MUST be verified or escalated to the human authority. The participant MUST NOT silently guess.

## 7. Session protocol

### 7.1 START

Before significant analysis or changes, a Reader MUST:

1. read repository-level instructions;
2. read the canonical memory;
3. load only task-relevant evidence;
4. verify branch, revision, worktree, and external state when the task depends on them;
5. state or resolve conflicts between the current request and recorded constraints.

The repository MUST version the minimum instructions required to locate and
interpret canonical memory, including its exact path and baseline PMP START
behavior. External tools, skills, or local instructions MAY add capabilities,
but their absence MUST NOT block baseline START.

### 7.2 DURING

A participant:

1. MUST NOT rewrite memory for minor implementation details;
2. MUST preserve the distinction between observation, documentation, and assumption;
3. SHOULD collect decision-changing facts and evidence for the END phase;
4. MUST treat a new authorized human decision as superseding an older contradictory decision;
5. MUST NOT expose sensitive information through memory or session records.
6. SHOULD identify both the allowed scope and relevant adjacent actions that
   remain unauthorized for every bounded handoff.
7. MUST state applicable consequential exclusions when connected systems could
   otherwise permit persistent, externally visible, security-sensitive, or
   difficult-to-reverse changes.
8. MUST NOT infer authority for merge, deployment, infrastructure, database,
   credential, secret, or environment changes merely because the positive task
   description does not mention them.
9. SHOULD record material findings outside the authorized scope as risks,
   blockers, or follow-up evidence without silently remediating them.

### 7.3 END

When a session changes operational state, an authorized Writer MUST:

1. verify what actually changed;
2. update the canonical memory to represent current state only;
3. update decisions, constraints, priorities, and next action as needed;
4. add evidence references;
5. record consequential work that was explicitly not performed when omission could cause a dangerous assumption;
6. create a session record when historical detail will help a future participant;
7. include memory changes in the same logical review/commit boundary as the state change, or in a clearly linked documentation commit.
8. publish mutually dependent canonical memory and handoff evidence atomically in one commit when either artifact directs the next participant to the other; an intermediate commit MUST NOT expose a next action whose required canonical state is not yet present.
9. promote an adjacent finding to canonical memory when it remains actionable,
   constrains later work, changes current risk, or blocks the next action.

If operational state did not change, a Writer SHOULD leave canonical memory untouched.
Recording or verifying an adjacent finding does not expand authorization. A
Reader or other participant without Writer authority MUST preserve the finding
in its handoff and request or propose the exact canonical update.

## 8. Session records

A session record SHOULD use `.project-memory/sessions/YYYY-MM-DD-topic.md` and SHOULD include:

- objective;
- actor and agent/tool when relevant;
- start and end revision or branch, if known;
- changes made;
- verification performed;
- decisions and constraints changed;
- risks or blockers;
- work intentionally excluded;
- exact next action;
- evidence references.

Session records are historical. They MUST NOT outrank canonical memory.

## 9. Adapter contract

An adapter MUST:

- name the exact canonical memory path;
- require START behavior before significant work;
- require END behavior after operational state changes;
- include or reference the source-precedence rule;
- prohibit secrets and unsupported factual claims;
- avoid copying current project state into the adapter.

An adapter SHOULD be short. Tool-specific details belong in the adapter; project state does not.

## 10. Concurrent updates and merge conflicts

Writers SHOULD update from the latest shared revision before editing. When a merge conflict occurs, they MUST resolve it semantically:

1. retain the newest verified state;
2. preserve still-active decisions and constraints;
3. remove superseded or duplicate statements;
4. retain evidence from both sides when still relevant;
5. escalate unresolved decision conflicts to the human authority.

Concatenating both versions without reconciliation is non-conforming.

## 11. Security and privacy

Repositories are copied, indexed, forked, and shared. Writers MUST assume memory may become visible to every repository reader. Secret scanning SHOULD include canonical memory and new session records before commit.

Sensitive external state SHOULD be referenced by stable identifier, not reproduced. Personal information MUST be minimized.

## 12. Compatibility and optional profiles

PMP `0.2.1` retains the canonical headings, default paths, evidence
labels, source precedence, and basic Reader/Writer/Adapter model from PMP
`0.1.1`. Existing `0.1.1` projects remain valid and are not required to adopt
this stable version.

The optional `PMP Evidence-backed Handoff` profile adds authority records,
independent review, persisted external verification, artifact metadata, claim
separation, and asynchronous evidence closure for higher-assurance work. Core
does not require that profile for routine handoffs.

Projects MUST NOT claim released PMP `0.2.1` conformance until a corresponding
final tag is separately human-authorized and created.

## 13. Conformance claims

A project MAY claim:

- `PMP 0.2.1 Reader` if START and precedence requirements are implemented;
- `PMP 0.2.1 Writer` if Reader requirements and END/update requirements are implemented;
- `PMP 0.2.1 Adapter` if Section 9 is implemented.

A conformance claim SHOULD identify the canonical path. A released conformance
claim additionally requires the separately authorized stable tag.

## 14. Success criterion

PMP succeeds when a fresh participant can quickly and correctly answer:

- Where are we?
- What is decided?
- What must not be changed?
- What remains?
- What happens next?
- What evidence supports those answers?

without requiring the human to reconstruct the previous conversation.
