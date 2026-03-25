# Colorblind-Friendly Design Guide (Indigo, Gray, Magenta)

This guide provides practical palettes, UI/UX patterns, and data visualization recipes that work for all common color vision deficiencies (CVD): protanopia/protanomaly, deuteranopia/deuteranomaly, tritanopia/tritanomaly, and monochromacy. The brand foundation uses indigo and gray with magenta accents, adjusted per CVD profile to maintain discriminability and contrast.

---

## Principles

- Treat simulation, daltonization, recognition aids, and reconstructive models
  as different support modes; see
  [Color support accommodation taxonomy](/home/eirikr/Github/openperception/docs/color-support-accommodation-taxonomy.md).
- Prefer redundant cues over color alone: text labels, icons, shapes, patterns, underline links, and direct value annotations.
- Maintain contrast: 4.5:1 for body text, 3:1 for large text and UI graphics, 7:1 where possible for critical content.
- Separate by lightness, not just hue. For CVD, lightness differences and thickness/shape are most reliable.
- Limit simultaneous accents. Use 1 primary (indigo), 1 accent (magenta), and neutrals (gray). For many categories, extend with distinct shapes/patterns.
- Ensure focus, hover, and selected states do not rely solely on color; add outlines, elevation, underline, thickness.

---

## Brand Palette Overview

- Primary (Indigo): deep, cool blue‑violet. Robust on light and dark backgrounds.
- Accent (Magenta): warm purple‑pink. Tends to shift toward blue for red‑green deficiencies; preserve separation via lightness.
- Neutral (Gray): accessible grayscale ramp for text, surfaces, and dividers.

Base hexes (non‑CVD default):

- Indigo: `#3730A3` (700), `#4F46E5` (600), `#6366F1` (500), `#C7D2FE` (200)
- Magenta: `#86198F` (700), `#C026D3` (600), `#E879F9` (400), `#F5D0FE` (200)
- Gray: `#111827` (900), `#1F2937` (800), `#374151` (700), `#6B7280` (500), `#9CA3AF` (400), `#D1D5DB` (300), `#E5E7EB` (200), `#F3F4F6` (100), `#FFFFFF` (0)

Recommended text and surfaces:

- Text on light: `#111827` on `#FFFFFF` (≈ 15:1)
- Primary on light: `#3730A3` link/buttons on `#FFFFFF` (≥ 7:1 with white text on `#3730A3`)
- Accent on light: `#86198F` link/buttons on `#FFFFFF` (≥ 6:1 with white text on `#86198F`)
- Surfaces: use Gray 50–200 for cards and panels, with borders Gray 200–300.

---

## CVD Profiles and Adjustments

All variants use the same tokens but tweak hue/lightness to preserve separability between Indigo and Magenta.

### 1) Protan (red‑weak) and Deutan (green‑weak)

- Risk: Magenta shifts toward blue/purple and can collapse into Indigo.
- Strategy: Darken Indigo and warm/brighten Magenta to pink‑magenta to maximize lightness separation; keep neutrals unchanged.
- Tokens (key examples):
  - Indigo base: `#2E2AA1` (darker, more blue‑violet)
  - Magenta base: `#D62A8A` (redder, higher lightness)
  - Emphasis: use border/underline and shape differences for Indigo vs Magenta actions.

### 2) Tritan (blue‑weak)

- Risk: Blues lose chroma; Indigo can appear grayish; blue‑yellow confusion.
- Strategy: Shift Indigo slightly toward violet and increase chroma; keep Magenta slightly redder for larger hue distance.
- Tokens (key examples):
  - Indigo base: `#5B33BF` (violet‑leaning)
  - Magenta base: `#C81A78` (red‑magenta)
  - Increase thickness/underline for Indigo links; use filled shapes for Magenta accents.

### 3) Monochromacy (achromatopsia)

- Risk: Hue is unavailable; only lightness matters.
- Strategy: Use grayscale only for meaning plus patterns, textures, icon shapes, and direct labels.
- Tokens (key examples):
  - Indigo base: `#1E293B` (slate‑like)
  - Magenta base: `#6B7280` (neutral midgray)
  - Rely on: line styles, markers, hatch fills, icons, text labels, and position.

Each variant’s full token set is provided in `tokens/color-tokens.css` and `tokens/color-tokens.json` under attribute selectors like `[data-cvd="protan"]`.

---

## UI Patterns

- Links: Use underline by default. Hover adds underline thickness or offset, not just color.
- Buttons: Solid (filled) for primary/critical, outline for secondary. Always include a shape/icon cue for destructive and success states.
- States: Hover adds subtle elevation or outline; focus uses high‑contrast outline `2–3px` with offset; selected uses a check/icon and weight change; disabled reduces opacity and removes shadows.
- Forms: Always pair color with text (e.g., “Error: …”), icon, and helper text. Red/green alone is not sufficient.
- Toggles and chips: Include icons (✓, !), shape changes, and labels. Use patterns for status (e.g., hatch background for “paused”).
- Content links vs buttons: Links keep underline; buttons never use underline to avoid confusion.

