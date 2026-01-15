#!/usr/bin/env python3
"""
Minimal sRGB <-> Oklab utilities to compute OKLCH from hex colors.
Implements Björn Ottosson's Oklab algorithm.
"""

from __future__ import annotations
import math
from typing import Tuple


def hex_to_srgb(hex_str: str) -> Tuple[float, float, float]:
    s = hex_str.strip().lstrip('#')
    if len(s) == 3:
        s = ''.join([c*2 for c in s])
    if len(s) != 6:
        raise ValueError(f"Invalid hex: {hex_str}")
    r = int(s[0:2], 16) / 255.0
    g = int(s[2:4], 16) / 255.0
    b = int(s[4:6], 16) / 255.0
    return r, g, b


def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def srgb_to_oklab(r: float, g: float, b: float) -> Tuple[float, float, float]:
    # Linearize
    rl, gl, bl = srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)

    # to LMS using matrix M1
    l = 0.4122214708 * rl + 0.5363325363 * gl + 0.0514459929 * bl
    m = 0.2119034982 * rl + 0.6806995451 * gl + 0.1073969566 * bl
    s = 0.0883024619 * rl + 0.2817188376 * gl + 0.6299787005 * bl

    l_ = math.copysign(abs(l) ** (1/3), l)
    m_ = math.copysign(abs(m) ** (1/3), m)
    s_ = math.copysign(abs(s) ** (1/3), s)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, a, b


def oklab_to_oklch(L: float, a: float, b: float) -> Tuple[float, float, float]:
    C = math.hypot(a, b)
    h = math.degrees(math.atan2(b, a)) % 360.0
    return L, C, h


def hex_to_oklch(hex_str: str) -> Tuple[float, float, float]:
    r, g, b = hex_to_srgb(hex_str)
    L, a, b2 = srgb_to_oklab(r, g, b)
    Lc, C, h = oklab_to_oklch(L, a, b2)
    return (Lc, C, h)


def format_oklch_tuple(t: Tuple[float, float, float], precision: int = 5) -> Tuple[float, float, float]:
    L, C, h = t
    return (round(L, precision), round(C, precision), round(h, 2))


if __name__ == '__main__':
    import sys, json
    for hex_code in sys.argv[1:]:
        print(hex_code, format_oklch_tuple(hex_to_oklch(hex_code)))

