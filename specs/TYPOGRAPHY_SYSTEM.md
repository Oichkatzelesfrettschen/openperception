# Typography System Specification

**Version:** 1.0.0
**Purpose:** Define measurable typography requirements as invariants and dials within the UVAS framework

---

## 1. Derived Axis: Legibility

The **Legibility axis** is derived from Spatial + Cognitive + Luminance. It governs all typography-related constraints.

```
LEGIBILITY AXIS COMPOSITION
===========================

Spatial ──────┬──> x-height ratio
              ├──> character spacing
              ├──> line height
              └──> column width

Cognitive ────┬──> disambiguation clarity (I l 1, 0 O)
              ├──> reading rhythm stability
              └──> hierarchy scanability

Luminance ────┬──> stroke contrast
              ├──> weight rendering
              └──> anti-aliasing behavior
```

---

## 2. Font Contract

A font is "UVAS-approved" if it satisfies all contract properties. This allows font substitution without breaking accessibility guarantees.

### 2.1 Static Metrics

| Property | Requirement | Rationale |
|----------|-------------|-----------|
| x-height ratio | >= 0.50 | Readability at small sizes |
| Cap-height ratio | 0.68-0.75 | Proportional hierarchy |
| Disambiguation score | Pass | `I l 1`, `0 O`, `rn m` must be visually distinct |
| Weight range | 400-700 minimum | Regular and bold available |
| Width consistency | < 5% shift across weights | Prevents reflow on weight change |
| Hinting quality | Pass at 12-16px | Crisp rendering at body sizes |

### 2.2 Disambiguation Test Characters

```
REQUIRED DISAMBIGUATION PAIRS
=============================

Set A (must be distinct):
  I (capital i) vs l (lowercase L) vs 1 (digit one)

Set B (must be distinct):
  0 (zero) vs O (capital o) vs o (lowercase o)

Set C (must be distinct):
  rn (r-n ligature area) vs m

Set D (punctuation):
  ' (apostrophe) vs ' (right single quote) vs ` (backtick)
  - (hyphen) vs – (en-dash) vs — (em-dash)

TESTING METHOD:
  Display "Il1 0Oo rnm" at 12px, 14px, 16px
  All pairs must be distinguishable by naive observers
```

### 2.3 Rendering Behavior

| Property | Requirement | Test Method |
|----------|-------------|-------------|
| Scale stability | Legible at 120%, 150%, 200% zoom | Visual inspection at scale factors |
| Contrast theme compatibility | No collapse in high-contrast or low-glare modes | Test against white/black, cream/dark-gray |
| Fractional scaling | No blurring at 125%, 175% | Test on Windows/Linux fractional DPI |
| Subpixel rendering | Graceful degradation without subpixel | Disable ClearType/FreeType subpixel |

### 2.4 Cognitive Properties

| Property | Requirement | Rationale |
|----------|-------------|-----------|
| Rhythm stability | Even letter spacing, no optical gaps | Prevents "shimmer" during reading |
| Italic distinctiveness | Clearly different from roman | Semantic clarity for emphasis |
| Weight progression | Linear perceived weight steps | Consistent hierarchy signaling |

---

## 3. Font Decision Matrix

### 3.1 Use-Case Categories

```
FONT CATEGORIES
===============

UI_SANS:
  Purpose: Interface labels, buttons, menus, short text
  Requirements:
    - High legibility at 12-16px
    - Strong disambiguation
    - Weights: 400, 500, 600, 700
    - Compact but not cramped

READING_SANS:
  Purpose: Long-form body text in sans-serif contexts
  Requirements:
    - Comfortable at 16-20px
    - Open counters, generous x-height
    - Good rhythm for continuous reading
    - Weights: 400, 700

READING_SERIF:
  Purpose: Long-form body text, academic/literary contexts
  Requirements:
    - Optimized for 16-24px
    - Clear serifs that don't blur at low DPI
    - Strong italic distinction
    - Weights: 400, 700

MONO:
  Purpose: Code, data, tabular content
  Requirements:
    - Fixed-width with clear disambiguation
    - Distinct 0/O, I/l/1
    - Ligatures optional but must not obscure meaning
    - Weights: 400, 700
