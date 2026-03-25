"""Tests for the Blender palette showcase scene script helpers."""
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blender_palette_showcase_scene import _hex_to_rgba, parse_args


def test_parse_args_reads_required_paths() -> None:
    args = parse_args(
        [
            "--spec",
            "artifacts/blender_showcase/showcase.json",
            "--output",
            "artifacts/blender_showcase/showcase.png",
            "--engine",
            "octane",
            "--blend-output",
            "artifacts/blender_showcase/showcase.blend",
        ]
    )

    assert args.spec == "artifacts/blender_showcase/showcase.json"
    assert args.output == "artifacts/blender_showcase/showcase.png"
    assert args.engine == "octane"
    assert args.blend_output == "artifacts/blender_showcase/showcase.blend"


def test_hex_to_rgba_returns_linearized_tuple() -> None:
    rgba = _hex_to_rgba("#FFFFFF")

    assert rgba == (1.0, 1.0, 1.0, 1.0)
