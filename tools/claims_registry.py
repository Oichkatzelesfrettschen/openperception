"""
Helpers for the claims-to-runtime coverage registry.

WHY: The evidence matrix describes many claims, but the runtime previously had
no machine-readable way to say which claims are implemented, partial, or still
prose-only. This module provides the shared loader and summary helpers.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from validator_registry import get_gate_specs


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLAIMS_REGISTRY = REPO_ROOT / "specs" / "CLAIMS_RUNTIME_REGISTRY.json"
ALLOWED_CLAIM_STATUSES = {"implemented", "partial", "spec_only"}


def load_claims_registry(path: Path | None = None) -> dict[str, Any]:
    registry_path = path or DEFAULT_CLAIMS_REGISTRY
    return json.loads(registry_path.read_text())


def summarize_claims_registry(path: Path | None = None) -> dict[str, Any]:
    registry = load_claims_registry(path)
    claims = registry["claims"]
    by_status: dict[str, int] = {}
    by_gate: dict[str, list[str]] = {}

    for claim in claims:
        by_status[claim["status"]] = by_status.get(claim["status"], 0) + 1
        for gate_id in claim.get("validator_gates", []):
            by_gate.setdefault(gate_id, []).append(claim["claim_id"])

    uncovered = [
        claim["claim_id"]
        for claim in claims
        if not claim.get("validator_gates") and claim["status"] != "implemented"
    ]

    return {
        "registry_path": str(path or DEFAULT_CLAIMS_REGISTRY),
        "claim_count": len(claims),
        "status_counts": by_status,
        "claims_by_gate": by_gate,
        "uncovered_claims": uncovered,
    }


def validate_claims_registry(path: Path | None = None) -> list[str]:
    registry_path = path or DEFAULT_CLAIMS_REGISTRY
    registry = load_claims_registry(registry_path)
    claims = registry.get("claims")
    errors: list[str] = []
    known_gates = {spec.gate_id for spec in get_gate_specs()}
    seen_ids: set[str] = set()

    if not isinstance(claims, list):
        return [f"{registry_path}: top-level 'claims' must be a list"]

    for index, claim in enumerate(claims):
        prefix = f"{registry_path}: claims[{index}]"
        claim_id = claim.get("claim_id")
        if not claim_id:
            errors.append(f"{prefix} is missing claim_id")
        elif claim_id in seen_ids:
            errors.append(f"{prefix} duplicates claim_id {claim_id}")
        else:
            seen_ids.add(claim_id)

        status = claim.get("status")
        if status not in ALLOWED_CLAIM_STATUSES:
            errors.append(
                f"{prefix} has invalid status {status!r}; expected one of "
                f"{sorted(ALLOWED_CLAIM_STATUSES)}"
            )

        for gate_id in claim.get("validator_gates", []):
            if gate_id not in known_gates:
                errors.append(f"{prefix} references unknown gate {gate_id}")

        for field_name in ("runtime_artifacts", "tests", "docs"):
            field_value = claim.get(field_name, [])
            if not isinstance(field_value, list):
                errors.append(f"{prefix}.{field_name} must be a list")
                continue
            for relative_path in field_value:
                candidate = REPO_ROOT / relative_path
                if not candidate.exists():
                    errors.append(
                        f"{prefix}.{field_name} references missing path {relative_path}"
                    )

        if status == "implemented":
            has_runtime_link = bool(claim.get("runtime_artifacts")) or bool(
                claim.get("tests")
            )
            if not has_runtime_link:
                errors.append(
                    f"{prefix} is implemented but has no runtime_artifacts or tests"
                )

    return errors
