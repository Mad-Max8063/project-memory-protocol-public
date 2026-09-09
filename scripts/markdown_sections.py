"""Read PMP H2 sections without treating examples as headings.

This is a bounded Markdown reader, not a complete CommonMark implementation.
Fenced examples and HTML comments cannot supply section headings. Visible
quoted/inline/fenced action text is retained; profile fields use prose only.
"""

from __future__ import annotations

import re
import string
from typing import NamedTuple


class Section(NamedTuple):
    name: str
    body: str
    prose: str


def _comments(line: str, inside: bool, code: str | None, following: str) -> tuple[str, bool, str | None]:
    result: list[str] = []
    position = 0
    while position < len(line):
        if inside:
            end = line.find("-->", position)
            if end < 0:
                result.append("\n" if line.endswith("\n") else "")
                break
            position, inside = end + 3, False
        elif code is not None:
            closing = re.search(rf"(?<!`){re.escape(code)}(?!`)", line[position:])
            if closing is None:
                result.append(line[position:])
                break
            end = position + closing.end()
            result.append(line[position:end])
            position, code = end, None
        elif line[position] == "\\" and position + 1 < len(line) and line[position + 1] in string.punctuation:
            # Escapes apply outside code spans, including odd/even backslashes.
            result.append(line[position:position + 2])
            position += 2
        elif line.startswith("<!--", position):
            position, inside = position + 4, True
        elif line[position] == "`":
            run = re.match(r"`+", line[position:]).group()
            closing = re.search(rf"(?<!`){re.escape(run)}(?!`)", line[position + len(run):] + following)
            result.append(run)
            position += len(run)
            if closing:
                code = run
        else:
            result.append(line[position])
            position += 1
    return "".join(result), inside, code


def _paragraph_tail(lines: list[str], index: int) -> str:
    """Inline spans can cross soft line breaks, but not a new block."""
    tail: list[str] = []
    boundary = re.compile(r" {0,3}(?:#{1,6}(?:[ \t]|$)|`{3,}|~{3,}|>|(?:[-+*]|\d+[.)])[ \t]+|<!--)")
    # Block structure takes precedence over inline code. Include thematic
    # breaks and setext underlines; lookalikes with text/mixed marks do not.
    separator = re.compile(r" {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,}|=+[ \t]*|-+[ \t]*)")
    for line in lines[index + 1:]:
        if not line.strip() or boundary.match(line) or separator.fullmatch(line.rstrip("\r\n")):
            break
        tail.append(line)
    return "".join(tail)


def parse_sections(text: str) -> list[Section]:
    sections: list[Section] = []
    name: str | None = None
    body: list[str] = []
    prose: list[str] = []
    fence: str | None = None
    in_comment = False
    code: str | None = None
    lines = text.splitlines(keepends=True)
    for index, raw_line in enumerate(lines):
        if fence is not None:
            if re.fullmatch(rf" {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*", raw_line.rstrip("\r\n")):
                fence = None
            else:
                body.append(raw_line)
            continue

        line, in_comment, code = _comments(raw_line, in_comment, code, _paragraph_tail(lines, index))
        opening = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", line.rstrip("\r\n"))
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = opening[1]
            continue
        heading = re.fullmatch(r" {0,3}##[ \t]+(.+?)[ \t]*", line.rstrip("\r\n"))
        if heading:
            if name is not None:
                sections.append(Section(name, "".join(body).strip(), "".join(prose).strip()))
            name = re.sub(r"[ \t]+#+$", "", heading[1]).strip()
            body, prose = [], []
        else:
            body.append(line)
            prose.append(line)
    if name is not None:
        sections.append(Section(name, "".join(body).strip(), "".join(prose).strip()))
    return sections
