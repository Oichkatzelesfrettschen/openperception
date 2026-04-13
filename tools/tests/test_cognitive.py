"""Tests for the first cognitive/navigation validator."""

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validators.base import Status
from validators.cognitive import CognitiveGate, CognitiveHTMLParser


def write_profiles(path: Path) -> None:
    payload = {
        "profiles": {
            "standard": {"axes": {"cognitive": "full HUD"}},
            "reduced-cognitive": {"axes": {"cognitive": "minimal HUD"}},
        }
    }
    path.write_text(json.dumps(payload))


def write_html(
    path: Path,
    *,
    nav_count: int = 3,
    nested_depth: int = 1,
    summary_view: bool = True,
    notification_count: int = 1,
    hud_complexity: str = "simple",
    region_count: int = 5,
    primary_action_count: int = 3,
    panel_group_count: int = 1,
    metric_group_count: int = 0,
    copy: str = "Short demo. Clear controls.",
) -> None:
    nav_links = "\n".join(
        f'<a href="#item-{index}">Item {index}</a>' for index in range(1, nav_count + 1)
    )
    nested_open = "\n".join("<ul>" for _ in range(max(nested_depth - 1, 0)))
    nested_close = "\n".join("</ul>" for _ in range(max(nested_depth - 1, 0)))
    summary_block = (
        '<details data-summary-view="true"><summary>Summary</summary><p>Quick summary.</p></details>'
        if summary_view
        else ""
    )
    notifications = "\n".join(
        f'<p role="status" aria-live="polite" data-notification="status">Notice {index}</p>'
        for index in range(1, notification_count + 1)
    )
    regions = "\n".join(
        f'<section data-density-region="region-{index}">Region {index}</section>'
        for index in range(1, max(region_count - 1, 0) + 1)
    )
    actions = "\n".join(
        f"<button>Action {index}</button>"
        for index in range(1, primary_action_count + 1)
    )
    path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                (
                    f'<html><body data-hud-complexity="{hud_complexity}" '
                    f'data-cognitive-complex="true" '
                    f'data-panel-groups="{panel_group_count}" '
                    f'data-metric-groups="{metric_group_count}">'
                ),
                '<nav data-density-region="nav">',
                nested_open,
                nav_links,
                nested_close,
                "</nav>",
                f"<p>{copy}</p>",
                summary_block,
                regions,
                notifications,
                f'<div data-primary-actions="true">{actions}</div>',
                "</body></html>",
            ]
        )
    )


def test_cognitive_gate_passes_on_valid_profiles_and_html(tmp_path: Path) -> None:
    profiles = tmp_path / "profiles.json"
    html = tmp_path / "example.html"
    write_profiles(profiles)
    write_html(html)

    result = CognitiveGate(
        profile_manifest_path=profiles, html_paths=(html,)
    ).validate()

    assert result.status in {Status.PASS, Status.WARN}
    assert any(
        check.name == "example.html/density_regions" and check.status == Status.PASS
        for check in result.checks
    )
    assert any(
        check.name == "example.html/primary_action_density"
        and check.status == Status.PASS
        for check in result.checks
    )
    assert any(
        check.name == "example.html/visible_control_burden"
        and check.status == Status.PASS
        for check in result.checks
    )
    assert any(
        check.name == "example.html/panel_group_density" and check.status == Status.PASS
        for check in result.checks
    )


def test_cognitive_gate_fails_on_dense_nav_without_summary(tmp_path: Path) -> None:
    profiles = tmp_path / "profiles.json"
    html = tmp_path / "example.html"
    write_profiles(profiles)
    write_html(
        html,
        nav_count=10,
        nested_depth=4,
        summary_view=False,
        notification_count=4,
        hud_complexity="simple",
        region_count=8,
        primary_action_count=5,
        panel_group_count=5,
        metric_group_count=3,
        copy=(
            "Interoperability rationalization and multidimensional abstraction "
            "significantly complicate comprehension for generalized audiences."
        ),
    )

    result = CognitiveGate(
        profile_manifest_path=profiles, html_paths=(html,)
    ).validate()

    assert result.status == Status.FAIL
    assert any(
        check.name == "example.html/navigation_item_count"
        and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "example.html/progressive_disclosure"
        and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "example.html/concurrent_notifications"
        and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "example.html/density_regions" and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "example.html/primary_action_density"
        and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "example.html/visible_control_burden"
        and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "example.html/panel_group_density" and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "example.html/metric_group_density"
        and check.status == Status.FAIL
        for check in result.checks
    )


def test_cognitive_parser_recovers_after_self_closing_ignored_svg_tags() -> None:
    parser = CognitiveHTMLParser()
    parser.feed(
        "\n".join(
            [
                "<!doctype html>",
                "<html><body>",
                '<svg width="0" height="0"><defs><feColorMatrix type="matrix" values="1" /></defs></svg>',
                "<p>Plain words stay visible.</p>",
                "</body></html>",
            ]
        )
    )

    assert "Plain words stay visible." in " ".join(parser.text_chunks)
