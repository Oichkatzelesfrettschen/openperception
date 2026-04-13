"""Tests for the first spatial validator gate."""

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validators.base import Status
from validators.spatial import SpatialGate


def write_spacing(
    path: Path, *, min_target: int = 44, min_spacing: int = 8, outline: int = 2
) -> None:
    payload = {
        "interactive": {
            "touch": {
                "minTarget": {"value": min_target},
                "minSpacing": {"value": min_spacing},
            },
            "focus": {
                "outlineWidth": {"value": outline},
            },
        }
    }
    path.write_text(json.dumps(payload))


def write_css(
    path: Path,
    *,
    underline: bool = True,
    outline_px: int = 3,
    outline_offset_px: int = 2,
) -> None:
    text_decoration = "underline" if underline else "none"
    path.write_text(
        "\n".join(
            [
                ".link {",
                f"  text-decoration: {text_decoration};",
                "}",
                ".focus-ring:focus {",
                f"  outline: {outline_px}px solid #abcdef;",
                f"  outline-offset: {outline_offset_px}px;",
                "}",
                ".btn-primary, .btn-secondary {",
                "  min-width: 44px;",
                "  min-height: 44px;",
                "}",
            ]
        )
    )


def write_html(
    path: Path,
    *,
    include_viewport: bool = True,
    wrap_selector: str = ".page-nav",
    wrap_enabled: bool = True,
    include_media_query: bool = True,
    include_main: bool = False,
    main_template: str = "repeat(auto-fit, minmax(min(100%, 320px), 1fr))",
    main_padding: str = "1rem",
    include_swatch_grid: bool = False,
    swatch_grid_template: str = "repeat(auto-fit, minmax(110px, 1fr))",
    body: str = '<div class="card focus-ring" tabindex="0"></div>',
) -> None:
    media_parts = ["body { padding: 1rem; }"]
    if include_main:
        media_parts.append("main { padding: 1rem; }")
    media_block = (
        "@media (max-width: 640px) { " + " ".join(media_parts) + " }"
        if include_media_query
        else ""
    )
    wrap_block = (
        f"{wrap_selector} {{ display: flex; flex-wrap: wrap; gap: .5rem; }}"
        if wrap_enabled
        else f"{wrap_selector} {{ display: flex; gap: .5rem; }}"
    )
    main_block = (
        f"main {{ display: grid; grid-template-columns: {main_template}; gap: 1rem; padding: {main_padding}; }}"
        if include_main
        else ""
    )
    swatch_block = (
        f".swatch-grid {{ display: grid; grid-template-columns: {swatch_grid_template}; gap: .5rem; }}"
        if include_swatch_grid
        else ""
    )
    viewport = (
        '<meta name="viewport" content="width=device-width, initial-scale=1" />'
        if include_viewport
        else ""
    )
    path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<html>",
                "<head>",
                viewport,
                "<style>",
                wrap_block,
                main_block,
                swatch_block,
                media_block,
                "</style>",
                "</head>",
                (
                    f'<body><nav class="page-nav">One</nav><main>{body}</main></body>'
                    if include_main
                    else f'<body><nav class="page-nav">One</nav>{body}</body>'
                ),
                "</html>",
            ]
        )
    )


def test_spatial_gate_passes_on_valid_static_surface(tmp_path: Path) -> None:
    spacing = tmp_path / "spacing.json"
    css = tmp_path / "tokens.css"
    html = tmp_path / "example.html"
    write_spacing(spacing)
    write_css(css)
    write_html(html)

    gate = SpatialGate(
        spacing_json_path=spacing,
        css_path=css,
        html_paths=(html,),
    )
    result = gate.validate()

    assert result.status == Status.PASS


def test_spatial_gate_fails_on_duplicate_class_and_missing_focus_ring(
    tmp_path: Path,
) -> None:
    spacing = tmp_path / "spacing.json"
    css = tmp_path / "tokens.css"
    html = tmp_path / "example.html"
    write_spacing(spacing, min_target=40)
    write_css(css, underline=False, outline_px=1)
    write_html(
        html,
        include_viewport=False,
        wrap_enabled=False,
        include_media_query=False,
        body='<div class="card" tabindex="0" class="focus-ring"></div>',
    )

    gate = SpatialGate(
        spacing_json_path=spacing,
        css_path=css,
        html_paths=(html,),
    )
    result = gate.validate()

    assert result.status == Status.FAIL
    assert any(
        check.name.endswith("duplicate_class_attributes")
        and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "css/link_not_color_only" and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "css/btn-primary_target_height" and check.status == Status.PASS
        for check in result.checks
    )


