#!/usr/bin/env python3
"""Derive the 'mono' token variant via BT.709 luminance projection.

WHY: The mono variant must reflect how an achromat (complete achromatopsia)
     perceives each brand color -- i.e., only BT.709 photopic luminance matters.
     Hand-crafted slate values do not align with the simulation math in
     Simulator_Achromat or dl_simulate_cvd_achromat.

WHAT:
  - Reads tokens/color-tokens.json, processes the 'default' variant
  - For each chromatic hex value: sRGB -> linear -> BT.709 Y -> sRGB gray
  - Snaps to the nearest stop in the gray ramp (by absolute value distance)
  - Writes updated 'mono' block back to color-tokens.json in-place
  - Rewrites the [data-cvd="mono"] block in tokens/color-tokens.css

HOW:
  python tools/gen_mono_tokens.py
  # or
  make mono-tokens

GRAY RAMP (from default.gray in color-tokens.json):
  900:#111827(~17)  800:#1F2937(~31)  700:#374151(~55)  500:#6B7280(~107)
  400:#9CA3AF(~156) 300:#D1D5DB(~209) 200:#E5E7EB(~229) 100:#F3F4F6(~243)
    0:#FFFFFF(255)

Snapping avoids perceptual clustering: two semantically-distinct colors that
project to nearby luminances get mapped to the same ramp step, which would
make them indistinguishable. Contrast GATE-007 validates the final result.
"""

import json
import re
from pathlib import Path


ROOT = Path(__file__).parent.parent
TOKENS_JSON = ROOT / "tokens" / "color-tokens.json"
TOKENS_CSS = ROOT / "tokens" / "color-tokens.css"

# Gray ramp: (display_8bit_value, hex_string)
# Values computed as round(int(hex, 16) * 0.2126-weight equivalent) -- but
# we use the actual sRGB gray value of each stop for snapping distance.
GRAY_RAMP = [
    (17, "#111827"),  # 900
    (31, "#1F2937"),  # 800
    (55, "#374151"),  # 700
    (107, "#6B7280"),  # 500
    (156, "#9CA3AF"),  # 400
    (209, "#D1D5DB"),  # 300
    (229, "#E5E7EB"),  # 200
    (243, "#F3F4F6"),  # 100
    (255, "#FFFFFF"),  # 0
]


def _srgb_to_linear(c: float) -> float:
    """IEC 61966-2-1 inverse companding."""
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    """IEC 61966-2-1 forward companding, clamped to [0,1]."""
    c = max(0.0, min(1.0, c))
    if c <= 0.0031308:
        return c * 12.92
    return 1.055 * (c ** (1.0 / 2.4)) - 0.055


def hex_to_bt709_gray8(hex_color: str) -> int:
    """Return BT.709 luminance of hex_color as an 8-bit sRGB gray value."""
    h = hex_color.lstrip("#")
    r8, g8, b8 = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r_lin = _srgb_to_linear(r8 / 255.0)
    g_lin = _srgb_to_linear(g8 / 255.0)
    b_lin = _srgb_to_linear(b8 / 255.0)
    y_lin = 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
    y_srgb = _linear_to_srgb(y_lin)
    return round(y_srgb * 255)


def snap_to_ramp(gray8: int) -> str:
    """Return the hex string of the nearest gray ramp stop."""
    best_hex = GRAY_RAMP[0][1]
    best_dist = abs(gray8 - GRAY_RAMP[0][0])
    for stop_val, stop_hex in GRAY_RAMP[1:]:
        dist = abs(gray8 - stop_val)
        if dist < best_dist:
            best_dist = dist
            best_hex = stop_hex
    return best_hex


def project_hex(hex_color: str) -> str:
    """Project a color to its BT.709 gray ramp stop."""
    return snap_to_ramp(hex_to_bt709_gray8(hex_color))


