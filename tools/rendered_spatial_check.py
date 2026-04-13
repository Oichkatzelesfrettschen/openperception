#!/usr/bin/env python3
"""
Browser-backed spatial audit for rendered layout safety.

WHY: The static spatial gate can now catch many declared layout risks, but it
still cannot observe the browser's actual scroll and overflow behavior. This
tool adds a first renderer-backed audit over repo-owned example pages using
Playwright and a temporary local HTTP server.
"""

# ruff: noqa: I001
from __future__ import annotations

import argparse
import contextlib
import http.server
import json
import socketserver
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from validators.base import CheckResult, GateResult, Severity, Status

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright
except Exception:  # pragma: no cover - exercised through runtime fallback
    PlaywrightError = RuntimeError
    sync_playwright = None


if TYPE_CHECKING:
    from collections.abc import Iterator


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO_ROOT
DEFAULT_PAGE_PATHS = (
    Path("examples/ui/variant-toggle.html"),
    Path("examples/ui/palette-compare.html"),
)
DEFAULT_VIEWPORTS = (
    (320, 900),
    (768, 900),
)
DEFAULT_ROW_SELECTORS = (
    ".page-nav",
    ".toolbar",
    ".controls",
    ".pill-row",
    ".demo-actions",
    ".swatch-grid",
)
DEFAULT_FOCUS_SELECTORS = (
    ".focus-ring",
    "button",
    "select",
    "summary",
    '[tabindex="0"]',
)
RENDERED_GATE_ID = "GATE-004R"
RENDERED_GATE_NAME = "SPATIAL_RENDERED"
LAUNCH_ARGS = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]


@dataclass(frozen=True)
class Viewport:
    width: int
    height: int

    @property
    def label(self) -> str:
        return f"{self.width}x{self.height}"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        del fmt, args


class _ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def _make_result() -> GateResult:
    return GateResult(
        gate_id=RENDERED_GATE_ID,
        gate_name=RENDERED_GATE_NAME,
        severity=Severity.WARNING,
    )


def browser_is_available() -> bool:
    if sync_playwright is None:
        return False
    try:
        with sync_playwright() as playwright:
            browser = _launch_browser(playwright, timeout=5000)
            browser.close()
        return True
    except Exception:
        return False


@contextlib.contextmanager
def serve_directory(root: Path) -> Iterator[str]:
    def handler(*args, **kwargs):
        return _QuietHandler(*args, directory=str(root), **kwargs)

    server = _ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address[:2]
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1.0)


def _relative_url(page_path: Path) -> str:
    return "/" + page_path.as_posix().lstrip("/")


def _launch_browser(playwright, *, timeout: int):
    last_error = None
    for attempt in range(2):
        try:
            return playwright.chromium.launch(
                headless=True,
                timeout=timeout,
                args=LAUNCH_ARGS,
            )
        except PlaywrightError as exc:
            last_error = exc
            if attempt == 0:
                time.sleep(0.25)
                continue
            raise
    raise last_error


def _measure_page(
    page,
    row_selectors: tuple[str, ...],
    focus_selectors: tuple[str, ...],
) -> list[dict[str, object]]:
    return page.evaluate(
        """({rowSelectors, focusSelectors}) => {
          const tolerance = 1;
          const checks = [];
          const root = document.documentElement;
          const clipsOverflow = (style) => {
            return ['hidden', 'clip', 'scroll', 'auto'].includes(style.overflow)
              || ['hidden', 'clip', 'scroll', 'auto'].includes(style.overflowX)
              || ['hidden', 'clip', 'scroll', 'auto'].includes(style.overflowY);
          };
          checks.push({
            name: "page_horizontal_overflow",
            ok: root.scrollWidth <= window.innerWidth + tolerance,
            message: `document ${root.scrollWidth}px vs viewport ${window.innerWidth}px`,
            value: root.scrollWidth,
            threshold: window.innerWidth
          });

          const main = document.querySelector("main");
          if (main) {
            checks.push({
              name: "main_horizontal_overflow",
              ok: main.scrollWidth <= main.clientWidth + tolerance,
              message: `main ${main.scrollWidth}px vs client ${main.clientWidth}px`,
              value: main.scrollWidth,
              threshold: main.clientWidth
            });
          } else {
            checks.push({
              name: "main_horizontal_overflow",
              ok: true,
              message: "No main element on page",
              value: null,
              threshold: null
            });
          }

          for (const selector of rowSelectors) {
            const nodes = Array.from(document.querySelectorAll(selector));
            nodes.forEach((node, index) => {
              const rect = node.getBoundingClientRect();
              if (rect.width <= 0 || rect.height <= 0) {
                return;
              }
              checks.push({
                name: `row_overflow:${selector}:${index}`,
                ok: node.scrollWidth <= node.clientWidth + tolerance,
                message: `${selector} scroll ${node.scrollWidth}px vs client ${node.clientWidth}px`,
                value: node.scrollWidth,
                threshold: node.clientWidth
              });
            });
          }
          for (const selector of focusSelectors) {
            const nodes = Array.from(document.querySelectorAll(selector));
            nodes.forEach((node, index) => {
              if (typeof node.focus !== 'function') {
                return;
              }
              node.focus();
              const rect = node.getBoundingClientRect();
              if (rect.width <= 0 || rect.height <= 0) {
                return;
              }
              const style = getComputedStyle(node);
              const outlineWidth = parseFloat(style.outlineWidth || '0') || 0;
              const outlineOffset = parseFloat(style.outlineOffset || '0') || 0;
              const focusMargin = Math.max(2, outlineWidth + Math.max(0, outlineOffset));
              let clippedBy = null;
              let ancestor = node.parentElement;
              while (ancestor) {
                const ancestorStyle = getComputedStyle(ancestor);
                if (clipsOverflow(ancestorStyle)) {
                  const ancestorRect = ancestor.getBoundingClientRect();
                  const clipped =
                    rect.left - focusMargin < ancestorRect.left - tolerance ||
                    rect.top - focusMargin < ancestorRect.top - tolerance ||
                    rect.right + focusMargin > ancestorRect.right + tolerance ||
                    rect.bottom + focusMargin > ancestorRect.bottom + tolerance;
                  if (clipped) {
                    clippedBy = ancestor.className
                      ? `${ancestor.tagName.toLowerCase()}.${ancestor.className}`
                      : ancestor.tagName.toLowerCase();
                    break;
                  }
                }
                ancestor = ancestor.parentElement;
              }
              const withinViewport =
                rect.left >= -tolerance &&
                rect.top >= -tolerance &&
                rect.right <= window.innerWidth + tolerance &&
                rect.bottom <= window.innerHeight + tolerance;
              checks.push({
                name: `focus_visible:${selector}:${index}`,
                ok: withinViewport && !clippedBy,
                message: clippedBy
                  ? `${selector} focus treatment is clipped by ${clippedBy}`
                  : `${selector} focus treatment fits within viewport bounds`,
                value: rect.right + focusMargin,
                threshold: window.innerWidth
              });
            });
          }
          return checks;
        }""",
        {
            "rowSelectors": list(row_selectors),
            "focusSelectors": list(focus_selectors),
        },
    )


