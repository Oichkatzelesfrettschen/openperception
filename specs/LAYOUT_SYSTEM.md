# Layout System Specification

> **Status:** SPECIFICATION ONLY -- not yet targeted for implementation

**Version:** 1.0.0
**Purpose:** Define measurable layout requirements as invariants and dials within the UVAS framework

---

## 1. Derived Axis: Structure

The **Structure axis** is derived from Cognitive + Spatial. It governs all layout-related constraints.

```
STRUCTURE AXIS COMPOSITION
==========================

Cognitive ────┬──> hierarchy clarity
              ├──> grouping (Gestalt proximity)
              ├──> progressive disclosure
              └──> navigation depth limits

Spatial ──────┬──> whitespace ratios
              ├──> density distribution
              ├──> alignment consistency
              └──> responsive breakpoints
```

---

## 2. The Reflow Contract

**Core Principle:** Scaling increases content size, but layout must **reflow** to accommodate without breaking functionality or readability.

### 2.1 Contract Requirements

When zoom or text scale increases (125%, 150%, 200%), the following must hold:

| Requirement | Description | Failure Mode |
|-------------|-------------|--------------|
| No truncation without affordance | Critical labels must not clip | Ellipsis with tooltip, or text wraps |
| No overlap | Interactive elements must not overlap | Buttons stack vertically, menus expand |
| Touch targets maintained | 44px minimum even at high zoom | Scale interactive areas proportionally |
| Reading order preserved | DOM/semantic order equals visual order | No reflow to out-of-order positions |
| Focus visibility maintained | Focus indicators remain visible | Outline not clipped by overflow:hidden |
| Scrollability maintained | Content remains scrollable in at least one axis | No dead-end layouts |

### 2.2 Reflow Breakpoints

```
REFLOW BEHAVIOR BY SCALE FACTOR
===============================

1.0x (default):
  - Standard layout
  - All content visible as designed

1.25x:
  - Trigger first reflow if needed
  - Sidebar may collapse to hamburger
  - Cards may reduce from 3-column to 2-column

1.5x:
  - Major reflow expected
  - Multi-column layouts become single-column
  - Navigation becomes vertical stack
  - Modals may become full-screen

2.0x:
  - Maximum reflow
  - Equivalent to mobile layout
  - All optional UI chrome hidden
  - Focus on essential content
```

### 2.3 Reflow Validation

```yaml
reflow_validation:
  test_scales: [1.0, 1.25, 1.5, 2.0]
  checks:
    - name: truncation_audit
      method: "Scan all text elements for overflow:hidden with text-overflow:ellipsis"
      pass_criteria: "All truncated elements have accessible full text (title/tooltip/expandable)"

    - name: overlap_audit
      method: "Check bounding box intersections of interactive elements"
      pass_criteria: "No overlapping clickable/focusable elements"

    - name: touch_target_audit
      method: "Measure smallest dimension of all interactive elements"
      pass_criteria: "min(width, height) >= 44px at each scale"

    - name: reading_order_audit
      method: "Compare DOM order to visual render order"
      pass_criteria: "Tab sequence matches visual top-to-bottom, left-to-right flow"

    - name: focus_visibility_audit
      method: "Tab through all focusable elements"
      pass_criteria: "Focus indicator visible for every element"
```

---

## 3. Spacing Token System

### 3.1 Spacing Scale

```
SPACING SCALE (base: 4px)
=========================

Token             Value    Use Case
-------------------------------------------------
space.0           0        No space
space.1           4px      Tightest grouping (icon-label)
space.2           8px      Compact grouping (form field padding)
space.3           12px     Default inline spacing
space.4           16px     Default block spacing (1rem)
space.5           24px     Section separation
space.6           32px     Major section breaks
space.7           48px     Large gaps, hero spacing
space.8           64px     Maximum spacing
space.9           96px     Page-level margins

SEMANTIC ALIASES:
  space.none      = space.0
  space.xs        = space.1
  space.sm        = space.2
  space.md        = space.4
  space.lg        = space.6
  space.xl        = space.8
```

### 3.2 Grid Tokens

