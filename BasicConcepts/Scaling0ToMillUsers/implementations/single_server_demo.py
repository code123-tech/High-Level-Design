#!/usr/bin/env python3
"""
Single-Server Demo
==================
This lightweight script represents the very first stage of the scaling journey:
everything on one machine.  It spawns Python's built-in HTTP server (port 8000)
and exposes a **very** small key-value API to mimic an app + DB living together.

Endpoints
---------
GET /
    Show a welcome page with usage instructions.

GET /set?key=<k>&value=<v>
    Save *v* under key *k* in the in-memory store.

GET /get?key=<k>
    Retrieve value for key *k*.  404 if absent.

Run directly or via the quick-start launcher:
    python single_server_demo.py
Press CTRL-C to stop.
"""
from __future__ import annotations

import html
import http.server
import os
import socketserver
from typing import Dict
from urllib.parse import parse_qs, urlparse

_PORT = 8000
_STORE: Dict[str, str] = {}


class _Handler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler implementing our tiny key-value API."""

    def do_GET(self):  # noqa: N802 – HTTP verb naming
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self._respond(
                200,
                """
                <h1>📦 Single-Server Demo</h1>
                <p>This machine hosts <em>everything</em>—application + DB.</p>
                <p>Try:
                   <code>/set?key=name&value=alice</code><br>
                   then <code>/get?key=name</code></p>""",
            )
            return

        if path == "/set":
            qs = parse_qs(parsed.query)
            key = qs.get("key", [""])[0]
            value = qs.get("value", [""])[0]
            if not key:
                self._respond(400, "Missing 'key' query param")
                return
            _STORE[key] = value
            self._respond(200, f"Saved {html.escape(key)} = {html.escape(value)}")
            return

        if path == "/get":
            qs = parse_qs(parsed.query)
            key = qs.get("key", [""])[0]
            value = _STORE.get(key)
            if value is None:
                self._respond(404, f"Key '{html.escape(key)}' not found")
            else:
                self._respond(200, value)
            return

        # Default to static file behaviour
        super().do_GET()

    # ---------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------
    def _respond(self, status: int, body: str) -> None:  # noqa: D401
        body_bytes = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)


def main() -> None:
    host = os.environ.get("HOST", "localhost")
    with socketserver.TCPServer(("", _PORT), _Handler) as httpd:
        print(f"🏃  Serving on http://{host}:{_PORT}  (CTRL+C to quit)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑  Shutting down…")


if __name__ == "__main__":
    main() 