def test_spatial_gate_fails_when_button_targets_lack_minimums(tmp_path: Path) -> None:
    spacing = tmp_path / "spacing.json"
    css = tmp_path / "tokens.css"
    html = tmp_path / "example.html"
    write_spacing(spacing)
    write_html(
        html,
        body='<button class="btn-primary focus-ring">Go</button>',
    )
    css.write_text(
        "\n".join(
            [
                ".link {",
                "  text-decoration: underline;",
                "}",
                ".focus-ring:focus {",
                "  outline: 3px solid #abcdef;",
                "  outline-offset: 2px;",
                "}",
                ".btn-primary, .btn-secondary {",
                "  min-width: 32px;",
                "  min-height: 40px;",
                "}",
            ]
        )
    )

    gate = SpatialGate(
        spacing_json_path=spacing,
        css_path=css,
        html_paths=(html,),
    )
    result = gate.validate()

    assert result.status == Status.FAIL
    assert any(
        check.name == "css/btn-primary_target_height" and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "css/btn-secondary_target_width" and check.status == Status.FAIL
        for check in result.checks
    )


def test_spatial_gate_fails_when_control_rows_do_not_wrap(tmp_path: Path) -> None:
    spacing = tmp_path / "spacing.json"
    css = tmp_path / "tokens.css"
    html = tmp_path / "example.html"
    write_spacing(spacing)
    write_css(css)
    write_html(html, wrap_enabled=False)

    gate = SpatialGate(
        spacing_json_path=spacing,
        css_path=css,
        html_paths=(html,),
    )
    result = gate.validate()

    assert result.status == Status.FAIL
    assert any(
        check.name == "example.html/wrapping_control_rows"
        and check.status == Status.FAIL
        for check in result.checks
    )


def test_spatial_gate_merges_repeated_main_selectors(tmp_path: Path) -> None:
    spacing = tmp_path / "spacing.json"
    css = tmp_path / "tokens.css"
    html = tmp_path / "example.html"
    write_spacing(spacing)
    write_css(css)
    write_html(
        html,
        include_main=True,
        body='<section class="card focus-ring" tabindex="0">Panel</section>',
    )

    gate = SpatialGate(
        spacing_json_path=spacing,
        css_path=css,
        html_paths=(html,),
    )
    result = gate.validate()

    assert result.status == Status.PASS
    assert any(
        check.name == "example.html/main_layout_responsiveness"
        and check.status == Status.PASS
        for check in result.checks
    )


def test_spatial_gate_fails_when_main_grid_overflows_narrow_viewport(
    tmp_path: Path,
) -> None:
    spacing = tmp_path / "spacing.json"
    css = tmp_path / "tokens.css"
    html = tmp_path / "example.html"
    write_spacing(spacing)
    write_css(css)
    write_html(
        html,
        include_main=True,
        main_template="repeat(auto-fit, minmax(320px, 1fr))",
        main_padding="18px",
        include_media_query=False,
        body='<section class="card focus-ring" tabindex="0">Panel</section>',
    )

    gate = SpatialGate(
        spacing_json_path=spacing,
        css_path=css,
        html_paths=(html,),
    )
    result = gate.validate()

    assert result.status == Status.FAIL
    assert any(
        check.name == "example.html/main_mobile_column_fit"
        and check.status == Status.FAIL
        for check in result.checks
    )


def test_spatial_gate_flags_fixed_swatch_grid_without_adaptation(
    tmp_path: Path,
) -> None:
    spacing = tmp_path / "spacing.json"
    css = tmp_path / "tokens.css"
    html = tmp_path / "example.html"
    write_spacing(spacing)
    write_css(css)
    write_html(
        html,
        include_swatch_grid=True,
        swatch_grid_template="repeat(4, minmax(0, 1fr))",
    )

    gate = SpatialGate(
        spacing_json_path=spacing,
        css_path=css,
        html_paths=(html,),
    )
    result = gate.validate()

    assert result.status == Status.FAIL
    assert any(
        check.name == "example.html/swatch_grid_adaptation"
        and check.status == Status.FAIL
        for check in result.checks
    )
