"""Minimal markdown → HTML for local frsr.com preview (no third-party deps)."""

from __future__ import annotations

import html
import re

_BLOCK = re.compile(r"\n{2,}")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_H1 = re.compile(r"^# (.+)$", re.M)
_H2 = re.compile(r"^## (.+)$", re.M)
_H3 = re.compile(r"^### (.+)$", re.M)
_HR = re.compile(r"^---\s*$", re.M)
_UL_ITEM = re.compile(r"^[-*] (.+)$", re.M)


def _inline(text: str) -> str:
    text = html.escape(text)
    text = _LINK.sub(r'<a href="\2">\1</a>', text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)
    return text


def _block(paragraph: str) -> str:
    p = paragraph.strip()
    if not p:
        return ""
    if m := _H1.fullmatch(p):
        return f"<h1>{_inline(m.group(1))}</h1>"
    if m := _H2.fullmatch(p):
        return f"<h2>{_inline(m.group(1))}</h2>"
    if m := _H3.fullmatch(p):
        return f"<h3>{_inline(m.group(1))}</h3>"
    if p == "---":
        return "<hr>"

    lines = p.split("\n")
    if all(_UL_ITEM.match(line) for line in lines):
        items = "".join(
            f"<li>{_inline(_UL_ITEM.match(line).group(1))}</li>" for line in lines
        )
        return f"<ul>{items}</ul>"

    if len(lines) == 1 and _UL_ITEM.match(lines[0]):
        return f"<p>{_inline(_UL_ITEM.match(lines[0]).group(1))}</p>"

  # Multi-line paragraph with possible list — rare in our dump; flatten to <br>
    inner = "<br>\n".join(_inline(line) for line in lines)
    return f"<p>{inner}</p>"


def markdown_to_html(source: str) -> str:
    source = _HR.sub("\n\n---\n\n", source)
    parts = _BLOCK.split(source.strip())
    return "\n".join(block for p in parts if (block := _block(p)))