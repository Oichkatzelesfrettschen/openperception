# OKLCH Palette Guide

This document explains how to use perceptually uniform OKLCH values for the brand palette and its CVD variants.

Artifacts generated:
- `tokens/color-oklch-map.json` — hex to `[L, C, h]`
- `tokens/color-tokens-oklch.css` — CSS variables per ramp/role and per CVD variant

Why OKLCH?
- More uniform lightness and chroma perception across hues than sRGB/HSV
- Easier to maintain contrast and separability under CVD by controlling `L` and `C`

How to use in CSS:
- The CSS file exports variables like `--oklch-indigo-600: L C h;` and `--oklch-brand-primary: L C h;`
- When supported, use `oklch()`:
  - `color: oklch(var(--oklch-brand-primary) / 1);`
- For today’s browsers, keep hex as source of truth and use OKLCH for design checks and future support.

How to regenerate:
- `python3 tools/gen_oklch_tokens.py`

