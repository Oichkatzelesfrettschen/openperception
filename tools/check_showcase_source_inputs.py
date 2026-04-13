#!/usr/bin/env python3
"""Validate sibling-repo source inputs for the Blender showcase."""

from __future__ import annotations

import argparse

from check_report import emit_check_report
from showcase_physics_views import validate_showcase_source_inputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate sibling-repo inputs used by the Blender showcase.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of human-readable text.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_showcase_source_inputs()
    return emit_check_report(
        check_id="showcase_source_inputs",
        display_name="Showcase source input check",
        scope="compact-common + Blackhole sibling-repo artifacts referenced by tools/showcase_physics_views.py",
        errors=errors,
        json_output=args.json,
        task_refs=["T107", "T108"],
        issue_refs=["KI-005"],
    )


if __name__ == "__main__":
    raise SystemExit(main())
