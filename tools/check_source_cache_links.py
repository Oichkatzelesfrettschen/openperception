#!/usr/bin/env python3
"""
Validate source-cache markdown links into live research-facing repo docs.
"""
from __future__ import annotations

from source_cache_links import validate_source_cache_links


def main() -> int:
    errors = validate_source_cache_links()
    if errors:
        print("Source cache link check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Source cache link check passed: docs/external_sources/*_source_cache.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
