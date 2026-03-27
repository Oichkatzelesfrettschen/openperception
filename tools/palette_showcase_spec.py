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
        "Research",
        REPO_ROOT / "tokens" / "color-tokens.json",
        "Primary sources, provenance, and synthesized notes rendered as structured evidence.",
    ),
    (
        "accessible-mauve-burgundy",
        "Validation",
        REPO_ROOT / "tokens" / "experimental-mauve-burgundy.json",
        "Machine checks, constraints, and evidence gates that shape the repo's claims.",
    ),
    (
        "atmosphere-red-mahogany",
        "Accommodations",
        REPO_ROOT / "tokens" / "experimental-red-mahogany.json",
        "One source branching into contrast-led, guided-symbol-led, and depth-safe outputs.",
    ),
)
LIVING_CONCEPT = {
    "artifact_kind": "living_accessibility_concept_scene",
    "scene_header": "OpenPerception accessibility system",
    "plaque_text": "same source, adapted views",
    "flow": ["research", "validation", "accommodations"],
    "caption_dependence": "low",
    "representation": {
        "research": "Primary sources, cache provenance, and synthesis notes.",
        "validation": "Machine checks and policy gates that keep claims honest.",
        "accommodations": [
            "contrast_led",
            "guided_symbol_led",
            "depth_safe",
        ],
    },
    "visual_logic": {
        "research": "many sources converge into synthesized evidence",
        "validation": "intake passes through checks into accepted and rejected paths",
        "accommodations": "one source branches into distinct usable transformed views",
    },
    "repo_stats_binding": {
        "research_sources_metric": "source_cache_doc_count",
        "validation_inputs_metric": "primary_source_notes_count",
        "validation_gate_metric": "source_cache_doc_count",
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
    return {
        "scene_id": "openperception-palette-showcase",
        "summary": (
            "Living concept scene for research flowing through validation into "
            "transformed accommodations."
        ),
        "concept": LIVING_CONCEPT,
        "repo_stats": generate_repo_stats(REPO_ROOT),
        "render_preference": RENDER_PREFERENCE,
        "depth_accommodation": DEPTH_ACCOMMODATION,
        "lanes": [
            _build_lane(scheme_id, label, path, description)
            for scheme_id, label, path, description in TOKEN_SOURCES
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
