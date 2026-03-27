#!/usr/bin/env python3
"""
Validate the claims-to-runtime registry for internal consistency.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from check_report import emit_check_report
from claims_registry import DEFAULT_CLAIMS_REGISTRY, validate_claims_registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate claims registry paths, gate references, and statuses.",
    )
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_CLAIMS_REGISTRY),
        help="Path to the claims registry JSON file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of human-readable text.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry_path = Path(args.registry)
    errors = validate_claims_registry(registry_path)
    return emit_check_report(
        check_id="claims_registry",
        display_name="Claims registry check",
        scope=str(registry_path),
        errors=errors,
        json_output=args.json,
        task_refs=[f"T{index:03d}" for index in range(41, 61)],
        issue_refs=["KI-006"],
        metadata={"registry_path": str(registry_path)},
    )


if __name__ == "__main__":
    raise SystemExit(main())