def run_rendered_spatial_audit(
    *,
    root: Path = DEFAULT_ROOT,
    page_paths: tuple[Path, ...] = DEFAULT_PAGE_PATHS,
    viewports: tuple[Viewport, ...] = tuple(
        Viewport(*item) for item in DEFAULT_VIEWPORTS
    ),
    row_selectors: tuple[str, ...] = DEFAULT_ROW_SELECTORS,
    focus_selectors: tuple[str, ...] = DEFAULT_FOCUS_SELECTORS,
) -> GateResult:
    result = _make_result()
    if sync_playwright is None:
        result.checks.append(
            CheckResult(
                name="rendered/browser_available",
                status=Status.WARN,
                message="Playwright is not importable in this environment",
            )
        )
        return result

    try:
        with serve_directory(root) as base_url, sync_playwright() as playwright:
            browser = _launch_browser(playwright, timeout=10000)
            try:
                for viewport in viewports:
                    page = browser.new_page(
                        viewport={
                            "width": viewport.width,
                            "height": viewport.height,
                        }
                    )
                    try:
                        for page_path in page_paths:
                            page.goto(
                                base_url + _relative_url(page_path),
                                wait_until="networkidle",
                                timeout=10000,
                            )
                            for measurement in _measure_page(
                                page,
                                row_selectors,
                                focus_selectors,
                            ):
                                status = (
                                    Status.PASS
                                    if bool(measurement["ok"])
                                    else Status.FAIL
                                )
                                result.checks.append(
                                    CheckResult(
                                        name=(
                                            f"{page_path.name}@{viewport.label}/"
                                            f"{measurement['name']}"
                                        ),
                                        status=status,
                                        message=str(measurement["message"]),
                                        value=(
                                            float(measurement["value"])
                                            if measurement["value"] is not None
                                            else None
                                        ),
                                        threshold=(
                                            float(measurement["threshold"])
                                            if measurement["threshold"] is not None
                                            else None
                                        ),
                                    )
                                )
                    finally:
                        page.close()
            finally:
                browser.close()
    except PlaywrightError as exc:
        result.checks.append(
            CheckResult(
                name="rendered/browser_available",
                status=Status.WARN,
                message=f"Playwright launch failed: {exc}",
            )
        )

    return result


def _parse_viewport(value: str) -> Viewport:
    width_text, height_text = value.lower().split("x", 1)
    return Viewport(width=int(width_text), height=int(height_text))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a rendered spatial audit with Playwright.",
    )
    parser.add_argument(
        "--root",
        default=str(DEFAULT_ROOT),
        help="Root directory to serve over HTTP.",
    )
    parser.add_argument(
        "--page",
        action="append",
        help="Page path relative to --root. May be passed multiple times.",
    )
    parser.add_argument(
        "--viewport",
        action="append",
        help="Viewport in WIDTHxHEIGHT form. May be passed multiple times.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of text output.",
    )
    return parser.parse_args()


def _result_to_json(result: GateResult) -> dict[str, object]:
    return {
        "gate_id": result.gate_id,
        "gate_name": result.gate_name,
        "severity": result.severity.value,
        "status": result.status.value,
        "checks": [
            {
                "name": check.name,
                "status": check.status.value,
                "message": check.message,
                "value": check.value,
                "threshold": check.threshold,
            }
            for check in result.checks
        ],
    }


def main() -> int:
    args = parse_args()
    page_paths = (
        tuple(Path(item) for item in args.page) if args.page else DEFAULT_PAGE_PATHS
    )
    viewports = (
        tuple(_parse_viewport(item) for item in args.viewport)
        if args.viewport
        else tuple(Viewport(*item) for item in DEFAULT_VIEWPORTS)
    )
    result = run_rendered_spatial_audit(
        root=Path(args.root),
        page_paths=page_paths,
        viewports=viewports,
    )
    if args.json:
        print(json.dumps(_result_to_json(result), indent=2))
    else:
        print(result)
    return 0 if result.status != Status.FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