```

### 3.2 Recommended Fonts by Category

| Category | Primary | Alternates | Fallback Stack |
|----------|---------|------------|----------------|
| UI_SANS | Inter | Source Sans 3, Noto Sans, IBM Plex Sans | system-ui, -apple-system, sans-serif |
| READING_SANS | Atkinson Hyperlegible | Lexend, OpenDyslexic (accessibility), Source Sans 3 | system-ui, sans-serif |
| READING_SERIF | Literata | Source Serif 4, Noto Serif | Georgia, serif |
| MONO | JetBrains Mono | Fira Code, Source Code Pro, IBM Plex Mono | ui-monospace, monospace |

### 3.3 Accessibility-First Alternates

| Need | Recommended Font | Rationale |
|------|------------------|-----------|
| Dyslexia | Atkinson Hyperlegible, Lexend | Optimized disambiguation, open letterforms |
| Low vision | APHont, Atkinson Hyperlegible | Designed for visual impairment |
| Cognitive load | Lexend | Variable familiarity axis reduces cognitive effort |

---

## 4. Typography Invariants

Hard floors that cannot be violated.

### INV-T01: Minimum Body Text Size

```yaml
id: INV-T01
name: minimum_body_text_size
rule: "font_size >= 16px at 1x scale"
threshold: 16
unit: "CSS px"
source: "WCAG 1.4.4, low vision research"
applies_to: "Body text, paragraphs, primary content"
rationale: "Below 16px, readability degrades significantly for users with mild vision impairment"
```

### INV-T02: Minimum Line Height

```yaml
id: INV-T02
name: minimum_line_height
rule: "line_height >= 1.5 * font_size"
threshold: 1.5
unit: "multiplier"
source: "WCAG 1.4.12"
applies_to: "Body text, paragraphs"
rationale: "Adequate line spacing prevents line-skipping and reduces cognitive load"
```

### INV-T03: Minimum Paragraph Spacing

```yaml
id: INV-T03
name: minimum_paragraph_spacing
rule: "paragraph_margin >= 1.5 * font_size"
threshold: 1.5
unit: "multiplier"
source: "WCAG 1.4.12"
applies_to: "Paragraph elements"
rationale: "Visual separation between paragraphs aids comprehension and scanning"
```

### INV-T04: Minimum Letter Spacing

```yaml
id: INV-T04
name: minimum_letter_spacing
rule: "letter_spacing >= 0"
threshold: 0
unit: "em"
source: "Typography best practices"
applies_to: "All text"
rationale: "Negative tracking impairs readability, especially at small sizes"
note: "For small text (<14px), minimum 0.01em recommended"
```

### INV-T05: Maximum Line Length

```yaml
id: INV-T05
name: maximum_line_length
rule: "line_length <= 80ch"
threshold: 80
unit: "characters"
source: "Readability research (optimal 45-75ch)"
applies_to: "Body text, paragraphs"
rationale: "Lines exceeding 80 characters cause eye-tracking fatigue"
```

### INV-T06: All-Caps Restriction

```yaml
id: INV-T06
name: all_caps_restriction
rule: "all_caps_text_length <= 50 characters"
threshold: 50
unit: "characters"
source: "Readability research"
applies_to: "Text styled in uppercase"
rationale: "Extended all-caps impairs word-shape recognition"
exception: "Acronyms, labels under 50 characters with increased letter-spacing"
required_mitigation: "If all-caps > 10 chars, letter-spacing >= 0.05em"
```

### INV-T07: Font Contract Compliance

```yaml
id: INV-T07
name: font_contract_compliance
rule: "all_fonts_pass_disambiguation_test"
threshold: "pass"
unit: "boolean"
applies_to: "All fonts in the design system"
rationale: "Fonts failing disambiguation cause character confusion errors"
test: "Display 'Il1 0Oo rnm' at body size; all pairs distinct"
```

---

## 5. Typography Dials

User/author-tunable settings with bounded ranges.

### DIAL-T01: Text Scale

```yaml
id: DIAL-T01
name: text_scale
description: "Global text size multiplier"
range:
  min: 1.0
  default: 1.0
  max: 2.0
step: 0.125
unit: "multiplier"
affected_tokens:
  - "type.size.body"
  - "type.size.heading.*"
  - "type.size.caption"
interaction: "Multiplies all text size tokens by this factor"
```

### DIAL-T02: Line Spacing

```yaml
id: DIAL-T02
name: line_spacing
description: "Line height preference"
options:
  compact:
    value: 1.4
    description: "Denser text for experienced readers"
  comfortable:
    value: 1.5
    description: "Default balanced spacing"
  spacious:
    value: 1.8
    description: "Extra spacing for readability needs"
default: "comfortable"
floor: 1.4
ceiling: 2.0
```

### DIAL-T03: Letter Spacing

```yaml
id: DIAL-T03
name: letter_spacing
description: "Character spacing adjustment"
options:
  default:
    value: 0
    description: "Font's designed spacing"
  relaxed:
    value: 0.02
    description: "Slightly open for dyslexia support"
  spacious:
    value: 0.05
    description: "Maximum spacing for accessibility"
default: "default"
floor: 0
ceiling: 0.1
unit: "em"
```

### DIAL-T04: Word Spacing

```yaml
id: DIAL-T04
name: word_spacing
description: "Space between words"
options:
  default:
    value: 0
    description: "Font's designed spacing"
  increased:
    value: 0.05
    description: "Slight increase for clarity"
  maximum:
    value: 0.16
    description: "Maximum for reading difficulties"
