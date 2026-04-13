#!/usr/bin/env python3
"""
DaltonLens CLI - Simulate and correct color vision deficiencies.

This tool provides two main functions:
- simulate: Show how an image appears to someone with CVD
- daltonize: Adjust colors to help CVD viewers distinguish them

Single-image mode (default):
    daltonlens input.png output.png [options]

Batch mode:
    daltonlens --batch "path/to/*.png" --output-dir out/ [options]
    daltonlens --batch "dir/**/*.jpg" --output-dir out/ [options]
"""

import sys
import glob as glob_module
import numpy as np
from pathlib import Path
from PIL import Image

from daltonlens import convert, simulate, daltonize as daltonize_module


def parse_command_line():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(
        description="Toolbox to simulate and correct color vision deficiencies.",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    # Single-image mode positional args (optional when --batch is used)
    parser.add_argument(
        "input_image",
        type=Path,
        nargs="?",
        default=None,
        help="Image to process (single-image mode).",
    )
    parser.add_argument(
        "output_image",
        type=Path,
        nargs="?",
        default=None,
        help="Output image path (single-image mode).",
    )

    # Batch mode
    parser.add_argument(
        "--batch",
        "-b",
        type=str,
        default=None,
        metavar="GLOB",
        help=(
            "Glob pattern for batch processing, e.g. 'images/*.png'. "
            "Requires --output-dir. Replaces single-image positional args."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for batch mode. Created if it does not exist.",
    )

    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="auto",
        choices=["auto", "vienot", "brettel", "machado", "vischeck", "coblisV1", "coblisV2"],
        help="CVD simulation model to use.",
    )

    parser.add_argument(
        "--filter",
        "-f",
        type=str,
        default="simulate",
        choices=["simulate", "daltonize"],
        help="Filter to apply: simulate (show CVD view) or daltonize (correct for CVD).",
    )

    parser.add_argument(
        "--deficiency",
        "-d",
        type=str,
        default="protan",
        choices=["protan", "deutan", "tritan", "achromat", "bcm"],
        help=(
            "Deficiency type: protan (red-weak), deutan (green-weak), tritan (blue-weak), "
            "achromat (rod monochromacy / complete achromatopsia), "
            "bcm (blue-cone monochromacy)."
        ),
    )

    parser.add_argument(
        "--severity",
        "-s",
        type=float,
        default=1.0,
        help="Severity between 0.0 (normal vision) and 1.0 (full dichromacy).",
    )

    parser.add_argument(
        "--daltonize-method",
        type=str,
        default="fidaner",
        choices=["fidaner", "simple"],
        help="Daltonization method (only used with --filter daltonize).",
    )

    args = parser.parse_args()
    return args


DEFICIENCY_FROM_STR = {
    "protan":   simulate.Deficiency.PROTAN,
    "deutan":   simulate.Deficiency.DEUTAN,
    "tritan":   simulate.Deficiency.TRITAN,
    "achromat": simulate.Deficiency.ACHROMAT,
    "bcm":      simulate.Deficiency.BCM,
}


def get_simulator(model_name: str) -> simulate.Simulator:
    """Get the simulator instance for the given model name."""
    # Lazy lambdas so only the requested simulator is instantiated.
    # Eager construction would trigger DeprecationWarning for coblisV1
    # on every call regardless of the model actually requested.
    simulators = {
        "vienot": lambda: simulate.Simulator_Vienot1999(convert.LMSModel_sRGB_SmithPokorny75()),
        "brettel": lambda: simulate.Simulator_Brettel1997(convert.LMSModel_sRGB_SmithPokorny75()),
        "vischeck": lambda: simulate.Simulator_Vischeck(),
        "machado": lambda: simulate.Simulator_Machado2009(),
        "coblisV1": lambda: simulate.Simulator_CoblisV1(),
        "coblisV2": lambda: simulate.Simulator_CoblisV2(),
        "auto": lambda: simulate.Simulator_AutoSelect(),
    }
    return simulators[model_name]()


def _process_one(im_path: Path, out_path: Path, args) -> bool:
    """Process a single image.  Returns True on success, False on failure."""
    try:
        im = np.asarray(Image.open(im_path).convert("RGB"))
    except Exception as e:
        print(f"ERROR: Failed to load {im_path}: {e}", file=sys.stderr)
        return False

    deficiency = DEFICIENCY_FROM_STR[args.deficiency]

    if args.filter == "simulate":
        simulator = get_simulator(args.model)
        out = simulator.simulate_cvd(im, deficiency=deficiency, severity=args.severity)
    else:
        simulator = get_simulator(args.model) if args.model != "auto" else None
        out = daltonize_module.daltonize(
            im,
            deficiency=deficiency,
            severity=args.severity,
            method=args.daltonize_method,
            simulator=simulator,
        )

    try:
        Image.fromarray(out).save(out_path)
        print(f"Saved: {out_path}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to save {out_path}: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for the DaltonLens CLI."""
    args = parse_command_line()

    # ------------------------------------------------------------------
    # Batch mode
    # ------------------------------------------------------------------
    if args.batch is not None:
        if args.output_dir is None:
            print("ERROR: --batch requires --output-dir", file=sys.stderr)
            sys.exit(1)

        matches = sorted(glob_module.glob(args.batch, recursive=True))
        if not matches:
            print(f"ERROR: No files matched pattern: {args.batch}", file=sys.stderr)
            sys.exit(1)

        out_dir = args.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        failed = 0
        for src in matches:
            src_path = Path(src)
            if not src_path.is_file():
                continue
            dst = out_dir / src_path.name
            if not _process_one(src_path, dst, args):
                failed += 1

        processed = len(matches) - failed
        print(f"Batch complete: {processed}/{len(matches)} images processed.")
        if failed:
            sys.exit(1)
        return

    # ------------------------------------------------------------------
    # Single-image mode
    # ------------------------------------------------------------------
    if args.input_image is None or args.output_image is None:
        print(
            "ERROR: Provide input_image and output_image, or use --batch with --output-dir.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.input_image.exists():
        print(f"ERROR: Input file not found: {args.input_image}", file=sys.stderr)
        sys.exit(1)

    if not _process_one(args.input_image, args.output_image, args):
        sys.exit(1)


if __name__ == "__main__":
    main()
