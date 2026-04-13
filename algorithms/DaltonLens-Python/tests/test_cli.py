"""Integration tests for the daltonlens CLI (daltonlens-python command)."""

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest


try:
    from PIL import Image

    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def _run_cli(*args):
    """Run the daltonlens CLI and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, "-m", "daltonlens", *args],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).resolve().parents[1]),
    )
    return result.returncode, result.stdout, result.stderr


def _make_test_image(path: str, size=(16, 16)):
    """Create a small test PNG image."""
    arr = np.random.randint(0, 255, (*size, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    img.save(path)


@pytest.mark.skipif(not HAS_PIL, reason="Pillow required for CLI tests")
class TestCLIHelp:
    def test_help_exits_zero(self):
        rc, _stdout, _stderr = _run_cli("--help")
        assert rc == 0

    def test_help_contains_usage(self):
        _rc, stdout, stderr = _run_cli("--help")
        assert "usage" in stdout.lower() or "usage" in stderr.lower()


@pytest.mark.skipif(not HAS_PIL, reason="Pillow required for CLI tests")
class TestCLISimulate:
    def test_simulate_protan(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, stderr = _run_cli(inp, out, "--deficiency", "protan")
            assert rc == 0, f"CLI failed: {stderr}"
            assert out.exists()

    def test_simulate_deutan(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, stderr = _run_cli(inp, out, "--deficiency", "deutan")
            assert rc == 0, f"CLI failed: {stderr}"

    def test_simulate_tritan(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, stderr = _run_cli(inp, out, "--deficiency", "tritan")
            assert rc == 0, f"CLI failed: {stderr}"

    def test_output_is_valid_image(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp, size=(32, 32))
            rc, _, _ = _run_cli(inp, out, "--deficiency", "protan")
            assert rc == 0
            with Image.open(out) as im:
                size = im.size
            assert size == (32, 32)

    def test_model_brettel(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, stderr = _run_cli(
                inp, out, "--model", "brettel", "--deficiency", "protan"
            )
            assert rc == 0, f"CLI failed: {stderr}"


@pytest.mark.skipif(not HAS_PIL, reason="Pillow required for CLI tests")
class TestCLIDaltonize:
    def test_daltonize_fidaner(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, stderr = _run_cli(
                inp, out, "--filter", "daltonize", "--deficiency", "protan"
            )
            assert rc == 0, f"CLI daltonize failed: {stderr}"
            assert out.exists()


@pytest.mark.skipif(not HAS_PIL, reason="Pillow required for CLI tests")
class TestCLIErrorHandling:
    def test_missing_input_file(self):
        rc, _stdout, _stderr = _run_cli("/nonexistent/path.png", "/tmp/out.png")
        assert rc != 0

    def test_output_to_nonexistent_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            _make_test_image(inp)
            out = "/nonexistent_dir/output.png"
            rc, _stdout, _stderr = _run_cli(inp, out)
            assert rc != 0

    def test_invalid_model_choice(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, _stderr = _run_cli(inp, out, "--model", "invalidmodel")
            # argparse rejects invalid choices with nonzero exit
            assert rc != 0

    def test_invalid_deficiency_choice(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, _stderr = _run_cli(inp, out, "--deficiency", "quatran")
            assert rc != 0

    def test_invalid_filter_choice(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, _stderr = _run_cli(inp, out, "--filter", "notafilter")
            assert rc != 0

    def test_severity_above_one(self):
        """severity > 1.0 should cause a nonzero exit (ValueError in simulate_cvd)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, _stderr = _run_cli(inp, out, "--severity", "1.5")
            assert rc != 0

    def test_severity_below_zero(self):
        """severity < 0.0 should cause a nonzero exit (ValueError in simulate_cvd)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            inp = tmpdir / "input.png"
            out = tmpdir / "output.png"
            _make_test_image(inp)
            rc, _stdout, _stderr = _run_cli(inp, out, "--severity", "-0.5")
            assert rc != 0
