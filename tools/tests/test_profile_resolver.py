"""Tests for axis/display profile composition."""
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from profile_resolver import compose_profiles, load_profile_manifest


def test_load_profile_manifest_has_standard_profile() -> None:
    manifest = load_profile_manifest()

    assert "profiles" in manifest
    assert "standard" in manifest["profiles"]


def test_compose_profiles_prefers_most_restrictive_temporal_caps() -> None:
    payload = compose_profiles(["standard", "flicker-sensitive", "reduced-motion"])

    assert payload["resolved_axes"]["temporal"] == "reduced motion"
    assert payload["resolved_caps"]["max_animation_hz"] == 0
    assert payload["resolved_caps"]["max_luminance_modulation_hz"] == 0
    assert payload["resolved_caps"]["min_transition_duration_ms"] == 0
    assert any(conflict["axis"] == "temporal" for conflict in payload["conflicts"])


def test_compose_profiles_detects_chromatic_conflict() -> None:
    payload = compose_profiles(["protan-safe", "deutan-safe"])

    assert payload["resolved_axes"]["chromatic"] == "conflict"
    assert any(
        conflict["axis"] == "chromatic" and conflict["kind"] == "needs_attention"
        for conflict in payload["conflicts"]
    )


def test_compose_profiles_detects_luminance_conflict() -> None:
    payload = compose_profiles(["high-contrast", "low-glare"])

    assert payload["resolved_axes"]["luminance"] == "conflict"
    assert any(
        conflict["axis"] == "luminance" and conflict["kind"] == "needs_attention"
        for conflict in payload["conflicts"]
    )
