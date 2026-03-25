#!/usr/bin/env python3
"""
Validate canonical paper-cache paths, provenance hashes, and duplicate coverage.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from paper_corpus import DEFAULT_PAPER_CORPUS_REGISTRY, validate_paper_corpus


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the paper corpus registry and cached artifacts.",
    )
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_PAPER_CORPUS_REGISTRY),
        help="Path to the canonical paper corpus registry JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry_path = Path(args.registry)
    errors = validate_paper_corpus(registry_path)
    if errors:
        print("Paper corpus check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Paper corpus check passed: {registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
