"""Tests for the browser-backed rendered spatial audit."""
# ruff: noqa: I001
from __future__ import annotations

import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rendered_spatial_check import Viewport, browser_is_available, run_rendered_spatial_audit
from validators.base import Status


pytestmark = pytest.mark.skipif(
    not browser_is_available(),
    reason="Playwright browser runtime is unavailable",
)


def write_page(path: Path, *, style: str, body: str) -> None:
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
                f"<body>{body}</body>",
                "</html>",
            ]
        )
    )


def test_rendered_spatial_audit_passes_on_wrapping_surface(tmp_path: Path) -> None:
    page_path = tmp_path / "index.html"
    write_page(
        page_path,
        style="\n".join(
            [
                "body { margin: 0; }",
                "main { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 1rem; padding: 1rem; }",
                ".toolbar { display: flex; flex-wrap: wrap; gap: .5rem; }",
                ".swatch-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: .5rem; }",
                ".focus-ring:focus { outline: 3px solid #2255cc; outline-offset: 2px; }",
                ".swatch { min-height: 40px; background: #ddd; }",
            ]
        ),
        body="\n".join(
            [
                '<div class="toolbar"><button class="focus-ring">One</button><button>Two</button><button>Three</button></div>',
                '<main><div class="swatch-grid"><div class="swatch"></div><div class="swatch"></div><div class="swatch"></div></div></main>',
            ]
        ),
    )

    result = run_rendered_spatial_audit(
        root=tmp_path,
        page_paths=(Path("index.html"),),
        viewports=(Viewport(320, 700),),
    )

    assert result.status == Status.PASS
    assert any(
        check.name == "index.html@320x700/page_horizontal_overflow" and check.status == Status.PASS
        for check in result.checks
    )
    assert any(
        check.name == "index.html@320x700/focus_visible:.focus-ring:0" and check.status == Status.PASS
        for check in result.checks
    )


def test_rendered_spatial_audit_fails_on_page_overflow(tmp_path: Path) -> None:
    page_path = tmp_path / "index.html"
    write_page(
        page_path,
        style="body { margin: 0; } .toolbar { display: flex; flex-wrap: nowrap; }",
        body='<div style="width: 420px; height: 20px; background: #ddd;"></div><div class="toolbar"><button>One</button><button>Two</button><button>Three</button></div>',
    )

    result = run_rendered_spatial_audit(
        root=tmp_path,
        page_paths=(Path("index.html"),),
        viewports=(Viewport(320, 700),),
    )

    assert result.status == Status.FAIL
    assert any(
        check.name == "index.html@320x700/page_horizontal_overflow" and check.status == Status.FAIL
        for check in result.checks
    )


def test_rendered_spatial_audit_fails_when_focus_is_clipped(tmp_path: Path) -> None:
    page_path = tmp_path / "index.html"
    write_page(
        page_path,
        style="\n".join(
            [
                "body { margin: 0; padding: 1rem; }",
                ".frame { width: 140px; overflow: hidden; border: 1px solid #999; }",
                ".focus-ring { position: relative; left: 110px; width: 60px; }",
                ".focus-ring:focus { outline: 3px solid #2255cc; outline-offset: 2px; }",
            ]
        ),
        body='<div class="frame"><button class="focus-ring">Go</button></div>',
    )

    result = run_rendered_spatial_audit(
        root=tmp_path,
        page_paths=(Path("index.html"),),
        viewports=(Viewport(320, 700),),
    )

    assert result.status == Status.FAIL
    assert any(
        check.name == "index.html@320x700/focus_visible:.focus-ring:0" and check.status == Status.FAIL
        for check in result.checks
    )
