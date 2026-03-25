#!/usr/bin/env python3
"""
Validate the claims-to-runtime registry for internal consistency.
"""
from __future__ import annotations

import argparse
from pathlib import Path

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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry_path = Path(args.registry)
    errors = validate_claims_registry(registry_path)
    if errors:
        print("Claims registry check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Claims registry check passed: {registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
