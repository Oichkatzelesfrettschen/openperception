#!/usr/bin/env python3
"""
Validate dataset source-asset provenance and cached artifact integrity.
"""
from __future__ import annotations

from source_assets import validate_source_assets


def main() -> int:
    errors = validate_source_assets()
    if errors:
        print("Source assets check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Source assets check passed: datasets/source_assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
