"""Tests for token-driven palette showcase scene payloads."""

import sys
from pathlib import Path

from PIL import Image


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import palette_showcase_spec as pss


def _write_test_image(path: Path, color: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (32, 32), color).save(path)


def _fake_physics_views(tmp_path: Path) -> dict:
    generated_dir = tmp_path / "generated"
    views = []
    for view_id, case_title, source_repo, color in (
        ("gw_chirp", "GW Chirp", "compact-common", "#112233"),
        ("neutrino_cooling", "Neutrino Cooling", "compact-common", "#223311"),
        ("blackhole_lensing", "Black Hole Lensing", "Blackhole", "#331122"),
    ):
        panel_texture = generated_dir / f"{view_id}.png"
        _write_test_image(panel_texture, color)
        views.append(
            {
                "id": view_id,
                "case_title": case_title,
                "mode_label": "test",
                "source_repo": source_repo,
                "panel_texture": str(panel_texture),
                "source_path": str(tmp_path / "sources" / f"{view_id}.png"),
            }
        )
    return {
        "schema_version": 2,
        "concept": "test physics views",
        "generated_dir": str(generated_dir),
        "views": views,
    }


def _fake_animated_views(tmp_path: Path) -> dict:
    animated_dir = tmp_path / "animated"
    views = []
    for view_id, color in (
        ("gw_chirp", "#445566"),
        ("neutrino_cooling", "#554466"),
        ("blackhole_lensing", "#665544"),
    ):
        animation_path = animated_dir / f"{view_id}.gif"
        _write_test_image(animation_path, color)
        views.append(
            {
                "id": view_id,
                "case_title": view_id,
                "mode_label": "test",
                "source_repo": "test",
                "animation_path": str(animation_path),
                "animation_basis": str(tmp_path / "sources" / f"{view_id}.png"),
                "frame_count": 1,
            }
        )
    return {
        "schema_version": 1,
        "concept": "test animated views",
        "generated_dir": str(animated_dir),
        "views": views,
        "deferred_views": [],
    }


def _build_showcase_spec(monkeypatch, tmp_path: Path) -> dict:
    monkeypatch.setattr(
        pss,
        "build_showcase_physics_views",
        lambda _output_dir: _fake_physics_views(tmp_path),
    )
    monkeypatch.setattr(
        pss,
        "build_showcase_animated_views",
        lambda _output_dir: _fake_animated_views(tmp_path),
    )
    return pss.build_showcase_spec()


def test_showcase_spec_has_expected_lane_ids(monkeypatch, tmp_path) -> None:
    payload = _build_showcase_spec(monkeypatch, tmp_path)

    assert payload["scene_id"] == "openperception-palette-showcase"
    assert payload["concept"]["artifact_kind"] == "living_accessibility_concept_scene"
    assert payload["concept"]["concept_phrase"] == (
        "real physics use cases turned into real accessible and animated views showcase"
    )
    assert payload["concept"]["scene_header"] == ""
    assert payload["concept"]["plaque_text"] == ""
    assert payload["concept"]["caption_dependence"] == "low"
    assert payload["render_preference"]["preferred_engine"] == "octane"
    assert payload["depth_accommodation"]["stereo_role"] == (
        "Stereo enriches the scene but is not required for comprehension."
    )
    assert payload["repo_stats"]["metrics"]["canonical_pdf_count"] > 0
    assert [lane["scheme_id"] for lane in payload["lanes"]] == [
        "production-indigo-magenta",
        "accessible-mauve-burgundy",
        "atmosphere-red-mahogany",
    ]
    assert [lane["label"] for lane in payload["lanes"]] == [
        "Color-safe",
        "Symbol-guided",
        "Depth-safe",
    ]
    assert [lane["case_title"] for lane in payload["lanes"]] == [
        "GW Chirp",
        "Neutrino Cooling",
        "Black Hole Lensing",
    ]


def test_showcase_spec_uses_current_token_values(monkeypatch, tmp_path) -> None:
    payload = _build_showcase_spec(monkeypatch, tmp_path)
    lanes = {lane["scheme_id"]: lane for lane in payload["lanes"]}

    assert lanes["production-indigo-magenta"]["brand"]["primaryStrong"] == "#3730A3"
    assert lanes["accessible-mauve-burgundy"]["brand"]["tertiaryStrong"] == "#901C32"
    assert lanes["atmosphere-red-mahogany"]["brand"]["surface"] == "#F7F2EC"


def test_showcase_spec_exposes_variant_payloads(monkeypatch, tmp_path) -> None:
    payload = _build_showcase_spec(monkeypatch, tmp_path)
    lanes = {lane["scheme_id"]: lane for lane in payload["lanes"]}

    assert lanes["production-indigo-magenta"]["available_variants"] == [
        "default",
        "protan",
        "deutan",
        "tritan",
        "mono",
    ]
    assert (
        lanes["accessible-mauve-burgundy"]["variants"]["mono"]["brand"]["primaryStrong"]
        == "#1E293B"
    )
    assert lanes["atmosphere-red-mahogany"]["available_variants"] == [
        "default",
        "protan",
        "deutan",
        "tritan",
        "mono",
    ]


def test_showcase_spec_embeds_live_repo_snapshot(monkeypatch, tmp_path) -> None:
    payload = _build_showcase_spec(monkeypatch, tmp_path)

    assert payload["repo_stats"]["metrics"]["source_cache_doc_count"] >= 1
    assert (
        payload["concept"]["repo_stats_binding"]["source_assembly_inputs_metric"]
        == "source_cache_doc_count"
    )
    assert (
        payload["concept"]["repo_stats_binding"]["source_assembly_notes_metric"]
        == "primary_source_notes_count"
    )
    assert payload["concept"]["repo_stats_binding"]["accommodation_modes"] == 3
    assert payload["concept"]["repo_stats_source"] == "docs/generated/repo_stats.json"
    assert len(payload["physics_views"]["views"]) == 3
    assert [entry["id"] for entry in payload["animated_views"]["views"]] == [
        "gw_chirp",
        "neutrino_cooling",
        "blackhole_lensing",
    ]
    assert payload["animated_views"]["deferred_views"] == []
    for lane in payload["lanes"]:
        assert Path(lane["panel_texture"]).exists()
    assert Path(payload["lanes"][0]["animated_artifact"]).exists()
    assert Path(payload["lanes"][1]["animated_artifact"]).exists()
    assert Path(payload["lanes"][2]["animated_artifact"]).exists()
