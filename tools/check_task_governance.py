#!/usr/bin/env python3
"""
Validate repo task-tracking and known-issues governance surfaces.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from check_report import emit_check_report
from task_governance import validate_task_governance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate task-ledger and known-issues governance docs.",
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
    errors = validate_task_governance(repo_root) if repo_root else validate_task_governance()
    return emit_check_report(
        check_id="governance",
        display_name="Task governance check",
        scope="docs/task-ledger.md and docs/KNOWN_ISSUES.md",
        errors=errors,
        json_output=args.json,
        task_refs=[f"T{index:03d}" for index in range(1, 21)],
        issue_refs=["KI-004"],
    )


if __name__ == "__main__":
    raise SystemExit(main())