```
GRID TOKENS
===========

Token                   Default    Description
-------------------------------------------------
grid.gutter             16px       Gap between grid columns
grid.margin             24px       Page edge margins
grid.column-count       12         Base column count
grid.max-width          1200px     Maximum content width

RESPONSIVE GRID:
  viewport >= 1200px: 12 columns, 24px gutter
  viewport >= 768px:  8 columns, 16px gutter
  viewport < 768px:   4 columns, 12px gutter
```

### 3.3 Interactive Element Spacing

```
INTERACTIVE SPACING
===================

Token                        Value     Rationale
-------------------------------------------------
touch.minTarget              44px      WCAG 2.5.5 minimum
touch.minSpacing             8px       Prevent mis-taps
focus.outlineWidth           2px       Visibility minimum
focus.outlineOffset          2px       Separation from element

CLUSTER SPACING:
  When interactive elements are grouped (e.g., button row):
  - Minimum gap between elements: 8px
  - Padding around cluster: 16px
  - Cluster should be visually bounded
```

### 3.4 Border Radius Scale

```
RADIUS SCALE
============

Token             Value    Use Case
-------------------------------------------------
radius.0          0        Sharp corners (tables, code blocks)
radius.1          2px      Subtle rounding (input fields)
radius.2          4px      Default rounding
radius.3          8px      Cards, panels
radius.4          16px     Prominently rounded (pills, tags)
radius.full       9999px   Fully circular

SEMANTIC ALIASES:
  radius.none     = radius.0
  radius.sm       = radius.1
  radius.md       = radius.2
  radius.lg       = radius.3
```

### 3.5 Stroke/Border Scale

```
STROKE SCALE
============

Token             Value    Use Case
-------------------------------------------------
stroke.0          0        No border
stroke.1          1px      Subtle dividers
stroke.2          2px      Default borders, focus rings
stroke.3          3px      Emphasized borders
stroke.4          4px      Heavy borders, active states

SEMANTIC ALIASES:
  stroke.none     = stroke.0
  stroke.thin     = stroke.1
  stroke.default  = stroke.2
  stroke.thick    = stroke.3
```

---

## 4. Layout Invariants

Hard floors that cannot be violated.

### INV-L01: Minimum Touch Target Size

```yaml
id: INV-L01
name: minimum_touch_target
rule: "min(width, height) >= 44px"
threshold: 44
unit: "CSS px"
source: "WCAG 2.5.5"
applies_to: "All interactive elements (buttons, links, form controls)"
rationale: "Smaller targets cause motor-impaired users to mis-tap"
```

### INV-L02: Minimum Touch Target Spacing

```yaml
id: INV-L02
name: minimum_touch_spacing
rule: "gap between adjacent interactive elements >= 8px"
threshold: 8
unit: "px"
source: "WCAG 2.5.8 (draft)"
applies_to: "Adjacent buttons, links, form controls"
rationale: "Prevents accidental activation of wrong target"
```

### INV-L03: Focus Indicator Visibility

```yaml
id: INV-L03
name: focus_indicator_visible
rule: "focus_indicator.area >= 2px * perimeter AND contrast >= 3:1"
threshold:
  width: 2
  contrast: 3.0
source: "WCAG 2.4.11, 2.4.12"
applies_to: "All focusable elements"
rationale: "Keyboard users must see current focus position"
```

### INV-L04: No Content Overlap

```yaml
id: INV-L04
name: no_content_overlap
rule: "bounding_boxes of adjacent elements do not intersect"
threshold: 0
unit: "px overlap"
applies_to: "All content at all zoom levels 1x-2x"
rationale: "Overlapping content is inaccessible"
```

### INV-L05: Scrollable Content Access

```yaml
id: INV-L05
name: scrollable_content
rule: "all content reachable via scroll OR layout reflow"
threshold: "100% content accessible"
applies_to: "All viewports and zoom levels"
rationale: "Hidden content with no scroll access is lost"
```

### INV-L06: Navigation Depth Limit

```yaml
id: INV-L06
name: navigation_depth
rule: "max_nesting_depth <= 4"
threshold: 4
unit: "levels"
source: "Cognitive load research"
applies_to: "Menu hierarchies, breadcrumb depth"
rationale: "Deeper nesting overwhelms working memory"
```

