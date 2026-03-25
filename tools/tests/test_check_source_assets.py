"""Tests for dataset source-asset provenance validation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from source_assets import validate_source_assets


MINIMAL_PDF = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF\n"
MINIMAL_PDF_SHA256 = hashlib.sha256(MINIMAL_PDF).hexdigest()


def write_provenance(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def seed_asset_repo(repo_root: Path) -> None:
    asset = repo_root / "datasets" / "source_assets" / "topic" / "sample.pdf"
    asset.parent.mkdir(parents=True, exist_ok=True)
    asset.write_bytes(MINIMAL_PDF)
    trace = repo_root / "datasets" / "source_assets" / "topic" / "trace.md"
    trace.write_text("trace\n", encoding="utf-8")
    write_provenance(
        repo_root / "datasets" / "source_assets" / "topic" / "PROVENANCE.json",
        {
            "assets": [
                {
                    "id": "sample_asset",
                    "asset_type": "nonpaper_reference_pdf",
                    "local_path": "datasets/source_assets/topic/sample.pdf",
                    "sha256": MINIMAL_PDF_SHA256,
                    "size_bytes": len(MINIMAL_PDF),
                    "upstream_url": "https://example.com/sample.pdf",
                    "verification_trace": "datasets/source_assets/topic/trace.md",
                }
            ]
        },
    )


def test_validate_source_assets_accepts_seeded_repo(tmp_path: Path) -> None:
    seed_asset_repo(tmp_path)

    assert validate_source_assets(tmp_path) == []


def test_validate_source_assets_rejects_unindexed_asset_file(tmp_path: Path) -> None:
    seed_asset_repo(tmp_path)
    extra = tmp_path / "datasets" / "source_assets" / "topic" / "extra.pdf"
    extra.write_bytes(MINIMAL_PDF)

    errors = validate_source_assets(tmp_path)

    assert any("source-asset file is not indexed in provenance" in error for error in errors)


def test_validate_source_assets_rejects_missing_trace_and_missing_urls(
    tmp_path: Path,
) -> None:
    asset = tmp_path / "datasets" / "source_assets" / "topic" / "sample.pdf"
    asset.parent.mkdir(parents=True, exist_ok=True)
    asset.write_bytes(MINIMAL_PDF)
    write_provenance(
        tmp_path / "datasets" / "source_assets" / "topic" / "PROVENANCE.json",
        {
            "assets": [
                {
                    "id": "sample_asset",
                    "local_path": "datasets/source_assets/topic/sample.pdf",
                    "sha256": MINIMAL_PDF_SHA256,
                    "size_bytes": len(MINIMAL_PDF),
                    "verification_trace": "datasets/source_assets/topic/missing.md",
                }
            ]
        },
    )

    errors = validate_source_assets(tmp_path)

    assert any("verification trace is missing" in error for error in errors)
    assert any("must provide upstream_url or reference_urls" in error for error in errors)


def test_validate_source_assets_rejects_hash_mismatch(tmp_path: Path) -> None:
    seed_asset_repo(tmp_path)
    provenance_path = tmp_path / "datasets" / "source_assets" / "topic" / "PROVENANCE.json"
    payload = json.loads(provenance_path.read_text(encoding="utf-8"))
    payload["assets"][0]["sha256"] = "0" * 64
    provenance_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    errors = validate_source_assets(tmp_path)

    assert any("source-asset hash mismatch" in error for error in errors)
