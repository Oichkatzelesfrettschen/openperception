#!/usr/bin/env python3
"""check_overclaims.py -- Scan repo docs for unsupported certainty phrases.

Flags language that asserts stronger guarantees than the evidence base
supports. The goal is not to ban all strong language, but to catch phrases
that imply correctness, completeness, or production-readiness without
explicit qualification or citation.

WHY: Evidence-based research repos are vulnerable to marketing drift.
     Unchecked certainty phrases mislead contributors and undermine the
     credibility of legitimate verified claims.

WHAT: Scans *.md and *.rst files (excluding vendor, venv, papers/ and
      research/ directories) for a curated list of overclaim patterns.

HOW:
    python3 tools/check_overclaims.py [--json]
    make check-overclaims
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Patterns that signal unsupported certainty.
# Each entry: (pattern, human_label, rationale)
# Patterns must be valid Python regex; match is case-insensitive.
OVERCLAIM_PATTERNS: list[tuple[str, str, str]] = [
    (
        # Skip "Production Ready" in ROADMAP milestone headings (aspirational)
        # and "production-ready" when it appears inside a task-ledger audit item.
        r"\bproduction.?ready\b(?!.*aspirational)(?!.*milestone)(?!.*roadmap)",
        "production-ready",
        "Implies deployment stability that has not been audited end-to-end.",
    ),
    (
        # "guaranteed" is an overclaim; "not a guarantee" / "cannot guarantee"
        # are fine (they are explicitly scoping limitations).
        r"(?<!not a )\bguaranteed?\b(?!\s*:)(?!.*\b(cannot|can not|not fully|not a)\b)",
        "guaranteed",
        "Absolute guarantee requires formal proof or specification backing.",
    ),
    (
        r"\bstate.of.the.art\b",
        "state-of-the-art",
        "Superlative comparative claim; requires citation or qualification.",
    ),
    (
        r"\bbest.in.class\b",
        "best-in-class",
        "Comparative superlative without evidence.",
    ),
    (
        r"\bindisputabl[ye]\b",
        "indisputably",
        "Absolute epistemic claim; all empirical claims are disputable.",
    ),
    (
        r"\bproven\b(?!.*\bcitation\b)(?!.*\bsee\b)(?!.*\bref\b)(?!.*\bpaper\b)",
        "proven (no citation visible)",
        "Strong epistemic claim; must be paired with a citation or qualifier.",
    ),
    (
        r"\balways\s+(accurate|correct|works?|succeeds?|ensures?)\b",
        "always <verb>",
        "Universal quantifier over correctness; needs formal proof or scope.",
    ),
    (
        r"\bnever\s+(fails?|errors?|breaks?|misses?)\b",
        "never <fails>",
        "Universal negative correctness claim; needs formal proof or scope.",
    ),
    (
        r"\bfully\s+(tested|validated|verified|compliant)\b",
        "fully <tested/validated>",
        "Completeness claim that exceeds what the current test suite covers.",
    ),
    (
        r"\bcomprehensive(?:ly)?\s+(coverage|support|guarantee|compliance)\b",
        "comprehensive <coverage/support>",
        "Completeness claim; acceptable only with explicit scope statement.",
    ),
]

# Directories and file patterns to skip entirely.
SKIP_DIRS: frozenset[str] = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        "papers",          # research literature; external authors' language
        "research",        # literature summaries; external authors' language
        "build",
        "dist",
    }
)

# Individual files to skip (relative to repo root).
SKIP_FILES: frozenset[str] = frozenset(
    {
        # Specs that have explicit "what we can/cannot guarantee" tables --
        # the word "guarantee" is used to scope limitations, not assert them.
        "specs/DISPLAY_ADAPTATION_LAYER.md",
        "specs/TEST_MATRIX.md",
        # docs that explicitly state "not a guarantee"
        "docs/layout-system-foundations.md",
        "docs/references-bibliography-foundations.md",
        "docs/typography-system-foundations.md",
        # task-ledger references to auditing overclaims are meta, not claims
        "docs/task-ledger.md",
        # CLAUDE.md is an internal project-memory file, not published claims
        "CLAUDE.md",
    }
)

# Lines that contain this substring are treated as allowlisted (already
# reviewed). Add lines here when the phrase is intentional and justified.
ALLOWLIST_SUBSTRINGS: list[str] = [
    # pixel-perfect is a typographic term, not a correctness claim
    "pixel-perfect",
    "pixel perfect",
    # "proven" in a test-result context
    "proven algorithm",
    "well-proven",
    # v1.0.0 milestone heading in ROADMAP is an aspirational goal, not a claim
    "v1.0.0 - production ready",
    "### v1.0.0",
    # explicitly scoped guarantee language
    "not a guarantee",
    "not a runtime guarantee",
    "cannot guarantee",
    "can not guarantee",
    "cannot fully guarantee",
    "## 9. What UVAS+ Can and Cannot",
    "### 9.1",
    "### 9.2",
    "CAN Guarantee",
    "CANNOT Fully Guarantee",
]


def _is_skipped(path: Path, repo_root: Path) -> bool:
    rel = path.relative_to(repo_root)
    parts = rel.parts
    for part in parts[:-1]:           # directory components
        if part in SKIP_DIRS:
            return True
    return str(rel) in SKIP_FILES


def _is_allowlisted(line: str) -> bool:
    line_lower = line.lower()
    return any(phrase.lower() in line_lower for phrase in ALLOWLIST_SUBSTRINGS)


def scan_file(
    path: Path,
) -> list[tuple[int, str, str, str]]:
    """Return (lineno, label, pattern, excerpt) for each hit."""
    results: list[tuple[int, str, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return results

    for lineno, line in enumerate(text.splitlines(), 1):
        if _is_allowlisted(line):
            continue
        for pattern, label, _ in OVERCLAIM_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                excerpt = line.strip()[:120]
                results.append((lineno, label, pattern, excerpt))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable output.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repo root directory (default: parent of this script's parent).",
    )
    args = parser.parse_args(argv)

    repo_root = args.root or Path(__file__).resolve().parent.parent
    target_exts = {".md", ".rst"}

    total_hits = 0
    file_hits: list[dict] = []

    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in target_exts:
            continue
        if _is_skipped(path, repo_root):
            continue

        hits = scan_file(path)
        if not hits:
            continue

        total_hits += len(hits)
        rel_str = str(path.relative_to(repo_root))

        if args.json:
            for lineno, label, pattern, excerpt in hits:
                file_hits.append(
                    {
                        "file": rel_str,
                        "line": lineno,
                        "label": label,
                        "pattern": pattern,
                        "excerpt": excerpt,
                    }
                )
        else:
            for lineno, label, _pattern, excerpt in hits:
                print(f"{rel_str}:{lineno}: [OVERCLAIM:{label}] {excerpt}")

    if args.json:
        print(
            json.dumps(
                {"total": total_hits, "hits": file_hits}, indent=2
            )
        )
    else:
        if total_hits == 0:
            print("check_overclaims: no overclaim phrases found.")
        else:
            print(
                f"\ncheck_overclaims: {total_hits} overclaim phrase(s) found."
            )

    return 1 if total_hits > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
