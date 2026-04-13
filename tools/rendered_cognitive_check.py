#!/usr/bin/env python3
"""
Browser-backed cognitive density audit for rendered first-screen burden.

WHY: The static cognitive validator can reason about declared structure, but it
cannot tell how many controls and regions actually compete for attention in the
initial viewport. This tool measures first-screen visible burden in Chromium.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rendered_spatial_check import (
    _launch_browser,
    browser_is_available,
    serve_directory,
)
from validators.base import CheckResult, GateResult, Severity, Status


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
RENDERED_GATE_ID = "GATE-006R"
RENDERED_GATE_NAME = "COGNITIVE_RENDERED"
HUD_VISIBLE_CONTROL_THRESHOLDS = {
    "minimal": (4, 6),
    "simple": (8, 10),
    "full": (12, 14),
}
HUD_VISIBLE_REGION_THRESHOLDS = {
    "minimal": (3, 4),
    "simple": (5, 6),
    "full": (5, 6),
}
HUD_VISIBLE_CLUSTER_THRESHOLDS = {
    "minimal": (3, 4),
    "simple": (6, 7),
    "full": (8, 10),
}
HUD_VISIBLE_NOTIFICATION_THRESHOLDS = {
    "minimal": (1, 1),
    "simple": (1, 2),
    "full": (1, 2),
}


class Viewport(tuple):
    __slots__ = ()

    def __new__(cls, width: int, height: int):
        return super().__new__(cls, (width, height))

    @property
    def width(self) -> int:
        return int(self[0])

    @property
    def height(self) -> int:
        return int(self[1])

    @property
    def label(self) -> str:
        return f"{self.width}x{self.height}"


def _make_result() -> GateResult:
    return GateResult(
        gate_id=RENDERED_GATE_ID,
        gate_name=RENDERED_GATE_NAME,
        severity=Severity.WARNING,
    )


def _relative_url(page_path: Path) -> str:
    return "/" + page_path.as_posix().lstrip("/")


def _status_for_count(value: int, thresholds: tuple[int, int]) -> Status:
    passed, warned = thresholds
    if value <= passed:
        return Status.PASS
    if value <= warned:
        return Status.WARN
    return Status.FAIL


def _measure_page(page) -> dict[str, object]:
    return page.evaluate(
        """() => {
          const visible = (el) => {
            const style = getComputedStyle(el);
            if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
              return false;
            }
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0 && rect.bottom > 0 && rect.top < window.innerHeight;
          };
          const uniqueCount = (selectors) => {
            const seen = new Set();
            for (const selector of selectors) {
              for (const el of document.querySelectorAll(selector)) {
                if (visible(el)) {
                  seen.add(el);
                }
              }
            }
            return seen.size;
          };

          const body = document.body;
          return {
            hudMode: body?.dataset?.hudComplexity || null,
            visibleControls: uniqueCount([
              'a',
              'button',
              'select',
              'summary',
              'textarea',
              'input:not([type=hidden])'
            ]),
            visibleRegions: uniqueCount([
              '[data-density-region]'
            ]),
            visibleClusters: uniqueCount([
              '.page-nav',
              '.toolbar',
              '.controls',
              '.pill-row',
              '.demo-actions',
              '[data-primary-actions]',
              '[data-density-region]'
            ]),
            visibleNotifications: uniqueCount([
              '[role=status]',
              '[role=alert]',
              '[aria-live]',
              '[data-notification]'
            ]),
          };
        }"""
    )


def run_rendered_cognitive_audit(
    *,
    root: Path = DEFAULT_ROOT,
    page_paths: tuple[Path, ...] = DEFAULT_PAGE_PATHS,
    viewports: tuple[Viewport, ...] = tuple(
        Viewport(*item) for item in DEFAULT_VIEWPORTS
    ),
) -> GateResult:
    result = _make_result()
    if not browser_is_available():
        result.checks.append(
            CheckResult(
                name="rendered/browser_available",
                status=Status.WARN,
                message="Playwright browser runtime is unavailable",
            )
        )
        return result

    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright

    try:
        with serve_directory(root) as base_url, sync_playwright() as playwright:
            browser = _launch_browser(playwright, timeout=10000)
            try:
                for viewport in viewports:
                    page = browser.new_page(
                        viewport={"width": viewport.width, "height": viewport.height}
                    )
                    try:
                        for page_path in page_paths:
                            page.goto(
                                base_url + _relative_url(page_path),
                                wait_until="networkidle",
                                timeout=10000,
                            )
                            if page_path.name == "palette-compare.html":
                                page.wait_for_selector(".lane", timeout=10000)
                            data = _measure_page(page)
                            hud_mode = str(data["hudMode"] or "full")

                            control_count = int(data["visibleControls"])
                            region_count = int(data["visibleRegions"])
                            cluster_count = int(data["visibleClusters"])
                            notification_count = int(data["visibleNotifications"])

                            result.checks.append(
                                CheckResult(
                                    name=f"{page_path.name}@{viewport.label}/visible_controls",
                                    status=_status_for_count(
                                        control_count,
                                        HUD_VISIBLE_CONTROL_THRESHOLDS[hud_mode],
                                    ),
                                    message=(
                                        f"{control_count} visible control(s) in first viewport for {hud_mode} HUD"
                                    ),
                                    value=float(control_count),
                                    threshold=float(
                                        HUD_VISIBLE_CONTROL_THRESHOLDS[hud_mode][0]
                                    ),
                                )
                            )
                            result.checks.append(
                                CheckResult(
                                    name=f"{page_path.name}@{viewport.label}/visible_regions",
                                    status=_status_for_count(
                                        region_count,
                                        HUD_VISIBLE_REGION_THRESHOLDS[hud_mode],
                                    ),
                                    message=(
                                        f"{region_count} visible density region(s) in first viewport for {hud_mode} HUD"
                                    ),
                                    value=float(region_count),
                                    threshold=float(
                                        HUD_VISIBLE_REGION_THRESHOLDS[hud_mode][0]
                                    ),
                                )
                            )
                            result.checks.append(
                                CheckResult(
                                    name=f"{page_path.name}@{viewport.label}/visible_clusters",
                                    status=_status_for_count(
                                        cluster_count,
                                        HUD_VISIBLE_CLUSTER_THRESHOLDS[hud_mode],
                                    ),
                                    message=(
                                        f"{cluster_count} visible cluster(s) in first viewport for {hud_mode} HUD"
                                    ),
                                    value=float(cluster_count),
                                    threshold=float(
                                        HUD_VISIBLE_CLUSTER_THRESHOLDS[hud_mode][0]
                                    ),
                                )
                            )
                            result.checks.append(
                                CheckResult(
                                    name=f"{page_path.name}@{viewport.label}/visible_notifications",
                                    status=_status_for_count(
                                        notification_count,
                                        HUD_VISIBLE_NOTIFICATION_THRESHOLDS[hud_mode],
                                    ),
                                    message=(
                                        f"{notification_count} visible notification region(s) in first viewport for {hud_mode} HUD"
                                    ),
                                    value=float(notification_count),
                                    threshold=float(
                                        HUD_VISIBLE_NOTIFICATION_THRESHOLDS[hud_mode][0]
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
    return Viewport(int(width_text), int(height_text))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a rendered cognitive audit with Playwright.",
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
    result = run_rendered_cognitive_audit(
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
