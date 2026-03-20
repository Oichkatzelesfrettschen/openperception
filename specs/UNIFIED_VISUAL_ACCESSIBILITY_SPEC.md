# Unified Visual Accessibility Specification (UVAS)

> **Implementation Status:** Partially implemented. GATE-002 (CONTRAST) and GATE-003 (CVD)
> validators exist in `tools/validators/`. Invariants INV-001 through INV-010 are
> specification only -- no automated enforcement code exists yet (targeted for v0.3.0+).

**Version:** 1.0.0
**Date:** 2025-12-27
**Repository:** OpenPerception (see repository root)
**Scope:** Cross-platform games, web, mobile, desktop, console UI/UX

---

## Table of Contents

1. [End State Definition](#1-end-state-definition)
2. [Cross-Domain Ontology](#2-cross-domain-ontology)
3. [Constraint Axes](#3-constraint-axes)
4. [Invariants vs Dials](#4-invariants-vs-dials)
5. [Evidence Matrix](#5-evidence-matrix)
6. [Design Token System](#6-design-token-system)
7. [Validator Framework](#7-validator-framework)
8. [Implementation Priority](#8-implementation-priority)

---

## 1. End State Definition

### Five Measurable Pillars

The goal is NOT "acceptable to everyone" (unmeasurable). Instead, we define explicit, testable criteria:

| Pillar | Definition | Measurable Target | Standard Reference |
|--------|------------|-------------------|-------------------|
| **Safety** | Content must not trigger seizures | 0 violations of flash/pattern thresholds | WCAG 2.3.1, ITU-R BT.1702-3 |
| **Perceptibility** | Critical info is detectable | Contrast >= 4.5:1 (text), >= 3:1 (UI) | WCAG 1.4.3, 1.4.11 |
| **Discriminability** | Categories/states are distinguishable | CVD simulation delta-E > 10 | Brettel/Machado simulation |
| **Comprehensibility** | Meaning inferrable without excessive WM | <= 7 concurrent attention items | Miller's Law, COGA |
| **Controllability** | Users can tune without breaking gameplay | All dials have min 3 settings | Xbox XAG 102 |

### Safety: Hard Constraint (MANDATORY)

```
INVARIANT: seizure_safe = TRUE
- Flash rate: <= 3 per second
- Flash area: < 25% of 10-degree visual field (341x256 px @ 1024x768)
- Red flash: R < 80% OR (R - G - B) < 80%
- Pattern: < 5 light-dark pairs oscillating
```

### Perceptibility: Floor + Dial

```
INVARIANT: contrast_floor = 4.5:1 (text), 3:1 (UI components)
DIAL: contrast_theme = {default, high_contrast, low_glare}
  - default: 4.5:1 - 12:1
  - high_contrast: 7:1 - 21:1
  - low_glare: 4.5:1 - 7:1 (for photophobia)
```

### Discriminability: Semantic Encoding

```
INVARIANT: meaning != color_only
- Every semantic role has: color + shape/pattern + label backup
- CVD simulation must pass discriminability test
```

### Comprehensibility: Cognitive Load Bounds

```
INVARIANT: concurrent_items <= 7 (navigation menus)
DIAL: density_mode = {default, minimal, detailed}
- Progressive disclosure: essential first, details on demand
```

### Controllability: User Agency

```
INVARIANT: every_dial_accessible = TRUE
DIAL: motion_intensity = {full, reduced, none}
DIAL: text_scale = {100%, 125%, 150%, 200%}
DIAL: color_profile = {default, protan_safe, deutan_safe, high_contrast}
```

---

## 2. Cross-Domain Ontology

### A. Human Functional Limits (What Changes in the Channel)

| Limit | Description | Affected Population | Primary Axis |
|-------|-------------|---------------------|--------------|
| **Chromatic Discrimination** | L/M/S cone loss or shift | 8% males, 0.5% females | Chromatic |
| **Luminance Contrast Sensitivity** | Min detectable contrast | 30.6% use high contrast | Luminance |
| **Visual Acuity** | High spatial frequency loss | 2.2B people globally | Spatial |
| **Visual Field** | Central/peripheral loss | 80M glaucoma, 200M AMD | Spatial |
| **Oculomotor Stability** | Nystagmus, fixation instability | 1 in 1,000 | Temporal |
| **Stereo Fusion** | Stereoblindness | 5-10% population | Depth |
| **Temporal Sensitivity** | Flicker/flash risk, motion | 1 in 4,000 PSE | Temporal |
| **Attention Control** | Distractibility, task switching | 2-8% ADHD | Cognitive |
| **Working Memory** | Capacity limits | 19% cognitive disability | Cognitive |

### B. UI/Game Meaning Primitives (What Must Be Conveyed)

| Primitive | Description | Example Uses |
|-----------|-------------|--------------|
| **Priority/Urgency** | Importance level | Alerts, notifications, health bars |
| **State** | Current condition | Selected, disabled, active, error |
| **Selection/Focus** | What's currently targeted | Cursor, highlight, focus ring |
| **Affordance** | What can be interacted with | Buttons, links, interactive elements |
| **Hazard** | Danger indication | Damage zones, warnings, enemies |
| **Feedback** | Response to action | Success, failure, progress |
| **Progress** | Completion status | Loading bars, timers, countdowns |
| **Identity/Team** | Who/what something belongs to | Player colors, faction markers |
| **Depth/Occlusion** | Spatial layering | 3D positioning, UI layers |
| **Navigation** | Wayfinding cues | Menus, breadcrumbs, maps |
| **Timing Windows** | When action is valid | QTE indicators, cooldowns |

### C. Rendering Degrees of Freedom (What You Can Vary)

| Category | Parameters | Range/Units |
|----------|------------|-------------|
| **Luminance** | Lightness, brightness | L* 0-100 (CIELAB) |
| **Chroma** | Saturation, colorfulness | C* 0-150+ (OKLCH) |
| **Hue** | Color identity | h 0-360 degrees |
| **Spatial: Size** | Element dimensions | px, rem, % |
| **Spatial: Spacing** | Margins, padding, gaps | px, rem, em |
| **Spatial: Stroke** | Line thickness, borders | px, rem |
| **Spatial: Blur** | Focus, depth of field | px radius |
| **Temporal: Frequency** | Animation speed | Hz, ms |
| **Temporal: Amplitude** | Movement magnitude | px, %, deg |
| **Temporal: Easing** | Acceleration curve | cubic-bezier |
| **Temporal: Persistence** | How long visible | ms, s |
| **Depth: Parallax** | Relative motion | ratio |
| **Depth: Occlusion** | Z-ordering | z-index |
| **Depth: Perspective** | Vanishing point | fov degrees |
| **Depth: Outlines** | Edge definition | px, contrast |
| **Density** | Info per screen | items/viewport |
| **Grouping** | Visual clustering | Gestalt principles |

---

## 3. Constraint Axes

### Six Unified Axes

Every research domain maps to one or more axes. Every feature must pass through its axis gatekeeping.

| Axis | Domains Affected | Typical Failure Mode | Integration Point |
|------|------------------|----------------------|-------------------|
| **Chromatic** | CVD, some low vision | Teams/items indistinguishable | Semantic color roles + non-color redundancy |
| **Luminance** | Low vision, contrast sensitivity, photophobia | Text/UI unreadable or painful | Contrast budgets + theme dials + outlines |
| **Spatial** | Low acuity, field loss, dyslexia/crowding | Too small, too dense, too similar | Scaling + spacing rules + HUD layout modes |
| **Temporal** | PSE, motion sensitivity, attention capture | Flicker, strobe, aggressive motion | Flash invariants + reduced-motion + governor |
| **Depth** | Stereoblindness, some low vision | Gameplay requires stereo | Monocular cues (occlusion, size, outlines) |
| **Cognitive** | ADHD, autism variability, cognitive load | Overload, distraction, unclear priorities | Priority grammar + progressive disclosure |

### Axis Constraint Table

```
CHROMATIC_AXIS:
  floor: "non-color redundancy for all semantic roles"
  dial: "color_profile" {default, protan_safe, deutan_safe, tritan_safe}
  validator: CVD_simulation_discriminability_test

LUMINANCE_AXIS:
  floor: "4.5:1 text, 3:1 UI components"
  dial: "contrast_theme" {default, high_contrast, low_glare}
  validator: WCAG_contrast_check, APCA_Lc_check

SPATIAL_AXIS:
  floor: "44px touch targets, 16px min text, 1.5x line height"
  dial: "text_scale" {100%, 125%, 150%, 200%}
  dial: "density_mode" {default, minimal, spacious}
  validator: WCAG_resize_test, crowding_check

TEMPORAL_AXIS:
  floor: "0 seizure triggers"
  dial: "motion_intensity" {full, reduced, none}
  validator: PEAT_flash_check, EA_IRIS

DEPTH_AXIS:
  floor: "stereo not required for essential info"
  dial: "depth_cues" {all, monocular_only}
  validator: monocular_cue_audit

COGNITIVE_AXIS:
  floor: "7 max concurrent nav items, progressive disclosure"
  dial: "hud_complexity" {full, simple, minimal}
  validator: attention_item_counter, reading_level_check
```

---

## 4. Invariants vs Dials

### Invariants (Non-Negotiable - Cannot Be Violated)

| ID | Invariant | Threshold | Source |
|----|-----------|-----------|--------|
| INV-001 | No seizure-provocative flashing | <= 3 flashes/second | WCAG 2.3.1 |
| INV-002 | No red flashes above saturation threshold | R < 80% OR (R-G-B) < 80% | ISO 9241-391 |
| INV-003 | Flash area limit | < 25% of 10-degree FOV | WCAG 2.3.1 |
| INV-004 | Pattern oscillation limit | < 5 light-dark pairs | ITU-R BT.1702-3 |
| INV-005 | Text contrast floor | >= 4.5:1 (normal), >= 3:1 (large) | WCAG 1.4.3 |
| INV-006 | UI component contrast floor | >= 3:1 | WCAG 1.4.11 |
| INV-007 | Non-color semantic encoding | Every role has shape/pattern/label | WCAG 1.4.1 |
| INV-008 | Touch target minimum | >= 44x44 CSS px | WCAG 2.5.5 |
| INV-009 | Stereo independence | Essential info has monocular cues | XAG, research |
| INV-010 | Cognitive function auth bypass | No memory/puzzle required for login | WCAG 3.3.8 |

### Dials (User-Tunable, Bounded)

| ID | Dial | Options | Default | Bounds |
|----|------|---------|---------|--------|
| DIAL-001 | contrast_theme | default, high_contrast, low_glare | default | Floor = 4.5:1 |
| DIAL-002 | text_scale | 100%, 125%, 150%, 200% | 100% | Min = 100% |
| DIAL-003 | motion_intensity | full, reduced, none | full | respects prefers-reduced-motion |
| DIAL-004 | color_profile | default, protan_safe, deutan_safe, tritan_safe | default | CVD validated |
| DIAL-005 | hud_complexity | full, simple, minimal | full | Essential info always visible |
| DIAL-006 | text_spacing | normal, wide, extra_wide | normal | Min = WCAG 1.4.12 |
| DIAL-007 | audio_description | off, on | off | - |
| DIAL-008 | captions | off, on, custom_style | off | - |
| DIAL-009 | screen_shake | full, reduced, off | full | - |
| DIAL-010 | notification_intensity | all, important, critical | all | - |

---

## 5. Evidence Matrix

### Matrix Structure

Each claim from research is extracted into standardized format:

```yaml
claim:
  id: "CLM-XXXX"
  statement: "One sentence, testable if possible"
  applies_to:
    channel: [chromatic|luminance|temporal|spatial|depth|cognitive]
    axis: [chromatic|luminance|spatial|temporal|depth|cognitive]
  ui_primitive: [focus|hazard|state|priority|feedback|progress|identity|depth|navigation|timing]
  constraint_type: [hard_safety|soft_comfort|performance_tradeoff]
  threshold:
    value: "quantitative value if available"
    unit: "unit of measurement"
  evidence_weight: [standard|guideline|clinical|controlled_study|observational|model]
  source:
    citation: "Author et al. (Year)"
    doi: "DOI or URL"
  notes: "Context, screen size, distance, HDR/SDR considerations"
```

### Sample Evidence Entries

```yaml
# SEIZURE SAFETY
- id: CLM-0001
  statement: "Flash frequency above 3Hz triggers seizures in susceptible individuals"
  applies_to:
    channel: temporal
    axis: temporal
  ui_primitive: [hazard, feedback]
  constraint_type: hard_safety
  threshold:
    value: 3
    unit: "flashes/second"
  evidence_weight: standard
  source:
    citation: "WCAG 2.3.1"
    doi: "https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold"
  notes: "Danger zone 15-25Hz, risk range 3-60Hz"

- id: CLM-0002
  statement: "Red flashes are more dangerous than other colors due to L-cone isolation"
  applies_to:
    channel: [chromatic, temporal]
    axis: temporal
  ui_primitive: [hazard, feedback]
  constraint_type: hard_safety
  threshold:
    value: "R>=80% AND (R-G-B)>=80%"
    unit: "8-bit color percentage"
  evidence_weight: standard
  source:
    citation: "ISO 9241-391:2016"
    doi: "https://www.iso.org/standard/56350.html"
  notes: "Pokemon incident 1997 involved pure red that excited red cones alone"

- id: CLM-0003
  statement: "Flash area exceeding 25% of 10-degree visual field increases seizure risk"
  applies_to:
    channel: [spatial, temporal]
    axis: temporal
  ui_primitive: [hazard, feedback]
  constraint_type: hard_safety
  threshold:
    value: 25
    unit: "% of 10-degree FOV (341x256px @ 1024x768)"
  evidence_weight: standard
  source:
    citation: "WCAG 2.3.1"
    doi: "https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold"

# CONTRAST
- id: CLM-0010
  statement: "4.5:1 contrast compensates for vision loss equivalent to 20/40 acuity"
  applies_to:
    channel: luminance
    axis: luminance
  ui_primitive: [state, focus, navigation]
  constraint_type: soft_comfort
  threshold:
    value: 4.5
    unit: "contrast ratio"
  evidence_weight: standard
  source:
    citation: "WCAG Understanding Contrast Minimum"
    doi: "https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html"

- id: CLM-0011
  statement: "7:1 contrast compensates for vision loss equivalent to 20/80 acuity"
  applies_to:
    channel: luminance
    axis: luminance
  ui_primitive: [state, focus, navigation]
  constraint_type: soft_comfort
  threshold:
    value: 7
    unit: "contrast ratio"
  evidence_weight: standard
  source:
    citation: "WCAG Understanding Contrast Enhanced"

- id: CLM-0012
  statement: "High contrast (21:1 black-on-white) causes discomfort for photophobia and some migraines"
  applies_to:
    channel: luminance
    axis: luminance
  ui_primitive: [state, focus]
  constraint_type: soft_comfort
  threshold:
    value: "<21:1 for comfort modes"
    unit: "contrast ratio"
  evidence_weight: observational
  source:
    citation: "Neurodiversity Design System"
    doi: "https://neurodiversity.design/principles/colour/"
  notes: "Conflict with low vision needs - requires dial, not single value"

# CVD SIMULATION
- id: CLM-0020
  statement: "Brettel 1997 half-plane projection is gold standard for dichromat simulation"
  applies_to:
    channel: chromatic
    axis: chromatic
  constraint_type: performance_tradeoff
  evidence_weight: model
  source:
    citation: "Brettel, Vienot, Mollon (1997)"
    doi: "JOSA-A"
  notes: "Uses 475nm/575nm for protan/deutan, 485nm/660nm for tritan"

- id: CLM-0021
  statement: "CVD simulation requires gamma linearization before LMS conversion"
  applies_to:
    channel: chromatic
    axis: chromatic
  constraint_type: hard_safety
  evidence_weight: model
  source:
    citation: "DaltonLens documentation"
    doi: "https://daltonlens.org"
  notes: "Missing gamma causes incorrect simulation - colors appear too dark"

# COGNITIVE LOAD
- id: CLM-0030
  statement: "Working memory holds 7 plus/minus 2 items simultaneously"
  applies_to:
    channel: cognitive
    axis: cognitive
  ui_primitive: [navigation, priority]
  constraint_type: soft_comfort
  threshold:
    value: "5-9"
    unit: "items"
  evidence_weight: controlled_study
  source:
    citation: "Miller (1956)"
  notes: "Navigation menus should limit to 5-9 options"

- id: CLM-0031
  statement: "Age-specific UI design reduced cognitive load by 42% per NASA-TLX"
  applies_to:
    channel: cognitive
    axis: cognitive
  constraint_type: performance_tradeoff
  threshold:
    value: 42
    unit: "% reduction"
  evidence_weight: controlled_study
  source:
    citation: "2024 Cognitive Architecture Research"
    doi: "https://jicrcr.com/index.php/jicrcr/article/download/3359/2862/7217"

# NEURODIVERGENCE
- id: CLM-0040
  statement: "15-20% of global population is neurodivergent"
  applies_to:
    channel: cognitive
    axis: cognitive
  evidence_weight: observational
  source:
    citation: "Neurodivergence Research Report 2024"

- id: CLM-0041
  statement: "Progressive disclosure reduces cognitive load for ADHD users"
  applies_to:
    channel: cognitive
    axis: cognitive
  ui_primitive: [navigation, progress]
  constraint_type: soft_comfort
  evidence_weight: controlled_study
  source:
    citation: "Weyerhauser & Piccolo, INTERACT 2025"
    doi: "https://link.springer.com/chapter/10.1007/978-3-032-05008-3_59"

# STEREOBLINDNESS
- id: CLM-0050
  statement: "5-10% of population has some degree of stereoblindness"
  applies_to:
    channel: depth
    axis: depth
  evidence_weight: clinical
  source:
    citation: "Stereoblindness Research Report"

- id: CLM-0051
  statement: "Monocular depth cues (occlusion, size, perspective) sufficient for most tasks"
  applies_to:
    channel: depth
    axis: depth
  ui_primitive: [depth, navigation]
  constraint_type: soft_comfort
  evidence_weight: controlled_study
  source:
    citation: "Szafir AR Depth Cue Research"
```

---

## 6. Design Token System

### Token Architecture

```
tokens/
  semantic/
    color-roles.json      # danger, ally, focus, disabled, etc.
    spacing-scale.json    # base units, multipliers
    timing-scale.json     # animation durations
  profiles/
    default.json          # standard theme
    protan-safe.json      # CVD-validated palette
    deutan-safe.json
    tritan-safe.json
    high-contrast.json    # 7:1+ ratios
    low-glare.json        # 4.5:1-7:1, reduced brightness
    reduced-motion.json   # minimal animation
    minimal-hud.json      # simplified interface
```

### Semantic Color Roles

```json
{
  "color-role": {
    "danger": {
      "description": "Hazards, damage, critical errors",
      "hue-range": "0-30 (warm)",
      "backup-pattern": "diagonal-stripes",
      "backup-icon": "exclamation-triangle",
      "cvd-validation": {
        "protan-deutan-delta-e": ">15 from ally",
        "tritan-delta-e": ">10 from ally"
      }
    },
    "ally": {
      "description": "Friendly, safe, success",
      "hue-range": "120-180 (cool)",
      "backup-pattern": "solid",
      "backup-icon": "checkmark",
      "cvd-validation": {
        "protan-deutan-delta-e": ">15 from danger",
        "tritan-delta-e": ">10 from danger"
      }
    },
    "focus": {
      "description": "Current selection, interactive element",
      "hue-range": "200-280 (blue-violet)",
      "backup-pattern": "outline-double",
      "backup-icon": null,
      "min-contrast": "3:1 against adjacent"
    },
    "disabled": {
      "description": "Unavailable, inactive",
      "chroma": "<10 (desaturated)",
      "backup-pattern": "dashed-outline",
      "min-contrast": "3:1"
    },
    "warning": {
      "description": "Caution, attention needed",
      "hue-range": "30-60 (yellow-orange)",
      "backup-pattern": "chevron-stripes",
      "backup-icon": "warning"
    },
    "info": {
      "description": "Neutral information",
      "hue-range": "180-220 (cyan-blue)",
      "backup-pattern": "dotted-outline",
      "backup-icon": "info-circle"
    }
  }
}
```

### Contrast Validation

```json
{
  "contrast-requirements": {
    "text-normal": {
      "min-ratio": 4.5,
      "apca-lc-min": 75
    },
    "text-large": {
      "min-ratio": 3.0,
      "apca-lc-min": 60,
      "size-threshold": "18pt or 14pt bold"
    },
    "ui-component": {
      "min-ratio": 3.0,
      "apca-lc-min": 45
    },
    "focus-indicator": {
      "min-ratio": 3.0,
      "min-thickness": "2px"
    }
  }
}
```

---

## 7. Validator Framework

### Automated Checks

```yaml
validators:
  # TEMPORAL AXIS - SEIZURE SAFETY
  flash-checker:
    tool: [PEAT, EA-IRIS, Apple-VideoFlashingReduction]
    checks:
      - flash_rate_per_second <= 3
      - red_flash_saturation < 0.8
      - flash_area_percent < 25
      - pattern_oscillations < 5
    severity: BLOCKING
    run_on: [video, animation, shader, particle-system]

  # LUMINANCE AXIS - CONTRAST
  contrast-checker:
    tool: [WCAG-contrast, APCA-calculator]
    checks:
      - text_normal_ratio >= 4.5
      - text_large_ratio >= 3.0
      - ui_component_ratio >= 3.0
    severity: BLOCKING
    run_on: [stylesheet, theme-definition]

  # CHROMATIC AXIS - CVD
  cvd-discriminability:
    tool: [Brettel-simulator, Machado-simulator]
    checks:
      - protan_delta_e_between_semantic_pairs > 10
      - deutan_delta_e_between_semantic_pairs > 10
      - tritan_delta_e_between_semantic_pairs > 8
    severity: WARNING
    run_on: [palette-definition, ui-mockup]

  # SPATIAL AXIS
  touch-target-checker:
    checks:
      - interactive_element_size >= 44px
      - spacing_between_targets >= 8px
    severity: WARNING
    run_on: [layout-definition, component-library]

  text-spacing-checker:
    checks:
      - line_height >= 1.5
      - paragraph_spacing >= 2.0
      - letter_spacing >= 0.12
      - word_spacing >= 0.16
    severity: WARNING
    run_on: [typography-definition]

  # DEPTH AXIS
  monocular-cue-audit:
    checks:
      - essential_depth_info_has_occlusion_cue
      - essential_depth_info_has_size_cue
      - essential_depth_info_has_outline_cue
    severity: WARNING
    run_on: [3d-scene, gameplay-mechanic]

  # COGNITIVE AXIS
  navigation-complexity:
    checks:
      - menu_items <= 9
      - nesting_depth <= 3
      - progressive_disclosure_available
    severity: WARNING
    run_on: [navigation-structure, menu-definition]

  reading-level:
    checks:
      - flesch_kincaid_grade <= 9
      - sentences_per_paragraph <= 5
    severity: INFO
    run_on: [ui-text, tutorial-content]
```

### CI/CD Integration

```yaml
# .github/workflows/accessibility-check.yml
name: Accessibility Validation

on: [push, pull_request]

jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Flash Safety Check
        run: |
          # Run EA IRIS on video assets
          for video in assets/videos/*.mp4; do
            iris-cli check "$video" --threshold strict
          done

      - name: Contrast Validation
        run: |
          # Check theme files against WCAG
          node scripts/contrast-check.js themes/*.json

      - name: CVD Simulation Test
        run: |
          # Validate color palettes under CVD simulation
          python scripts/cvd-validate.py palettes/*.json

      - name: Touch Target Audit
        run: |
          # Check component sizes
          node scripts/touch-target-audit.js components/**/*.tsx
```

---

## 8. Implementation Priority

### Phase Order (Prevents Rework)

```
PHASE 1: SEIZURE SAFETY INVARIANTS (Hardest to retrofit)
├── Implement flash governor
├── Implement animation frequency limiter
├── Add flash linter to asset pipeline
└── Add pattern analyzer for textures

PHASE 2: CONTRAST + SCALING SYSTEM (Everything depends on this)
├── Define contrast token system
├── Implement theme switching infrastructure
├── Build adaptive outline system
└── Create background plate components

PHASE 3: SEMANTIC COLOR ROLES + REDUNDANCY (CVD + low vision + cognitive)
├── Define semantic palette with roles
├── Add non-color redundancy to all roles
├── Validate palettes under CVD simulation
└── Create CVD-safe profile variants

PHASE 4: MOTION/TEMPORAL GOVERNOR (Comfort + safety)
├── Implement prefers-reduced-motion
├── Add animation intensity dial
├── Create motion governor middleware
└── Validate all animations < threshold

PHASE 5: DEPTH CUE SUFFICIENCY (Stereo independence)
├── Audit all 3D mechanics for stereo dependency
├── Add monocular cue fallbacks
├── Create outline enhancement system
└── Test with stereo disabled

PHASE 6: COGNITIVE LOAD MODES (Density, predictability, focus)
├── Implement HUD complexity dial
├── Add progressive disclosure patterns
├── Create notification intensity system
└── Build focus protection mode
```

---

## Appendix A: Standards Cross-Reference

| Standard | Scope | Key Requirements |
|----------|-------|------------------|
| WCAG 2.2 | Web | Contrast, timing, cognitive, input |
| WCAG 3.0 (Draft) | Web | APCA contrast, outcomes-based |
| ISO 9241-391 | Displays | Seizure safety, red flash |
| ITU-R BT.1702-3 | Broadcast | Flash limits, HDR |
| Xbox XAGs | Gaming | Configurability, profiles |
| Apple HIG | iOS/macOS | Accessibility, Dynamic Type |
| Material Design | Android | Touch targets, contrast |

## Appendix B: Tool Links

| Tool | Purpose | URL |
|------|---------|-----|
| PEAT | Flash/pattern analysis | https://trace.umd.edu/peat/ |
| EA IRIS | Game flash detection | https://github.com/electronicarts |
| Apple VideoFlashingReduction | Video analysis | https://github.com/apple/VideoFlashingReduction |
| DaltonLens | CVD simulation | https://daltonlens.org |
| APCA Calculator | Perceptual contrast | https://www.myndex.com/APCA/ |
| WebAIM Contrast Checker | WCAG contrast | https://webaim.org/resources/contrastchecker/ |

---

*Specification Version 1.0.0 - Generated 2025-12-27*
*Based on 7 markdown compendiums, 400+ cataloged papers (PDFs not distributed due to copyright)*
