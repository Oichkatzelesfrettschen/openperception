"""Tests for first-class semantic runtime tokens."""
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from semantic_tokens import (
    get_variant_roles,
    load_semantic_tokens,
    validate_semantic_tokens,
)


def test_load_semantic_tokens_has_default_variant() -> None:
    payload = load_semantic_tokens()

    assert "default" in payload["variants"]
    assert "danger" in payload["variants"]["default"]["roles"]


def test_get_variant_roles_returns_runtime_roles() -> None:
    payload = load_semantic_tokens()
    roles = get_variant_roles(payload, "default")

    assert roles["danger"]["color"].startswith("#")
    assert len(roles["danger"]["color"]) == 7
    assert roles["danger"]["source"]
    assert roles["ally"]["redundancy"]["marker"] == "circle"
    assert roles["warning"]["redundancy"]["marker"] == "diamond"
    assert roles["progress"]["redundancy"]["label"] == "percent-complete"


def test_validate_semantic_tokens_rejects_missing_role(tmp_path: Path) -> None:
    path = tmp_path / "semantic.json"
    path.write_text(
        json.dumps(
            {
                "variants": {
                    "default": {
                        "roles": {
                            "danger": {"color": "#111111", "redundancy": {"marker": "triangle", "dash": [1, 1]}},
                            "ally": {"color": "#222222", "redundancy": {"marker": "circle", "dash": [0, 0]}},
                        }
                    }
                }
            }
        )
    )

    errors = validate_semantic_tokens(path)

    assert any("missing role focus" in error for error in errors)
