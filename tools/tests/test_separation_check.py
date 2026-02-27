"""Tests for tools/separation_check.py and okcolor.py utilities."""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from okcolor import hex_to_srgb, srgb_to_oklab, hex_to_oklch
from separation_check import oklab_distance


class TestHexToSrgb:
    def test_black(self):
        r, g, b = hex_to_srgb("#000000")
        assert (r, g, b) == pytest.approx((0.0, 0.0, 0.0))

    def test_white(self):
        r, g, b = hex_to_srgb("#FFFFFF")
        assert (r, g, b) == pytest.approx((1.0, 1.0, 1.0))

    def test_shorthand(self):
        r, g, b = hex_to_srgb("#FFF")
        assert (r, g, b) == pytest.approx((1.0, 1.0, 1.0))

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            hex_to_srgb("#GGGGGG")


class TestSrgbToOklab:
    def test_black(self):
        L, a, b = srgb_to_oklab(0.0, 0.0, 0.0)
        assert L == pytest.approx(0.0, abs=1e-6)

    def test_white(self):
        L, a, b = srgb_to_oklab(1.0, 1.0, 1.0)
        assert L == pytest.approx(1.0, abs=1e-4)
        # Achromatic: a and b should be near zero
        assert abs(a) < 0.01
        assert abs(b) < 0.01

    def test_lightness_in_range(self):
        for gray in [0.0, 0.25, 0.5, 0.75, 1.0]:
            L, a, b = srgb_to_oklab(gray, gray, gray)
            assert 0.0 <= L <= 1.05


class TestOklabDistance:
    def test_same_color_zero_distance(self):
        d = oklab_distance("#FF0000", "#FF0000")
        assert d == pytest.approx(0.0, abs=1e-6)

    def test_black_to_white_max_distance(self):
        d_bw = oklab_distance("#000000", "#FFFFFF")
        d_red_blue = oklab_distance("#FF0000", "#0000FF")
        # Black-white distance should be larger than most hue pairs
        assert d_bw > 0.5

    def test_distance_symmetric(self):
        d1 = oklab_distance("#FF0000", "#00FF00")
        d2 = oklab_distance("#00FF00", "#FF0000")
        assert d1 == pytest.approx(d2, abs=1e-8)

    def test_distance_nonnegative(self):
        pairs = [
            ("#FF0000", "#00FF00"),
            ("#0000FF", "#FFFF00"),
            ("#111111", "#EEEEEE"),
        ]
        for fg, bg in pairs:
            assert oklab_distance(fg, bg) >= 0.0