default: "default"
floor: 0
ceiling: 0.2
unit: "em"
source: "WCAG 1.4.12 allows up to 0.16em user override"
```

### DIAL-T05: Reading Mode

```yaml
id: DIAL-T05
name: reading_mode
description: "Optimized layout for long-form reading"
options:
  off:
    description: "Standard UI layout"
    changes: []
  on:
    description: "Reading-optimized layout"
    changes:
      - "Increase body text to 18-20px"
      - "Reduce line length to 65ch max"
      - "Increase line height to 1.6"
      - "Increase paragraph spacing to 2em"
      - "Hide non-essential UI chrome"
      - "Widen content margins"
default: "off"
```

### DIAL-T06: Dyslexia-Friendly Mode

```yaml
id: DIAL-T06
name: dyslexia_friendly
description: "Typography adjustments for dyslexia"
options:
  off:
    description: "Standard typography"
  on:
    description: "Dyslexia-optimized settings"
    changes:
      - "Switch to Atkinson Hyperlegible or Lexend"
      - "Increase letter-spacing to 0.05em"
      - "Increase word-spacing to 0.12em"
      - "Increase line-height to 1.8"
      - "Left-align text (no justification)"
      - "Disable hyphenation"
      - "Use heavier font weight (500 instead of 400)"
default: "off"
source: "British Dyslexia Association guidelines"
```

---

## 6. Typography Scale

Modular scale for consistent hierarchy.

```
TYPOGRAPHY SCALE (base: 16px, ratio: 1.25 Major Third)
======================================================

Token                 Size    Line-Height   Weight   Use Case
--------------------------------------------------------------
type.size.xs          12px    1.4           400      Captions, metadata
type.size.sm          14px    1.5           400      Secondary text, labels
type.size.base        16px    1.5           400      Body text (invariant floor)
type.size.md          20px    1.4           400      Lead paragraphs
type.size.lg          25px    1.3           500      Heading 3
type.size.xl          31px    1.2           600      Heading 2
type.size.2xl         39px    1.1           700      Heading 1
type.size.3xl         49px    1.1           700      Display, hero
type.size.4xl         61px    1.05          700      Display large

SCALE BEHAVIOR UNDER DIAL-T01 (text_scale):
- All sizes multiply by dial value
- Line-height ratios preserved
- Minimum 16px floor still applies after scaling
```

---

## 7. Axis Mapping

How typography connects to the 6 primary constraint axes:

| Typography Property | Primary Axis | Secondary Axis | Constraint Type |
|---------------------|--------------|----------------|-----------------|
| Font size | Spatial | Cognitive | Invariant floor |
| Line height | Spatial | Cognitive | Invariant floor |
| Letter spacing | Spatial | Cognitive | Bounded dial |
| Line length | Cognitive | Spatial | Invariant ceiling |
| Weight contrast | Luminance | Cognitive | Invariant floor |
| Color contrast | Luminance | - | Invariant floor (from UVAS core) |
| Font disambiguation | Cognitive | - | Invariant (pass/fail) |
| Reading mode | Cognitive | Spatial | Dial |

---

## 8. Validator Integration

### TYPOGRAPHY_GATE (WARNING)

```yaml
typography_gate:
  id: GATE-007
  severity: WARNING
  checks:
    - name: body_text_size
      rule: "font_size >= 16px"
      threshold: 16
      unit: "px"

    - name: line_height_ratio
      rule: "line_height >= 1.5 * font_size"
      threshold: 1.5

    - name: line_length
      rule: "max_width <= 80ch"
      threshold: 80
      unit: "ch"

    - name: paragraph_spacing
      rule: "margin_bottom >= 1.5 * font_size"
      threshold: 1.5

    - name: all_caps_length
      rule: "uppercase_text_length <= 50"
      threshold: 50
      unit: "characters"

    - name: font_disambiguation
      rule: "font_passes_confusion_test"
      test_string: "Il1 0Oo rnm"

  warning_message: |
    TYPOGRAPHY WARNING
    Element: {element}
    Issue: {check_name}
    Measured: {measured_value}
    Threshold: {threshold}

    RECOMMENDATION: {recommendation}
```

---

## 9. Platform Considerations

### Web (CSS)

```css
/* Typography invariants as CSS custom properties */
:root {
  --type-size-floor: 16px;
  --type-line-height-floor: 1.5;
  --type-line-length-ceiling: 80ch;
  --type-letter-spacing-floor: 0;
}

/* Dial implementation */
:root[data-text-scale="1.25"] {
  --type-scale: 1.25;
}

body {
  font-size: calc(var(--type-size-floor) * var(--type-scale, 1));
  line-height: var(--type-line-height-floor);
  max-width: var(--type-line-length-ceiling);
}
```

### Game Engines (Unity/Unreal)

- Implement text scale as global multiplier in UI system
- Ensure TextMeshPro/UMG fonts pass disambiguation test
- Provide in-game typography settings menu
- Test at 4K, 1080p, and 720p resolutions

### Native Applications

- Respect OS text size preferences (iOS Dynamic Type, Android font scale)
- Ensure minimum sizes even when OS scale is reduced
- Test with screen readers for font fallback behavior

---

*Typography System Version 1.0.0 - Generated 2025-12-27*