### INV-L07: Maximum Items Per Navigation Level

```yaml
id: INV-L07
name: nav_items_per_level
rule: "visible_items_per_nav_level <= 9"
threshold: 9
unit: "items"
source: "Miller's Law (7 +/- 2)"
applies_to: "Navigation menus, tab bars, toolbars"
rationale: "Exceeding working memory capacity causes errors"
```

---

## 5. Layout Dials

User/author-tunable settings with bounded ranges.

### DIAL-L01: Density Mode

```yaml
id: DIAL-L01
name: density_mode
description: "Overall layout density preference"
options:
  compact:
    description: "Maximum information density"
    spacing_multiplier: 0.75
    padding_reduction: "25%"
    use_case: "Power users, large screens, data-heavy views"
  comfortable:
    description: "Balanced default"
    spacing_multiplier: 1.0
    padding_reduction: "0%"
    use_case: "General use"
  spacious:
    description: "Maximum breathing room"
    spacing_multiplier: 1.5
    padding_increase: "50%"
    use_case: "Cognitive accessibility, touch-primary interfaces"
default: "comfortable"
```

### DIAL-L02: Progressive Disclosure Level

```yaml
id: DIAL-L02
name: progressive_disclosure
description: "How aggressively to hide secondary content"
options:
  none:
    description: "Show all content by default"
    hidden_by_default: []
  normal:
    description: "Hide advanced options"
    hidden_by_default: ["advanced_settings", "developer_options", "full_details"]
  aggressive:
    description: "Minimal initial view"
    hidden_by_default: ["secondary_info", "metadata", "advanced_settings", "full_details"]
default: "normal"
```

### DIAL-L03: Animation Layout Transitions

```yaml
id: DIAL-L03
name: layout_animation
description: "Whether layout changes animate"
options:
  on:
    description: "Smooth transitions between layout states"
    duration: "200-300ms"
  off:
    description: "Instant layout changes"
    duration: "0ms"
default: "on"
respects: "prefers-reduced-motion"
note: "If prefers-reduced-motion is set, this dial is forced to 'off'"
```

### DIAL-L04: Sidebar Behavior

```yaml
id: DIAL-L04
name: sidebar_behavior
description: "How sidebars behave at narrow viewports"
options:
  collapse:
    description: "Collapse to icon bar"
    reflow_trigger: "<1024px viewport"
  overlay:
    description: "Hide and show as overlay"
    reflow_trigger: "<768px viewport"
  push:
    description: "Push content when shown"
    reflow_trigger: "never hidden"
default: "collapse"
```

---

## 6. Density Mode Implementation

### 6.1 Spacing Multipliers

```
DENSITY MULTIPLIERS
===================

                    Compact   Comfortable   Spacious
--------------------------------------------------
space.xs (4px)      3px       4px           6px
space.sm (8px)      6px       8px           12px
space.md (16px)     12px      16px          24px
space.lg (32px)     24px      32px          48px
grid.gutter         12px      16px          24px
grid.margin         16px      24px          32px
```

### 6.2 Density CSS Variables

```css
:root {
  --density-multiplier: 1.0; /* comfortable */
}

:root[data-density="compact"] {
  --density-multiplier: 0.75;
}

:root[data-density="spacious"] {
  --density-multiplier: 1.5;
}

.card {
  padding: calc(var(--space-md) * var(--density-multiplier));
  gap: calc(var(--space-sm) * var(--density-multiplier));
}
```

---

## 7. Responsive Breakpoints

```
BREAKPOINT SYSTEM
=================

Token               Value      Description
-------------------------------------------------
breakpoint.xs       0          Mobile portrait (< 576px)
breakpoint.sm       576px      Mobile landscape
breakpoint.md       768px      Tablet portrait
breakpoint.lg       1024px     Tablet landscape / Small desktop
breakpoint.xl       1200px     Desktop
breakpoint.2xl      1400px     Large desktop

REFLOW TRIGGERS:
  xs-sm: Stack all columns, hide sidebars, full-width modals
  sm-md: 2-column layouts become 1-column
  md-lg: Sidebars collapse, secondary nav hides
  lg-xl: Full desktop layout
```

