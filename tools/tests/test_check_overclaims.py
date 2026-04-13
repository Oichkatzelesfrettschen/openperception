"""Tests for tools/check_overclaims.py."""

import json
from pathlib import Path

from check_overclaims import _is_allowlisted, main, scan_file


# ---------------------------------------------------------------------------
# Unit: _is_allowlisted
# ---------------------------------------------------------------------------


class TestAllowlist:
    def test_pixel_perfect_allowed(self):
        assert _is_allowlisted("Use pixel-perfect alignment for icons.")

    def test_plain_line_not_allowed(self):
        assert not _is_allowlisted("This algorithm is production-ready.")

    def test_not_a_guarantee_allowed(self):
        assert _is_allowlisted("This is not a guarantee of correctness.")

    def test_cannot_guarantee_allowed(self):
        assert _is_allowlisted("We cannot guarantee hardware behavior.")

    def test_v100_milestone_allowed(self):
        assert _is_allowlisted("### v1.0.0 - Production Ready")


# ---------------------------------------------------------------------------
# Unit: scan_file
# ---------------------------------------------------------------------------


class TestScanFile:
    def test_no_hits_on_clean_file(self, tmp_path):
        p = tmp_path / "clean.md"
        p.write_text("# Clean doc\n\nThis is fine.\n")
        assert scan_file(p) == []

    def test_production_ready_detected(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("This library is production-ready.\n")
        hits = scan_file(p)
        assert len(hits) == 1
        lineno, label, _, _excerpt = hits[0]
        assert lineno == 1
        assert "production" in label

    def test_guaranteed_detected(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("Results are guaranteed to be correct.\n")
        hits = scan_file(p)
        assert any("guaranteed" in h[1] for h in hits)

    def test_state_of_the_art_detected(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("Uses state-of-the-art algorithms.\n")
        hits = scan_file(p)
        assert any("state-of-the-art" in h[1] for h in hits)

    def test_never_fails_detected(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("The validator never fails on valid input.\n")
        hits = scan_file(p)
        assert any("never" in h[1] for h in hits)

    def test_always_accurate_detected(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("The simulation always accurate.\n")
        hits = scan_file(p)
        assert any("always" in h[1] for h in hits)

    def test_pixel_perfect_not_flagged(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("Icons require pixel-perfect alignment.\n")
        hits = scan_file(p)
        assert hits == []

    def test_not_a_guarantee_not_flagged(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("This is not a guarantee of production behavior.\n")
        hits = scan_file(p)
        assert hits == []

    def test_multiline_multiple_hits(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text("# Docs\n\nThis is production-ready.\nResults guaranteed.\n")
        hits = scan_file(p)
        assert len(hits) >= 2


# ---------------------------------------------------------------------------
# Integration: main() exit code and JSON output
# ---------------------------------------------------------------------------


class TestMain:
    def test_clean_repo_exits_zero(self, tmp_path):
        (tmp_path / "clean.md").write_text("No overclaims here.\n")
        rc = main(["--root", str(tmp_path)])
        assert rc == 0

    def test_dirty_repo_exits_nonzero(self, tmp_path):
        (tmp_path / "bad.md").write_text("This is production-ready.\n")
        rc = main(["--root", str(tmp_path)])
        assert rc == 1

    def test_json_mode_on_dirty(self, tmp_path, capsys):
        (tmp_path / "bad.md").write_text("Results are guaranteed.\n")
        rc = main(["--root", str(tmp_path), "--json"])
        assert rc == 1
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["total"] >= 1
        assert data["hits"][0]["file"] == "bad.md"

    def test_json_mode_on_clean(self, tmp_path, capsys):
        (tmp_path / "ok.md").write_text("Nothing to flag.\n")
        rc = main(["--root", str(tmp_path), "--json"])
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert data["total"] == 0

    def test_skip_dirs_respected(self, tmp_path):
        papers = tmp_path / "papers"
        papers.mkdir()
        (papers / "overclaim.md").write_text("This is state-of-the-art.\n")
        rc = main(["--root", str(tmp_path)])
        assert rc == 0

    def test_skip_files_respected(self, tmp_path):
        # CLAUDE.md is in SKIP_FILES; create one with an overclaim
        (tmp_path / "CLAUDE.md").write_text("Production-ready implementations.\n")
        rc = main(["--root", str(tmp_path)])
        assert rc == 0

    def test_real_repo_passes(self):
        """Verify the actual repo passes its own linter."""
        repo_root = Path(__file__).resolve().parents[2]
        rc = main(["--root", str(repo_root)])
        assert rc == 0, "Overclaim phrases found in real repo docs"
