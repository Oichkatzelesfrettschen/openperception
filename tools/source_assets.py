"""
Validate dataset source-asset provenance and local artifact integrity.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ASSETS_ROOT = REPO_ROOT / "datasets" / "source_assets"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _looks_like_pdf(path: Path) -> bool:
    return path.read_bytes().startswith(b"%PDF")


def _load_provenance(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_source_assets(repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    source_assets_root = repo_root / "datasets" / "source_assets"
    if not source_assets_root.exists():
        return errors

    provenance_files = sorted(source_assets_root.rglob("PROVENANCE.json"))
    if not provenance_files:
        errors.append("datasets/source_assets exists but has no PROVENANCE.json files")
        return errors

    indexed_paths: dict[str, Path] = {}
    for provenance_path in provenance_files:
        payload = _load_provenance(provenance_path)
        assets = payload.get("assets", [])
        if not assets:
            errors.append(
                f"source-assets provenance file has no assets: {provenance_path.relative_to(repo_root).as_posix()}"
            )
            continue
        for asset in assets:
            asset_id = asset.get("id", "<missing-id>")
            local_path = asset.get("local_path")
            if not local_path:
                errors.append(
                    f"source-asset entry {asset_id} missing local_path in "
                    f"{provenance_path.relative_to(repo_root).as_posix()}"
                )
                continue
            if local_path in indexed_paths:
                errors.append(
                    f"source-asset local_path is duplicated across provenance files: {local_path}"
                )
                continue
            indexed_paths[local_path] = provenance_path

            asset_path = repo_root / local_path
            if not asset_path.exists():
                errors.append(f"source-asset entry {asset_id} references missing file {local_path}")
                continue

            size_bytes = asset_path.stat().st_size
            if size_bytes == 0:
                errors.append(f"source-asset file is zero-byte: {local_path}")
            if asset_path.suffix.lower() == ".pdf" and not _looks_like_pdf(asset_path):
                errors.append(f"source-asset PDF does not start with %PDF: {local_path}")

            expected_hash = asset.get("sha256")
            if expected_hash != _sha256(asset_path):
                errors.append(
                    f"source-asset hash mismatch for {local_path}: "
                    f"expected {expected_hash} got {_sha256(asset_path)}"
                )
            if asset.get("size_bytes") != size_bytes:
                errors.append(
                    f"source-asset size mismatch for {local_path}: "
                    f"expected {asset.get('size_bytes')} got {size_bytes}"
                )

            verification_trace = asset.get("verification_trace")
            upstream_url = asset.get("upstream_url")
            reference_urls = asset.get("reference_urls", [])
            if verification_trace:
                trace_path = repo_root / verification_trace
                if not trace_path.exists():
                    errors.append(
                        f"source-asset verification trace is missing for {local_path}: {verification_trace}"
                    )
            if not upstream_url and not reference_urls:
                errors.append(
                    f"source-asset entry {asset_id} must provide upstream_url or reference_urls"
                )

    actual_asset_files = sorted(
        path.relative_to(repo_root).as_posix()
        for path in source_assets_root.rglob("*")
        if path.is_file() and path.name not in {"README.md", "PROVENANCE.json"}
    )
    tracked_asset_files = sorted(
        path for path in actual_asset_files if not path.endswith(".md")
    )
    for rel_path in tracked_asset_files:
        if rel_path not in indexed_paths:
            errors.append(f"source-asset file is not indexed in provenance: {rel_path}")

    return errors
