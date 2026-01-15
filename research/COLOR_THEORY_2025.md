# Color Theory Research Summary (2024-2025)

**Compiled:** 2025-12-27
**Purpose:** Synthesis of modern color theory research for UVAS+ accessibility specifications
**Focus Areas:** Perceptually uniform color spaces, CVD-safe palettes, indigo+gray base combinations

---

## 1. Executive Summary

Modern color theory has evolved significantly with the adoption of perceptually uniform color spaces (Oklab, OKLCH, HSLuv) that provide more predictable accessibility outcomes than traditional RGB/HSL. For UVAS+, the key findings are:

1. **Perceptual uniformity** enables predictable contrast calculations
2. **OKLCH** is becoming the CSS standard for accessible color work
3. **Indigo + neutral gray** provides a strong accessibility foundation when paired correctly
4. **CVD-safe palettes** require blue-orange/blue-yellow axes, not red-green

---

## 2. Perceptually Uniform Color Spaces

### 2.1 The Problem with Traditional Spaces

Traditional color spaces (sRGB, HSL, HSV) have significant perceptual non-uniformity:

| Issue | Example | Impact |
|-------|---------|--------|
| Inconsistent lightness | Yellow appears brighter than blue at same L value | Contrast predictions fail |
| Hue shifts | Adjusting saturation shifts perceived hue | Color harmony breaks |
| Non-linear brightness | Equal RGB steps produce unequal brightness steps | Gradient banding |

### 2.2 Modern Solutions

#### Oklab (2020)

