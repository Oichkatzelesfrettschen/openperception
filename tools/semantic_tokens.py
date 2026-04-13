"""
Helpers for first-class runtime semantic role tokens.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEMANTIC_TOKENS = REPO_ROOT / "tokens" / "semantic-role-tokens.json"
REQUIRED_RUNTIME_ROLES = (
    "danger",
    "ally",
    "focus",
    "disabled",
    "interactable",
    "warning",
    "info",
    "progress",
)


def load_semantic_tokens(path: Path | None = None) -> dict[str, Any]:
    semantic_path = path or DEFAULT_SEMANTIC_TOKENS
    return json.loads(semantic_path.read_text())


def get_variant_roles(payload: dict[str, Any], variant_name: str) -> dict[str, Any]:
    return payload["variants"][variant_name]["roles"]


def validate_semantic_tokens(path: Path | None = None) -> list[str]:
    semantic_path = path or DEFAULT_SEMANTIC_TOKENS
    payload = load_semantic_tokens(semantic_path)
    variants = payload.get("variants", {})
    errors: list[str] = []

    for variant_name, variant_data in variants.items():
        roles = variant_data.get("roles", {})
        for role in REQUIRED_RUNTIME_ROLES:
            role_data = roles.get(role)
            if role_data is None:
                errors.append(
                    f"{semantic_path}: variant {variant_name} missing role {role}"
                )
                continue
            if not role_data.get("color"):
                errors.append(
                    f"{semantic_path}: variant {variant_name} role {role} missing color"
                )
            if not isinstance(role_data.get("redundancy"), dict):
                errors.append(
                    f"{semantic_path}: variant {variant_name} role {role} missing redundancy mapping"
                )

        for role_name, role_data in roles.items():
            if role_name in {"danger", "ally", "warning", "info"}:
                redundancy = role_data.get("redundancy", {})
                if redundancy.get("marker") is None or redundancy.get("dash") is None:
                    errors.append(
                        f"{semantic_path}: variant {variant_name} role {role_name} missing marker/dash redundancy"
                    )

    return errors
