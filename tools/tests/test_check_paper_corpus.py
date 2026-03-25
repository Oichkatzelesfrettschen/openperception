"""Tests for paper corpus registry validation."""
from __future__ import annotations

import json
from pathlib import Path

from paper_corpus import validate_paper_corpus


MINIMAL_PDF = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF\n"


def write_registry(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_validate_paper_corpus_accepts_seeded_registry() -> None:
    assert validate_paper_corpus() == []


def test_validate_paper_corpus_rejects_zero_byte_pdf(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifact = repo_root / "papers" / "downloads" / "topic" / "broken.pdf"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(b"")
    registry_path = repo_root / "papers" / "downloads" / "CANONICAL_REGISTRY.json"
    write_registry(
        registry_path,
        {
            "sources": [
                {
                    "id": "broken_source",
                    "artifacts": ["papers/downloads/topic/broken.pdf"],
                }
            ],
            "legacy_aliases": [],
            "duplicate_groups": [],
            "files": [
                {
                    "path": "papers/downloads/topic/broken.pdf",
                    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "size_bytes": 0,
                }
            ],
        },
    )

    errors = validate_paper_corpus(registry_path, repo_root=repo_root)

    assert any("zero-byte PDF detected" in error for error in errors)


def test_validate_paper_corpus_rejects_unregistered_duplicate_group(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path
    first = repo_root / "papers" / "downloads" / "topic" / "one.pdf"
    second = repo_root / "research" / "topic" / "two.pdf"
    first.parent.mkdir(parents=True, exist_ok=True)
    second.parent.mkdir(parents=True, exist_ok=True)
    first.write_bytes(MINIMAL_PDF)
    second.write_bytes(MINIMAL_PDF)
    registry_path = repo_root / "papers" / "downloads" / "CANONICAL_REGISTRY.json"
    digest = (
        "b3ec0ca7710d1025ee7ac7994d83b2ddbc200e5543df1066717d7124faf71d8f"
    )
    write_registry(
        registry_path,
        {
            "sources": [
                {
                    "id": "source_one",
                    "artifacts": ["papers/downloads/topic/one.pdf"],
                }
            ],
            "legacy_aliases": [],
            "duplicate_groups": [],
            "files": [
                {
                    "path": "papers/downloads/topic/one.pdf",
                    "sha256": digest,
                    "size_bytes": len(MINIMAL_PDF),
                }
            ],
        },
    )

    errors = validate_paper_corpus(registry_path, repo_root=repo_root)

    assert any("duplicate PDF groups differ from registry" in error for error in errors)


def test_validate_paper_corpus_rejects_lingering_legacy_path(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifact = repo_root / "papers" / "downloads" / "topic" / "one.pdf"
    legacy = repo_root / "research" / "topic" / "old.pdf"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    legacy.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(MINIMAL_PDF)
    legacy.write_bytes(MINIMAL_PDF)
    registry_path = repo_root / "papers" / "downloads" / "CANONICAL_REGISTRY.json"
    digest = (
        "b3ec0ca7710d1025ee7ac7994d83b2ddbc200e5543df1066717d7124faf71d8f"
    )
    write_registry(
        registry_path,
        {
            "sources": [
                {
                    "id": "source_one",
                    "artifacts": ["papers/downloads/topic/one.pdf"],
                }
            ],
            "legacy_aliases": [
                {
                    "legacy_path": "research/topic/old.pdf",
                    "canonical_artifacts": ["papers/downloads/topic/one.pdf"],
                }
            ],
            "duplicate_groups": [
                {
                    "id": "documented_dup",
                    "canonical_path": "papers/downloads/topic/one.pdf",
                    "alias_paths": ["research/topic/old.pdf"],
                }
            ],
            "files": [
                {
                    "path": "papers/downloads/topic/one.pdf",
                    "sha256": digest,
                    "size_bytes": len(MINIMAL_PDF),
                }
            ],
        },
    )

    errors = validate_paper_corpus(registry_path, repo_root=repo_root)

    assert any("legacy path still exists" in error for error in errors)
