"""Tests for the Blender palette showcase scene script helpers."""
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blender_palette_showcase_scene import (
    _hex_to_rgba,
    _select_render_engine,
    parse_args,
)


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


def test_select_render_engine_can_use_octane_even_when_enum_metadata_is_incomplete() -> None:
    class _EnumItem:
        def __init__(self, identifier: str) -> None:
            self.identifier = identifier

    class _Property:
        def __init__(self) -> None:
            self.enum_items = [_EnumItem("BLENDER_EEVEE_NEXT")]

    class _RNA:
        def __init__(self) -> None:
            self.properties = {"engine": _Property()}

    class _Render:
        def __init__(self) -> None:
            self.bl_rna = _RNA()
            self._engine = "BLENDER_EEVEE_NEXT"

        @property
        def engine(self) -> str:
            return self._engine

        @engine.setter
        def engine(self, value: str) -> None:
            if value not in {"octane", "BLENDER_EEVEE_NEXT", "CYCLES"}:
                raise TypeError(value)
            self._engine = value

    class _Scene:
        def __init__(self) -> None:
            self.render = _Render()

    scene = _Scene()

    assert _select_render_engine(scene, "octane") == "octane"
    assert scene.render.engine == "octane"