---

## 8. Accessibility Layout Patterns

### 8.1 Skip Links

```yaml
skip_links:
  requirement: "Every page must have skip link to main content"
  position: "First focusable element"
  visibility: "Visible on focus, hidden otherwise"
  destinations:
    - "#main-content"
    - "#navigation" (optional)
    - "#search" (optional)
```

### 8.2 Landmark Structure

```yaml
landmarks:
  required:
    - banner: "Site header (one per page)"
    - main: "Primary content (one per page)"
    - contentinfo: "Site footer (one per page)"
  optional:
    - navigation: "Major navigation (multiple allowed)"
    - complementary: "Sidebar, related content"
    - search: "Search functionality"
```

### 8.3 Heading Hierarchy

```yaml
heading_hierarchy:
  rule: "No skipped heading levels"
  valid_sequences:
    - [h1, h2, h3, h4]
    - [h1, h2, h2, h3]
  invalid_sequences:
    - [h1, h3]  # Skipped h2
    - [h2, h4]  # Skipped h3
  h1_per_page: 1
  rationale: "Screen reader users navigate by headings; gaps cause confusion"
```

---

## 9. Axis Mapping

How layout connects to the 6 primary constraint axes:

| Layout Property | Primary Axis | Secondary Axis | Constraint Type |
|-----------------|--------------|----------------|-----------------|
| Touch target size | Spatial | Cognitive | Invariant floor |
| Touch spacing | Spatial | - | Invariant floor |
| Density mode | Cognitive | Spatial | Bounded dial |
| Navigation depth | Cognitive | - | Invariant ceiling |
| Items per level | Cognitive | - | Invariant ceiling |
| Focus visibility | Luminance | Spatial | Invariant floor |
| Reflow behavior | Spatial | Cognitive | Contract |
| Progressive disclosure | Cognitive | - | Dial |

---

## 10. Validator Integration

### LAYOUT_GATE (WARNING)

```yaml
layout_gate:
  id: GATE-008
  severity: WARNING
  checks:
    - name: touch_target_size
      rule: "min(width, height) >= 44px"
      threshold: 44
      unit: "px"

    - name: touch_target_spacing
      rule: "gap >= 8px"
      threshold: 8
      unit: "px"

    - name: focus_indicator_presence
      rule: "every focusable element has visible focus style"
      threshold: "exists"

    - name: focus_indicator_contrast
      rule: "focus_outline.contrast_ratio >= 3.0"
      threshold: 3.0

    - name: nav_depth
      rule: "max_menu_depth <= 4"
      threshold: 4
      unit: "levels"

    - name: nav_items
      rule: "items_per_level <= 9"
      threshold: 9
      unit: "items"

    - name: heading_hierarchy
      rule: "no_skipped_heading_levels"
      threshold: "pass"

    - name: reflow_at_200_percent
      rule: "no_horizontal_scroll_at_320px_equivalent"
      source: "WCAG 1.4.10"

  warning_message: |
    LAYOUT WARNING
    Element: {element}
    Issue: {check_name}
    Measured: {measured_value}
    Threshold: {threshold}

    RECOMMENDATION: {recommendation}
```

### REFLOW_GATE (WARNING)

```yaml
reflow_gate:
  id: GATE-009
  severity: WARNING
  test_scales: [1.0, 1.25, 1.5, 2.0]
  checks:
    - name: no_horizontal_scroll
      rule: "viewport_width - content_width >= 0"
      applies_to: "All scales"

    - name: no_truncation_without_affordance
      rule: "truncated_text.has_accessible_full_text == true"

    - name: no_element_overlap
      rule: "interactive_element_intersections == 0"

    - name: touch_targets_maintained
      rule: "min_target_size >= 44px at all scales"

    - name: reading_order_preserved
      rule: "dom_order == visual_order"

  warning_message: |
    REFLOW WARNING at {scale}x
    Issue: {check_name}
    Details: {details}

    RECOMMENDATION: Implement responsive reflow for this content.
```

---

*Layout System Version 1.0.0 - Generated 2025-12-27*
