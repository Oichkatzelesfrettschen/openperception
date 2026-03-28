"""Tests for token-driven palette showcase scene payloads."""
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from palette_showcase_spec import build_showcase_spec


def test_showcase_spec_has_expected_lane_ids() -> None:
    payload = build_showcase_spec()

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


def test_showcase_spec_uses_current_token_values() -> None:
    payload = build_showcase_spec()
    lanes = {lane["scheme_id"]: lane for lane in payload["lanes"]}

    assert lanes["production-indigo-magenta"]["brand"]["primaryStrong"] == "#3730A3"
    assert lanes["accessible-mauve-burgundy"]["brand"]["tertiaryStrong"] == "#901C32"
    assert lanes["atmosphere-red-mahogany"]["brand"]["surface"] == "#F7F2EC"


def test_showcase_spec_exposes_variant_payloads() -> None:
    payload = build_showcase_spec()
    lanes = {lane["scheme_id"]: lane for lane in payload["lanes"]}

    assert lanes["production-indigo-magenta"]["available_variants"] == [
        "default",
        "protan",
        "deutan",
        "tritan",
        "mono",
    ]
    assert lanes["accessible-mauve-burgundy"]["variants"]["mono"]["brand"]["primaryStrong"] == "#1E293B"
    assert lanes["atmosphere-red-mahogany"]["available_variants"] == [
        "default",
        "protan",
        "deutan",
        "tritan",
        "mono",
    ]


def test_showcase_spec_embeds_live_repo_snapshot() -> None:
    payload = build_showcase_spec()

    assert payload["repo_stats"]["metrics"]["source_cache_doc_count"] >= 1
    assert payload["concept"]["repo_stats_binding"]["source_assembly_inputs_metric"] == "source_cache_doc_count"
    assert payload["concept"]["repo_stats_binding"]["source_assembly_notes_metric"] == "primary_source_notes_count"
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
