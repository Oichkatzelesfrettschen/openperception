#!/usr/bin/env python3
"""
Resolve and compose axis/display profiles into one runtime view.

WHY: AXIS_OVERLAP_MAP and DISPLAY_ADAPTATION_LAYER define profile composition,
but the runtime previously had no executable manifest loader or conflict
reporter. This module provides the first partial implementation.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_MANIFEST = REPO_ROOT / "specs" / "tokens" / "profiles" / "axis-profiles.json"
AXES = ("chromatic", "luminance", "spatial", "temporal", "depth", "cognitive")
TEMPORAL_PRIORITY = {"full motion": 0, "reduced motion": 1, "static": 2}
COGNITIVE_PRIORITY = {"full HUD": 0, "simple HUD": 1, "minimal HUD": 2}
LUMINANCE_LEVELS = {"default", "high", "low"}
PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)%")


def load_profile_manifest(path: Path | None = None) -> dict[str, Any]:
    manifest_path = path or DEFAULT_PROFILE_MANIFEST
    return json.loads(manifest_path.read_text())


def _parse_scale_percent(value: str) -> float:
    match = PERCENT_RE.search(value)
    if not match:
        return 100.0
    return float(match.group(1))


def _resolve_axis(axis: str, values: list[str], conflicts: list[dict[str, str]]) -> str:
    distinct = list(dict.fromkeys(values))
    if len(distinct) == 1:
        return distinct[0]

    if axis == "temporal":
        conflicts.append(
            {
                "axis": axis,
                "kind": "resolved",
                "message": f"Temporal profiles disagree ({', '.join(distinct)}); most restrictive mode wins.",
            }
        )
        return max(distinct, key=lambda value: TEMPORAL_PRIORITY.get(value, -1))

    if axis == "cognitive":
        conflicts.append(
            {
                "axis": axis,
                "kind": "resolved",
                "message": f"Cognitive profiles disagree ({', '.join(distinct)}); least dense HUD wins.",
            }
        )
        return max(distinct, key=lambda value: COGNITIVE_PRIORITY.get(value, -1))

    if axis == "spatial":
        conflicts.append(
            {
                "axis": axis,
                "kind": "resolved",
                "message": f"Spatial scales disagree ({', '.join(distinct)}); largest scale wins.",
            }
        )
        return max(distinct, key=_parse_scale_percent)

    if axis == "luminance":
        active_levels = {value for value in distinct if value in LUMINANCE_LEVELS and value != "default"}
        if len(active_levels) > 1:
            conflicts.append(
                {
                    "axis": axis,
                    "kind": "needs_attention",
                    "message": f"Luminance profiles conflict: {', '.join(distinct)}.",
                }
            )
            return "conflict"
        return next(iter(active_levels), "default")

    if axis == "chromatic":
        active_variants = {value for value in distinct if value != "default"}
        if len(active_variants) > 1:
            conflicts.append(
                {
                    "axis": axis,
                    "kind": "needs_attention",
                    "message": f"Chromatic variants conflict: {', '.join(distinct)}.",
                }
            )
            return "conflict"
        return next(iter(active_variants), "default")

    conflicts.append(
        {
            "axis": axis,
            "kind": "resolved",
            "message": f"Multiple values supplied for {axis}; first value retained.",
        }
    )
    return distinct[0]


def compose_profiles(
    profile_names: list[str] | None = None,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    manifest = load_profile_manifest(manifest_path)
    profiles = manifest["profiles"]
    selected_names = profile_names or ["standard"]
    unknown = [name for name in selected_names if name not in profiles]
    if unknown:
        raise ValueError(f"Unknown profile(s): {', '.join(unknown)}")

    selected = [profiles[name] for name in selected_names]
    conflicts: list[dict[str, str]] = []
    resolved_axes = {
        axis: _resolve_axis(axis, [profile["axes"][axis] for profile in selected], conflicts)
        for axis in AXES
    }

    max_animation_hz = min(profile["caps"]["max_animation_hz"] for profile in selected)
    max_luminance_modulation_hz = min(
        profile["caps"]["max_luminance_modulation_hz"] for profile in selected
    )
    min_transition_duration_ms_values = [
        profile["caps"]["min_transition_duration_ms"] for profile in selected
    ]
    min_transition_duration_ms = (
        0
        if 0 in min_transition_duration_ms_values
        else max(min_transition_duration_ms_values)
    )
    pattern_encoding_required = any(
        profile["caps"].get("pattern_encoding_required", False) for profile in selected
    )

    palette_values = [
        profile["caps"].get("palette_variant", "full") for profile in selected
    ]
    non_default_palettes = {value for value in palette_values if value != "full"}
    if len(non_default_palettes) > 1:
        conflicts.append(
            {
                "axis": "palette_variant",
                "kind": "needs_attention",
                "message": "Palette variants conflict: " + ", ".join(sorted(non_default_palettes)),
            }
        )
        palette_variant = "conflict"
    else:
        palette_variant = next(iter(non_default_palettes), "full")

    return {
        "manifest_path": str(manifest_path or DEFAULT_PROFILE_MANIFEST),
        "selected_profiles": selected_names,
        "resolved_axes": resolved_axes,
        "resolved_caps": {
            "max_animation_hz": max_animation_hz,
            "max_luminance_modulation_hz": max_luminance_modulation_hz,
            "min_transition_duration_ms": min_transition_duration_ms,
            "palette_variant": palette_variant,
            "pattern_encoding_required": pattern_encoding_required,
        },
        "conflicts": conflicts,
    }


def build_text_report(payload: dict[str, Any]) -> str:
    lines = [
        "OpenPerception Profile Resolver",
        "",
        "Selected profiles: " + ", ".join(payload["selected_profiles"]),
        "",
        "Resolved axes:",
    ]
    for axis, value in payload["resolved_axes"].items():
        lines.append(f"- {axis}: {value}")
    lines.append("")
    lines.append("Resolved caps:")
    for key, value in payload["resolved_caps"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("Conflicts:")
    if payload["conflicts"]:
        for conflict in payload["conflicts"]:
            lines.append(
                f"- {conflict['axis']} [{conflict['kind']}]: {conflict['message']}"
            )
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compose OpenPerception axis/display profiles and report conflicts.",
    )
    parser.add_argument(
        "--profiles",
        help="Comma-separated profile names to compose (default: standard).",
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_PROFILE_MANIFEST),
        help="Path to the axis profile manifest JSON file.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    profile_names = [part.strip() for part in args.profiles.split(",")] if args.profiles else None
    payload = compose_profiles(profile_names, Path(args.manifest))
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(build_text_report(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
