"""Tests for tools/contrast_check.py - WCAG contrast utilities."""
import sys
from pathlib import Path

# Allow importing contrast_check from the tools directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from contrast_check import hex_to_rgb, srgb_channel_to_lum, relative_luminance, contrast_ratio


class TestHexToRgb:
    def test_black(self):
        assert hex_to_rgb("#000000") == (0, 0, 0)

    def test_white(self):
        assert hex_to_rgb("#FFFFFF") == (255, 255, 255)

    def test_red(self):
        assert hex_to_rgb("#FF0000") == (255, 0, 0)

    def test_shorthand(self):
        assert hex_to_rgb("#FFF") == (255, 255, 255)

    def test_without_hash(self):
        assert hex_to_rgb("000000") == (0, 0, 0)


class TestSrgbChannelToLum:
    def test_zero(self):
        assert srgb_channel_to_lum(0) == pytest.approx(0.0, abs=1e-7)

    def test_255(self):
        assert srgb_channel_to_lum(255) == pytest.approx(1.0, abs=1e-4)

    def test_midpoint_uses_linear_segment(self):
        # sRGB value 10 (about 0.039) uses linear segment c/12.92
        result = srgb_channel_to_lum(10)
        expected = (10 / 255.0) / 12.92
        assert result == pytest.approx(expected, abs=1e-7)


class TestRelativeLuminance:
    def test_black(self):
        assert relative_luminance((0, 0, 0)) == pytest.approx(0.0, abs=1e-7)

    def test_white(self):
        assert relative_luminance((255, 255, 255)) == pytest.approx(1.0, abs=1e-4)

    def test_luminance_in_range(self):
        for val in range(0, 256, 25):
            lum = relative_luminance((val, val, val))
            assert 0.0 <= lum <= 1.0


class TestContrastRatio:
    def test_black_on_white(self):
        ratio = contrast_ratio("#000000", "#FFFFFF")
        assert ratio == pytest.approx(21.0, abs=0.1)

    def test_white_on_black(self):
        ratio = contrast_ratio("#FFFFFF", "#000000")
        assert ratio == pytest.approx(21.0, abs=0.1)

    def test_same_color(self):
        ratio = contrast_ratio("#FF0000", "#FF0000")
        assert ratio == pytest.approx(1.0, abs=0.01)

    def test_wcag_aa_threshold(self):
        # A compliant pair should be >= 4.5
        ratio = contrast_ratio("#000000", "#FFFFFF")
        assert ratio >= 4.5

    def test_ratio_always_at_least_one(self):
        for hex_color in ("#FF0000", "#00FF00", "#0000FF", "#888888"):
            ratio = contrast_ratio(hex_color, hex_color)
            assert ratio >= 1.0
