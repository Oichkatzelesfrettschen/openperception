#!/usr/bin/env python3
"""
Contrast checker for brand tokens across variants.
Reports WCAG contrast for common text/background pairs.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKENS_JSON = ROOT / 'tokens' / 'color-tokens.json'


def hex_to_rgb(hex_str: str):
    s = hex_str.strip().lstrip('#')
    if len(s) == 3:
        s = ''.join(c*2 for c in s)
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    return (r, g, b)


def srgb_channel_to_lum(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: tuple) -> float:
    r, g, b = rgb
    R = srgb_channel_to_lum(r)
    G = srgb_channel_to_lum(g)
    B = srgb_channel_to_lum(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    L1 = relative_luminance(hex_to_rgb(fg_hex))
    L2 = relative_luminance(hex_to_rgb(bg_hex))
    L_light = max(L1, L2)
    L_dark = min(L1, L2)
    return (L_light + 0.05) / (L_dark + 0.05)


def check_variant(name: str, data: dict):
    out = []
    b = data.get('brand', {})
    gray = data.get('gray', {})

    pairs = [
        (b.get('text'), b.get('surface'), 'text on surface'),
        (b.get('primaryStrong'), b.get('surface'), 'primaryStrong on surface'),
        (b.get('accentStrong'), b.get('surface'), 'accentStrong on surface'),
        ('#FFFFFF', b.get('primaryStrong'), 'white on primaryStrong'),
        ('#FFFFFF', b.get('accentStrong'), 'white on accentStrong'),
        (gray.get('700'), b.get('surface'), 'gray700 on surface'),
        (gray.get('500'), b.get('surface'), 'gray500 on surface'),
        (gray.get('400'), b.get('surface'), 'gray400 on surface'),
    ]
    for fg, bg, label in pairs:
        if not fg or not bg:
            continue
        ratio = contrast_ratio(fg, bg)
        out.append((label, fg, bg, ratio))
    return out


def main():
    tokens = json.loads(TOKENS_JSON.read_text())
    for variant, data in tokens.items():
        print(f"\nVariant: {variant}")
        results = check_variant(variant, data)
        for label, fg, bg, ratio in results:
            status = 'AA 4.5:1' if ratio >= 4.5 else ('AA Large 3:1' if ratio >= 3.0 else 'FAIL')
            print(f"- {label:28s} {fg} on {bg} -> {ratio:.2f} ({status})")


if __name__ == '__main__':
    main()

