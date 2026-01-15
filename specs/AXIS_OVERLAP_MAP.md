# Axis Overlap and Seams Map

**Purpose:** Shows where research domains intersect and where design conflicts require resolution

---

## Domain-to-Axis Mapping

```
RESEARCH DOMAIN                    CONSTRAINT AXES
================                   ================

Color Vision Deficiency ─────────> CHROMATIC
  - Protanopia                      └── color discriminability
  - Deuteranopia                    └── semantic role encoding
  - Tritanopia                      └── palette validation
  - Achromatopsia ──────────────> LUMINANCE (depends on lightness only)
  - Blue Cone Monochromacy

Visual Impairments
  - Low Vision ─────────────────> LUMINANCE (contrast)
                                  └> SPATIAL (size, spacing)
  - Visual Field Loss ──────────> SPATIAL (layout, density)
  - Contrast Sensitivity ───────> LUMINANCE
  - Stereoblindness ────────────> DEPTH
  - Nystagmus ──────────────────> TEMPORAL (motion tolerance)
                                  └> SPATIAL (target size)

Neurodivergence
  - ADHD ───────────────────────> COGNITIVE (attention, distraction)
                                  └> TEMPORAL (animation, urgency)
  - Autism ─────────────────────> COGNITIVE (predictability, load)
                                  └> TEMPORAL (motion sensitivity)
                                  └> LUMINANCE (contrast preferences)
  - Dyslexia ───────────────────> SPATIAL (typography, spacing)
                                  └> COGNITIVE (processing)
  - Dyscalculia ────────────────> COGNITIVE (numerical processing)
                                  └> SPATIAL (number layout)

Seizures
  - Photosensitive Epilepsy ────> TEMPORAL (flash frequency)
                                  └> CHROMATIC (red flash)
                                  └> SPATIAL (flash area)
  - Pattern Sensitivity ────────> SPATIAL (pattern density)
                                  └> TEMPORAL (oscillation)

Cognitive Load
  - Working Memory ─────────────> COGNITIVE
  - Attention ──────────────────> COGNITIVE
                                  └> TEMPORAL (interruptions)
  - Processing Speed ───────────> TEMPORAL (timing)
                                  └> COGNITIVE (density)
```

---

## Axis Intersection Matrix

Shows which axis pairs have potential conflicts or synergies:

```
              CHROMATIC  LUMINANCE  SPATIAL  TEMPORAL  DEPTH  COGNITIVE
CHROMATIC        -          A          -        B        -        C
LUMINANCE        A          -          D        -        E        F
SPATIAL          -          D          -        G        H        I
TEMPORAL         B          -          G        -        -        J
DEPTH            -          E          H        -        -        K
COGNITIVE        C          F          I        J        K        -
```

### Key Intersections

#### A: Chromatic × Luminance
**Synergy:** CVD users rely more on luminance contrast when chroma is confusable
**Design Pattern:** Ensure lightness difference even when hues are similar
**Token Rule:** `danger.lightness != ally.lightness` (delta >= 20 L*)

#### B: Chromatic × Temporal
**Conflict:** Red flash is extra dangerous (seizure safety)
**Design Pattern:** Never use saturated red (R>=80%) in flashing content
**Invariant:** `INV-002: red_flash_saturation < 0.8`

#### C: Chromatic × Cognitive
**Synergy:** Color coding reduces cognitive load IF perceivable
**Design Pattern:** Color roles must have non-color backup for CVD users
**Token Rule:** Every semantic role has shape/pattern/label redundancy

#### D: Luminance × Spatial
**Synergy:** Higher contrast allows smaller text; larger text tolerates lower contrast
**Trade-off:** 4.5:1 at 16px ≈ 3:1 at 24px
**Token Rule:** `contrast_floor(font_size)` function

#### E: Luminance × Depth
**Synergy:** Depth perception aided by contrast gradients
**Design Pattern:** Use atmospheric perspective (reduced contrast for distant objects)
**Token Rule:** Near objects have higher contrast than far objects

#### F: Luminance × Cognitive
**Conflict:** High contrast helps low vision BUT causes fatigue for some neurodivergent users
**Resolution:** Bounded dial with floor (4.5:1) and ceiling (configurable)
**Token Rule:** `contrast_theme = {default, high_contrast, low_glare}`

#### G: Spatial × Temporal
**Synergy:** Smaller flash area = lower seizure risk
**Design Pattern:** Limit flash area to <25% of viewport
**Invariant:** `INV-003: flash_area < 25%`

#### H: Spatial × Depth
**Synergy:** Size is a monocular depth cue
**Design Pattern:** Relative size indicates distance without stereo
**Token Rule:** Depth semantics must include size gradient

#### I: Spatial × Cognitive
**Synergy:** Adequate spacing reduces cognitive load
**Design Pattern:** Whitespace groups related items (Gestalt)
**Token Rule:** `spacing.group > spacing.item`

#### J: Temporal × Cognitive
**Conflict:** Urgency animations grab attention BUT cause distraction for ADHD
**Resolution:** Notification intensity dial
**Token Rule:** `notification_intensity = {all, important, critical}`

#### K: Depth × Cognitive
**Synergy:** Depth layering creates visual hierarchy
**Design Pattern:** Important items "forward" in Z-order
**Token Rule:** `z-index(priority=high) > z-index(priority=low)`

---

## Conflict Resolution Table

