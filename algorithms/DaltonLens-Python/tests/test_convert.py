"""Tests for daltonlens/convert.py - color space conversions."""

import numpy as np

from daltonlens import convert


class TestAsFloat32AndUint8:
    def test_as_float32_zeros(self):
        im = np.zeros((4, 4, 3), dtype=np.uint8)
        result = convert.as_float32(im)
        assert result.dtype == np.float32
        assert result.max() == 0.0

    def test_as_float32_full(self):
        im = np.full((2, 2, 3), 255, dtype=np.uint8)
        result = convert.as_float32(im)
        np.testing.assert_allclose(result, 1.0, atol=1e-6)

    def test_as_uint8_zeros(self):
        im = np.zeros((4, 4, 3), dtype=np.float32)
        result = convert.as_uint8(im)
        assert result.dtype == np.uint8
        assert result.max() == 0

    def test_as_uint8_ones(self):
        im = np.ones((2, 2, 3), dtype=np.float32)
        result = convert.as_uint8(im)
        assert result.max() == 255

    def test_round_trip(self):
        original = np.array([[[0, 127, 255]]], dtype=np.uint8)
        result = convert.as_uint8(convert.as_float32(original))
        # Allow off-by-one due to float precision
        np.testing.assert_array_less(
            np.abs(result.astype(int) - original.astype(int)), 2
        )


class TestGammaConversions:
    def test_srgb_linearrgb_round_trip(self):
        """Converting sRGB to linear and back should recover the original."""
        im = np.linspace(0, 1, 100, dtype=np.float32).reshape(1, -1, 1)
        im = np.repeat(im, 3, axis=2)
        linear = convert.linearRGB_from_sRGB(im)
        recovered = convert.sRGB_from_linearRGB(linear)
        np.testing.assert_allclose(recovered, im, atol=1e-6)

    def test_linearrgb_from_srgb_black(self):
        im = np.zeros((1, 1, 3), dtype=np.float32)
        result = convert.linearRGB_from_sRGB(im)
        np.testing.assert_allclose(result, 0.0, atol=1e-7)

    def test_linearrgb_from_srgb_white(self):
        im = np.ones((1, 1, 3), dtype=np.float32)
        result = convert.linearRGB_from_sRGB(im)
        np.testing.assert_allclose(result, 1.0, atol=1e-6)

    def test_gamma22_round_trip(self):
        im = np.linspace(0.01, 1, 50, dtype=np.float32).reshape(1, -1, 1)
        im = np.repeat(im, 3, axis=2)
        linear = convert.linearRGB_from_gamma22(im)
        recovered = convert.gamma22_from_linearRGB(linear)
        np.testing.assert_allclose(recovered, im, atol=1e-6)

    def test_srgb_from_linearrgb_clamps_negative(self):
        """Negative linear values should not cause NaN in gamma output."""
        im = np.array([[[-0.1, 0.5, 1.1]]], dtype=np.float32)
        result = convert.sRGB_from_linearRGB(im)
        assert np.all(np.isfinite(result))


class TestApplyColorMatrix:
    def test_identity_matrix(self):
        im = np.random.rand(4, 4, 3).astype(np.float32)
        identity = np.eye(3, dtype=np.float32)
        result = convert.apply_color_matrix(im, identity)
        np.testing.assert_allclose(result, im, atol=1e-6)

    def test_zero_matrix(self):
        im = np.ones((2, 2, 3), dtype=np.float32)
        zero = np.zeros((3, 3), dtype=np.float32)
        result = convert.apply_color_matrix(im, zero)
        np.testing.assert_allclose(result, 0.0, atol=1e-7)

    def test_channel_swap(self):
        """Swap R and G channels with a permutation matrix."""
        im = np.array([[[1.0, 0.5, 0.25]]], dtype=np.float32)
        swap = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], dtype=np.float32)
        result = convert.apply_color_matrix(im, swap)
        np.testing.assert_allclose(result[0, 0], [0.5, 1.0, 0.25], atol=1e-6)


class TestLMSModels:
    """Verify LMS model construction and invertibility."""

    def _check_model_invertible(self, model):
        """LMS_from_linearRGB @ linearRGB_from_LMS should be near identity."""
        product = model.LMS_from_linearRGB @ model.linearRGB_from_LMS
        np.testing.assert_allclose(product, np.eye(3), atol=1e-6)

    def test_smith_pokorny_invertible(self):
        model = convert.LMSModel_sRGB_SmithPokorny75()
        self._check_model_invertible(model)

    def test_vischeck_invertible(self):
        model = convert.LMSModel_Vischeck_GIMP()
        self._check_model_invertible(model)

    def test_linearize_then_lms_roundtrip(self):
        """sRGB -> linear -> LMS -> linear -> sRGB should round-trip."""
        model = convert.LMSModel_sRGB_SmithPokorny75()
        im = np.random.rand(5, 5, 3).astype(np.float64)
        linear = convert.linearRGB_from_sRGB(im)
        lms = convert.apply_color_matrix(linear, model.LMS_from_linearRGB)
        back = convert.apply_color_matrix(lms, model.linearRGB_from_LMS)
        np.testing.assert_allclose(back, linear, atol=1e-10)
