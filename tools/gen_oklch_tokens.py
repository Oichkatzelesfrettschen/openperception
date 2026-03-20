#!/usr/bin/env python3
"""
Generate OKLCH mappings for brand tokens.
Reads tokens/color-tokens.json and writes:
- tokens/color-oklch-map.json (hex -> [L, C, h])
- tokens/color-tokens-oklch.css (CSS variables with OKLCH triples per variant)
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from okcolor import format_oklch_tuple, hex_to_oklch


ROOT = Path(__file__).resolve().parents[1]
TOKENS_JSON = ROOT / 'tokens' / 'color-tokens.json'
OKLCH_MAP_JSON = ROOT / 'tokens' / 'color-oklch-map.json'
OKLCH_CSS = ROOT / 'tokens' / 'color-tokens-oklch.css'


def collect_hex_values(tokens: dict[str, Any]) -> dict[str, set]:
    by_variant: dict[str, set] = {}
    for variant, data in tokens.items():
        colors = set()
        # brand roles
        if 'brand' in data:
            for k, v in data['brand'].items():
                if isinstance(v, str) and v.startswith('#'):
                    colors.add(v)
        # ramps
        for ramp in ('indigo', 'magenta', 'gray'):
            if ramp in data and isinstance(data[ramp], dict):
                for _, hexv in data[ramp].items():
                    if isinstance(hexv, str) and hexv.startswith('#'):
                        colors.add(hexv)
        # viz colors
        if 'viz' in data and 'categorical' in data['viz']:
            for hexv in data['viz']['categorical']:
                if isinstance(hexv, str) and hexv.startswith('#'):
                    colors.add(hexv)
        by_variant[variant] = colors
    return by_variant


def compute_oklch_map(colors: set) -> dict[str, tuple[float, float, float]]:
    result: dict[str, tuple[float, float, float]] = {}
    for hexv in sorted(colors):
        try:
            result[hexv] = format_oklch_tuple(hex_to_oklch(hexv))
        except Exception:
            pass
    return result


def write_oklch_css(tokens: dict[str, Any], oklch_map: dict[str, tuple[float, float, float]]) -> str:
    lines = []
    # Default/root
    def add_block(selector: str, data: dict[str, Any]):
        lines.append(f"{selector} {{")
        # Emit OKLCH variables for ramps present
        for ramp in ('indigo', 'magenta', 'gray'):
            ramp_data = data.get(ramp, {})
            if isinstance(ramp_data, dict):
                for key, hexv in ramp_data.items():
                    if isinstance(hexv, str) and hexv in oklch_map:
                        L, C, h = oklch_map[hexv]
                        var = f"--oklch-{ramp}-{key}"
                        lines.append(f"  {var}: {L} {C} {h};")
        # Brand roles
        brand = data.get('brand', {})
        for name, hexv in brand.items():
            if isinstance(hexv, str) and hexv in oklch_map:
                L, C, h = oklch_map[hexv]
                var = f"--oklch-brand-{name}"
                lines.append(f"  {var}: {L} {C} {h};")
        lines.append("}")

    add_block(':root', tokens['default'])
    # Variants
    for variant in tokens:
        if variant == 'default':
            continue
        add_block(f"[data-cvd=\"{variant}\"]", tokens[variant])

    return '\n'.join(lines) + '\n'


def main():
    tokens = json.loads(TOKENS_JSON.read_text())
    by_variant = collect_hex_values(tokens)
    all_colors = set()
    for s in by_variant.values():
        all_colors |= s
    oklch_map = compute_oklch_map(all_colors)

    OKLCH_MAP_JSON.write_text(json.dumps(oklch_map, indent=2))
    css = write_oklch_css(tokens, oklch_map)
    OKLCH_CSS.write_text(css)
    print(f"Wrote {OKLCH_MAP_JSON} and {OKLCH_CSS}")


if __name__ == '__main__':
    main()

