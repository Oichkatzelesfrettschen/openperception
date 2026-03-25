"""
Validate source-cache docs for live related-doc links into research surfaces.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CACHE_SUFFIX = "_source_cache.md"
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((/[^)]+)\)")
QUALIFYING_RESEARCH_PREFIXES = ("research/", "papers/")


def _tracked_source_cache_paths(repo_root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "ls-files",
                "--",
                "docs/external_sources/*_source_cache.md",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted((repo_root / "docs" / "external_sources").glob(f"*{SOURCE_CACHE_SUFFIX}"))

    return sorted(
        repo_root / line
        for line in result.stdout.splitlines()
        if line.strip().endswith(SOURCE_CACHE_SUFFIX)
    )


def _extract_repo_local_link_targets(doc_path: Path, repo_root: Path) -> list[str]:
    text = doc_path.read_text(encoding="utf-8")
    targets: list[str] = []
    for absolute_path in MARKDOWN_LINK_PATTERN.findall(text):
        candidate = Path(absolute_path)
        try:
            rel_path = candidate.relative_to(repo_root)
        except ValueError:
            continue
        targets.append(rel_path.as_posix())
    return targets


def _is_qualifying_research_doc(rel_path: str) -> bool:
    return rel_path.startswith(QUALIFYING_RESEARCH_PREFIXES)


def validate_source_cache_links(repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    for doc_path in _tracked_source_cache_paths(repo_root):
        rel_doc = doc_path.relative_to(repo_root).as_posix()
        targets = _extract_repo_local_link_targets(doc_path, repo_root)
        qualifying_targets = []
        for target in targets:
            target_path = repo_root / target
            if not target_path.exists():
                errors.append(
                    f"source-cache doc links to missing repo path: {target} in {rel_doc}"
                )
                continue
            if _is_qualifying_research_doc(target):
                qualifying_targets.append(target)
        if not qualifying_targets:
            errors.append(
                "source-cache doc must link to at least one research-facing repo doc "
                f"under research/ or papers/: {rel_doc}"
            )
    return sorted(errors)
