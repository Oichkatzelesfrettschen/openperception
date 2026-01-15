#!/usr/bin/env python3
"""
Simple HTTP dev server with optional live-reload via SSE.

Usage:
  python3 tools/devserver.py --port 8000 --dir .

Add this tag to HTML pages to enable reload:
  <script src="/__livereload.js"></script>
"""
from __future__ import annotations

import argparse
import http.server
import io
import os
import socketserver
import sys
import threading
import time
from pathlib import Path
from typing import Set


ROOT = Path.cwd()
IGNORE_DIRS = {'.git', '__pycache__', '.idea', '.vscode', '.tox', 'node_modules', '.venv', 'venv'}
WATCH_EXT = {'.html', '.css', '.js', '.json', '.md', '.py', '.tex', '.sty'}


class LiveReloadRegistry:
    def __init__(self):
        self.clients: Set[http.server.BaseHTTPRequestHandler] = set()
        self.lock = threading.Lock()

    def register(self, handler):
        with self.lock:
            self.clients.add(handler)

    def unregister(self, handler):
        with self.lock:
            self.clients.discard(handler)

    def broadcast(self, msg: str):
        dead = []
        with self.lock:
            for h in list(self.clients):
                try:
                    h.wfile.write(f"data: {msg}\n\n".encode('utf-8'))
                    h.wfile.flush()
                except Exception:
                    dead.append(h)
            for h in dead:
                self.clients.discard(h)


REG = LiveReloadRegistry()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("[devserver] " + fmt % args + "\n")

    def do_GET(self):
        if self.path == '/__livereload.js':
            src = (
                "var es=new EventSource('/__events');"\
                "es.onmessage=function(e){if(e.data==='reload'){location.reload();}};"
            ).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Content-Length', str(len(src)))
            self.end_headers()
            self.wfile.write(src)
            return
        if self.path == '/__events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            REG.register(self)
            try:
                # Keep connection open
                while True:
                    time.sleep(60)
                    # heartbeat
                    self.wfile.write(b":\n\n")
                    self.wfile.flush()
            except Exception:
                pass
            finally:
                REG.unregister(self)
            return
        return super().do_GET()


def scan_mtimes(root: Path):
    mtimes = {}
    for p in root.rglob('*'):
        if p.is_dir():
            if p.name in IGNORE_DIRS:
                continue
            else:
                continue
        if p.suffix.lower() not in WATCH_EXT:
            continue
        try:
            mtimes[p] = p.stat().st_mtime
        except FileNotFoundError:
            pass
    return mtimes


def watch_thread(root: Path, interval: float = 0.5):
    prev = scan_mtimes(root)
    while True:
        time.sleep(interval)
        now = scan_mtimes(root)
        if now.keys() != prev.keys():
            REG.broadcast('reload')
            prev = now
            continue
        # Check changes
        changed = [p for p, m in now.items() if prev.get(p) != m]
        if changed:
            REG.broadcast('reload')
            prev = now


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=8000)
    ap.add_argument('--dir', default='.')
    ap.add_argument('--no-livereload', action='store_true')
    args = ap.parse_args()

    os.chdir(args.dir)
    root = Path(args.dir).resolve()
    handler = lambda *a, **kw: Handler(*a, directory=str(root), **kw)
    with socketserver.ThreadingTCPServer(('', args.port), handler) as httpd:
        print(f"Serving {root} on http://localhost:{args.port}")
        if not args.no_livereload:
            t = threading.Thread(target=watch_thread, args=(root,), daemon=True)
            t.start()
            print("Live-reload enabled. Add <script src=\"/__livereload.js\"></script> to pages.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")


if __name__ == '__main__':
    main()