**Source:** [A perceptual color space for image processing](https://bottosson.github.io/posts/oklab/)

Oklab uses three coordinates:
- **L** (lightness): 0 to 1, perceptually uniform
- **a** (green-red axis): opponent color dimension
- **b** (blue-yellow axis): opponent color dimension

**Performance vs. CIELAB:**
| Metric | Oklab | CIELAB |
|--------|-------|--------|
| Lightness RMS error | 0.20 | 1.70 |
| Chroma RMS error | 0.81 | 1.84 |

**Adoption (2025):**
- CSS Color Level 4/5 specification
- Adobe Photoshop (gradient interpolation)
- Chrome, Safari, Firefox support for `oklch()`
- Unity, Godot game engines

#### OKLCH (Cylindrical Oklab)

**Source:** [OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)

OKLCH expresses Oklab in cylindrical coordinates:
- **L** (lightness): 0% to 100%
- **C** (chroma): 0 to ~0.4
- **H** (hue): 0 to 360 degrees

**CSS Syntax:**
```css
.button {
  background-color: oklch(70% 0.15 250);  /* L C H */
}
```

**Accessibility Benefits:**
- Predictable contrast from L values (correlation, not exact)
- No hue shift when adjusting lightness
- Better a11y with predictable lightness
- Generate entire design systems with predicted contrast

#### HSLuv

**Source:** [InclusiveColors](https://www.inclusivecolors.com/)

HSLuv stretches CIELUV LCh chroma so every color has the same range (0-100%):
- Preserves lightness and hue from CIELUV
- Percentage-based chroma (easier to reason about)
- Used by InclusiveColors tool for palette generation

**Trade-off:** Scaling by maximum chroma affects interior of color space unevenly.

### 2.3 Lightness vs. Contrast

**Critical Insight:** Perceptual lightness does NOT equal contrast.

> "When people first hear about perceptually uniform color spaces like Lab, LCH or their improved versions, OkLab and OKLCH, they imagine that they can infer the contrast between two colors by simply comparing their L(ightness) values. This is unfortunately not true, as contrast depends on more factors than perceptual lightness."

**Source:** [Lea Verou on contrast-color](https://lea.verou.me/blog/2024/contrast-color/)

Contrast depends on:
- Lightness difference (primary factor)
- Chroma (saturation) levels
- Background luminance (dark mode vs. light mode)
- Spatial frequency (text size)

---

## 3. CVD-Safe Color Design

### 3.1 Prevalence Statistics

| Type | Affected | Description |
|------|----------|-------------|
| Deuteranomaly | ~6% of males | Reduced green sensitivity |
| Protanomaly | ~2% of males | Reduced red sensitivity |
| Tritanomaly | 0.01% | Reduced blue sensitivity |
| **Total CVD** | **~8% of males, 0.5% of females** | Any form |

**Source:** [Color Blind Awareness](https://www.colourblindawareness.org/)

### 3.2 Colors to Avoid Together

**Source:** [Colorblind Association - Inclusive Design](https://colorblind.org/index.php/2024/08/26/creating-inclusive-design-top-10-ways-graphic-designers-can-accommodate-colorblindness/)

| Problematic Pair | CVD Type Affected | Alternative |
|------------------|-------------------|-------------|
| Red + Green | Deuteranopia, Protanopia | Blue + Orange |
| Green + Brown | Deuteranomaly | Blue + Yellow |
| Blue + Purple | Tritanopia | Blue + Orange |
| Green + Blue | Deuteranomaly | Yellow + Purple |

### 3.3 CVD-Safe Strategies

1. **Use luminance variation:** Different brightness levels distinguish colors even without hue perception
2. **Add patterns/textures:** Stripes, dots, hatching alongside color
3. **Include text labels:** Never rely on color alone
4. **Use icons/shapes:** Supplement color with form
5. **Test with simulators:** Color Oracle, Coblis, Adobe CVD proofing

### 3.4 Safe Color Axes

**CVD-Safe Primary Axis:** Blue-Orange (perceived by all CVD types)
**CVD-Safe Secondary Axis:** Blue-Yellow (maintained in most CVD)
**High-Risk Axis:** Red-Green (confused by ~8% of males)

---

## 4. Indigo + Gray Base Palette

### 4.1 Rationale

Indigo combined with neutral gray provides:
- **Professional appearance** without stark black/white
- **CVD-safe base** (blue family unaffected by red-green CVD)
- **Flexible accent compatibility** (coral, teal, yellow all work)
- **Dark mode friendly** (indigo darkens smoothly)

### 4.2 Recommended Palette Structure

Based on [Tailwind CSS](https://tailwindcss.com/docs/colors) and [Open Color](https://yeun.github.io/open-color/) patterns:

**Gray Shades (10 levels):**
```
gray-50:  oklch(98% 0 0)      // Near white
gray-100: oklch(96% 0 0)
gray-200: oklch(90% 0 0)
gray-300: oklch(82% 0 0)
gray-400: oklch(70% 0 0)
gray-500: oklch(55% 0 0)      // Mid gray
gray-600: oklch(45% 0 0)
gray-700: oklch(35% 0 0)
gray-800: oklch(25% 0 0)
gray-900: oklch(15% 0 0)      // Near black
gray-950: oklch(10% 0 0)
```

**Indigo Shades (10 levels):**
```
indigo-50:  oklch(97% 0.02 270)   // Very light indigo
indigo-100: oklch(94% 0.04 270)
indigo-200: oklch(88% 0.08 270)
indigo-300: oklch(78% 0.12 270)
indigo-400: oklch(65% 0.18 270)
indigo-500: oklch(55% 0.22 270)  // Primary indigo
indigo-600: oklch(48% 0.22 270)
indigo-700: oklch(40% 0.20 270)
indigo-800: oklch(32% 0.16 270)
indigo-900: oklch(24% 0.12 270)  // Deep indigo
indigo-950: oklch(18% 0.08 270)
```

### 4.3 Contrast Pairs

**Light Mode (white background):**
| Foreground | Background | Contrast | Use |
|------------|------------|----------|-----|
| gray-900 | white | ~15:1 | Primary text |
| gray-700 | white | ~7:1 | Secondary text |
| indigo-600 | white | ~5:1 | Links/accents |
| indigo-700 | white | ~7:1 | AAA text |

**Dark Mode (gray-900 background):**
| Foreground | Background | Contrast | Use |
|------------|------------|----------|-----|
| gray-100 | gray-900 | ~12:1 | Primary text |
| gray-300 | gray-900 | ~8:1 | Secondary text |
| indigo-300 | gray-900 | ~6:1 | Links/accents |
| indigo-200 | gray-900 | ~8:1 | AAA text |

### 4.4 Accent Colors (CVD-Safe)

To complement indigo+gray, use:

| Accent | Purpose | CVD Safety |
|--------|---------|------------|
| Orange (oklch 65% 0.20 45) | Warning, calls to action | Distinguishable by all CVD |
| Teal (oklch 65% 0.15 195) | Success, links | Blue-family safe |
| Yellow (oklch 85% 0.15 90) | Highlights | High luminance safe |
| Coral (oklch 70% 0.18 25) | Warm accents | Orange-family safe |

---

## 5. WCAG Contrast Requirements

### 5.1 WCAG 2.x (Current Standard)

| Level | Normal Text | Large Text | UI Components |
|-------|-------------|------------|---------------|
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | N/A |

**Large Text:** 18pt (24px) normal, or 14pt (19px) bold

### 5.2 APCA (WCAG 3.0 Candidate)

**Source:** [APCA Repository](https://github.com/Myndex/SAPC-APCA)

APCA uses perceptual contrast (Lc values):
- **Lc 60** minimum for body text
- **Lc 45** minimum for large headlines
- **Lc 30** minimum for non-text UI

**Key Differences:**
- Polarity matters: light-on-dark differs from dark-on-light
- Better for dark mode (WCAG 2.x has dark mode issues)
- Stricter overall than WCAG 2.x

### 5.3 "Magic Number" System

**Source:** [U.S. Web Design System](https://designsystem.digital.gov/design-tokens/color/overview/)

Contrast expressed as difference in lightness scale (0-100):
- **40+:** WCAG AA for large text
- **50+:** WCAG AA for normal text / AAA for large text
- **70+:** WCAG AAA for normal text

---

## 6. Tools and Resources

### 6.1 Color Palette Generators

| Tool | URL | Features |
|------|-----|----------|
| InclusiveColors | https://www.inclusivecolors.com/ | HSLuv-based, WCAG/APCA checking |
| Atmos | https://atmos.style/playground | LCH/OKLCH palette generator |
| oklch.com | https://oklch.com/ | OKLCH picker and converter |
| Leonardo | https://leonardocolor.io/ | Adobe contrast-based palette |

### 6.2 CVD Simulation

| Tool | Platform | License |
|------|----------|---------|
| Color Oracle | Windows/Mac/Linux | Free |
| DaltonLens | Library | MIT |
| Adobe Color | Web | Free |
| Coblis | Web | Free |

### 6.3 Contrast Checkers

| Tool | Standard | URL |
|------|----------|-----|
| WebAIM | WCAG 2.x | https://webaim.org/resources/contrastchecker/ |
| APCA Calculator | WCAG 3.0 | https://www.myndex.com/APCA/ |
| Siege Media | WCAG 2.x | https://www.siegemedia.com/contrast-ratio |

---

## 7. Regulatory Context

### 7.1 European Accessibility Act (EAA)

**Effective:** June 2025

Requires digital products/services to meet accessibility standards, including color accessibility for users with visual impairments.

### 7.2 Section 508 (US)

Requires WCAG 2.0 AA compliance for federal websites and technology.

### 7.3 AODA (Canada)

Requires WCAG 2.0 AA for public sector and large organizations in Ontario.

---

## 8. Recommendations for UVAS+

### 8.1 Color Space Selection

**Recommendation:** Use OKLCH as the canonical color representation.

Rationale:
- CSS-native (no conversion needed for web)
- Predictable lightness for contrast estimation
- No hue shift when adjusting L or C
- Industry adoption momentum

### 8.2 Palette Architecture

**Recommendation:** 10-shade scales with linked lightness.

Structure:
- 10 shades per color (50, 100, 200, ... 950)
- Consistent L values across colors at same shade level
- Minimum 3 neutral grays + 1 primary + 2-3 accents

### 8.3 Contrast Strategy

**Recommendation:** Design for APCA Lc 60+ for body text, validate against WCAG 2.x for compliance.

Dual-check approach:
1. Primary: APCA Lc values for perceptual accuracy
2. Secondary: WCAG 2.x ratios for legal compliance
3. Both must pass for approval

### 8.4 CVD Validation

**Recommendation:** Mandatory CVD simulation at all three severity levels.

Check matrix:
- Deuteranopia (red-green, severe)
- Protanopia (red-green, severe)
- Tritanopia (blue-yellow, severe)
- Anomalous trichromacy (all mild forms)

---

## 9. References

### Standards
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [CSS Color Level 4](https://www.w3.org/TR/css-color-4/)
- [APCA Specification](https://github.com/Myndex/SAPC-APCA)

### Research
- [Oklab: A perceptual color space](https://bottosson.github.io/posts/oklab/)
- [OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- [Contrast color in CSS](https://lea.verou.me/blog/2024/contrast-color/)
- [Color Theory and Accessibility 2025](https://618media.com/en/blog/color-theory-and-accessibility/)

### Tools
- [InclusiveColors](https://www.inclusivecolors.com/)
- [Atmos OKLCH Playground](https://atmos.style/playground)
- [Color Oracle](https://colororacle.org/)
- [DaltonLens](https://daltonlens.org/)

### Industry Resources
- [Tailwind CSS Colors](https://tailwindcss.com/docs/colors)
- [Open Color](https://yeun.github.io/open-color/)
- [Material Design Colors](https://m2.material.io/design/color/)
- [U.S. Web Design System](https://designsystem.digital.gov/design-tokens/color/overview/)

---

*COLOR_THEORY_2025.md - Compiled 2025-12-27*
