#!/usr/bin/env python3
"""
Validate dataset source-asset provenance and cached artifact integrity.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from check_report import emit_check_report
from source_assets import validate_source_assets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate dataset source-asset provenance and artifact integrity.",
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
        validate_source_assets(repo_root) if repo_root else validate_source_assets()
    )
    return emit_check_report(
        check_id="source_assets",
        display_name="Source assets check",
        scope="datasets/source_assets",
        errors=errors,
        json_output=args.json,
        task_refs=["T082", "T085", "T091", "T094"],
        issue_refs=["KI-006"],
    )


if __name__ == "__main__":
    raise SystemExit(main())
