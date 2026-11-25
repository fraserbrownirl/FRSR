#!/usr/bin/env python3
"""Copy generated site/below-banner.md into entropy-studio-vault for local/preview builds."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site" / "below-banner.md"
GENERATOR = ROOT / "scripts" / "generate-career-site.py"
DEFAULT_VAULT = Path.home() / "entropy-studio-vault"
DEST = DEFAULT_VAULT / "src" / "content" / "below-banner.md"


def main() -> None:
    ap = argparse.ArgumentParser(description="Sync below-banner.md to entropy-studio-vault")
    ap.add_argument(
        "--vault",
        type=Path,
        default=DEFAULT_VAULT,
        help=f"Path to entropy-studio-vault (default: {DEFAULT_VAULT})",
    )
    ap.add_argument(
        "--generate",
        action="store_true",
        help="Run generate-career-site.py before copying",
    )
    args = ap.parse_args()
    dest = args.vault / "src" / "content" / "below-banner.md"

    if args.generate:
        subprocess.run([sys.executable, str(GENERATOR)], check=True, cwd=ROOT)

    if not SOURCE.is_file():
        subprocess.run([sys.executable, str(GENERATOR)], check=True, cwd=ROOT)

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE, dest)
    print(f"Synced → {dest}")


if __name__ == "__main__":
    main()