| Conflict | Domains | Resolution Strategy |
|----------|---------|---------------------|
| High contrast vs photophobia | Low vision × Autism/Migraine | Bounded dial: floor=4.5:1, ceiling=configurable |
| Red danger cue vs seizure safety | CVD × PSE | Never flash red; use orange or non-color redundancy |
| Animation feedback vs motion sensitivity | UX × Vestibular | `prefers-reduced-motion` respected; <0.5s safe |
| Dense info vs cognitive load | Information density × ADHD | Progressive disclosure; density dial |
| Small touch targets vs screen space | Mobile UX × Motor | 44px minimum invariant; spacing dial |
| Stereo depth cues vs stereoblindness | 3D games × Depth | Monocular cues always available |
| Color-coded teams vs CVD | Multiplayer × CVD | Shape + pattern + label for every team |

---

## Seams Diagram (Where to Fix Once)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         UNIFIED PIPELINE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CONTENT          SEMANTIC           RENDERING        OUTPUT         │
│  CREATION         TOKENS             ENGINE           PROFILE        │
│                                                                      │
│  ┌─────────┐      ┌─────────┐       ┌─────────┐     ┌─────────┐    │
│  │ Design  │──────│ Color   │───────│ Theme   │─────│ Default │    │
│  │ Intent  │      │ Roles   │       │ Resolver│     │ Profile │    │
│  │         │      │         │       │         │     └─────────┘    │
│  │ "danger"│      │ danger: │       │ Apply   │     ┌─────────┐    │
│  │ "ally"  │      │ {color, │       │ profile │─────│ Protan  │    │
│  │ "focus" │      │  pattern│       │ variant │     │ Safe    │    │
│  └─────────┘      │  icon}  │       │         │     └─────────┘    │
│       │           └────┬────┘       │         │     ┌─────────┐    │
│       │                │            │ Validate│─────│ High    │    │
│       │           ┌────┴────┐       │ contrast│     │ Contrast│    │
│       │           │ Spacing │       │ CVD sim │     └─────────┘    │
│       │           │ Scale   │       │ flash   │     ┌─────────┐    │
│       │           │         │       │ check   │─────│ Reduced │    │
│       │           │ base=8px│       │         │     │ Motion  │    │
│       │           └────┬────┘       └────┬────┘     └─────────┘    │
│       │                │                 │                          │
│       │           ┌────┴────┐            │                          │
│       │           │ Timing  │            │                          │
│       │           │ Scale   │────────────┘                          │
│       │           │         │                                       │
│       │           │ <3Hz    │                                       │
│       │           │ flash   │                                       │
│       │           └─────────┘                                       │
│                                                                      │
│  GATES (validation checkpoints):                                    │
│  ├── SEIZURE_GATE: flash_rate, red_saturation, area                │
│  ├── CONTRAST_GATE: ratio >= floor for text/UI                     │
│  ├── CVD_GATE: delta-E between semantic pairs                      │
│  ├── SPATIAL_GATE: touch_target >= 44px                            │
│  └── COGNITIVE_GATE: nav_items <= 9                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Integration Points by Axis

### Chromatic Axis Integration Point
**Location:** Palette definition + theme resolver
**Gate:** CVD simulation discriminability test
**Fix Once:** Define semantic color roles with validated CVD-safe variants
**Never:** Use hex colors directly in components

### Luminance Axis Integration Point
**Location:** Theme resolver + contrast validator
**Gate:** WCAG contrast check + APCA Lc check
**Fix Once:** Define contrast budgets per content type
**Never:** Hard-code color pairs without validation

### Spatial Axis Integration Point
**Location:** Layout engine + spacing scale
**Gate:** Touch target checker + text spacing validator
**Fix Once:** Define spacing scale (4px, 8px, 16px, 24px, 32px, 48px)
**Never:** Use arbitrary pixel values

### Temporal Axis Integration Point
**Location:** Animation governor middleware
**Gate:** Flash checker (PEAT/IRIS) + motion validator
**Fix Once:** Define timing scale with max frequency cap
**Never:** Allow raw frequency parameters in content

### Depth Axis Integration Point
**Location:** 3D renderer + depth cue system
**Gate:** Monocular cue sufficiency audit
**Fix Once:** Require multiple depth cues for essential info
**Never:** Gate gameplay on stereo perception alone

### Cognitive Axis Integration Point
**Location:** Navigation structure + HUD complexity modes
**Gate:** Attention item counter + reading level check
**Fix Once:** Define HUD variants (full, simple, minimal)
**Never:** Exceed 7 concurrent navigation items at one level

---

## Profile Composition

Each output profile is a combination of axis settings:

```yaml
default:
  chromatic: default
  luminance: default (4.5:1 - 12:1)
  spatial: 100% scale
  temporal: full motion
  depth: all cues
  cognitive: full HUD

protan-safe:
  chromatic: protan-safe palette
  luminance: default
  spatial: 100% scale
  temporal: full motion
  depth: all cues
  cognitive: full HUD

high-contrast:
  chromatic: default
  luminance: high (7:1 - 21:1)
  spatial: 100% scale
  temporal: full motion
  depth: all cues
  cognitive: full HUD

low-glare:
  chromatic: desaturated
  luminance: low (4.5:1 - 7:1)
  spatial: 100% scale
  temporal: reduced motion
  depth: all cues
  cognitive: full HUD

reduced-cognitive:
  chromatic: default
  luminance: default
  spatial: 150% scale
  temporal: reduced motion
  depth: all cues
  cognitive: minimal HUD
```

---

*Map Version 1.0.0 - Generated 2025-12-27*
