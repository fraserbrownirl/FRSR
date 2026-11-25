"""Read/write experience markdown with YAML front matter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

STORY_SECTIONS: tuple[tuple[str, str], ...] = (
    ("Structural problem", "structural_problem"),
    ("Insight", "insight"),
    ("What Fraser did", "what_fraser_did"),
    ("Status", "outcome"),
)


def build_story_body(meta: dict[str, Any], slug: str) -> str:
    title = str(meta.get("title") or slug.replace("-", " ").title())
    parts = [f"# {title}", ""]
    for heading, key in STORY_SECTIONS:
        parts.append(f"## {heading}")
        parts.append("")
        val = meta.get(key)
        text = val.strip() if isinstance(val, str) else ""
        if text:
            parts.append(text)
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def split_document(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end]
    meta = yaml.safe_load(block) or {}
    if not isinstance(meta, dict):
        meta = {}
    body = text[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    meta.pop("moves", None)
    return meta, body


def compose_document(meta: dict[str, Any], body: str) -> str:
    meta = {k: v for k, v in meta.items() if k != "moves" and not str(k).startswith("_")}
    dump = yaml.dump(
        meta,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=88,
    )
    return f"---\n{dump}---\n\n{body.rstrip()}\n"


def load_page(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    return split_document(text)


def save_page(path: Path, payload: dict[str, Any], body: str) -> None:
    from career_schema import prune_meta

    meta = prune_meta({k: v for k, v in payload.items() if not str(k).startswith("_")})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(compose_document(meta, body), encoding="utf-8")