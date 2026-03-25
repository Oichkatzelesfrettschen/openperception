"""Tests for paper corpus registry validation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from paper_corpus import (
    ALLOWED_NONCANONICAL_REFERENCE_DOCS,
    collect_noncanonical_reference_violations,
    collect_remaining_research_pdf_paths,
    validate_paper_corpus,
)


MINIMAL_PDF = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF\n"
MINIMAL_PDF_SHA256 = hashlib.sha256(MINIMAL_PDF).hexdigest()


def write_registry(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def minimal_registry() -> dict:
    return {
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
        "duplicate_groups": [],
        "files": [
            {
                "path": "papers/downloads/topic/one.pdf",
                "sha256": MINIMAL_PDF_SHA256,
                "size_bytes": len(MINIMAL_PDF),
            }
        ],
    }


def seed_minimal_repo(repo_root: Path) -> Path:
    artifact = repo_root / "papers" / "downloads" / "topic" / "one.pdf"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(MINIMAL_PDF)
    registry_path = repo_root / "papers" / "downloads" / "CANONICAL_REGISTRY.json"
    write_registry(registry_path, minimal_registry())
    return registry_path


def seed_research_pdf(repo_root: Path, rel_path: str) -> Path:
    path = repo_root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(MINIMAL_PDF)
    return path


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
    digest = MINIMAL_PDF_SHA256
    payload = minimal_registry()
    payload["legacy_aliases"] = []
    payload["files"][0]["sha256"] = digest
    write_registry(registry_path, payload)

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
    digest = MINIMAL_PDF_SHA256
    payload = minimal_registry()
    payload["duplicate_groups"] = [
        {
            "id": "documented_dup",
            "canonical_path": "papers/downloads/topic/one.pdf",
            "alias_paths": ["research/topic/old.pdf"],
        }
    ]
    payload["files"][0]["sha256"] = digest
    write_registry(registry_path, payload)

    errors = validate_paper_corpus(registry_path, repo_root=repo_root)

    assert any("legacy path still exists" in error for error in errors)


def test_collect_noncanonical_reference_violations_rejects_stale_markdown_reference(
    tmp_path: Path,
) -> None:
    registry_path = seed_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "Stale reference: research/topic/old.pdf\n",
        encoding="utf-8",
    )

    errors = validate_paper_corpus(registry_path, repo_root=tmp_path)

    assert any(
        "noncanonical research PDF reference outside allowed provenance docs" in error
        for error in errors
    )


def test_collect_noncanonical_reference_violations_allows_provenance_docs(
    tmp_path: Path,
) -> None:
    registry_path = seed_minimal_repo(tmp_path)
    for rel_path in ALLOWED_NONCANONICAL_REFERENCE_DOCS:
        path = tmp_path / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Documented alias: research/topic/old.pdf\n", encoding="utf-8")

    registry = json.loads(registry_path.read_text(encoding="utf-8"))

    assert collect_noncanonical_reference_violations(registry, tmp_path) == []


def test_collect_noncanonical_reference_violations_rejects_live_research_pdf_path_in_bib(
    tmp_path: Path,
) -> None:
    registry_path = seed_minimal_repo(tmp_path)
    seed_research_pdf(tmp_path, "research/topic/live.pdf")
    (tmp_path / "refs.bib").write_text(
        "@misc{live,\n  file = {research/topic/live.pdf}\n}\n",
        encoding="utf-8",
    )

    errors = validate_paper_corpus(registry_path, repo_root=tmp_path)

    assert any(
        "noncanonical research PDF reference outside allowed provenance docs: "
        "research/topic/live.pdf in refs.bib" in error
        for error in errors
    )


def test_collect_noncanonical_reference_violations_allows_canonical_cache_path(
    tmp_path: Path,
) -> None:
    registry_path = seed_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "Canonical reference: papers/downloads/topic/one.pdf\n",
        encoding="utf-8",
    )

    assert validate_paper_corpus(registry_path, repo_root=tmp_path) == []


def test_collect_remaining_research_pdf_paths_reports_unmigrated_research_pdfs(
    tmp_path: Path,
) -> None:
    registry_path = seed_minimal_repo(tmp_path)
    seed_research_pdf(tmp_path, "research/topic/live.pdf")
    seed_research_pdf(tmp_path, "research/topic/second.pdf")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))

    assert collect_remaining_research_pdf_paths(registry, tmp_path) == [
        "research/topic/live.pdf",
        "research/topic/second.pdf",
    ]
