#!/usr/bin/env python3
"""
Build a reproducible palette-showcase scene specification from repo token files.

WHY: OpenPerception now has multiple validated palette lanes. This helper turns
the current production and experimental token packs into one machine-readable
scene payload so downstream visualizations, including Blender renders, can use
source-of-truth token values instead of copied hex codes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOKEN_SOURCES = (
    (
        "production-indigo-magenta",
        "Production Indigo/Magenta",
        REPO_ROOT / "tokens" / "color-tokens.json",
        "Current default production lane.",
    ),
    (
        "accessible-mauve-burgundy",
        "Accessible Indigo/Mauve/Burgundy",
        REPO_ROOT / "tokens" / "experimental-mauve-burgundy.json",
        "Accessibility-first experimental lane with tertiary burgundy support.",
    ),
    (
        "atmosphere-red-mahogany",
        "Axiomatic Mahogany/Brass/Burgundy",
        REPO_ROOT / "tokens" / "experimental-red-mahogany.json",
        "Warm atmosphere lane with grounded structure, brass interpretation, and burgundy high-gravity emphasis.",
    ),
)


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
            "Three-lane palette showcase for production, accessibility-first, "
            "and axiomatic warm-atmosphere perceptual schemes."
        ),
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
