"""Tests for generated physics showcase views."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import showcase_physics_views as spv


def test_build_showcase_physics_views_writes_expected_panels(
    monkeypatch, tmp_path
) -> None:
    def _fake_builder(spec, output_dir):
        output_path = output_dir / f"{spec['id']}.png"
        Image.new("RGB", (32, 32), "#112233").save(output_path)
        return {
            "panel_texture": str(output_path),
            "source_path": str(spec["source_path"]),
        }

    def _fake_animation_builder(spec, output_dir):
        output_path = output_dir / f"{spec['id']}.gif"
        Image.new("RGB", (32, 32), "#221133").save(output_path)
        return {
            "animation_path": str(output_path),
            "animation_basis": str(
                spec.get("data_path")
                or spec.get("contact_sheet_path")
                or spec["source_path"]
            ),
            "frame_count": 4,
        }

    monkeypatch.setattr(
        spv,
        "PANEL_BUILDERS",
        {
            "gw_chirp": _fake_builder,
            "neutrino_cooling": _fake_builder,
            "blackhole_lensing": _fake_builder,
        },
    )
    monkeypatch.setattr(
        spv,
        "ANIMATION_BUILDERS",
        {
            "gw_chirp": _fake_animation_builder,
            "neutrino_cooling": _fake_animation_builder,
        },
    )

    manifest = spv.build_showcase_physics_views(tmp_path)
    animated = spv.build_showcase_animated_views(tmp_path / "animated")

    assert (
        manifest["concept"]
        == "real physics use cases turned into real accessible and animated views showcase"
    )
    assert [entry["id"] for entry in manifest["views"]] == [
        "gw_chirp",
        "neutrino_cooling",
        "blackhole_lensing",
    ]
    for entry in manifest["views"]:
        assert Path(entry["panel_texture"]).exists()
    assert (tmp_path / spv.MANIFEST_NAME).exists()
    assert [entry["id"] for entry in animated["views"]] == [
        "gw_chirp",
        "neutrino_cooling",
    ]
    for entry in animated["views"]:
        assert Path(entry["animation_path"]).exists()
    assert (tmp_path / "animated" / spv.ANIMATED_MANIFEST_NAME).exists()
