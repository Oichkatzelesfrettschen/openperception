#!/usr/bin/env python3
"""
Validate an experimental palette pack.

Reports:
- authored contrast for strong brand tokens against white
- authored Oklab separation between primary/accent/tertiary
- simulated separation for the experimental default theme under
  protan, deutan, and tritan full-severity views
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools"
DALTONLENS_DIR = ROOT / "algorithms" / "DaltonLens-Python"
DEFAULT_TOKENS_JSON = ROOT / "tokens" / "experimental-mauve-burgundy.json"

sys.path.insert(0, str(TOOLS_DIR))
sys.path.insert(0, str(DALTONLENS_DIR))

import numpy as np  # noqa: E402
from contrast_check import contrast_ratio  # noqa: E402
from okcolor import hex_to_srgb, srgb_to_oklab  # noqa: E402

from daltonlens import simulate  # noqa: E402


def oklab_distance(hex1: str, hex2: str) -> float:
    r1, g1, b1 = hex_to_srgb(hex1)
    L1, a1, b1_ = srgb_to_oklab(r1, g1, b1)
    r2, g2, b2 = hex_to_srgb(hex2)
    L2, a2, b2_ = srgb_to_oklab(r2, g2, b2)
    return math.sqrt((L1 - L2) ** 2 + (a1 - a2) ** 2 + (b1_ - b2_) ** 2)


def hex_to_rgb8(hex_str: str) -> np.ndarray:
    value = hex_str.lstrip("#")
    return np.array([int(value[i : i + 2], 16) for i in (0, 2, 4)], dtype=np.uint8)


def simulate_hex(hex_str: str, deficiency: simulate.Deficiency) -> str:
    sim = simulate.Simulator_AutoSelect()
    image = np.array([[hex_to_rgb8(hex_str)]], dtype=np.uint8)
    out = sim.simulate_cvd(image, deficiency, 1.0)
    r, g, b = (int(x) for x in out[0, 0])
    return f"#{r:02X}{g:02X}{b:02X}"


def report_variant(name: str, data: dict) -> None:
    brand = data["brand"]
    p = brand["primaryStrong"]
    a = brand["accentStrong"]
    t = brand["tertiaryStrong"]
    print(f"\nVariant: {name}")
    print(f"- white on primaryStrong   {contrast_ratio('#FFFFFF', p):.2f}")
    print(f"- white on accentStrong    {contrast_ratio('#FFFFFF', a):.2f}")
    print(f"- white on tertiaryStrong  {contrast_ratio('#FFFFFF', t):.2f}")
    print(f"- dist primary/accent      {oklab_distance(p, a):.3f}")
    print(f"- dist primary/tertiary    {oklab_distance(p, t):.3f}")
    print(f"- dist accent/tertiary     {oklab_distance(a, t):.3f}")


def report_simulated_default(tokens: dict) -> None:
    brand = tokens["default"]["brand"]
    p = brand["primaryStrong"]
    a = brand["accentStrong"]
    print("\nSimulated default pair (primaryStrong vs accentStrong)")
    for deficiency in (
        simulate.Deficiency.PROTAN,
        simulate.Deficiency.DEUTAN,
        simulate.Deficiency.TRITAN,
    ):
        sp = simulate_hex(p, deficiency)
        sa = simulate_hex(a, deficiency)
        print(
            f"- {deficiency.name.lower():7s} {sp} vs {sa} -> {oklab_distance(sp, sa):.3f}"
        )


def main() -> None:
    tokens_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TOKENS_JSON
    if not tokens_path.is_absolute():
        tokens_path = ROOT / tokens_path
    tokens = json.loads(tokens_path.read_text())
    print(f"Experimental palette report for {tokens_path}")
    for variant, data in tokens.items():
        report_variant(variant, data)
    if "default" in tokens and "accentStrong" in tokens["default"].get("brand", {}):
        report_simulated_default(tokens)


if __name__ == "__main__":
    main()