def derive_mono(default_variant: dict) -> dict:
    """Build the complete mono variant from the default variant.

    Rules:
    - gray ramp: copied verbatim from default (already achromatic)
    - indigo, magenta: project each stop
    - brand: project primary, primaryStrong, accent, accentStrong, link;
             copy text, surface, border, focusRing as-is (already gray/white)
    - viz.categorical: project each entry
    - viz.markers, viz.dashes: copied unchanged (non-color redundancy)
    """
    mono = {}

    # --- gray: copy verbatim ---
    mono["gray"] = dict(default_variant["gray"])

    # --- indigo ---
    mono["indigo"] = {k: project_hex(v) for k, v in default_variant["indigo"].items()}

    # --- magenta ---
    mono["magenta"] = {k: project_hex(v) for k, v in default_variant["magenta"].items()}

    # --- brand ---
    d_brand = default_variant["brand"]
    mono["brand"] = {
        "primary": project_hex(d_brand["primary"]),
        "primaryStrong": project_hex(d_brand["primaryStrong"]),
        "accent": project_hex(d_brand["accent"]),
        "accentStrong": project_hex(d_brand["accentStrong"]),
        "text": d_brand["text"],  # already #111827 (near-black)
        "surface": d_brand["surface"],  # already #FFFFFF
        "border": d_brand["border"],  # already #D1D5DB (gray-300)
        "focusRing": project_hex(d_brand["focusRing"]),
        "link": project_hex(d_brand["link"]),
    }

    # --- contrast guard: brand.primary on white must be >= 4.5:1 WCAG AA ---
    primary_gray8 = hex_to_bt709_gray8(mono["brand"]["primary"])
    # relative luminance of primary
    prim_lin = _srgb_to_linear(primary_gray8 / 255.0)
    white_lum = 1.0
    l1 = max(prim_lin, white_lum)
    l2 = min(prim_lin, white_lum)
    ratio = (l1 + 0.05) / (l2 + 0.05)
    if ratio < 4.5:
        # Escalate to nearest darker ramp stop than current primary
        cur_stop_val = next(v for v, h in GRAY_RAMP if h == mono["brand"]["primary"])
        darker = [h for v, h in GRAY_RAMP if v < cur_stop_val]
        if darker:
            darker_hex = darker[-1]  # closest darker
            mono["brand"]["primary"] = darker_hex
            mono["brand"]["link"] = darker_hex

    # --- viz ---
    d_viz = default_variant["viz"]
    mono["viz"] = {
        "categorical": [project_hex(c) for c in d_viz["categorical"]],
        "markers": list(d_viz["markers"]),
        "dashes": [list(d) for d in d_viz["dashes"]],
    }

    return mono


def update_json(tokens_path: Path, mono: dict) -> None:
    """Write mono variant back to color-tokens.json, preserving key order."""
    with tokens_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    data["mono"] = mono
    with tokens_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")


def build_css_block(mono: dict) -> str:
    """Render [data-cvd="mono"] CSS block from mono variant."""
    ind = mono["indigo"]
    mag = mono["magenta"]
    lines = [
        "/* Monochrome (achromatopsia) -- derived via BT.709 luminance projection */",
        '[data-cvd="mono"] {',
    ]
    # indigo
    for stop, hex_val in ind.items():
        lines.append(f"  --indigo-{stop}: {hex_val};")
    lines.append("")
    # magenta
    for stop, hex_val in mag.items():
        lines.append(f"  --magenta-{stop}: {hex_val};")
    lines.append("")
    # brand
    lines += [
        "  --brand-primary: var(--indigo-600);",
        "  --brand-primary-strong: var(--indigo-700);",
        "  --brand-accent: var(--magenta-600);",
        "  --brand-accent-strong: var(--magenta-700);",
        "}",
    ]
    return "\n".join(lines)


def update_css(css_path: Path, new_block: str) -> None:
    """Replace the [data-cvd="mono"] block in the CSS file."""
    text = css_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'/\* Monochrome.*?\[data-cvd="mono"\] \{.*?\}',
        re.DOTALL,
    )
    if pattern.search(text):
        updated = pattern.sub(new_block, text)
    else:
        # Append before the first non-CVD rule block after the last CVD block
        insert_marker = "\n/* Utility examples */"
        updated = text.replace(
            insert_marker, "\n" + new_block + "\n" + "/* Utility examples */"
        )
    css_path.write_text(updated, encoding="utf-8")


def main() -> None:
    with TOKENS_JSON.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    default = data["default"]
    mono = derive_mono(default)

    update_json(TOKENS_JSON, mono)
    print(f"Updated {TOKENS_JSON}")

    css_block = build_css_block(mono)
    update_css(TOKENS_CSS, css_block)
    print(f"Updated {TOKENS_CSS}")

    # Summary
    print("\nMono token summary:")
    print(f"  indigo:   {mono['indigo']}")
    print(f"  magenta:  {mono['magenta']}")
    print(
        f"  brand.primary: {mono['brand']['primary']} "
        f"(accent: {mono['brand']['accent']})"
    )
    print(f"  viz.categorical: {mono['viz']['categorical']}")


if __name__ == "__main__":
    main()
