#!/usr/bin/env python3
"""
Reusable scaling and quantization helpers derived from UVAS scaling specs.

WHY: SCALING_MATHEMATICS.md and QUANTIZATION_POLICY.md define the unit system
and snap-class behavior, but the runtime previously had no shared
implementation. This module provides the first reusable substrate.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from profile_resolver import compose_profiles


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOGICAL_PIXELS_JSON = (
    REPO_ROOT / "specs" / "tokens" / "units" / "logical-pixels.json"
)


@dataclass(frozen=True)
class SnapClass:
    precision: float
    hysteresis: float
    round_mode: str = "round"


BASE_SNAP_CLASSES = {
    "stroke": SnapClass(precision=1.0, hysteresis=0.2),
    "layout": SnapClass(precision=1.0, hysteresis=0.2),
    "icon": SnapClass(precision=1.0, hysteresis=0.2),
    "spacing": SnapClass(precision=1.0, hysteresis=0.2),
    "touch-target": SnapClass(precision=1.0, hysteresis=0.0, round_mode="ceil"),
    "text-size": SnapClass(precision=0.25, hysteresis=0.1),
    "text-position": SnapClass(precision=0.5, hysteresis=0.15),
}


def load_logical_pixels_spec(path: Path | None = None) -> dict[str, Any]:
    spec_path = path or DEFAULT_LOGICAL_PIXELS_JSON
    return json.loads(spec_path.read_text())


def reference_dpi(path: Path | None = None) -> float:
    spec = load_logical_pixels_spec(path)
    return float(spec["reference"]["dpi_ref"])


def effective_scale(dpi_phys: float, user_scale: float, dpi_ref: float = 96.0) -> float:
    return (dpi_phys / dpi_ref) * user_scale


def logical_to_physical_px(
    value_lp: float,
    dpi_phys: float,
    user_scale: float,
    dpi_ref: float = 96.0,
) -> float:
    return value_lp * effective_scale(dpi_phys, user_scale, dpi_ref)


def modular_scale(step: int, base_lp: float = 16.0, ratio: float = 1.25) -> float:
    return base_lp * (ratio**step)


def practical_typography_size(step: int, base_lp: float = 16.0, ratio: float = 1.25) -> int:
    return round(modular_scale(step, base_lp=base_lp, ratio=ratio))


def get_dpi_adjusted_snap_class(snap_class: str, dpi: float) -> SnapClass:
    base = BASE_SNAP_CLASSES.get(snap_class, BASE_SNAP_CLASSES["layout"])
    precision = base.precision
    hysteresis = base.hysteresis

    if dpi < 96:
        if snap_class == "text-size":
            precision = 0.5
        hysteresis = 0.3
    elif dpi >= 192:
        if snap_class == "text-size":
            precision = 0.125
        elif snap_class == "stroke":
            precision = 0.5
        hysteresis = 0.1
    elif dpi >= 144:
        if snap_class == "stroke":
            precision = 0.5
        hysteresis = 0.15

    return SnapClass(
        precision=precision,
        hysteresis=hysteresis if base.round_mode != "ceil" else 0.0,
        round_mode=base.round_mode,
    )


@dataclass
class HysteresisQuantizer:
    """Quantizer with per-key memory to suppress jitter near snap boundaries."""

    state: dict[str, float] = field(default_factory=dict)

    def quantize(self, value: float, key: str, snap_class: SnapClass) -> float:
        if snap_class.round_mode == "ceil":
            return math.ceil(value / snap_class.precision) * snap_class.precision

        candidate = round(value / snap_class.precision) * snap_class.precision
        if key not in self.state:
            self.state[key] = candidate
            return candidate

        last = self.state[key]
        lower_bound = last - (snap_class.precision / 2) - snap_class.hysteresis
        upper_bound = last + (snap_class.precision / 2) + snap_class.hysteresis
        if lower_bound <= value <= upper_bound:
            return last

        self.state[key] = candidate
        return candidate

    def reset(self, key: str | None = None) -> None:
        if key is None:
            self.state.clear()
        else:
            self.state.pop(key, None)


def quantize_value(
    value_px: float,
    snap_class_name: str,
    dpi: float,
    key: str,
    quantizer: HysteresisQuantizer | None = None,
) -> float:
    quantizer = quantizer or HysteresisQuantizer()
    snap_class = get_dpi_adjusted_snap_class(snap_class_name, dpi)
    return quantizer.quantize(value_px, key, snap_class)


def touch_target_physical_px(
    value_lp: float,
    dpi_phys: float,
    user_scale: float,
    quantizer: HysteresisQuantizer | None = None,
) -> float:
    raw_px = logical_to_physical_px(value_lp, dpi_phys, user_scale)
    quantized = quantize_value(
        raw_px,
        snap_class_name="touch-target",
        dpi=dpi_phys,
        key="touch-target",
        quantizer=quantizer,
    )
    return max(44.0, quantized)


def build_report(
    value_lp: float,
    dpi_phys: float,
    user_scale: float,
    snap_class_name: str,
    profile_names: list[str] | None = None,
) -> dict[str, Any]:
    raw_px = logical_to_physical_px(value_lp, dpi_phys, user_scale)
    adjusted = get_dpi_adjusted_snap_class(snap_class_name, dpi_phys)
    quantizer = HysteresisQuantizer()
    if snap_class_name == "touch-target":
        quantized_px = touch_target_physical_px(
            value_lp,
            dpi_phys=dpi_phys,
            user_scale=user_scale,
            quantizer=quantizer,
        )
    else:
        quantized_px = quantize_value(
            raw_px,
            snap_class_name=snap_class_name,
            dpi=dpi_phys,
            key=f"{snap_class_name}:{value_lp}",
            quantizer=quantizer,
        )
    payload = {
        "value_lp": value_lp,
        "dpi_phys": dpi_phys,
        "user_scale": user_scale,
        "effective_scale": effective_scale(dpi_phys, user_scale),
        "raw_px": raw_px,
        "snap_class": snap_class_name,
        "precision_px": adjusted.precision,
        "hysteresis_px": adjusted.hysteresis,
        "round_mode": adjusted.round_mode,
        "quantized_px": quantized_px,
    }
    if profile_names:
        payload["profile_composition"] = compose_profiles(profile_names)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert logical pixels to physical pixels and apply snap-class quantization.",
    )
    parser.add_argument("--lp", type=float, default=16.0, help="Value in logical pixels.")
    parser.add_argument("--dpi", type=float, default=96.0, help="Physical DPI.")
    parser.add_argument("--scale", type=float, default=1.0, help="User scale factor.")
    parser.add_argument(
        "--snap-class",
        default="layout",
        choices=sorted(BASE_SNAP_CLASSES),
        help="Snap class to apply.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of text.",
    )
    parser.add_argument(
        "--profiles",
        help="Comma-separated profile names to attach to the scaling report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    profile_names = [part.strip() for part in args.profiles.split(",")] if args.profiles else None
    payload = build_report(args.lp, args.dpi, args.scale, args.snap_class, profile_names)
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print("OpenPerception Scaling Report")
        print(f"Logical value: {payload['value_lp']} lp")
        print(f"Effective scale: {payload['effective_scale']:.3f}")
        print(f"Raw physical size: {payload['raw_px']:.3f}px")
        print(
            f"Snap class: {payload['snap_class']} "
            f"(precision {payload['precision_px']}px, hysteresis {payload['hysteresis_px']}px, "
            f"mode {payload['round_mode']})"
        )
        print(f"Quantized size: {payload['quantized_px']:.3f}px")
        if "profile_composition" in payload:
            profiles = payload["profile_composition"]
            print("Profiles: " + ", ".join(profiles["selected_profiles"]))
            print(
                "Resolved caps: "
                + json.dumps(profiles["resolved_caps"], sort_keys=True)
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
