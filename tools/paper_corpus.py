"""
Validate the curated paper corpus and its canonical source registry.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PAPER_CORPUS_REGISTRY = (
    REPO_ROOT / "papers" / "downloads" / "CANONICAL_REGISTRY.json"
)
ALLOWED_NONCANONICAL_REFERENCE_DOCS = {
    "docs/external_sources/paper_corpus_audit.md",
    "docs/external_sources/paper_corpus_registry.md",
    "docs/external_sources/research_pdf_migration_inventory.md",
}
TRACKED_TEXT_GLOBS = ("*.md", "*.bib", "*.bibtex")
RESEARCH_PDF_PATTERN = re.compile(r"research/[A-Za-z0-9_./-]+\.pdf")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _looks_like_pdf(path: Path) -> bool:
    return path.read_bytes().startswith(b"%PDF")


def _load_registry(registry_path: Path) -> dict[str, Any]:
    return json.loads(registry_path.read_text(encoding="utf-8"))


def _tracked_text_paths(repo_root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "ls-files",
                "--",
                *TRACKED_TEXT_GLOBS,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        paths = []
        for pattern in TRACKED_TEXT_GLOBS:
            paths.extend(repo_root.rglob(pattern))
        return sorted(set(paths))

    paths = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        paths.append(repo_root / line)
    return sorted(paths)


def collect_duplicate_pdf_groups(repo_root: Path = REPO_ROOT) -> list[list[str]]:
    pdf_paths = sorted(
        {
            *repo_root.glob("papers/**/*.pdf"),
            *repo_root.glob("research/**/*.pdf"),
        }
    )
    by_hash: dict[str, list[str]] = defaultdict(list)
    for path in pdf_paths:
        digest = _sha256(path)
        by_hash[digest].append(path.relative_to(repo_root).as_posix())
    return sorted(
        [sorted(paths) for paths in by_hash.values() if len(paths) > 1],
        key=lambda paths: paths[0],
    )


def collect_remaining_research_pdf_paths(
    registry: dict[str, Any],
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    retired_paths = {
        entry["legacy_path"]
        for entry in registry.get("legacy_aliases", [])
        if entry.get("legacy_path", "").startswith("research/")
        and entry.get("legacy_path", "").endswith(".pdf")
    }
    remaining_paths = []
    for path in sorted(repo_root.glob("research/**/*.pdf")):
        rel_path = path.relative_to(repo_root).as_posix()
        if rel_path not in retired_paths:
            remaining_paths.append(rel_path)
    return remaining_paths


def collect_noncanonical_reference_violations(
    registry: dict[str, Any],
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    noncanonical_paths = set(collect_remaining_research_pdf_paths(registry, repo_root))
    noncanonical_paths.update(
        entry["legacy_path"]
        for entry in registry.get("legacy_aliases", [])
        if entry.get("legacy_path", "").startswith("research/")
        and entry.get("legacy_path", "").endswith(".pdf")
    )
    violations: list[str] = []

    for path in _tracked_text_paths(repo_root):
        rel_path = path.relative_to(repo_root).as_posix()
        if rel_path in ALLOWED_NONCANONICAL_REFERENCE_DOCS:
            continue
        text = path.read_text(encoding="utf-8")
        for candidate in sorted(set(RESEARCH_PDF_PATTERN.findall(text))):
            if candidate in noncanonical_paths:
                violations.append(
                    "noncanonical research PDF reference outside allowed provenance docs: "
                    f"{candidate} in {rel_path}"
                )
    return violations


def validate_paper_corpus(
    registry_path: Path = DEFAULT_PAPER_CORPUS_REGISTRY,
    repo_root: Path | None = None,
) -> list[str]:
    repo_root = repo_root or registry_path.resolve().parents[2]
    registry = _load_registry(registry_path)
    errors: list[str] = []

    file_entries = registry.get("files", [])
    file_index: dict[str, dict[str, Any]] = {}
    for entry in file_entries:
        rel_path = entry["path"]
        if rel_path in file_index:
            errors.append(f"registry duplicates file entry {rel_path}")
            continue
        file_index[rel_path] = entry

    source_artifacts: set[str] = set()
    for source in registry.get("sources", []):
        source_id = source.get("id", "<missing-id>")
        artifacts = source.get("artifacts", [])
        if not artifacts:
            errors.append(f"source {source_id} has no artifacts")
            continue
        for rel_path in artifacts:
            source_artifacts.add(rel_path)
            artifact_path = repo_root / rel_path
            if not artifact_path.exists():
                errors.append(f"source {source_id} references missing artifact {rel_path}")
                continue
            size_bytes = artifact_path.stat().st_size
            if size_bytes == 0:
                errors.append(f"source {source_id} artifact is zero-byte: {rel_path}")
            if artifact_path.suffix.lower() == ".pdf" and not _looks_like_pdf(artifact_path):
                errors.append(f"source {source_id} artifact is not a valid PDF header: {rel_path}")
            entry = file_index.get(rel_path)
            if entry is None:
                errors.append(f"source {source_id} artifact missing from files table: {rel_path}")
                continue
            actual_hash = _sha256(artifact_path)
            if entry.get("sha256") != actual_hash:
                errors.append(
                    f"files table hash mismatch for {rel_path}: "
                    f"expected {entry.get('sha256')} got {actual_hash}"
                )
            if entry.get("size_bytes") != size_bytes:
                errors.append(
                    f"files table size mismatch for {rel_path}: "
                    f"expected {entry.get('size_bytes')} got {size_bytes}"
                )

    extra_file_entries = sorted(set(file_index) - source_artifacts)
    for rel_path in extra_file_entries:
        errors.append(f"files table contains unreferenced artifact {rel_path}")

    for path in sorted(
        {
            *repo_root.glob("papers/**/*.pdf"),
            *repo_root.glob("research/**/*.pdf"),
        }
    ):
        rel_path = path.relative_to(repo_root).as_posix()
        if path.stat().st_size == 0:
            errors.append(f"zero-byte PDF detected: {rel_path}")
        elif not _looks_like_pdf(path):
            errors.append(f"PDF path does not start with %PDF: {rel_path}")

    for alias in registry.get("legacy_aliases", []):
        legacy_path = repo_root / alias["legacy_path"]
        if legacy_path.exists():
            errors.append(f"legacy path still exists and should be removed: {alias['legacy_path']}")
        for rel_path in alias.get("canonical_artifacts", []):
            if not (repo_root / rel_path).exists():
                errors.append(
                    f"legacy alias {alias['legacy_path']} points to missing canonical artifact {rel_path}"
                )

    registered_duplicates: list[list[str]] = []
    for group in registry.get("duplicate_groups", []):
        canonical_path = group["canonical_path"]
        alias_paths = group.get("alias_paths", [])
        group_paths = [canonical_path, *alias_paths]
        existing_paths = []
        group_hashes = set()
        for rel_path in group_paths:
            path = repo_root / rel_path
            if not path.exists():
                errors.append(f"duplicate group references missing path {rel_path}")
                continue
            existing_paths.append(rel_path)
            group_hashes.add(_sha256(path))
        if len(existing_paths) < 2:
            errors.append(
                f"duplicate group {group.get('id', canonical_path)} needs at least two existing paths"
            )
            continue
        if len(group_hashes) != 1:
            errors.append(
                f"duplicate group {group.get('id', canonical_path)} does not hash-match across paths"
            )
        registered_duplicates.append(sorted(existing_paths))

    actual_duplicates = collect_duplicate_pdf_groups(repo_root)
    if sorted(registered_duplicates) != actual_duplicates:
        errors.append(
            "duplicate PDF groups differ from registry: "
            f"registered={registered_duplicates} actual={actual_duplicates}"
        )

    errors.extend(collect_noncanonical_reference_violations(registry, repo_root))

    return errors
