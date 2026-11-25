#!/usr/bin/env python3
"""Remove legacy agent-metadata keys from experience pages."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from career_schema import LEGACY_KEYS, infer_project_status, prune_meta  # noqa: E402
from experience_io import build_story_body, load_page, save_page  # noqa: E402

EXPERIENCE = ROOT / "site" / "experience"


def main() -> None:
    for path in sorted(EXPERIENCE.glob("*.md")):
        meta, _ = load_page(path)
        for key in LEGACY_KEYS:
            meta.pop(key, None)
        if not meta.get("status"):
            meta["status"] = infer_project_status(meta)
        meta = prune_meta(meta)
        body = build_story_body(meta, path.stem)
        save_page(path, meta, body)
        print(path.name)
    print("done")


if __name__ == "__main__":
    main()