# PMP adapters

Adapters connect a tool-specific instruction surface to one canonical memory file. They contain behavior, never current project state.

Use the file that matches your environment:

- `AGENTS.md`: merge into a repository `AGENTS.md` or equivalent instructions read by coding agents.
- `CLAUDE.md`: merge into the project's Claude instructions.
- `GEMINI.md`: merge into the project's Gemini instructions.
- `CHATGPT.md`: reuse as project instructions or as the opening instruction when ChatGPT has repository access. This filename is a portable snippet, not an auto-discovery guarantee.

If your tool uses another instruction surface, adapt the same contract. All adapters MUST point to the same canonical path.

Do not replace existing repository safety, testing, or contribution rules. Add PMP alongside them.
