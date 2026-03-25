# Experimental Mauve/Burgundy Guide

This guide documents the non-breaking experimental palette pack introduced in:

- `tokens/experimental-mauve-burgundy.json`
- `tokens/experimental-mauve-burgundy.css`
- `tokens/experimental-mauve-burgundy-oklch.css`

## Why this exists

The production palette is still indigo + magenta. The experimental pack explores
an equivalent family:

- indigo for stable structure,
- mauve for accent and annotation,
- burgundy for tertiary or "high gravity" emphasis.

The goal is to improve red-weak and green-weak separability without rewriting
the current CVD variant model.

## What is included

The experimental pack contains:

- a JSON source of truth with `default`, `protan`, `deutan`, `tritan`, and `mono`
- CSS variables for each authored variant
- OKLCH values for perceptual inspection
- a validation script: `python tools/experimental_palette_report.py`

## Adoption path

This pack is intentionally separate from `tokens/color-tokens.json`.

Recommended use:

1. Keep production examples and docs on the current tokens.
2. Use the experimental files in isolated prototypes, reports, or theme branches.
3. Compare authored contrast and pair separation with:

```bash
python tools/experimental_palette_report.py
```

4. Only merge into the main token source after validating:

- component contrast,
- chart distinguishability,
- grayscale/mono fallback,
- authored CVD variants,
- docs/example compatibility.

For a quick visual comparison, open:

```text
http://localhost:8000/examples/ui/palette-compare.html
```

## CSS usage

Swap the stylesheet:

```html
<link rel="stylesheet" href="../../tokens/experimental-mauve-burgundy.css">
```

The file keeps compatibility aliases for the existing `--magenta-*` variables by
mapping them to the mauve ramp. That lets existing examples render without
immediate HTML or JS changes.

## Notes

- `data-cvd` retains its original meaning. This pack does not reinterpret the
  deficiency selector as a general theme switch.
- `burgundy` is a new family. Existing production examples will not use it
  unless they explicitly opt in via `--brand-tertiary` or `--burgundy-*`.
- The pack is meant as a research lane, not as a silent production replacement.
