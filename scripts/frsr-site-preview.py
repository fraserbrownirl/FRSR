#!/usr/bin/env python3
"""Local preview: live frsr.com hero (iframe) + generated below-banner.md."""

from __future__ import annotations

import argparse
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PREVIEW_DIR = ROOT / "site-preview"
BELOW = SITE / "below-banner.md"
GENERATOR = ROOT / "scripts" / "generate-career-site.py"
LIVE_URL = "https://frsr.com/"

sys.path.insert(0, str(ROOT / "scripts"))
from md_preview import markdown_to_html  # noqa: E402


def ensure_below_banner() -> str:
    if not BELOW.is_file():
        subprocess.run([sys.executable, str(GENERATOR)], check=True, cwd=ROOT)
    return BELOW.read_text(encoding="utf-8")


def build_page() -> bytes:
    md = ensure_below_banner()
    body_html = markdown_to_html(md)
    shell = (PREVIEW_DIR / "shell.html").read_text(encoding="utf-8")
    page = (
        shell.replace("{{LIVE_URL}}", LIVE_URL)
        .replace("{{BODY}}", body_html)
    )
    return page.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "frsr-site-preview/1.0"

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/style.css":
            data = (PREVIEW_DIR / "style.css").read_bytes()
            self._send(200, data, "text/css; charset=utf-8")
            return
        if path == "/":
            self._send(200, build_page(), "text/html; charset=utf-8")
            return
        self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/regenerate":
            self.send_error(404)
            return
        subprocess.run([sys.executable, str(GENERATOR)], check=True, cwd=ROOT)
        self._send_json(200, {"ok": True})

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict) -> None:
        import json

        body = json.dumps(payload).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def log_message(self, fmt: str, *args) -> None:
        if args and isinstance(args[0], str) and "favicon" in args[0]:
            return
        super().log_message(fmt, *args)


def main() -> None:
    ap = argparse.ArgumentParser(description="Preview frsr.com hero + below-banner locally")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8767)
    args = ap.parse_args()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Open http://{args.host}:{args.port}/")
    print("Hero loads from production (not in GitHub). Text dump from site/below-banner.md.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()