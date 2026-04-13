#!/usr/bin/env python3
"""Check source-cache and provenance docs for unresolved placeholder language.

Scans docs/external_sources/*_source_cache.md and related provenance files for
placeholder markers that indicate incomplete provenance records.  Exits non-zero
if any are found so that CI catches regressions before they accumulate.

Placeholder patterns detected:
  - TODO, TBD (any case, as standalone words)
  - UNKNOWN SOURCE, SOURCE UNKNOWN (any case)
  - URL: TBD, DOI: TBD, ACCESS: PENDING (any case)
  - [MISSING], [PLACEHOLDER], [UNRESOLVED] (bracketed sentinels)

Run via `make provenance-check` or `python tools/check_provenance_placeholders.py`.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

SCAN_DIRS = [
    Path("docs/external_sources"),
    Path("research"),
]

# Only scan these suffixes inside SCAN_DIRS
SCAN_EXTS = {".md", ".rst", ".txt"}

# Patterns that flag a provenance placeholder
PLACEHOLDER_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("TODO", re.compile(r"\bTODO\b", re.IGNORECASE)),
    ("TBD", re.compile(r"\bTBD\b", re.IGNORECASE)),
    ("UNKNOWN SOURCE", re.compile(r"\bUNKNOWN\s+SOURCE\b", re.IGNORECASE)),
    ("SOURCE UNKNOWN", re.compile(r"\bSOURCE\s+UNKNOWN\b", re.IGNORECASE)),
    ("[MISSING]", re.compile(r"\[MISSING\]", re.IGNORECASE)),
    ("[PLACEHOLDER]", re.compile(r"\[PLACEHOLDER\]", re.IGNORECASE)),
    ("[UNRESOLVED]", re.compile(r"\[UNRESOLVED\]", re.IGNORECASE)),
    ("URL: TBD", re.compile(r"\bURL\s*:\s*TBD\b", re.IGNORECASE)),
    ("DOI: TBD", re.compile(r"\bDOI\s*:\s*TBD\b", re.IGNORECASE)),
    ("ACCESS: PENDING", re.compile(r"\bACCESS\s*:\s*PENDING\b", re.IGNORECASE)),
]


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Return (lineno, label, line) for each placeholder hit."""
    hits: list[tuple[int, str, str]] = []
    for lineno, raw in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        for label, pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(raw):
                hits.append((lineno, label, raw.strip()))
                break  # one hit per line
    return hits


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Check provenance docs for unresolved placeholder language."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable output.",
    )
    parser.add_argument("--root", type=Path, default=None, help="Repo root directory.")
    args = parser.parse_args(argv)

    repo_root = args.root or REPO_ROOT
    total_hits = 0
    file_hits: list[dict] = []

    for rel_dir in SCAN_DIRS:
        scan_dir = repo_root / rel_dir
        if not scan_dir.exists():
            continue
        for path in sorted(scan_dir.rglob("*")):
            if not path.is_file() or path.suffix not in SCAN_EXTS:
                continue
            hits = scan_file(path)
            if not hits:
                continue
            total_hits += len(hits)
            rel_str = str(path.relative_to(repo_root))
            if args.json:
                for lineno, label, excerpt in hits:
                    file_hits.append(
                        {
                            "file": rel_str,
                            "line": lineno,
                            "label": label,
                            "excerpt": excerpt,
                        }
                    )
            else:
                for lineno, label, excerpt in hits:
                    print(f"{rel_str}:{lineno}: [PROVENANCE:{label}] {excerpt}")

    if args.json:
        print(json.dumps({"total": total_hits, "hits": file_hits}, indent=2))
    elif total_hits == 0:
        print(
            "check_provenance_placeholders: no unresolved provenance placeholders found."
        )
    else:
        print(
            f"check_provenance_placeholders: {total_hits} unresolved provenance placeholder(s) found"
            " -- see docs/KNOWN_ISSUES.md for remediation guidance"
        )

    return 1 if total_hits > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