Component examples (light mode):

- Primary button: background `indigo-600`, text `white`, focus ring `indigo-300`, disabled `gray-300`.
- Secondary button: border `indigo-600`, text `indigo-700`, hover background `indigo-50`.
- Destructive: background `gray-900`, text `white`, icon `!` or trash; avoid red‑only reliance.
- Success: background `gray-900`, check icon and label “Success” to avoid green‑only.

Dark mode mirrors the same logic with higher lightness contrast and outlines.

---

## Data Visualization

General rules:

- Never encode with color alone. Add: marker shapes (● ■ ▲ ◆), line styles (solid, dash, dot‑dash), area hatch patterns, and direct labels.
- Keep categories ≤ 6 using brand colors; beyond that, use a known CVD‑safe extension or rely more on non‑color encodings.
- Label lines/areas directly instead of legend‑only whenever possible.

Brand‑first categorical set (works broadly; verify per dataset):

- 1: Indigo 700 `#3730A3` (solid, ●)
- 2: Magenta 600 `#C026D3` (dash, ▲)
- 3: Indigo 500 `#6366F1` (dot, ■)
- 4: Gray 700 `#374151` (dash‑dot, ◆)
- 5: Indigo 300 `#A5B4FC` (long‑dash, ▲)
- 6: Magenta 400 `#E879F9` (solid‑thick, ■)

For many categories, prefer a standard CVD‑safe set for the additional series and keep brand colors for emphasis series.

Patterns (CSS/Canvas/SVG):

- Lines: vary width and dash arrays (e.g., `4 2`, `2 2`, `6 2 2 2`).
- Areas/bars: apply cross‑hatch, dot, diagonal hatch; add value labels.
- Markers: circle, square, triangle, diamond, cross, plus.

---

## Content, Docs, and Reports

- Always annotate critical values directly (e.g., on bars/lines) and summarize trends in plain language.
- Provide alternative text and captions; describe what color encodes.
- Ensure table row highlights use both background and a left border or icon.
- PDFs: test with grayscale print and CVD simulation; ensure 1‑color reproduction remains legible.

---

## Testing and Verification

- Contrast: verify 4.5:1 for text, 3:1 for UI components and large text, 7:1 where feasible.
- Simulate CVD: test protan, deutan, tritan, and monochrome in design/dev tools or browser SVG color‑matrix filters.
- Keyboard focus: visible ring on all interactives; do not rely on color only.
- Snapshot tests for charts: include shape/pattern expectations (e.g., line dash, marker shapes), not just color.

---

## Implementation Cheatsheet

1) Use tokens from `tokens/color-tokens.css` via CSS variables.
2) Switch variants using a root attribute, e.g., `<html data-cvd="deutan">`.
3) For charts, apply both color and line/marker styles; see `examples/` configs.
4) Keep links underlined and add focus rings consistently.
5) TeX/pgfplots: include `tex/brandpalette.sty` and call `\brandsetup[variant=...]`; see `tex/example-pgfplots.tex`.
6) GNOME/GTK4: load `gtk4/brand_<variant>.css` via `Gtk.CssProvider`; see `docs/gnome-gtk4-guide.md` and `gtk4/demo.py`.
7) OKLCH: use `tokens/color-tokens-oklch.css` and `tokens/color-oklch-map.json` for perceptual tuning; see `docs/oklch-guide.md`.
8) Simulator: open `examples/simulator/index.html` to preview CVD filters; see `docs/simulator-guide.md`.
9) QA: run `python3 tools/contrast_check.py` and `python3 tools/separation_check.py`.
10) Contrast UI: open `examples/contrast/index.html`; see `docs/contrast-guide.md`.
11) Pandoc: use `templates/pandoc/brand.html`; see `docs/pandoc-guide.md`.
12) Sphinx: use `sphinx/brand_theme`; see `docs/sphinx-guide.md`.
13) Dev server: `python3 tools/devserver.py` with `<script src="/__livereload.js"></script>`; see `docs/devserver-guide.md`.
14) Makefile: `make serve`, `make oklch`, `make contrast-check`, `make separation-check`, `make pandoc-html`, `make sphinx-example-html`.
15) URL params: add `?variant=protan` to examples to set CVD; simulator supports `?simulate=protanopia`.

---

## Accessibility QA Checklist

- Text/controls meet contrast targets.
- Links always underlined; buttons never underlined.
- Error/success states have icons and text, not color only.
- Charts include shapes, patterns, and direct labels.
- Variants work for protan, deutan, tritan, and monochrome.

---

## Notes on Color Choice Rationale

- Indigo chosen for stability under red‑green deficiencies; darkened for separation from Magenta.
- Magenta chosen as accent that remains distinct by lightness and warmth; adjusted per CVD to avoid collapse into Indigo.
- Grays provide robust structure and ensure strong text contrast in light/dark contexts.
