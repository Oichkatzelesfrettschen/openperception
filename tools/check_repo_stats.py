#!/usr/bin/env python3
"""
Validate that checked-in repo stats match the current tracked tree.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from check_report import emit_check_report
from repo_stats import (
    DEFAULT_JSON_OUTPUT,
    DEFAULT_MD_OUTPUT,
    generate_repo_stats,
    render_repo_stats_markdown,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate generated repo stats against the current tree.",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Override the repository root for validation.",
    )
    parser.add_argument(
        "--stats-json",
        default=str(DEFAULT_JSON_OUTPUT),
        help="Path to the checked-in repo stats JSON file.",
    )
    parser.add_argument(
        "--stats-md",
        default=str(DEFAULT_MD_OUTPUT),
        help="Path to the checked-in repo stats Markdown file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of human-readable text.",
    )
    return parser.parse_args()


def validate_repo_stats(
    repo_root: Path, stats_json_path: Path, stats_md_path: Path
) -> list[str]:
    errors: list[str] = []
    if not stats_json_path.exists():
        errors.append(f"generated repo stats JSON is missing: {stats_json_path}")
    if not stats_md_path.exists():
        errors.append(f"generated repo stats Markdown is missing: {stats_md_path}")
    expected_stats = generate_repo_stats(repo_root)
    expected_json = json.dumps(expected_stats, indent=2, sort_keys=True) + "\n"
    expected_md = render_repo_stats_markdown(expected_stats)

    if stats_json_path.exists():
        actual_json = stats_json_path.read_text(encoding="utf-8")
        if actual_json != expected_json:
            errors.append(
                f"generated repo stats JSON is stale: {stats_json_path}; rerun tools/repo_stats.py"
            )
    if stats_md_path.exists():
        actual_md = stats_md_path.read_text(encoding="utf-8")
        if actual_md != expected_md:
            errors.append(
                f"generated repo stats Markdown is stale: {stats_md_path}; rerun tools/repo_stats.py"
            )
    return errors


def main() -> int:
    args = parse_args()
    repo_root = (
        Path(args.repo_root).resolve()
        if args.repo_root
        else Path(__file__).resolve().parents[1]
    )
    stats_json_path = Path(args.stats_json)
    stats_md_path = Path(args.stats_md)
    errors = validate_repo_stats(repo_root, stats_json_path, stats_md_path)
    return emit_check_report(
        check_id="repo_stats",
        display_name="Repo stats check",
        scope="docs/generated/repo_stats.json + docs/generated/repo_stats.md",
        errors=errors,
        json_output=args.json,
        task_refs=["T050", "T056", "T089", "T098"],
        issue_refs=["KI-004"],
        metadata={
            "stats_json_path": str(stats_json_path),
            "stats_md_path": str(stats_md_path),
        },
    )


if __name__ == "__main__":
    raise SystemExit(main())
