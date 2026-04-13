"""Edge-case tests for daltonlens/simulate.py."""
import numpy as np
import pytest

from daltonlens import convert, simulate
from daltonlens.simulate import Deficiency


def _make_sim():
    return simulate.Simulator_Brettel1997(convert.LMSModel_sRGB_SmithPokorny75())


class TestAllBlackAndWhite:
    def test_black_image_protan(self):
        sim = _make_sim()
        im = np.zeros((8, 8, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.PROTAN, severity=1.0)
        np.testing.assert_array_equal(result, 0)

    def test_white_image_deutan(self):
        sim = _make_sim()
        im = np.full((8, 8, 3), 255, dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.DEUTAN, severity=1.0)
        # White maps to white under dichromacy
        np.testing.assert_allclose(result.astype(float), 255.0, atol=2)

    def test_black_image_tritan(self):
        sim = _make_sim()
        im = np.zeros((6, 6, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.TRITAN, severity=1.0)
        np.testing.assert_array_equal(result, 0)


class TestMinimalImageSize:
    def test_1x1_pixel(self):
        sim = _make_sim()
        im = np.array([[[128, 64, 32]]], dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.PROTAN, severity=1.0)
        assert result.shape == (1, 1, 3)
        assert result.dtype == np.uint8

    def test_1xN_strip(self):
        sim = _make_sim()
        im = np.random.randint(0, 255, (1, 50, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.DEUTAN, severity=1.0)
        assert result.shape == (1, 50, 3)


class TestSeverityBounds:
    def test_severity_zero_identity(self):
        """Severity 0.0 means no CVD simulation; output should equal input."""
        sim = simulate.Simulator_Machado2009()
        im = np.random.randint(10, 245, (8, 8, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.PROTAN, severity=0.0)
        # At severity 0 the image should be identical (or very close)
        np.testing.assert_allclose(result.astype(float), im.astype(float), atol=1)

    def test_severity_one_produces_valid_output(self):
        sim = _make_sim()
        im = np.random.randint(0, 255, (8, 8, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.PROTAN, severity=1.0)
        assert result.dtype == np.uint8
        assert result.shape == im.shape

    def test_all_deficiency_types(self):
        # Use AutoSelect so all 5 Deficiency values are exercised without
        # hitting the Brettel None-return for ACHROMAT/BCM.
        sim = simulate.Simulator_AutoSelect()
        im = np.random.randint(0, 255, (8, 8, 3), dtype=np.uint8)
        for deficiency in Deficiency:
            result = sim.simulate_cvd(im, deficiency, severity=1.0)
            assert result.shape == im.shape
            assert result.dtype == np.uint8


class TestOutputRange:
    def test_output_is_uint8(self):
        sim = _make_sim()
        im = np.random.randint(0, 255, (16, 16, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.PROTAN, severity=1.0)
        assert result.dtype == np.uint8

    def test_output_within_0_255(self):
        sim = _make_sim()
        im = np.random.randint(0, 255, (16, 16, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.DEUTAN, severity=1.0)
        assert result.min() >= 0
        assert result.max() <= 255


class TestVienotSimulator:
    def test_basic_vienot(self):
        model = convert.LMSModel_sRGB_SmithPokorny75()
        sim = simulate.Simulator_Vienot1999(model)
        im = np.random.randint(0, 255, (8, 8, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.PROTAN, severity=1.0)
        assert result.shape == im.shape
        assert result.dtype == np.uint8


class TestAchromatAndBCM:
    """Edge cases specific to Simulator_Achromat and Simulator_BCM."""

    # ---- Simulator_Achromat ----

    def test_achromat_black_maps_to_black(self):
        sim = simulate.Simulator_Achromat()
        im = np.zeros((8, 8, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.ACHROMAT, severity=1.0)
        np.testing.assert_array_equal(result, 0)

    def test_achromat_white_maps_to_white(self):
        sim = simulate.Simulator_Achromat()
        im = np.full((8, 8, 3), 255, dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.ACHROMAT, severity=1.0)
        np.testing.assert_allclose(result.astype(float), 255.0, atol=1)

    def test_achromat_gray_all_channels_equal(self):
        """A mid-gray pixel must map to the same value in all three channels."""
        sim = simulate.Simulator_Achromat()
        im = np.full((8, 8, 3), 128, dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.ACHROMAT, severity=1.0)
        assert np.all(result[..., 0] == result[..., 1])
        assert np.all(result[..., 0] == result[..., 2])

    def test_achromat_bt709_green_brighter_than_red(self):
        """BT.709 green weight (0.7152) is ~3.4x the red weight (0.2126)."""
        sim = simulate.Simulator_Achromat()
        pure_red   = np.array([[[255,   0,   0]]], dtype=np.uint8)
        pure_green = np.array([[[  0, 255,   0]]], dtype=np.uint8)
        red_out   = sim.simulate_cvd(pure_red,   Deficiency.ACHROMAT, severity=1.0)
        green_out = sim.simulate_cvd(pure_green, Deficiency.ACHROMAT, severity=1.0)
        assert green_out[0, 0, 0] > red_out[0, 0, 0], (
            f"green lum {green_out[0,0,0]} should exceed red lum {red_out[0,0,0]}"
        )

    def test_achromat_severity_zero_identity(self):
        sim = simulate.Simulator_Achromat()
        rng = np.random.default_rng(42)
        im = rng.integers(10, 245, (8, 8, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.ACHROMAT, severity=0.0)
        np.testing.assert_allclose(result.astype(float), im.astype(float), atol=1)

    def test_achromat_output_shape_and_dtype(self):
        sim = simulate.Simulator_Achromat()
        im = np.random.randint(0, 255, (16, 16, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.ACHROMAT, severity=1.0)
        assert result.shape == im.shape
        assert result.dtype == np.uint8

    def test_achromat_all_channels_equal_at_full_severity(self):
        """At severity=1 every output pixel must be achromatic (R==G==B)."""
        sim = simulate.Simulator_Achromat()
        rng = np.random.default_rng(7)
        im = rng.integers(0, 256, (12, 12, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.ACHROMAT, severity=1.0)
        assert np.all(result[..., 0] == result[..., 1]), "R != G for achromat"
        assert np.all(result[..., 0] == result[..., 2]), "R != B for achromat"

    # ---- Simulator_BCM ----

    def test_bcm_black_maps_to_black(self):
        sim = simulate.Simulator_BCM()
        im = np.zeros((8, 8, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.BCM, severity=1.0)
        np.testing.assert_array_equal(result, 0)

    def test_bcm_white_maps_to_white(self):
        sim = simulate.Simulator_BCM()
        im = np.full((8, 8, 3), 255, dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.BCM, severity=1.0)
        np.testing.assert_allclose(result.astype(float), 255.0, atol=1)

    def test_bcm_pure_blue_retains_saturation(self):
        """BCM preserves S-cone; pure blue must keep a dominant B channel."""
        sim = simulate.Simulator_BCM()
        blue = np.array([[[0, 0, 255]]], dtype=np.uint8)
        result = sim.simulate_cvd(blue, Deficiency.BCM, severity=1.0)
        assert result[0, 0, 2] > result[0, 0, 0], "B should exceed R for pure-blue BCM"
        assert result[0, 0, 2] > result[0, 0, 1], "B should exceed G for pure-blue BCM"

    def test_bcm_severity_zero_identity(self):
        sim = simulate.Simulator_BCM()
        rng = np.random.default_rng(99)
        im = rng.integers(10, 245, (8, 8, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.BCM, severity=0.0)
        np.testing.assert_allclose(result.astype(float), im.astype(float), atol=1)

    def test_bcm_output_in_range(self):
        sim = simulate.Simulator_BCM()
        rng = np.random.default_rng(13)
        im = rng.integers(0, 256, (16, 16, 3), dtype=np.uint8)
        result = sim.simulate_cvd(im, Deficiency.BCM, severity=1.0)
        assert result.dtype == np.uint8
        assert result.min() >= 0
        assert result.max() <= 255

    # ---- AutoSelect routing ----

    def test_auto_select_routes_achromat(self):
        auto   = simulate.Simulator_AutoSelect()
        manual = simulate.Simulator_Achromat()
        from daltonlens import generate
        im = generate.rgb_span(27, 27)
        out_auto   = auto.simulate_cvd(im, Deficiency.ACHROMAT, severity=1.0)
        out_manual = manual.simulate_cvd(im, Deficiency.ACHROMAT, severity=1.0)
        np.testing.assert_array_equal(out_auto, out_manual)

    def test_auto_select_routes_bcm(self):
        auto   = simulate.Simulator_AutoSelect()
        manual = simulate.Simulator_BCM()
        from daltonlens import generate
        im = generate.rgb_span(27, 27)
        out_auto   = auto.simulate_cvd(im, Deficiency.BCM, severity=1.0)
        out_manual = manual.simulate_cvd(im, Deficiency.BCM, severity=1.0)
        np.testing.assert_array_equal(out_auto, out_manual)


# ---------------------------------------------------------------------------
# simulate.py utility functions coverage
# ---------------------------------------------------------------------------

class TestUtilityFunctions:
    def test_name_of_deficiency_all_values(self):
        assert simulate.name_of_deficiency(Deficiency.PROTAN)   == "protan"
        assert simulate.name_of_deficiency(Deficiency.DEUTAN)   == "deutan"
        assert simulate.name_of_deficiency(Deficiency.TRITAN)   == "tritan"
        assert simulate.name_of_deficiency(Deficiency.ACHROMAT) == "achromat"
        assert simulate.name_of_deficiency(Deficiency.BCM)      == "bcm"

    def test_plane_projection_matrix_returns_none_for_unknown(self):
        # ACHROMAT and BCM are not dichromacy types; function returns None
        result = simulate.plane_projection_matrix(np.array([1.0, 0.0, 0.0]), Deficiency.ACHROMAT)
        assert result is None

    def test_lms_confusion_axis_returns_none_for_unknown(self):
        result = simulate.lms_confusion_axis(Deficiency.ACHROMAT)
        assert result is None


class TestMachado2009Guard:
    def test_machado_raises_for_achromat(self):
        sim = simulate.Simulator_Machado2009()
        im  = np.full((4, 4, 3), 128, dtype=np.uint8)
        with pytest.raises(ValueError, match="Simulator_Machado2009 does not support"):
            sim.simulate_cvd(im, Deficiency.ACHROMAT, severity=1.0)

    def test_machado_raises_for_bcm(self):
        sim = simulate.Simulator_Machado2009()
        im  = np.full((4, 4, 3), 128, dtype=np.uint8)
        with pytest.raises(ValueError, match="Simulator_Machado2009 does not support"):
            sim.simulate_cvd(im, Deficiency.BCM, severity=1.0)


class TestBrettelNonJuddVosBranch:
    """Cover the usesJuddVosXYZ=False code path in Simulator_Brettel1997.

    SmithPokorny75 with ignoreJuddVosCorrection=True sets usesJuddVosXYZ=False,
    exercising the 'historical comparison' xyz constant branch (lines 297-300).
    """

    def test_brettel_no_judd_vos_protan(self):
        model = convert.LMSModel_sRGB_SmithPokorny75(ignoreJuddVosCorrection=True)
        sim   = simulate.Simulator_Brettel1997(model)
        im    = np.full((4, 4, 3), 128, dtype=np.uint8)
        out   = sim.simulate_cvd(im, Deficiency.PROTAN, severity=1.0)
        assert out.shape == (4, 4, 3)
        assert out.dtype == np.uint8

    def test_brettel_no_judd_vos_tritan(self):
        model = convert.LMSModel_sRGB_SmithPokorny75(ignoreJuddVosCorrection=True)
        sim   = simulate.Simulator_Brettel1997(model)
        im    = np.full((4, 4, 3), 128, dtype=np.uint8)
        out   = sim.simulate_cvd(im, Deficiency.TRITAN, severity=1.0)
        assert out.shape == (4, 4, 3)

    def test_brettel_non_white_neutral(self):
        """Cover use_white_as_neutral=False (equal-energy neutral) branch."""
        sim = simulate.Simulator_Brettel1997(
            convert.LMSModel_sRGB_SmithPokorny75(), use_white_as_neutral=False
        )
        im  = np.full((4, 4, 3), 128, dtype=np.uint8)
        out = sim.simulate_cvd(im, Deficiency.DEUTAN, severity=1.0)
        assert out.shape == (4, 4, 3)


class TestDumpPrecomputedValues:
    """Cover dumpPrecomputedValues=True path (developer C-constant export)."""

    def test_brettel_dump_does_not_raise(self, capsys):
        sim = simulate.Simulator_Brettel1997(convert.LMSModel_sRGB_SmithPokorny75())
        sim.dumpPrecomputedValues = True
        im  = np.full((2, 2, 3), 200, dtype=np.uint8)
        out = sim.simulate_cvd(im, Deficiency.PROTAN, severity=1.0)
        assert out.shape == (2, 2, 3)
        captured = capsys.readouterr()
        # Should have printed the C struct definitions
        assert "DLBrettel1997Params" in captured.out
