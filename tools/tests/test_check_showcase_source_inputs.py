"""Tests for sibling-repo showcase source input validation."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from showcase_physics_views import validate_showcase_source_inputs


def test_validate_showcase_source_inputs_accepts_readable_inputs(monkeypatch, tmp_path) -> None:
    image_path = tmp_path / "source.png"
    Image.new("RGB", (16, 16), "#112233").save(image_path)
    json_path = tmp_path / "data.json"
    json_path.write_text('{"arrays": {"real_time_s": [0.0], "detector_strain_whitened_visual": [1.0]}}', encoding="utf-8")
    monkeypatch.setattr(
        "showcase_physics_views.iter_showcase_source_inputs",
        lambda: [
            {"id": "gw_chirp", "path": image_path, "kind": "image", "role": "source_view"},
            {"id": "gw_chirp", "path": json_path, "kind": "json", "role": "animation_data"},
        ],
    )

    assert validate_showcase_source_inputs() == []


def test_validate_showcase_source_inputs_rejects_missing_or_broken_inputs(monkeypatch, tmp_path) -> None:
    broken_path = tmp_path / "broken.png"
    broken_path.write_text("not an image", encoding="utf-8")
    missing_path = tmp_path / "missing.json"
    monkeypatch.setattr(
        "showcase_physics_views.iter_showcase_source_inputs",
        lambda: [
            {"id": "gw_chirp", "path": broken_path, "kind": "image", "role": "source_view"},
            {"id": "gw_chirp", "path": missing_path, "kind": "json", "role": "animation_data"},
        ],
    )

    errors = validate_showcase_source_inputs()

    assert len(errors) == 2
    assert "unreadable image" in errors[0]
    assert "missing animation_data" in errors[1]
