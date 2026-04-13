#!/usr/bin/env python3
"""Run once to generate ground truth images for Simulator_Achromat and Simulator_BCM.

Usage (from repo root):
    cd algorithms/DaltonLens-Python
    python tests/gen_achromat_groundtruth.py

Commit the resulting PNG files in tests/images/.
"""

from pathlib import Path

from PIL import Image

from daltonlens import generate, simulate


IMAGES = Path(__file__).parent / "images"

CASES = [
    (simulate.Simulator_Achromat, "achromat", simulate.Deficiency.ACHROMAT),
    (simulate.Simulator_BCM, "bcm", simulate.Deficiency.BCM),
]


def main():
    IMAGES.mkdir(exist_ok=True)
    im = generate.rgb_span(27 * 8, 27 * 8)
    for SimClass, name, deficiency in CASES:
        sim = SimClass()
        for severity in [1.0, 0.55]:
            result = sim.simulate_cvd(im, deficiency, severity=severity)
            fname = f"{name}_{severity}.png"
            Image.fromarray(result).save(IMAGES / fname)
            print(f"Saved {IMAGES / fname}")


if __name__ == "__main__":
    main()
