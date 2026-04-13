#!/usr/bin/env python3
"""
Build a reproducible Blender showcase scene specification from repo token files.

WHY: OpenPerception now has a living Blender concept lane. This helper turns
the current production and experimental token packs into one machine-readable
scene payload so downstream visualizations can stay tied to current repo data
instead of copied hex codes or slogan-only descriptions.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from repo_stats import generate_repo_stats
from showcase_physics_views import (
    build_showcase_animated_views,
    build_showcase_physics_views,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DEPTH_ACCOMMODATION = {
    "principle": "Shared depth meaning through static monocular cues first.",
    "stereo_role": "Stereo enriches the scene but is not required for comprehension.",
    "motion_role": "Motion parallax reinforces depth but is not the only recovery path.",
    "static_cues": [
        "occlusion",
        "relative_size",
        "contact_shadows",
        "ground_plane_anchoring",
        "labels",
    ],
    "source": str(
        (
            REPO_ROOT / "docs" / "harmonized-depth-accommodation-guide.md"
        ).relative_to(REPO_ROOT)
    ),
}
RENDER_PREFERENCE = {
    "preferred_engine": "octane",
    "fallback_order": ["BLENDER_EEVEE_NEXT", "CYCLES"],
    "reason": (
        "Use Octane in Octane Blender when available for the canonical showcase "
        "artifact; fall back only when the live session does not expose it."
    ),
}
TOKEN_SOURCES = (
    (
        "production-indigo-magenta",
        "Color-safe",
        REPO_ROOT / "tokens" / "color-tokens.json",
        "A transformed view that reinforces color meaning with contrast, pattern, and markers.",
    ),
    (
        "accessible-mauve-burgundy",
        "Symbol-guided",
        REPO_ROOT / "tokens" / "experimental-mauve-burgundy.json",
        "A transformed view that carries interpretation through explicit paths and symbols.",
    ),
    (
        "atmosphere-red-mahogany",
        "Depth-safe",
        REPO_ROOT / "tokens" / "experimental-red-mahogany.json",
        "A transformed view that carries depth with contour, anchoring, and static relief cues.",
    ),
)
LIVING_CONCEPT = {
    "artifact_kind": "living_accessibility_concept_scene",
    "scene_header": "",
    "plaque_text": "",
    "flow": ["source_rail", "gw_chirp", "neutrino_cooling", "blackhole_lensing"],
    "caption_dependence": "low",
    "concept_phrase": "real physics use cases turned into real accessible and animated views showcase",
    "representation": {
        "source_rail": "Real adjacent-repo science artifacts staged as the substrate for accessible views.",
        "accessible_views": [
            "color_safe",
            "guided_symbol_led",
            "depth_safe",
        ],
    },
    "visual_logic": {
        "source_rail": "real science cases from compact-common and Blackhole remain visible as source material",
        "color_safe": "the gravitational-wave chirp is reinforced by contrast, pattern, and markers",
        "guided": "the neutrino explainer is reinforced by explicit paths, symbols, and motion-strip cues",
        "depth_safe": "the black-hole lensing view is reinforced by contour, anchoring, and static relief cues",
    },
    "repo_stats_binding": {
        "source_assembly_inputs_metric": "source_cache_doc_count",
        "source_assembly_notes_metric": "primary_source_notes_count",
        "source_assembly_gate_metric": "source_cache_doc_count",
        "accommodation_modes": 3,
    },
    "repo_stats_source": str(
        (REPO_ROOT / "docs" / "generated" / "repo_stats.json").relative_to(REPO_ROOT)
    ),
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_variant(variant_name: str, payload: dict, base_default: dict) -> dict:
    variant_payload = payload[variant_name]
    brand = {**base_default["brand"], **variant_payload.get("brand", {})}
    viz = {**base_default["viz"], **variant_payload.get("viz", {})}
    return {
        "brand": {
            "primary": brand["primary"],
            "primaryStrong": brand["primaryStrong"],
            "accent": brand["accent"],
            "accentStrong": brand["accentStrong"],
            "tertiary": brand.get("tertiary"),
            "tertiaryStrong": brand.get("tertiaryStrong"),
            "surface": brand["surface"],
            "text": brand["text"],
            "border": brand["border"],
            "focusRing": brand["focusRing"],
            "link": brand["link"],
        },
        "viz": {
            "categorical": viz["categorical"],
            "markers": viz["markers"],
            "dashes": viz["dashes"],
        },
    }


def _build_lane(scheme_id: str, label: str, path: Path, description: str) -> dict:
    payload = _load_json(path)
    default = payload["default"]
    variants = {
        variant_name: _normalize_variant(variant_name, payload, default)
        for variant_name in payload
    }
    return {
        "scheme_id": scheme_id,
        "label": label,
        "description": description,
        "source": str(path.relative_to(REPO_ROOT)),
        "available_variants": list(payload.keys()),
        "brand": variants["default"]["brand"],
        "viz": variants["default"]["viz"],
        "variants": variants,
    }


def build_showcase_spec() -> dict:
    physics_views = build_showcase_physics_views(
        REPO_ROOT / "artifacts" / "blender_showcase" / "generated"
    )
    animated_views = build_showcase_animated_views(
        REPO_ROOT / "artifacts" / "blender_showcase" / "animated"
    )
    animated_by_id = {view["id"]: view for view in animated_views["views"]}
    return {
        "scene_id": "openperception-palette-showcase",
        "summary": (
            "Living concept scene for real physics use cases transformed into "
            "accessible and animated views."
        ),
        "concept": LIVING_CONCEPT,
        "repo_stats": generate_repo_stats(REPO_ROOT),
        "physics_views": physics_views,
        "animated_views": animated_views,
        "render_preference": RENDER_PREFERENCE,
        "depth_accommodation": DEPTH_ACCOMMODATION,
        "lanes": [
            {
                **_build_lane(scheme_id, label, path, description),
                "case_title": physics_views["views"][index]["case_title"],
                "source_repo": physics_views["views"][index]["source_repo"],
                "panel_texture": physics_views["views"][index]["panel_texture"],
                "real_source_path": physics_views["views"][index]["source_path"],
                "animated_artifact": animated_by_id.get(physics_views["views"][index]["id"], {}).get("animation_path"),
            }
            for index, (scheme_id, label, path, description) in enumerate(TOKEN_SOURCES)
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Emit the token-driven palette showcase scene specification.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write the JSON payload.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    spec = build_showcase_spec()
    rendered = json.dumps(spec, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
