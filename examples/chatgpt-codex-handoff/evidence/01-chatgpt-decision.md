# Evidence 01 — ChatGPT records the decision

- Artifact type: reference demo evidence
- Actor: ChatGPT
- Human authority: demo operator
- Result: decision recorded; implementation not performed

## Human-approved behavior

The `slugify` function must:

1. trim surrounding whitespace;
2. lowercase text;
3. normalize with Unicode NFKD and discard remaining non-ASCII code points, converting Latin letters with decomposable diacritics to ASCII without claiming general transliteration;
4. replace each run of non-alphanumeric characters with one hyphen;
5. remove leading and trailing hyphens;
6. use only the Python standard library.

## Handoff boundary

ChatGPT updated project memory so the next actor could implement the behavior. It did not edit `slugify.py` and did not claim the tests passed.
