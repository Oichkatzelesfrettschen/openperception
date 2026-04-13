"""Tests for daltonlens/daltonize.py - daltonization algorithms."""

import numpy as np
import pytest

from daltonlens import daltonize
from daltonlens.simulate import Deficiency


def _solid_image(r, g, b, shape=(8, 8)):
    """Create a solid-color uint8 image."""
    im = np.zeros((*shape, 3), dtype=np.uint8)
    im[:, :, 0] = r
    im[:, :, 1] = g
    im[:, :, 2] = b
    return im


class TestDaltonizeFidaner:
    def test_output_shape_preserved(self):
        im = np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8)
        result = daltonize.daltonize_fidaner(im, Deficiency.PROTAN)
        assert result.shape == im.shape

    def test_output_dtype_uint8(self):
        im = _solid_image(200, 50, 50)
        result = daltonize.daltonize_fidaner(im, Deficiency.PROTAN)
        assert result.dtype == np.uint8

    def test_output_values_in_range(self):
        im = np.random.randint(0, 255, (12, 12, 3), dtype=np.uint8)
        for deficiency in (Deficiency.PROTAN, Deficiency.DEUTAN, Deficiency.TRITAN):
            result = daltonize.daltonize_fidaner(im, deficiency)
            assert result.min() >= 0 and result.max() <= 255

    def test_black_image_unchanged(self):
        """A black image should remain black after daltonization."""
        im = _solid_image(0, 0, 0)
        result = daltonize.daltonize_fidaner(im, Deficiency.DEUTAN)
        np.testing.assert_array_equal(result, im)

    def test_tritan_deficiency(self):
        im = np.random.randint(0, 255, (8, 8, 3), dtype=np.uint8)
        result = daltonize.daltonize_fidaner(im, Deficiency.TRITAN)
        assert result.shape == im.shape
        assert result.dtype == np.uint8


class TestDaltonizeSimple:
    def test_output_shape_preserved(self):
        im = np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8)
        result = daltonize.daltonize_simple(im, Deficiency.PROTAN)
        assert result.shape == im.shape

    def test_output_dtype_uint8(self):
        im = _solid_image(100, 200, 50)
        result = daltonize.daltonize_simple(im, Deficiency.DEUTAN)
        assert result.dtype == np.uint8

    def test_output_in_range(self):
        im = np.random.randint(0, 255, (8, 8, 3), dtype=np.uint8)
        for deficiency in (Deficiency.PROTAN, Deficiency.DEUTAN, Deficiency.TRITAN):
            result = daltonize.daltonize_simple(im, deficiency)
            assert result.min() >= 0 and result.max() <= 255

    def test_strength_zero_preserves_image(self):
        """strength=0 means no enhancement; result should match input."""
        im = np.random.randint(0, 255, (8, 8, 3), dtype=np.uint8)
        result = daltonize.daltonize_simple(im, Deficiency.PROTAN, strength=0.0)
        np.testing.assert_array_equal(result, im)


class TestDaltonizeDispatch:
    def test_fidaner_dispatch(self):
        im = np.random.randint(0, 255, (6, 6, 3), dtype=np.uint8)
        result = daltonize.daltonize(im, Deficiency.PROTAN, method="fidaner")
        assert result.shape == im.shape

    def test_simple_dispatch(self):
        im = np.random.randint(0, 255, (6, 6, 3), dtype=np.uint8)
        result = daltonize.daltonize(im, Deficiency.DEUTAN, method="simple")
        assert result.shape == im.shape

    def test_invalid_method_raises(self):
        im = np.random.randint(0, 255, (4, 4, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="Unknown daltonization method"):
            daltonize.daltonize(im, Deficiency.PROTAN, method="nonexistent")


class TestDaltonizeQuality:
    """Verify daltonization increases color distinguishability for CVD viewers.

    WHY: Shape/dtype tests don't verify correctness. These tests confirm that
    daltonization actually moves confused colors apart in perceptual space.

    Methodology:
    - Create two solid-color images that a dichromat would confuse (appear identical).
    - Simulate what the dichromat sees -- the simulated versions should be very similar.
    - Daltonize both images, then re-simulate.
    - After daltonization the re-simulated versions should be MORE different.
    """

    def _color_distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Mean Euclidean distance in sRGB space between two solid images."""
        return float(
            np.mean(np.sqrt(np.sum((a.astype(float) - b.astype(float)) ** 2, axis=2)))
        )

    def test_fidaner_increases_protan_separation(self):
        """A saturated red and saturated green should be more separable after fidaner daltonization."""
        from daltonlens import convert
        from daltonlens import simulate as sim_module

        # Red and green: strongly confused by protanopes
        red = _solid_image(220, 30, 30)
        green = _solid_image(30, 200, 30)

        simulator = sim_module.Simulator_Brettel1997(
            convert.LMSModel_sRGB_SmithPokorny75()
        )

        # Distance as seen by a simulated protanope (before daltonization)
        sim_red_before = simulator.simulate_cvd(red, Deficiency.PROTAN, severity=1.0)
        sim_green_before = simulator.simulate_cvd(
            green, Deficiency.PROTAN, severity=1.0
        )
        dist_before = self._color_distance(sim_red_before, sim_green_before)

        # Daltonize both images
        dal_red = daltonize.daltonize_fidaner(red, Deficiency.PROTAN)
        dal_green = daltonize.daltonize_fidaner(green, Deficiency.PROTAN)

        # Distance as seen by a simulated protanope (after daltonization)
        sim_red_after = simulator.simulate_cvd(dal_red, Deficiency.PROTAN, severity=1.0)
        sim_green_after = simulator.simulate_cvd(
            dal_green, Deficiency.PROTAN, severity=1.0
        )
        dist_after = self._color_distance(sim_red_after, sim_green_after)

        # Daltonization should increase the perceived distance between the colors
        assert dist_after > dist_before, (
            f"Fidaner daltonization did not increase protan separation: "
            f"before={dist_before:.2f}, after={dist_after:.2f}"
        )

    def test_simple_increases_deutan_separation(self):
        """Daltonize_simple should increase deutan separation for red/green pair."""
        from daltonlens import convert
        from daltonlens import simulate as sim_module

        red = _solid_image(210, 40, 40)
        green = _solid_image(40, 190, 40)

        simulator = sim_module.Simulator_Brettel1997(
            convert.LMSModel_sRGB_SmithPokorny75()
        )

        sim_red_before = simulator.simulate_cvd(red, Deficiency.DEUTAN, severity=1.0)
        sim_green_before = simulator.simulate_cvd(
            green, Deficiency.DEUTAN, severity=1.0
        )
        dist_before = self._color_distance(sim_red_before, sim_green_before)

        dal_red = daltonize.daltonize_simple(red, Deficiency.DEUTAN)
        dal_green = daltonize.daltonize_simple(green, Deficiency.DEUTAN)

        sim_red_after = simulator.simulate_cvd(dal_red, Deficiency.DEUTAN, severity=1.0)
        sim_green_after = simulator.simulate_cvd(
            dal_green, Deficiency.DEUTAN, severity=1.0
        )
        dist_after = self._color_distance(sim_red_after, sim_green_after)

        assert dist_after > dist_before, (
            f"Simple daltonization did not increase deutan separation: "
            f"before={dist_before:.2f}, after={dist_after:.2f}"
        )
