"""Direct-call tests for daltonlens.main to improve coverage.

The subprocess-based test_cli.py covers the full integration path but does
not register in pytest-cov because each subprocess is a separate process.
These tests call the Python functions directly so that coverage is tracked.
"""

import sys
from pathlib import Path
from unittest import mock

import numpy as np
import pytest

from daltonlens import simulate
from daltonlens.main import get_simulator, DEFICIENCY_FROM_STR


# ---------------------------------------------------------------------------
# get_simulator()
# ---------------------------------------------------------------------------

class TestGetSimulator:
    def test_auto(self):
        s = get_simulator("auto")
        assert isinstance(s, simulate.Simulator_AutoSelect)

    def test_vienot(self):
        s = get_simulator("vienot")
        assert isinstance(s, simulate.Simulator_Vienot1999)

    def test_brettel(self):
        s = get_simulator("brettel")
        assert isinstance(s, simulate.Simulator_Brettel1997)

    def test_machado(self):
        s = get_simulator("machado")
        assert isinstance(s, simulate.Simulator_Machado2009)

    def test_vischeck(self):
        s = get_simulator("vischeck")
        assert isinstance(s, simulate.Simulator_Vischeck)

    def test_coblis_v1(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            s = get_simulator("coblisV1")
        assert isinstance(s, simulate.Simulator_CoblisV1)

    def test_coblis_v2(self):
        s = get_simulator("coblisV2")
        assert isinstance(s, simulate.Simulator_CoblisV2)


# ---------------------------------------------------------------------------
# DEFICIENCY_FROM_STR
# ---------------------------------------------------------------------------

class TestDeficiencyFromStr:
    def test_protan(self):
        assert DEFICIENCY_FROM_STR["protan"] == simulate.Deficiency.PROTAN

    def test_deutan(self):
        assert DEFICIENCY_FROM_STR["deutan"] == simulate.Deficiency.DEUTAN

    def test_tritan(self):
        assert DEFICIENCY_FROM_STR["tritan"] == simulate.Deficiency.TRITAN

    def test_achromat(self):
        assert DEFICIENCY_FROM_STR["achromat"] == simulate.Deficiency.ACHROMAT

    def test_bcm(self):
        assert DEFICIENCY_FROM_STR["bcm"] == simulate.Deficiency.BCM


# ---------------------------------------------------------------------------
# main() called directly via sys.argv patching
# ---------------------------------------------------------------------------

@pytest.fixture()
def tiny_image(tmp_path):
    """Write a tiny 4x4 RGB PNG and return its path."""
    from PIL import Image as PILImage
    arr = np.full((4, 4, 3), 128, dtype=np.uint8)
    img = PILImage.fromarray(arr)
    p = tmp_path / "input.png"
    img.save(p)
    return p


class TestMainDirect:
    def _call_main(self, argv):
        with mock.patch("sys.argv", ["daltonlens"] + argv):
            from daltonlens.main import main
            main()

    def test_simulate_protan_default_model(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        self._call_main([str(tiny_image), str(out), "--deficiency", "protan"])
        assert out.exists()

    def test_simulate_deutan_brettel(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        self._call_main([
            str(tiny_image), str(out),
            "--deficiency", "deutan",
            "--model", "brettel",
        ])
        assert out.exists()

    def test_simulate_tritan_machado(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        self._call_main([
            str(tiny_image), str(out),
            "--deficiency", "tritan",
            "--model", "machado",
        ])
        assert out.exists()

    def test_simulate_achromat(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        self._call_main([str(tiny_image), str(out), "--deficiency", "achromat"])
        assert out.exists()

    def test_simulate_bcm(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        self._call_main([str(tiny_image), str(out), "--deficiency", "bcm"])
        assert out.exists()

    def test_simulate_severity_half(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        self._call_main([
            str(tiny_image), str(out),
            "--deficiency", "protan",
            "--severity", "0.5",
        ])
        assert out.exists()

    def test_daltonize_fidaner(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        self._call_main([
            str(tiny_image), str(out),
            "--filter", "daltonize",
            "--deficiency", "protan",
            "--daltonize-method", "fidaner",
        ])
        assert out.exists()

    def test_daltonize_simple(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        self._call_main([
            str(tiny_image), str(out),
            "--filter", "daltonize",
            "--deficiency", "deutan",
            "--daltonize-method", "simple",
        ])
        assert out.exists()

    def test_missing_input_exits_nonzero(self, tmp_path):
        out = tmp_path / "out.png"
        with pytest.raises(SystemExit) as exc:
            self._call_main([
                str(tmp_path / "nonexistent.png"),
                str(out),
            ])
        assert exc.value.code != 0

    def test_output_shape_preserved(self, tmp_path):
        from PIL import Image as PILImage
        arr = np.zeros((8, 12, 3), dtype=np.uint8)
        inp = tmp_path / "in.png"
        PILImage.fromarray(arr).save(inp)
        out = tmp_path / "out.png"
        self._call_main([str(inp), str(out)])
        with PILImage.open(out) as im:
            assert im.size == (12, 8)   # PIL size is (width, height)

    def test_load_failure_exits_nonzero(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        with mock.patch("daltonlens.main.Image.open", side_effect=OSError("corrupt")):
            with pytest.raises(SystemExit) as exc:
                self._call_main([str(tiny_image), str(out)])
        assert exc.value.code != 0

    def test_save_failure_exits_nonzero(self, tiny_image, tmp_path):
        out = tmp_path / "out.png"
        with mock.patch("daltonlens.main.Image.fromarray") as mock_fromarray:
            mock_fromarray.return_value.save.side_effect = OSError("disk full")
            with pytest.raises(SystemExit) as exc:
                self._call_main([str(tiny_image), str(out)])
        assert exc.value.code != 0


# ---------------------------------------------------------------------------
# Batch mode
# ---------------------------------------------------------------------------

class TestBatchMode:
    def _call_main(self, argv):
        with mock.patch("sys.argv", ["daltonlens"] + argv):
            from daltonlens.main import main
            main()

    def test_batch_processes_all_matches(self, tmp_path):
        from PIL import Image as PILImage
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        out_dir = tmp_path / "out"
        for name in ["a.png", "b.png", "c.png"]:
            arr = np.full((4, 4, 3), 64, dtype=np.uint8)
            PILImage.fromarray(arr).save(src_dir / name)

        self._call_main([
            "--batch", str(src_dir / "*.png"),
            "--output-dir", str(out_dir),
        ])

        assert len(list(out_dir.glob("*.png"))) == 3

    def test_batch_without_output_dir_exits_nonzero(self, tmp_path):
        with pytest.raises(SystemExit) as exc:
            self._call_main(["--batch", str(tmp_path / "*.png")])
        assert exc.value.code != 0

    def test_batch_no_matches_exits_nonzero(self, tmp_path):
        out_dir = tmp_path / "out"
        with pytest.raises(SystemExit) as exc:
            self._call_main([
                "--batch", str(tmp_path / "nonexistent*.png"),
                "--output-dir", str(out_dir),
            ])
        assert exc.value.code != 0

    def test_batch_creates_output_dir(self, tmp_path):
        from PIL import Image as PILImage
        src = tmp_path / "img.png"
        arr = np.full((4, 4, 3), 64, dtype=np.uint8)
        PILImage.fromarray(arr).save(src)
        out_dir = tmp_path / "new" / "subdir"

        self._call_main([
            "--batch", str(tmp_path / "*.png"),
            "--output-dir", str(out_dir),
        ])

        assert out_dir.exists()

    def test_single_mode_missing_output_exits_nonzero(self, tmp_path):
        # No positional args and no --batch -> error
        with pytest.raises(SystemExit) as exc:
            self._call_main([])
        assert exc.value.code != 0


# ---------------------------------------------------------------------------
# __main__.py entrypoint
# ---------------------------------------------------------------------------

class TestMainEntrypoint:
    def test_module_entrypoint_runs_main(self, tmp_path):
        """__main__.py calls main(); verify it executes via sys.argv patch."""
        import runpy
        from PIL import Image as PILImage
        arr = np.full((4, 4, 3), 64, dtype=np.uint8)
        inp = tmp_path / "in.png"
        out = tmp_path / "out.png"
        PILImage.fromarray(arr).save(inp)
        with mock.patch("sys.argv", ["daltonlens", str(inp), str(out)]):
            runpy.run_module("daltonlens", run_name="__main__", alter_sys=True)
        assert out.exists()
