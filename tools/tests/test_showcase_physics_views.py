"""Tests for generated physics showcase views."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import showcase_physics_views as spv


def test_build_showcase_physics_views_writes_expected_panels(monkeypatch, tmp_path) -> None:
    def _fake_builder(spec):
        output_path = tmp_path / f"{spec['id']}.png"
        Image.new("RGB", (32, 32), "#112233").save(output_path)
        return {"panel_texture": str(output_path), "source_path": str(spec["source_path"])}

    monkeypatch.setattr(
        spv,
        "BUILDERS",
        {
            "gw_chirp": _fake_builder,
            "neutrino_cooling": _fake_builder,
            "blackhole_lensing": _fake_builder,
        },
    )

    manifest = spv.build_showcase_physics_views(tmp_path)

    assert manifest["concept"] == "real physics use cases turned into real accessible and animated views showcase"
    assert [entry["id"] for entry in manifest["views"]] == [
        "gw_chirp",
        "neutrino_cooling",
        "blackhole_lensing",
    ]
    for entry in manifest["views"]:
        assert Path(entry["panel_texture"]).exists()
