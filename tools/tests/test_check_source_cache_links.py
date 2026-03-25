"""Tests for source-cache related-doc link validation."""
from __future__ import annotations

from pathlib import Path

from source_cache_links import validate_source_cache_links


def write_source_cache(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_validate_source_cache_links_accepts_report_and_notes_links(
    tmp_path: Path,
) -> None:
    report = tmp_path / "research" / "topic" / "REPORT.md"
    notes = tmp_path / "research" / "topic" / "primary_source_notes.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("# report\n", encoding="utf-8")
    notes.write_text("# notes\n", encoding="utf-8")
    write_source_cache(
        tmp_path / "docs" / "external_sources" / "topic_source_cache.md",
        "\n".join(
            [
                "# Topic Source Cache",
                "",
                f"- [Report]({report})",
                f"- [Notes]({notes})",
            ]
        ),
    )

    assert validate_source_cache_links(tmp_path) == []


def test_validate_source_cache_links_accepts_single_papers_link(tmp_path: Path) -> None:
    paper_doc = tmp_path / "papers" / "topic_compendium.md"
    paper_doc.parent.mkdir(parents=True, exist_ok=True)
    paper_doc.write_text("# compendium\n", encoding="utf-8")
    write_source_cache(
        tmp_path / "docs" / "external_sources" / "topic_source_cache.md",
        f"# Topic Source Cache\n\n- [Compendium]({paper_doc})\n",
    )

    assert validate_source_cache_links(tmp_path) == []


def test_validate_source_cache_links_rejects_registry_only_links(tmp_path: Path) -> None:
    registry = tmp_path / "docs" / "external_sources" / "paper_corpus_registry.md"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text("# registry\n", encoding="utf-8")
    write_source_cache(
        tmp_path / "docs" / "external_sources" / "topic_source_cache.md",
        f"# Topic Source Cache\n\n- [Registry]({registry})\n",
    )

    errors = validate_source_cache_links(tmp_path)

    assert any("must link to at least one research-facing repo doc" in error for error in errors)


def test_validate_source_cache_links_rejects_missing_target(tmp_path: Path) -> None:
    missing = tmp_path / "research" / "topic" / "REPORT.md"
    write_source_cache(
        tmp_path / "docs" / "external_sources" / "topic_source_cache.md",
        f"# Topic Source Cache\n\n- [Missing]({missing})\n",
    )

    errors = validate_source_cache_links(tmp_path)

    assert any("links to missing repo path" in error for error in errors)


def test_validate_source_cache_links_rejects_master_index_only(tmp_path: Path) -> None:
    master_index = tmp_path / "MASTER_INDEX.md"
    master_index.write_text("# index\n", encoding="utf-8")
    write_source_cache(
        tmp_path / "docs" / "external_sources" / "topic_source_cache.md",
        f"# Topic Source Cache\n\n- [Index]({master_index})\n",
    )

    errors = validate_source_cache_links(tmp_path)

    assert any("must link to at least one research-facing repo doc" in error for error in errors)
