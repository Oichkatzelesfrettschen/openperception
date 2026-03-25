"""Tests for the semantic-aware CVD gate."""
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validators.base import Status
from validators.cvd import CVDGate, derive_semantic_roles


def write_tokens(path: Path, *, accent: str, primary: str, link: str, border: str, focus_ring: str, markers=None, dashes=None) -> None:
    payload = {
        "default": {
            "gray": {
                "400": "#9CA3AF",
                "500": "#6B7280",
            },
            "brand": {
                "primaryStrong": primary,
                "accentStrong": accent,
                "link": link,
                "border": border,
                "focusRing": focus_ring,
            },
            "viz": {
                "markers": markers or ["circle", "triangle"],
                "dashes": dashes or [[0, 0], [6, 3]],
            },
        }
    }
    path.write_text(json.dumps(payload))


def write_semantic_tokens(
    path: Path,
    *,
    danger: str,
    ally: str,
    focus: str,
    disabled: str,
    interactable: str,
    warning: str = "#B45309",
    info: str = "#0369A1",
    progress: str = "#047857",
    danger_marker: str = "triangle",
    ally_marker: str = "circle",
    danger_dash=None,
    ally_dash=None,
) -> None:
    payload = {
        "variants": {
            "default": {
                "roles": {
                    "danger": {
                        "color": danger,
                        "redundancy": {
                            "marker": danger_marker,
                            "dash": danger_dash or [6, 3],
                        },
                    },
                    "ally": {
                        "color": ally,
                        "redundancy": {
                            "marker": ally_marker,
                            "dash": ally_dash or [0, 0],
                        },
                    },
                    "focus": {"color": focus, "redundancy": {"pattern": "outline"}},
                    "disabled": {"color": disabled, "redundancy": {"marker": "x", "dash": [2, 2], "pattern": "dashed", "icon": "lock"}},
                    "interactable": {"color": interactable, "redundancy": {"pattern": "underline"}},
                    "warning": {
                        "color": warning,
                        "redundancy": {"marker": "diamond", "dash": [3, 2, 1, 2], "pattern": "chevron"},
                    },
                    "info": {
                        "color": info,
                        "redundancy": {"marker": "square", "dash": [1, 2], "pattern": "dotted"},
                    },
                    "progress": {
                        "color": progress,
                        "redundancy": {"label": "percent", "pattern": "fill"},
                    },
                }
            }
        }
    }
    path.write_text(json.dumps(payload))


def test_derive_semantic_roles_uses_brand_and_gray_fallbacks() -> None:
    default_tokens = {
        "gray": {"400": "#9CA3AF"},
        "brand": {"focusRing": "#A5B4FC", "border": "#D1D5DB"},
    }
    variant_tokens = {
        "brand": {
            "primaryStrong": "#3730A3",
            "accentStrong": "#86198F",
            "link": "#3730A3",
        }
    }

    roles = derive_semantic_roles("protan", variant_tokens, default_tokens)

    assert roles["danger"] == "#86198F"
    assert roles["ally"] == "#3730A3"
    assert roles["focus"] == "#A5B4FC"
    assert roles["disabled"] == "#9CA3AF"


def test_cvd_gate_passes_semantic_role_checks_on_clear_fixture(tmp_path: Path) -> None:
    tokens = tmp_path / "tokens.json"
    semantic = tmp_path / "semantic.json"
    write_tokens(
        tokens,
        accent="#86198F",
        primary="#3730A3",
        link="#3730A3",
        border="#D1D5DB",
        focus_ring="#A5B4FC",
    )
    write_semantic_tokens(
        semantic,
        danger="#86198F",
        ally="#3730A3",
        focus="#A5B4FC",
        disabled="#D1D5DB",
        interactable="#3730A3",
    )

    result = CVDGate(tokens, semantic).validate()

    assert any(
        check.name == "default/danger-vs-ally" and check.status in {Status.PASS, Status.WARN}
        for check in result.checks
    )
    assert any(
        check.name == "default/warning-vs-info" and check.status in {Status.PASS, Status.WARN}
        for check in result.checks
    )
    assert any(
        check.name == "default/danger-ally_redundancy" and check.status == Status.PASS
        for check in result.checks
    )
    assert any(
        check.name == "default/warning-info_redundancy" and check.status == Status.PASS
        for check in result.checks
    )


def test_cvd_gate_fails_collapsed_semantic_roles_and_redundancy(tmp_path: Path) -> None:
    tokens = tmp_path / "tokens.json"
    semantic = tmp_path / "semantic.json"
    write_tokens(
        tokens,
        accent="#777777",
        primary="#777777",
        link="#888888",
        border="#8A8A8A",
        focus_ring="#8B8B8B",
        markers=["circle", "circle"],
        dashes=[[0, 0], [0, 0]],
    )
    write_semantic_tokens(
        semantic,
        danger="#777777",
        ally="#777777",
        focus="#8B8B8B",
        disabled="#8A8A8A",
        interactable="#888888",
        danger_marker="circle",
        ally_marker="circle",
        danger_dash=[0, 0],
        ally_dash=[0, 0],
    )

    result = CVDGate(tokens, semantic).validate()

    assert any(
        check.name == "default/danger-vs-ally" and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "default/danger-ally_redundancy" and check.status == Status.FAIL
        for check in result.checks
    )


def test_cvd_gate_can_fall_back_without_semantic_manifest(tmp_path: Path) -> None:
    tokens = tmp_path / "tokens.json"
    write_tokens(
        tokens,
        accent="#86198F",
        primary="#3730A3",
        link="#3730A3",
        border="#D1D5DB",
        focus_ring="#A5B4FC",
    )

    result = CVDGate(tokens, tmp_path / "missing.json").validate()

    assert any(
        check.name == "default/danger-vs-ally" and check.status in {Status.PASS, Status.WARN}
        for check in result.checks
    )
    assert any(
        check.name == "default/warning-vs-info" and check.status == Status.WARN
        for check in result.checks
    )
