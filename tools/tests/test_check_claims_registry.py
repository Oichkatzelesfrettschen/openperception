"""Tests for claims registry integrity checking."""

from __future__ import annotations

import json

from claims_registry import validate_claims_registry


def test_validate_claims_registry_accepts_seeded_registry() -> None:
    assert validate_claims_registry() == []


def test_validate_claims_registry_rejects_unknown_gate(tmp_path) -> None:
    registry = {
        "claims": [
            {
                "claim_id": "CLM-X",
                "status": "partial",
                "validator_gates": ["GATE-999"],
                "runtime_artifacts": [],
                "tests": [],
                "docs": [],
            }
        ]
    }
    path = tmp_path / "claims.json"
    path.write_text(json.dumps(registry))

    errors = validate_claims_registry(path)

    assert any("unknown gate GATE-999" in error for error in errors)


def test_validate_claims_registry_rejects_missing_paths(tmp_path) -> None:
    registry = {
        "claims": [
            {
                "claim_id": "CLM-Y",
                "status": "implemented",
                "validator_gates": [],
                "runtime_artifacts": ["docs/does-not-exist.md"],
                "tests": [],
                "docs": [],
            }
        ]
    }
    path = tmp_path / "claims.json"
    path.write_text(json.dumps(registry))

    errors = validate_claims_registry(path)

    assert any(
        "references missing path docs/does-not-exist.md" in error for error in errors
    )
