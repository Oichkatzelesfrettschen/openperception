"""Tests for the browser-backed rendered cognitive audit."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rendered_cognitive_check import Viewport, run_rendered_cognitive_audit
from rendered_spatial_check import browser_is_available
from validators.base import Status


pytestmark = pytest.mark.skipif(
    not browser_is_available(),
    reason="Playwright browser runtime is unavailable",
)


def write_page(path: Path, *, body_attrs: str, style: str, body: str) -> None:
    path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<html>",
                "<head>",
                '<meta name="viewport" content="width=device-width, initial-scale=1" />',
                "<style>",
                style,
                "</style>",
                "</head>",
                f"<body {body_attrs}>{body}</body>",
                "</html>",
            ]
        )
    )


def test_rendered_cognitive_audit_passes_on_compact_simple_surface(
    tmp_path: Path,
) -> None:
    page_path = tmp_path / "index.html"
    write_page(
        page_path,
        body_attrs='data-hud-complexity="simple"',
        style="\n".join(
            [
                "body { margin: 0; font: 16px/1.4 sans-serif; }",
                ".page-nav, .demo-actions { display: flex; flex-wrap: wrap; gap: .5rem; }",
                ".card { padding: 1rem; }",
            ]
        ),
        body="\n".join(
            [
                '<nav class="page-nav" data-density-region="nav"><a href="#a">A</a><a href="#b">B</a><a href="#c">C</a></nav>',
                '<details data-density-region="summary"><summary>Summary</summary><p>Short summary.</p></details>',
                '<div class="card" data-density-region="demo"><div class="demo-actions" data-primary-actions="true"><button>One</button><button>Two</button></div></div>',
                '<div data-density-region="controls"><select><option>Default</option></select></div>',
                '<p role="status" aria-live="polite">Ready</p>',
            ]
        ),
    )

    result = run_rendered_cognitive_audit(
        root=tmp_path,
        page_paths=(Path("index.html"),),
        viewports=(Viewport(320, 700),),
    )

    assert result.status == Status.PASS
    assert any(
        check.name == "index.html@320x700/visible_controls"
        and check.status == Status.PASS
        for check in result.checks
    )


def test_rendered_cognitive_audit_fails_on_crowded_simple_surface(
    tmp_path: Path,
) -> None:
    page_path = tmp_path / "index.html"
    controls = "".join(f"<button>Action {index}</button>" for index in range(1, 8))
    nav_links = "".join(
        f'<a href="#n{index}">Item {index}</a>' for index in range(1, 7)
    )
    write_page(
        page_path,
        body_attrs='data-hud-complexity="simple"',
        style="\n".join(
            [
                "body { margin: 0; font: 16px/1.4 sans-serif; }",
                ".page-nav, .toolbar, .controls, .pill-row, .demo-actions { display: flex; flex-wrap: wrap; gap: .5rem; }",
            ]
        ),
        body="\n".join(
            [
                f'<nav class="page-nav" data-density-region="nav">{nav_links}</nav>',
                '<details data-density-region="summary"><summary>Summary</summary><p>Dense summary.</p></details>',
                f'<div class="toolbar" data-density-region="toolbar">{controls}</div>',
                f'<div class="controls" data-density-region="controls">{controls}</div>',
                f'<div class="pill-row" data-density-region="extra">{controls}</div>',
                '<p role="status" aria-live="polite">Ready</p>',
                '<p role="status" aria-live="polite">Another notice</p>',
            ]
        ),
    )

    result = run_rendered_cognitive_audit(
        root=tmp_path,
        page_paths=(Path("index.html"),),
        viewports=(Viewport(320, 700),),
    )

    assert result.status == Status.FAIL
    assert any(
        check.name == "index.html@320x700/visible_controls"
        and check.status == Status.FAIL
        for check in result.checks
    )
