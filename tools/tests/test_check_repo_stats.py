"""Tests for generated repo stats and stale-output detection."""
from __future__ import annotations

import json
from pathlib import Path

from check_repo_stats import validate_repo_stats
from repo_stats import generate_repo_stats, render_repo_stats_markdown


def seed_repo(tmp_path: Path) -> tuple[Path, Path]:
    (tmp_path / "papers" / "downloads" / "topic").mkdir(parents=True, exist_ok=True)
    (tmp_path / "papers" / "downloads" / "topic" / "paper.pdf").write_text("pdf", encoding="utf-8")
    stats = generate_repo_stats(tmp_path)
    stats_json_path = tmp_path / "docs" / "generated" / "repo_stats.json"
    stats_md_path = tmp_path / "docs" / "generated" / "repo_stats.md"
    stats_json_path.parent.mkdir(parents=True, exist_ok=True)
    stats_json_path.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    stats_md_path.write_text(render_repo_stats_markdown(stats), encoding="utf-8")
    return stats_json_path, stats_md_path


def test_generate_repo_stats_counts_expected_surfaces(tmp_path: Path) -> None:
    (tmp_path / "papers" / "downloads" / "algorithms").mkdir(parents=True, exist_ok=True)
    (tmp_path / "papers" / "downloads" / "algorithms" / "one.pdf").write_text("pdf", encoding="utf-8")
    (tmp_path / "papers" / "A.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "papers" / "B.md").write_text("# B\n", encoding="utf-8")
    (tmp_path / "research" / "topic").mkdir(parents=True, exist_ok=True)
    (tmp_path / "research" / "topic" / "REPORT.md").write_text("# report\n", encoding="utf-8")
    (tmp_path / "research" / "topic" / "primary_source_notes.md").write_text("# notes\n", encoding="utf-8")
    (tmp_path / "docs" / "external_sources").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "external_sources" / "topic_source_cache.md").write_text("# cache\n", encoding="utf-8")
    (tmp_path / "datasets" / "source_assets" / "demo").mkdir(parents=True, exist_ok=True)
    (tmp_path / "datasets" / "source_assets" / "demo" / "asset.pdf").write_text("asset", encoding="utf-8")

    stats = generate_repo_stats(tmp_path)

    assert stats["metrics"]["canonical_pdf_count"] == 1
    assert stats["metrics"]["top_level_papers_markdown_count"] == 2
    assert stats["metrics"]["research_markdown_count"] == 2
    assert stats["metrics"]["source_cache_doc_count"] == 1
    assert stats["metrics"]["primary_source_notes_count"] == 1
    assert stats["metrics"]["source_asset_pdf_count"] == 1
    assert stats["pdf_by_topic"] == {"algorithms": 1}


def test_validate_repo_stats_accepts_current_generated_outputs(tmp_path: Path) -> None:
    stats_json_path, stats_md_path = seed_repo(tmp_path)

    assert validate_repo_stats(tmp_path, stats_json_path, stats_md_path) == []


def test_validate_repo_stats_rejects_stale_outputs(tmp_path: Path) -> None:
    (tmp_path / "papers" / "downloads" / "topic").mkdir(parents=True, exist_ok=True)
    (tmp_path / "papers" / "downloads" / "topic" / "paper.pdf").write_text("pdf", encoding="utf-8")
    stats_json_path = tmp_path / "docs" / "generated" / "repo_stats.json"
    stats_md_path = tmp_path / "docs" / "generated" / "repo_stats.md"
    stats_json_path.parent.mkdir(parents=True, exist_ok=True)
    stats_json_path.write_text("{}\n", encoding="utf-8")
    stats_md_path.write_text("# stale\n", encoding="utf-8")

    errors = validate_repo_stats(tmp_path, stats_json_path, stats_md_path)

    assert any("JSON is stale" in error for error in errors)
    assert any("Markdown is stale" in error for error in errors)
