#!/usr/bin/env python3
"""List FRSR studio projects from projects/*.md frontmatter."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"

REQUIRED = ("slug", "name", "github", "visibility", "studio_class", "status")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = val[1:-1]
        data[key] = val
    return data


def split_tags(raw: str) -> list[str]:
    if not raw or raw == "[]":
        return []
    parts = re.split(r"[,\s]+", raw.strip("[]"))
    return [p.strip().strip("'\"") for p in parts if p.strip().strip("'\"")]


def linkedin_url(meta: dict[str, str]) -> str | None:
    if meta.get("linkedin_url"):
        return meta["linkedin_url"]
    klass = meta.get("studio_class", "")
    if klass in ("oss-live", "private-live"):
        return meta.get("live_url") or None
    if klass == "oss-repo":
        return meta.get("readme_url") or (
            f"https://github.com/{meta['github']}#readme" if meta.get("github") else None
        )
    if klass == "private-pages":
        return meta.get("pages_url") or None
    return None


def validate(meta: dict[str, str]) -> list[str]:
    errs: list[str] = []
    for key in REQUIRED:
        if not meta.get(key):
            errs.append(f"missing {key}")
    klass = meta.get("studio_class", "")
    if klass in ("oss-live", "private-live") and not meta.get("live_url"):
        errs.append(f"{klass} requires live_url")
    if klass == "private-pages" and not meta.get("pages_url"):
        errs.append("private-pages requires pages_url")
    vis = meta.get("visibility", "")
    if vis == "public" and klass == "private-live":
        errs.append("visibility public conflicts with private-live")
    if vis == "private" and klass == "oss-live":
        errs.append("visibility private conflicts with oss-live")
    if vis == "private" and klass == "oss-repo":
        errs.append("visibility private conflicts with oss-repo")
    url = linkedin_url(meta)
    if not url:
        errs.append("cannot compute linkedin_url")
    return errs


def load_projects() -> list[tuple[Path, dict[str, str], list[str]]]:
    out: list[tuple[Path, dict[str, str], list[str]]] = []
    if not PROJECTS.is_dir():
        return out
    for path in sorted(PROJECTS.glob("*.md")):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        errs = validate(meta)
        out.append((path, meta, errs))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Query FRSR project registry")
    ap.add_argument("--slug", help="Single project slug")
    ap.add_argument("--class", dest="klass", help="Filter studio_class")
    ap.add_argument("--tag", help="Filter tag substring")
    ap.add_argument("--visibility", choices=["public", "private"])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = load_projects()
    if args.slug:
        rows = [r for r in rows if r[1].get("slug") == args.slug]
    if args.klass:
        rows = [r for r in rows if r[1].get("studio_class") == args.klass]
    if args.visibility:
        rows = [r for r in rows if r[1].get("visibility") == args.visibility]
    if args.tag:
        rows = [
            r for r in rows if args.tag.lower() in " ".join(split_tags(r[1].get("tags", ""))).lower()
        ]

    payload = []
    exit_code = 0
    for path, meta, errs in rows:
        if errs:
            exit_code = 1
        entry = {
            "slug": meta.get("slug"),
            "name": meta.get("name"),
            "github": meta.get("github"),
            "visibility": meta.get("visibility"),
            "studio_class": meta.get("studio_class"),
            "status": meta.get("status"),
            "headline": meta.get("headline"),
            "linkedin_url": linkedin_url(meta),
            "live_url": meta.get("live_url") or None,
            "pages_url": meta.get("pages_url") or None,
            "errors": errs,
            "file": str(path.relative_to(ROOT)),
        }
        payload.append(entry)

    if args.json:
        print(json.dumps(payload, indent=2))
        return exit_code

    if not payload:
        print("No projects matched.", file=sys.stderr)
        return 1 if args.slug else 0

    for e in payload:
        flag = " !" if e["errors"] else ""
        print(f"{e['slug']}{flag}\t{e['studio_class']}\t{e['linkedin_url']}\t{e['name']}")
        for err in e["errors"]:
            print(f"  error: {err}", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())