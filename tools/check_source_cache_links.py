#!/usr/bin/env python3
"""
Validate source-cache markdown links into live research-facing repo docs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from check_report import emit_check_report
from source_cache_links import validate_source_cache_links


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate source-cache markdown links into research-facing docs.",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Override the repository root for validation.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of human-readable text.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else None
    errors = (
        validate_source_cache_links(repo_root)
        if repo_root
        else validate_source_cache_links()
    )
    return emit_check_report(
        check_id="source_cache_links",
        display_name="Source cache link check",
        scope="docs/external_sources/*_source_cache.md",
        errors=errors,
        json_output=args.json,
        task_refs=["T083", "T084", "T087", "T093"],
        issue_refs=["KI-006"],
    )


if __name__ == "__main__":
    raise SystemExit(main())
