#!/usr/bin/env python3
"""Local console — edit the five story fields per experience page."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from career_schema import (  # noqa: E402
    FRONTMATTER_FIELDS,
    PROJECT_STATUSES,
    STORY_FIELDS,
    story_completion,
)
from experience_io import build_story_body, load_page, save_page  # noqa: E402

SITE = ROOT / "site"
EXPERIENCE = SITE / "experience"
CONSOLE_DIR = ROOT / "console-experience"
GENERATOR = SCRIPTS / "generate-career-site.py"


class Handler(BaseHTTPRequestHandler):
    server_version = "frsr-experience-console/2.0"

    def log_message(self, fmt: str, *args) -> None:
        if args and isinstance(args[0], str) and "/api" in args[0]:
            super().log_message(fmt, *args)

    def _send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _list_pages(self) -> list[dict]:
        out: list[dict] = []
        for path in sorted(EXPERIENCE.glob("*.md"), key=lambda p: p.stem):
            meta, _ = load_page(path)
            sf, st = story_completion(meta)
            out.append(
                {
                    "slug": path.stem,
                    "title": meta.get("title") or path.stem,
                    "story": {"filled": sf, "total": st},
                    "status": meta.get("status") or "",
                }
            )
        return out

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/schema":
            self._send_json(
                200,
                {
                    "fields": FRONTMATTER_FIELDS,
                    "story_fields": STORY_FIELDS,
                    "project_statuses": list(PROJECT_STATUSES),
                    "experience_dir": str(EXPERIENCE),
                },
            )
            return

        if path == "/api/pages":
            self._send_json(200, {"pages": self._list_pages()})
            return

        if path.startswith("/api/page/"):
            slug = path.removeprefix("/api/page/").strip("/")
            if not slug or "/" in slug:
                self.send_error(400)
                return
            file_path = EXPERIENCE / f"{slug}.md"
            if not file_path.is_file():
                self._send_json(404, {"error": "not found"})
                return
            meta, body = load_page(file_path)
            sf, st = story_completion(meta)
            self._send_json(
                200,
                {
                    "slug": slug,
                    "meta": meta,
                    "body": body,
                    "story": {"filled": sf, "total": st},
                },
            )
            return

        if path in ("/", "/index.html"):
            file_path = CONSOLE_DIR / "index.html"
        elif path.startswith("/"):
            file_path = CONSOLE_DIR / path.lstrip("/")
        else:
            file_path = CONSOLE_DIR / "index.html"

        if not file_path.is_file() or not str(file_path.resolve()).startswith(
            str(CONSOLE_DIR.resolve())
        ):
            self.send_error(404)
            return
        ct = "text/html; charset=utf-8"
        if file_path.suffix == ".css":
            ct = "text/css; charset=utf-8"
        elif file_path.suffix == ".js":
            ct = "application/javascript; charset=utf-8"
        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid JSON"})
            return

        if parsed.path == "/api/generate":
            proc = subprocess.run(
                [sys.executable, str(GENERATOR)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            if proc.returncode != 0:
                self._send_json(500, {"error": "generate failed", "stderr": proc.stderr[:2000]})
                return
            self._send_json(200, {"ok": True, "stdout": proc.stdout})
            return

        if parsed.path.startswith("/api/page/"):
            slug = parsed.path.removeprefix("/api/page/").strip("/")
            meta = payload.get("meta")
            if not slug or not isinstance(meta, dict):
                self._send_json(400, {"error": "expected meta object"})
                return
            body = build_story_body(meta, slug)
            try:
                save_page(EXPERIENCE / f"{slug}.md", meta, body)
            except OSError as e:
                self._send_json(500, {"error": str(e)})
                return
            sf, st = story_completion(meta)
            self._send_json(200, {"ok": True, "story": {"filled": sf, "total": st}})
            return

        self.send_error(404)


def main() -> None:
    ap = argparse.ArgumentParser(description="FRSR experience editor (localhost)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8766)
    args = ap.parse_args()
    EXPERIENCE.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Experience console: http://{args.host}:{args.port}/")
    httpd.serve_forever()


if __name__ == "__main__":
    main()