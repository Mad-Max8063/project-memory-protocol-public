# Project Memory Protocol

Persistent, model-agnostic project memory for humans and AI agents.

Project Memory Protocol (PMP) is a small, Git-native convention for preserving the current operational state of a project across tools, models, sessions, and people. It does not synchronize private model memory. It gives every participant the same versioned source to read and update.

> Human decisions -> Git -> canonical project memory <- any compatible agent

Status: **stable protocol line: Core `0.2.1`; Evidence-backed Handoff profile `0.1.1`**

Repository tag, GitHub Release, publication, deployment, and visibility state
is tracked in [canonical memory](PROJECT_MEMORY.md), not encoded as a timeless
protocol status.

[Stable specification](SPEC.md) · [Quick start](#five-minute-setup) · [Upgrade guide](docs/UPGRADING_0.1.1_TO_0.2.1.md) · [Evidence profile](profiles/evidence-backed-handoff/PROFILE.md) · [Verified handoff example](examples/chatgpt-codex-handoff/README.md) · [Release notes](docs/RELEASE_NOTES_0.2.1.md) · [Distribution provenance](docs/PROVENANCE.md)

## The problem in one minute

AI agents can read repository instructions, but a new session still needs to recover what is currently true: active decisions, verified work, constraints, blockers, and the exact next action. Chat transcripts and vendor-specific memory do not provide a portable project handoff.

PMP stores that operational state in one small, versioned Markdown file:

```text
Human decision
    -> PROJECT_MEMORY.md
    -> fresh agent reads current state
    -> agent performs and verifies work
    -> PROJECT_MEMORY.md advances
    -> next human or agent continues from Git
```

The result is model-agnostic continuity with a reviewable audit trail. PMP does not copy hidden model memory or claim that Git metadata proves which model performed the work.

## Why PMP?

Instruction files such as `AGENTS.md` are good at explaining how to work in a repository. They are not, by themselves, a reliable record of what is currently true, what was decided, what is blocked, and what should happen next.

PMP adds that missing operational layer:

- one concise canonical memory file;
- explicit evidence levels;
- deterministic source precedence;
- START, DURING, and END session behavior;
- optional session records for historical traceability;
- thin adapters for different agent instruction surfaces.

## Five-minute setup

1. Copy `templates/PROJECT_MEMORY.md` to `PROJECT_MEMORY.md` in your repository root.
2. Fill in only facts that are current and useful for the next session.
3. Copy or merge the relevant snippet from `adapters/` into your agent instruction file.
4. Commit the memory and adapter with the project.
5. At the end of meaningful work, update current state and next action before handing off.

The canonical path may be changed, but every adapter MUST point to the same file.

## Repository contents

```text
project-memory-protocol/
|-- PROJECT_MEMORY.md
|-- SPEC.md
|-- templates/
|   |-- PROJECT_MEMORY.md
|   `-- SESSION.md
|-- adapters/
|   |-- AGENTS.md
|   |-- CLAUDE.md
|   |-- GEMINI.md
|   `-- CHATGPT.md
|-- examples/
|   `-- chatgpt-codex-handoff/
|-- scripts/
|   |-- validate_memory.py
|   |-- validate_profile_record.py
|   `-- validate_release_candidate.py
|-- profiles/
|   `-- evidence-backed-handoff/
|-- docs/
|   |-- UPGRADING_0.1.1_TO_0.2.1.md
|   |-- RELEASE_NOTES_0.2.1.md
|   |-- DEMO_SCRIPT.md
|   `-- PROVENANCE.md
|-- CONTRIBUTING.md
|-- SECURITY.md
`-- CHANGELOG.md
```

## Core rule

The memory is a synthesis of current operational truth, not a transcript and not a second issue tracker. Keep detail in commits, issues, ADRs, runbooks, and session records; link to that evidence from the canonical memory.

## Conformance

- **PMP Reader:** loads the canonical memory before significant work and respects its constraints.
- **PMP Writer:** also updates it when operational state changes, without turning assumptions into facts.
- **PMP Adapter:** makes Reader/Writer behavior discoverable in a tool-specific instruction surface without copying project state.

See [SPEC.md](SPEC.md) for normative requirements.

## Validate a memory file

Requires Python 3 and no third-party packages.

```bash
python scripts/validate_memory.py PROJECT_MEMORY.md
```

Run the included handoff verification:

```bash
python scripts/validate_memory.py examples/chatgpt-codex-handoff/fixtures/before/PROJECT_MEMORY.md
python scripts/validate_memory.py examples/chatgpt-codex-handoff/fixtures/after/PROJECT_MEMORY.md
python examples/chatgpt-codex-handoff/verify_demo.py
```

For a blind live demonstration, create a separate disposable repository from `examples/chatgpt-codex-handoff/seed/`. Do not run the interoperability claim directly against this repository because its completed fixtures are intentionally inspectable.

## Verifiable evidence

The included artifact provides three evidence layers:

1. deterministic fixtures and executable tests that anyone can run locally;
2. a completed ChatGPT-to-Codex-to-ChatGPT evidence chain;
3. GitHub Actions release gates for compilation, memory validation, the packaged demo, and the intentionally incomplete seed.

The strongest public claim is therefore narrow and reproducible: PMP can preserve explicit operational state across independent agent sessions through repository context. External agent identity and session freshness require separate recording or platform evidence; the protocol does not infer them from Git authorship.

See the [live demo runbook](examples/chatgpt-codex-handoff/LIVE_DEMO_RUNBOOK.md) for the public verification procedure and [release notes](docs/RELEASE_NOTES_0.2.1.md) for the stable `v0.2.1` scope.

## Public verified replay

The separate
[`pmp-public-replay-01`](https://github.com/Mad-Max8063/pmp-public-replay-01)
repository provides an anonymously accessible blind replay with a four-commit
Human -> ChatGPT -> Codex -> ChatGPT chain:

1. [human baseline](https://github.com/Mad-Max8063/pmp-public-replay-01/commit/69573d2350327400d4c894ffd253beb10644174a);
2. [ChatGPT decision](https://github.com/Mad-Max8063/pmp-public-replay-01/commit/4d35d087eb8dd32e33b81754ff497e5adc8957ff);
3. [Codex implementation](https://github.com/Mad-Max8063/pmp-public-replay-01/commit/7cf171277fd33f7e7d24207b356cbb3210132f5c);
4. [fresh ChatGPT verification](https://github.com/Mad-Max8063/pmp-public-replay-01/commit/a4e6469a4257f32809b9405946b07fd2ef3e8416).

The [final GitHub Actions run](https://github.com/Mad-Max8063/pmp-public-replay-01/actions/runs/32791128976)
reports seven passing acceptance tests and
`REPLAY STAGE VERIFIED: chatgpt-verification`. The replay demonstrates
repository-mediated operational continuity. In accordance with PMP's evidence
boundaries, Git history alone does not prove hidden model identity, reasoning,
or session freshness.

## Stable protocol line

The stable protocol line integrates the accepted real-pilot findings into two
layers:

- [PMP Core 0.2.1](SPEC.md) is a self-contained specification for
  ordinary Reader and Writer workflows.
- [Evidence-backed Handoff profile](profiles/evidence-backed-handoff/PROFILE.md)
  adds authority records, persisted external verification, artifact metadata,
  claim separation, and asynchronous evidence closure for higher-assurance
  handoffs.

Core `0.2.1` and profile `0.1.1` preserve the normative behavior of the
accepted `0.2.0` line while correcting lifecycle metadata. The
[canonical memory](PROJECT_MEMORY.md) records current repository state. See the
[upgrade guide](docs/UPGRADING_0.1.1_TO_0.2.1.md) for compatibility and
[distribution provenance](docs/PROVENANCE.md) for the clean-history boundary.

## Design boundaries

PMP intentionally does not define a hosted service, database, vector store, agent framework, or hidden-memory synchronization mechanism. Git remains the transport and audit trail.

## Distribution boundary

This repository is a clean, self-contained distribution of the protocol. It
does not include private product history, internal release planning, or
operational evidence from unrelated repositories. See
[docs/PROVENANCE.md](docs/PROVENANCE.md).

## License

MIT. See [LICENSE](LICENSE).
