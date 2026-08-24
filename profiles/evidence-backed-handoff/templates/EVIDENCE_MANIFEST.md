# External evidence manifest — <topic>

## Subject

- Repository or project: `<identifier>`
- Branch or ref: `<branch or ref>`
- Verified revision: `<exact immutable revision>`
- Recorded at: `<timestamp and timezone>`

## Verification

- Platform: `<CI or external verifier>`
- Runner context: `<OS, runtime, or relevant environment>`
- Run ID: `<identifier>`
- Run URL: `<stable URL>`
- Conclusion: `<success, failure, cancelled, or other observed state>`
- Gates observed:
  - `<command or gate>` -> `<observed result>`

## Artifacts

- Artifact ID: `<identifier or none>`
- Name: `<name or none>`
- Digest: `<algorithm:value or unavailable>`
- Retention or expiry: `<timestamp, policy, or unavailable>`

## External state

- Effective permissions: `<relevant permissions>`
- Deployment or promotion state: `<success, failure, blocked, absent, or not checked>`
- Adjacent findings: `<finding and scope disposition, or none>`

## Evidence boundaries

- `<what this manifest proves>`
- `<what it does not prove, including identity or session freshness>`

## Closure

- Evidence-record location: `<path at the commit containing this manifest>`
- Stopping rule: `<how recursive evidence commits are prevented>`
- Exact next action: `<one bounded action or none>`
