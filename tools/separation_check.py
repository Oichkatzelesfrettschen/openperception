#!/usr/bin/env python3
"""
Check perceptual separation (Oklab distance) between primary and accent per variant.
"""
from __future__ import annotations
from pathlib import Path
import json
import math
from okcolor import hex_to_oklch, srgb_to_oklab, hex_to_srgb

ROOT = Path(__file__).resolve().parents[1]
TOKENS_JSON = ROOT / 'tokens' / 'color-tokens.json'


def oklab_distance(hex1: str, hex2: str) -> float:
    r1, g1, b1 = hex_to_srgb(hex1)
    L1, a1, b1_ = srgb_to_oklab(r1, g1, b1)
    r2, g2, b2 = hex_to_srgb(hex2)
    L2, a2, b2_ = srgb_to_oklab(r2, g2, b2)
    return math.sqrt((L1-L2)**2 + (a1-a2)**2 + (b1_-b2_)**2)


def main():
    tokens = json.loads(TOKENS_JSON.read_text())
    print("Oklab distance (higher is more distinct):")
    for variant, data in tokens.items():
        b = data.get('brand', {})
        p = b.get('primaryStrong') or b.get('primary')
        a = b.get('accentStrong') or b.get('accent')
        if p and a:
            d = oklab_distance(p, a)
            print(f"- {variant:7s}: {d:.3f} (primaryStrong vs accentStrong)")


if __name__ == '__main__':
    main()

