# Replay instructions

Canonical memory: `PROJECT_MEMORY.md` in this repository root (PMP 0.2.2).
START: read this file, memory, TASK.md and linked relevant evidence. Human
instruction > observed evidence > memory > docs > historical handoff > chat.
END: verify result and persist evidence, historical handoff and one next action
with canonical memory in the same Git commit. Never copy chat or secrets.
Allowed task: propose a replacement for fixture.json only. The bridge performs
bounded writes and fixed tests. Do not change tests, instructions or decisions.
No terminal/file/network tools for the model, deploy, purchases or destructive
operations. Logical actor labels do not certify model identity or freshness.
