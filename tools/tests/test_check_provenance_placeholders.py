"""Tests for check_provenance_placeholders provenance-sentinel scanner."""
from __future__ import annotations

import json

# Allow direct import from tools/
import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_provenance_placeholders import main, scan_file


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# scan_file unit tests
# ---------------------------------------------------------------------------

class TestScanFile:
    def test_clean_file_returns_no_hits(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "clean.md", "# Clean file\n\nAll good here.\n")
        assert scan_file(f) == []

    def test_detects_todo(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "- TODO: fill in the source\n")
        hits = scan_file(f)
        assert len(hits) == 1
        label = hits[0][1]
        assert label == "TODO"

    def test_detects_tbd(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "URL: TBD\n")
        hits = scan_file(f)
        assert len(hits) == 1

    def test_detects_unknown_source(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "UNKNOWN SOURCE for this entry\n")
        hits = scan_file(f)
        assert len(hits) == 1
        assert hits[0][1] == "UNKNOWN SOURCE"

    def test_detects_source_unknown(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "SOURCE UNKNOWN at the moment\n")
        hits = scan_file(f)
        assert len(hits) == 1

    def test_detects_missing_bracket(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "doi: [MISSING]\n")
        hits = scan_file(f)
        assert len(hits) == 1
        assert hits[0][1] == "[MISSING]"

    def test_detects_placeholder_bracket(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "author: [PLACEHOLDER]\n")
        hits = scan_file(f)
        assert hits[0][1] == "[PLACEHOLDER]"

    def test_detects_unresolved_bracket(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "status: [UNRESOLVED]\n")
        hits = scan_file(f)
        assert hits[0][1] == "[UNRESOLVED]"

    def test_detects_url_tbd(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "URL: TBD\n")
        hits = scan_file(f)
        assert any(h[1] == "URL: TBD" or h[1] == "TBD" for h in hits)

    def test_detects_doi_tbd(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "DOI: TBD\n")
        hits = scan_file(f)
        assert len(hits) == 1

    def test_detects_access_pending(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "ACCESS: PENDING\n")
        hits = scan_file(f)
        assert len(hits) == 1
        assert hits[0][1] == "ACCESS: PENDING"

    def test_one_hit_per_line(self, tmp_path: Path) -> None:
        # A line with both TODO and TBD should produce exactly one hit
        f = _write(tmp_path / "t.md", "TODO: URL is TBD\n")
        hits = scan_file(f)
        assert len(hits) == 1

    def test_hit_tuple_has_correct_lineno(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "line one\nTODO: fix this\nline three\n")
        hits = scan_file(f)
        assert hits[0][0] == 2  # second line

    def test_case_insensitive_todo(self, tmp_path: Path) -> None:
        f = _write(tmp_path / "t.md", "todo: lowercase variant\n")
        hits = scan_file(f)
        assert len(hits) == 1


# ---------------------------------------------------------------------------
# main() integration tests
# ---------------------------------------------------------------------------

class TestMain:
    def _make_scan_tree(self, root: Path, content: str = "") -> None:
        """Create a minimal SCAN_DIRS layout under root."""
        ext_dir = root / "docs" / "external_sources"
        ext_dir.mkdir(parents=True, exist_ok=True)
        (ext_dir / "sources.md").write_text(content, encoding="utf-8")

    def test_clean_repo_exits_zero(self, tmp_path: Path) -> None:
        self._make_scan_tree(tmp_path, "# Clean\n\nNo issues here.\n")
        rc = main(["--root", str(tmp_path)])
        assert rc == 0

    def test_dirty_repo_exits_nonzero(self, tmp_path: Path) -> None:
        self._make_scan_tree(tmp_path, "TODO: still missing source\n")
        rc = main(["--root", str(tmp_path)])
        assert rc == 1

    def test_missing_scan_dirs_exits_zero(self, tmp_path: Path) -> None:
        # No docs/external_sources or research dirs -> nothing to scan -> pass
        rc = main(["--root", str(tmp_path)])
        assert rc == 0

    def test_json_output_clean(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        self._make_scan_tree(tmp_path, "All clean.\n")
        rc = main(["--json", "--root", str(tmp_path)])
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["total"] == 0
        assert payload["hits"] == []
        assert rc == 0

    def test_json_output_with_hits(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        self._make_scan_tree(tmp_path, "TODO: check this source\n")
        rc = main(["--json", "--root", str(tmp_path)])
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["total"] >= 1
        hit = payload["hits"][0]
        assert "file" in hit
        assert "line" in hit
        assert "label" in hit
        assert "excerpt" in hit
        assert rc == 1

    def test_human_output_clean(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        self._make_scan_tree(tmp_path, "All good.\n")
        main(["--root", str(tmp_path)])
        captured = capsys.readouterr()
        assert "no unresolved" in captured.out

    def test_human_output_with_hit(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        self._make_scan_tree(tmp_path, "SOURCE UNKNOWN\n")
        main(["--root", str(tmp_path)])
        captured = capsys.readouterr()
        assert "PROVENANCE:" in captured.out

    def test_only_scans_target_extensions(self, tmp_path: Path) -> None:
        ext_dir = tmp_path / "docs" / "external_sources"
        ext_dir.mkdir(parents=True, exist_ok=True)
        (ext_dir / "data.csv").write_text("TODO: ignored\n", encoding="utf-8")
        (ext_dir / "script.py").write_text("TODO: ignored\n", encoding="utf-8")
        rc = main(["--root", str(tmp_path)])
        assert rc == 0  # .csv and .py are not in SCAN_EXTS

    def test_scans_research_dir(self, tmp_path: Path) -> None:
        research_dir = tmp_path / "research"
        research_dir.mkdir(parents=True, exist_ok=True)
        (research_dir / "notes.md").write_text("ACCESS: PENDING\n", encoding="utf-8")
        rc = main(["--root", str(tmp_path)])
        assert rc == 1
