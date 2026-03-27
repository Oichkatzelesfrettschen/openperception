#!/usr/bin/env python3
"""
Validate canonical paper-cache paths, provenance hashes, duplicate coverage,
zero research-local PDF drift, and zero stray paper-root PDF outliers.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from check_report import emit_check_report
from paper_corpus import DEFAULT_PAPER_CORPUS_REGISTRY, validate_paper_corpus


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the paper corpus registry, cached artifacts, and zero noncanonical PDF drift.",
    )
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_PAPER_CORPUS_REGISTRY),
        help="Path to the canonical paper corpus registry JSON file.",
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
    registry_path = Path(args.registry)
    repo_root = Path(args.repo_root).resolve() if args.repo_root else None
    errors = (
        validate_paper_corpus(registry_path, repo_root=repo_root)
        if repo_root
        else validate_paper_corpus(registry_path)
    )
    return emit_check_report(
        check_id="paper_corpus",
        display_name="Paper corpus check",
        scope=str(registry_path),
        errors=errors,
        json_output=args.json,
        task_refs=[f"T{index:03d}" for index in range(81, 101)],
        issue_refs=["KI-006"],
        metadata={"registry_path": str(registry_path)},
    )


if __name__ == "__main__":
    raise SystemExit(main())
