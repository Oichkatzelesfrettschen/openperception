"""Tests for scaling and quantization helpers."""

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scaling import (
    HysteresisQuantizer,
    build_report,
    effective_scale,
    get_dpi_adjusted_snap_class,
    logical_to_physical_px,
    modular_scale,
    practical_typography_size,
    quantize_value,
    touch_target_physical_px,
)


def test_effective_scale_matches_spec_examples() -> None:
    assert effective_scale(144, 1.25) == 1.875
    assert effective_scale(192, 1.0) == 2.0


def test_logical_to_physical_px_matches_reference_conversion() -> None:
    assert logical_to_physical_px(16, 144, 1.0) == 24
    assert round(logical_to_physical_px(16, 76, 1.0), 2) == 12.67


def test_modular_scale_and_practical_rounding() -> None:
    assert round(modular_scale(3), 2) == 31.25
    assert practical_typography_size(3) == 31


def test_hysteresis_quantizer_suppresses_layout_jitter() -> None:
    quantizer = HysteresisQuantizer()

    first = quantize_value(
        15.49, "layout", dpi=96, key="card.width", quantizer=quantizer
    )
    second = quantize_value(
        15.51, "layout", dpi=96, key="card.width", quantizer=quantizer
    )
    third = quantize_value(
        15.90, "layout", dpi=96, key="card.width", quantizer=quantizer
    )

    assert first == 15.0
    assert second == 15.0
    assert third == 16.0


def test_touch_target_floor_never_drops_below_44px() -> None:
    assert touch_target_physical_px(44, dpi_phys=76, user_scale=1.0) == 44.0


def test_high_dpi_text_size_quantization_tightens_precision() -> None:
    snap_class = get_dpi_adjusted_snap_class("text-size", dpi=192)
    quantizer = HysteresisQuantizer()
    value = quantize_value(
        15.18, "text-size", dpi=192, key="body.size", quantizer=quantizer
    )

    assert snap_class.precision == 0.125
    assert value == 15.125


def test_build_report_uses_touch_target_floor() -> None:
    payload = build_report(
        44, dpi_phys=76, user_scale=1.0, snap_class_name="touch-target"
    )

    assert payload["quantized_px"] == 44.0


def test_build_report_can_attach_profile_composition() -> None:
    payload = build_report(
        16,
        dpi_phys=96,
        user_scale=1.0,
        snap_class_name="layout",
        profile_names=["standard", "reduced-motion"],
    )

    assert payload["profile_composition"]["selected_profiles"] == [
        "standard",
        "reduced-motion",
    ]
    assert payload["profile_composition"]["resolved_caps"]["max_animation_hz"] == 0
