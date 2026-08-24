# Human-authored requirements

Implement `slugify(value: str) -> str` with these acceptance rules:

1. Trim surrounding whitespace.
2. Lowercase text.
3. Normalize with Unicode NFKD and discard remaining non-ASCII code points. This converts Latin letters with decomposable diacritics to ASCII (for example, `ó` to `o`); it is not general transliteration.
4. Replace each run of non-alphanumeric characters with one hyphen.
5. Remove leading and trailing hyphens.
6. Use only the Python standard library.

These requirements belong to the human authority. ChatGPT must first record them in canonical project memory without implementing code. A fresh Codex session must then implement them using only repository context.
