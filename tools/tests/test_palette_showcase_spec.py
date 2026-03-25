"""Tests for token-driven palette showcase scene payloads."""
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from palette_showcase_spec import build_showcase_spec


def test_showcase_spec_has_expected_lane_ids() -> None:
    payload = build_showcase_spec()

    assert payload["scene_id"] == "openperception-palette-showcase"
    assert [lane["scheme_id"] for lane in payload["lanes"]] == [
        "production-indigo-magenta",
        "accessible-mauve-burgundy",
        "atmosphere-red-mahogany",
    ]


def test_showcase_spec_uses_current_token_values() -> None:
    payload = build_showcase_spec()
    lanes = {lane["scheme_id"]: lane for lane in payload["lanes"]}

    assert lanes["production-indigo-magenta"]["brand"]["primaryStrong"] == "#3730A3"
    assert lanes["accessible-mauve-burgundy"]["brand"]["tertiaryStrong"] == "#901C32"
    assert lanes["atmosphere-red-mahogany"]["brand"]["surface"] == "#F7F2EC"


def test_showcase_spec_exposes_variant_payloads() -> None:
    payload = build_showcase_spec()
    lanes = {lane["scheme_id"]: lane for lane in payload["lanes"]}

    assert lanes["production-indigo-magenta"]["available_variants"] == [
        "default",
        "protan",
        "deutan",
        "tritan",
        "mono",
    ]
    assert lanes["accessible-mauve-burgundy"]["variants"]["mono"]["brand"]["primaryStrong"] == "#1E293B"
    assert lanes["atmosphere-red-mahogany"]["available_variants"] == [
        "default",
        "protan",
        "deutan",
        "tritan",
        "mono",
    ]
