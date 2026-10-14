# External reproduction request — English social drafts

Prepared copy only. No social post, private message, reviewer assignment or paid
promotion has been sent. The review destination is
[experimental PR #8](https://github.com/Mad-Max8063/project-memory-protocol-public/pull/8).
Publication state remains in PROJECT_MEMORY.md, not in this copy template.

## X — short post

Can you independently verify an archived Hermes → Claude → Codex handoff?

PMP keeps project state + evidence in Git. The offline verifier needs no AI account or API keys.

Please report results or failures:
https://github.com/Mad-Max8063/project-memory-protocol-public/pull/8

## LinkedIn — post

Can an incoming AI agent continue a project from repository state instead of a chat transcript?

We built a small experimental Project Memory Protocol replay involving Hermes, Claude and Codex. PMP keeps current state, decisions, evidence and the next action in versioned project files. The runtimes remain optional participants; PMP Core is unchanged.

Hermes and Claude proposed bounded data changes. The host applied them and ran trusted tests. A separate Codex continuation recovered the result from the repository without inherited conversation turns.

Now we are looking for independent reproductions of the archived evidence.

You need Git and Python 3.12+. No AI account, API keys, dependencies to install or model calls are required for the offline verifier. It checks three replay bundles, 14 historical inputs and six fixture tests, plus the handoff and recoverable next action.

This is a bounded experiment, not an autonomy benchmark. Verifying its archive does not rerun the live models, and Git does not certify model identity or hidden session freshness. A later Claude implementation timeout is documented separately.

If you work on agent tooling, developer workflows or reproducibility, please try it and report your source commit, environment, verifier output and any failures in the PR conversation.

English instructions, source and evidence:
https://github.com/Mad-Max8063/project-memory-protocol-public/pull/8

## Manual publishing checklist

- Open the PR without authentication and confirm that its instructions are accessible.
- Use this experiment link, not the stable release as proof of these new results.
- Copy the X or LinkedIn section only, excluding headings/checklist.
- Do not claim external reproduction until a reviewer supplies checkable evidence.
- Do not describe archive verification as a new live multi-model replay.
- Review platform/community rules before any cross-post.
- Respond to failures and ask for the five-item report in the English brief.
- No automatic tagging, direct messaging or outreach is included.
