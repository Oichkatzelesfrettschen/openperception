#!/usr/bin/env python3
"""
Benchmark suite for OpenPerception CVD simulation algorithms.

WHY: Performance claims need reproducible, versioned baselines. This script
measures wall-clock throughput for all Python simulators across image sizes and
records results with timestamps and dependency versions.

WHAT: Tests Python simulators on synthetic images (128x128, 512x512, 1024x1024).
      Outputs a Markdown table suitable for pasting into docs or commit messages.

HOW:
    # Install dependencies first
    pip install -e algorithms/DaltonLens-Python

    # Run from repository root
    python benchmarks/run_benchmarks.py

    # Save results
    python benchmarks/run_benchmarks.py --output benchmarks/results/$(date +%Y%m%d).md
"""

import argparse
import datetime
import importlib.metadata
import os
import platform
import sys
import time

import numpy as np


# Ensure the daltonlens package from the submodule is importable.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "algorithms", "DaltonLens-Python"))

from daltonlens import convert, simulate


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

IMAGE_SIZES = [
    (128, 128),
    (512, 512),
    (1024, 1024),
]

SIMULATORS = [
    ("Brettel1997",  lambda: simulate.Simulator_Brettel1997(convert.LMSModel_sRGB_SmithPokorny75())),
    ("Vienot1999",   lambda: simulate.Simulator_Vienot1999(convert.LMSModel_sRGB_SmithPokorny75())),
    ("Machado2009",  lambda: simulate.Simulator_Machado2009()),
    ("AutoSelect",   lambda: simulate.Simulator_AutoSelect()),
]

DEFICIENCIES = [
    simulate.Deficiency.PROTAN,
    simulate.Deficiency.DEUTAN,
    simulate.Deficiency.TRITAN,
]

SEVERITIES = [1.0]   # Use full dichromacy for reproducible timing (no severity interpolation branch)
REPEATS = 5          # Number of timed repetitions (best-of-N reported)


# ---------------------------------------------------------------------------
# Benchmark runner
# ---------------------------------------------------------------------------

def bench_one(sim, image, deficiency, severity, repeats):
    """Return the minimum wall-clock time in milliseconds over `repeats` runs."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        sim.simulate_cvd(image, deficiency, severity)
        times.append((time.perf_counter() - t0) * 1000.0)
    return min(times)


def make_image(height, width):
    """Generate a reproducible random sRGB uint8 image."""
    rng = np.random.default_rng(seed=42)
    return rng.integers(0, 256, size=(height, width, 3), dtype=np.uint8)


def collect_env():
    """Return a dict of environment metadata."""
    info = {
        "date": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu": platform.processor() or "unknown",
        "numpy": np.__version__,
    }
    try:
        info["daltonlens"] = importlib.metadata.version("daltonlens")
    except importlib.metadata.PackageNotFoundError:
        info["daltonlens"] = "unknown (dev install)"
    return info


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def results_to_markdown(rows, env):
    lines = []
    lines.append("# CVD Simulation Benchmark Results")
    lines.append("")
    lines.append("## Environment")
    lines.append("")
    for k, v in env.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append(f"## Results (best of {REPEATS} repeats, ms)")
    lines.append("")
    # Header
    deficiency_labels = [d.name.capitalize() for d in DEFICIENCIES]
    header = "| Simulator | Size | " + " | ".join(deficiency_labels) + " |"
    sep    = "| --- | --- | " + " | ".join(["---"] * len(DEFICIENCIES)) + " |"
    lines.append(header)
    lines.append(sep)
    for (sim_name, size_str, timings) in rows:
        timing_strs = [f"{t:.2f}" for t in timings]
        lines.append("| {} | {} | {} |".format(sim_name, size_str, " | ".join(timing_strs)))
    lines.append("")
    lines.append("*Timing excludes image allocation. Smaller is faster.*")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Benchmark CVD simulation algorithms")
    parser.add_argument("--output", help="Write Markdown results to this file")
    parser.add_argument("--repeats", type=int, default=REPEATS, help="Repetitions per measurement")
    args = parser.parse_args()

    env = collect_env()
    print(f"OpenPerception CVD Benchmark  --  {env['date']}")
    print(f"Python {env['python']} | NumPy {env['numpy']} | daltonlens {env['daltonlens']}")
    print(f"Platform: {env['platform']}\n")

    rows = []
    for (h, w) in IMAGE_SIZES:
        image = make_image(h, w)
        size_str = f"{w}x{h}"
        for (sim_name, sim_factory) in SIMULATORS:
            sim = sim_factory()
            timings = []
            for deficiency in DEFICIENCIES:
                try:
                    t = bench_one(sim, image, deficiency, SEVERITIES[0], args.repeats)
                    timings.append(t)
                except Exception as exc:
                    print(f"  SKIP {sim_name}/{deficiency.name}: {exc}", file=sys.stderr)
                    timings.append(float("nan"))
            timing_str = " | ".join(f"{t:6.2f}" for t in timings)
            print(f"  {sim_name:15s}  {size_str:8s}  [{timing_str}] ms (P D T)")
            rows.append((sim_name, size_str, timings))

    md = results_to_markdown(rows, env)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"\nResults written to: {args.output}")
    else:
        print("\n" + md)


if __name__ == "__main__":
    main()
