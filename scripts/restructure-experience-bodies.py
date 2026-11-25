#!/usr/bin/env python3
"""Normalize experience page bodies to four sections (Amplify structure)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIENCE = ROOT / "site" / "experience"
sys.path.insert(0, str(ROOT / "scripts"))

from experience_io import build_story_body, load_page, save_page  # noqa: E402


def main() -> None:
    for path in sorted(EXPERIENCE.glob("*.md")):
        meta, _ = load_page(path)
        body = build_story_body(meta, path.stem)
        save_page(path, meta, body)
        print(path.name)
    print(f"Restructured {len(list(EXPERIENCE.glob('*.md')))} pages.")


if __name__ == "__main__":
    main()