# OKLCH Color Token Guide

This guide explains the OKLCH color space and how OpenPerception generates perceptually
uniform color tokens from hex source values.

---

## WHY

Traditional HSL hue rotation produces colors with very different perceived lightness
(yellow appears much brighter than blue at the same L value in HSL). OKLCH fixes this
with a perceptually uniform lightness axis, making systematic palette design predictable.

---

## OKLCH Channels

| Channel | Range | Meaning |
|---------|-------|---------|
| L | 0.0 - 1.0 | Perceptual lightness (0=black, 1=white) |
| C | 0.0 - ~0.37 | Chroma (colorfulness; 0=gray) |
| H | 0 - 360 | Hue angle in degrees |

---

## Generated Artifacts

- `tokens/color-oklch-map.json` -- hex to `[L, C, H]` mapping for all tokens
- `tokens/color-tokens-oklch.css` -- CSS custom properties with OKLCH values per role and CVD variant

---

## Using in CSS

```css
/* Variables exported as: --oklch-brand-primary: L C H */
.button {
  color: oklch(var(--oklch-brand-primary) / 1);
}
```

For maximum compatibility, keep sRGB hex as the authoritative source in
`tokens/color-tokens.json` and use OKLCH for design validation and future support.

---

## Regenerate Tokens

```bash
# Regenerate after editing tokens/color-tokens.json
make oklch

# Then validate
make contrast-check
make separation-check
```

---

## CVD Variants

Five stylesheets are generated for CVD accommodation. Switch variants via the
`data-cvd` attribute on `<html>` or `<body>`:

| Attribute | Variant |
|-----------|---------|
| (none) | Normal vision |
| `data-cvd="protan"` | Protanopia/protanomaly |
| `data-cvd="deutan"` | Deuteranopia/deuteranomaly |
| `data-cvd="tritan"` | Tritanopia/tritanomaly |
| `data-cvd="achromat"` | Achromatopsia |

---

## References

- Ottosson, B. (2020). A perceptual color space for image processing.
  https://bottosson.github.io/posts/oklab/
- CSS Color 4 specification: https://www.w3.org/TR/css-color-4/#ok-lab

