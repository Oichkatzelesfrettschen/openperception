# Scaling Mathematics

**Version:** 1.0.0
**Purpose:** Define the canonical unit system, scaling equations, and quantization rules for UVAS+

---

## 1. The Problem

Consistent perceived sizes across:
- Different DPI monitors (76, 96, 110, 144, 192+)
- User scaling preferences (50% to 400%)
- Platform differences (Windows DIPs, CSS pixels, Wayland fractional)
- Layout preservation (reflow, not clipping)

This is a **unit system + rounding discipline + reflow contract** problem, not ML.

---

## 2. Canonical Unit: Logical Pixel (lp)

### 2.1 Definition

A **logical pixel (lp)** is a device-independent unit anchored to a reference DPI.

```
1 lp = 1/96 inch (at reference density)
```

This matches:
- **Windows DIPs:** 1 DIP = 1/96 inch
- **CSS reference pixel:** Conceptually tied to 96 DPI
- **macOS points:** 1 pt = 1/72 inch (multiply by 0.75 for lp)

### 2.2 Reference Constants

```
DPI_ref = 96        // Canonical reference DPI
lp_per_inch = 96    // Logical pixels per inch at reference
```

### 2.3 Why 96 DPI?

- Historical Windows standard (Windows 3.1 onward)
- CSS default assumption
- Allows clean integer math for common scaling factors
- Industry-wide de facto standard for UI design

---

## 3. Effective Scale Equation

### 3.1 Core Formula

```
S_eff = (DPI_phys / DPI_ref) * S_user
```

Where:
- `DPI_phys` = Physical DPI of the display
- `DPI_ref` = 96 (canonical reference)
- `S_user` = User scaling factor (1.0 = 100%)
- `S_eff` = Effective scale to apply

### 3.2 Logical to Physical Conversion

```
x_px = x_lp * S_eff
```

Where:
- `x_lp` = Size in logical pixels
- `x_px` = Size in physical pixels

### 3.3 Examples

| DPI_phys | S_user | S_eff | 16 lp -> px |
|----------|--------|-------|-------------|
| 96       | 1.0    | 1.0   | 16 px       |
| 96       | 1.25   | 1.25  | 20 px       |
| 96       | 1.5    | 1.5   | 24 px       |
| 96       | 2.0    | 2.0   | 32 px       |
| 144      | 1.0    | 1.5   | 24 px       |
| 192      | 1.0    | 2.0   | 32 px       |
| 76       | 1.0    | 0.79  | 12.7 px     |
| 110      | 1.25   | 1.43  | 22.9 px     |

---

## 4. Modular Typography Scale

### 4.1 Geometric Progression

Font sizes follow a **modular scale** because human perception of size is multiplicative:

```
f_lp(k) = f_0 * r^k
```

Where:
- `f_0` = Base font size (16 lp for body text)
- `r` = Scale ratio (1.25 recommended, "Major Third")
- `k` = Step index (integer, can be negative)

### 4.2 UVAS+ Typography Scale

Using `f_0 = 16 lp` and `r = 1.25`:

| Step (k) | Name        | Size (lp) | Use Case                    |
|----------|-------------|-----------|------------------------------|
| -2       | micro       | 10.24     | Legal text, captions         |
| -1       | small       | 12.80     | Secondary text, labels       |
| 0        | body        | 16.00     | Body text (base)             |
| 1        | large       | 20.00     | Lead paragraphs, emphasis    |
| 2        | h4          | 25.00     | Heading level 4              |
| 3        | h3          | 31.25     | Heading level 3              |
| 4        | h2          | 39.06     | Heading level 2              |
| 5        | h1          | 48.83     | Heading level 1              |
| 6        | display     | 61.04     | Hero text, display type      |

### 4.3 Practical Rounding

For implementation, round to convenient values:

| Step | Calculated | Practical |
|------|------------|-----------|
| -2   | 10.24      | 10        |
| -1   | 12.80      | 13        |
| 0    | 16.00      | 16        |
| 1    | 20.00      | 20        |
| 2    | 25.00      | 25        |
| 3    | 31.25      | 31        |
| 4    | 39.06      | 39        |
| 5    | 48.83      | 49        |
| 6    | 61.04      | 61        |

### 4.4 Alternative Ratios

| Ratio | Name           | Character                    |
|-------|----------------|------------------------------|
| 1.125 | Major Second   | Tight, dense hierarchy       |
| 1.200 | Minor Third    | Balanced, common             |
| 1.250 | Major Third    | Clear hierarchy (UVAS+ default) |
| 1.333 | Perfect Fourth | Strong contrast              |
| 1.414 | Augmented Fourth | Mathematical (sqrt(2))    |
| 1.500 | Perfect Fifth  | Very strong hierarchy        |
| 1.618 | Golden Ratio   | Dramatic, display-focused    |

---

## 5. Quantization Rules

### 5.1 The Problem

Fractional pixels cause:
- **Blur:** Subpixel rendering artifacts
- **Jitter:** Movement by fractions of pixels
- **Inconsistency:** Different rounding at different positions

### 5.2 Context-Specific Quantizers

```python
def quantize(x_px: float, context: str) -> float:
    """Apply context-appropriate rounding."""
    if context == "text_size":
        return round(x_px * 4) / 4  # 0.25 px precision
    elif context == "text_position":
        return round(x_px * 2) / 2  # 0.5 px precision
    elif context == "stroke":
        return round(x_px)  # whole pixels
    elif context == "layout":
        return round(x_px)  # whole pixels
    elif context == "icon":
        return round(x_px)  # whole pixels
    else:
        return round(x_px)  # default: whole pixels
```

### 5.3 Quantization Table

| Context        | Precision | Rationale                               |
|----------------|-----------|------------------------------------------|
| Text size      | 0.25 px   | Font engines handle subpixel well        |
| Text position  | 0.5 px    | Subpixel positioning for kerning         |
| Line/stroke    | 1.0 px    | Crisp edges require whole pixels         |
| Layout metrics | 1.0 px    | Predictable box model                    |
| Icon glyphs    | 1.0 px    | Pixel-perfect alignment                  |
| Spacing        | 1.0 px    | Consistent rhythm                        |

### 5.4 High-DPI Refinement

At high DPI (>= 144), finer quantization is permissible:

| DPI Range   | Text Quantization | Stroke Quantization |
|-------------|-------------------|---------------------|
| < 96        | 0.5 px            | 1.0 px              |
| 96-143      | 0.25 px           | 1.0 px              |
| >= 144      | 0.125 px          | 0.5 px              |

---

## 6. Base-4 Grid Alignment

### 6.1 Why Base-4?

Common scaling factors land cleanly on base-4:

| Scale | 4 lp -> px | 8 lp -> px | 16 lp -> px |
|-------|------------|------------|-------------|
| 1.0   | 4          | 8          | 16          |
| 1.25  | 5          | 10         | 20          |
| 1.5   | 6          | 12         | 24          |
| 2.0   | 8          | 16         | 32          |

All results are whole numbers, avoiding fractional pixel issues.

### 6.2 Spacing Scale (Base-4)

```json
{
  "spacing": {
    "0": 0,
    "1": 4,
    "2": 8,
    "3": 12,
    "4": 16,
    "5": 20,
    "6": 24,
    "7": 28,
    "8": 32,
    "9": 36,
    "10": 40
  }
}
```

### 6.3 Touch Target Alignment

Minimum touch target (44 lp) is not base-4, but scales reasonably:

| Scale | 44 lp -> px | Rounded |
|-------|-------------|---------|
| 1.0   | 44          | 44      |
| 1.25  | 55          | 56      |
| 1.5   | 66          | 66      |
| 2.0   | 88          | 88      |

---

## 7. Complete Scaling Pipeline

### 7.1 Pipeline Stages

```
[Token lp]
    |
    v
[Apply S_eff: x_px = x_lp * S_eff]
    |
    v
[Quantize: x_px_final = Q(x_px, context)]
    |
    v
[Layout / Reflow]
    |
    v
[Render]
```

### 7.2 Implementation Example

```python
class ScalingPipeline:
    def __init__(self, dpi_phys: float, scale_user: float):
        self.dpi_ref = 96
        self.s_eff = (dpi_phys / self.dpi_ref) * scale_user

    def to_px(self, value_lp: float, context: str = "layout") -> float:
        """Convert logical pixels to physical pixels with quantization."""
        x_px = value_lp * self.s_eff
        return self._quantize(x_px, context)

    def _quantize(self, x_px: float, context: str) -> float:
        quantizers = {
            "text_size": 0.25,
            "text_position": 0.5,
            "stroke": 1.0,
            "layout": 1.0,
            "icon": 1.0,
        }
        precision = quantizers.get(context, 1.0)
        return round(x_px / precision) * precision

    def font_scale_step(self, k: int, base: float = 16, ratio: float = 1.25) -> float:
        """Get font size at scale step k."""
        size_lp = base * (ratio ** k)
        return self.to_px(size_lp, "text_size")


# Usage
pipeline = ScalingPipeline(dpi_phys=144, scale_user=1.25)

# Body text (16 lp at step 0)
body_px = pipeline.font_scale_step(0)  # 16 * 1.875 = 30 px

# Spacing token (spacing.4 = 16 lp)
spacing_px = pipeline.to_px(16, "layout")  # 16 * 1.875 = 30 px

# Touch target (44 lp)
touch_px = pipeline.to_px(44, "layout")  # 44 * 1.875 = 82.5 -> 83 px
```

---

## 8. Reflow Requirements

### 8.1 The Contract

When scale changes, content must **reflow**, not clip or overlap.

WCAG requires text resize to 200% without loss of content/functionality.

### 8.2 What Reflow Means

| Behavior      | Allowed | Description                      |
|---------------|---------|----------------------------------|
| Line wrap     | Yes     | Text wraps to fit container      |
| Column stack  | Yes     | Multi-column becomes single      |
| Menu collapse | Yes     | Nav becomes hamburger            |
| Scroll        | Yes     | Content scrolls vertically       |
| Truncation    | No      | Text cut off with ellipsis       |
| Overlap       | No      | Elements overlapping             |
| Horizontal scroll | No  | Content requires H-scroll        |

### 8.3 Reflow Test Scales

```yaml
reflow_test_matrix:
  scales: [1.0, 1.25, 1.5, 2.0, 4.0]
  validations:
    - no_horizontal_scroll
    - no_element_overlap
    - no_text_truncation
    - touch_targets_maintained
    - reading_order_preserved
    - focus_order_preserved
```

---

## 9. Platform-Specific Notes

### 9.1 Windows

- Uses DIPs (Device Independent Pixels)
- Common scaling plateaus: 100%, 125%, 150%, 175%, 200%
- Query via `GetDpiForWindow()` or WM_DPICHANGED

### 9.2 macOS

- Uses points (1 pt = 1/72 inch)
- Retina = 2x backing scale
- Query via `NSScreen.backingScaleFactor`

### 9.3 Web/CSS

- Reference pixel at 96 DPI
- `window.devicePixelRatio` gives effective scale
- Use `rem` units tied to root font size

### 9.4 Wayland

- Integer scaling is cleanest
- Fractional scaling involves oversample + downsample
- Query via `wl_output.scale` and fractional-scale-v1 protocol

### 9.5 Unity/Unreal

- Native DPI awareness varies
- Use canvas scalers with "Scale With Screen Size"
- Reference resolution pattern recommended

---

## 10. Invariants and Dials

### 10.1 Scaling Invariants

```yaml
INV-S01:
  rule: "All sizes defined in logical pixels"
  severity: WARNING

INV-S02:
  rule: "Reflow, never clip, at scale changes"
  severity: BLOCKING

INV-S03:
  rule: "Touch targets >= 44 lp at all scales"
  severity: WARNING

INV-S04:
  rule: "200% text resize without content loss"
  severity: BLOCKING
  source: "WCAG 1.4.4"
```

### 10.2 Scaling Dials

```yaml
DIAL-S01:
  name: "user_scale"
  range: [0.5, 4.0]
  default: 1.0
  floor: 0.5
  description: "User scaling preference"

DIAL-S02:
  name: "density_mode"
  values: ["compact", "comfortable", "spacious"]
  default: "comfortable"
  description: "Spacing density preference"

DIAL-S03:
  name: "type_scale_ratio"
  range: [1.125, 1.618]
  default: 1.25
  description: "Typography scale ratio"
```

---

## 11. Quick Reference

### 11.1 The Three Formulas

```
1. Effective Scale:      S_eff = (DPI_phys / 96) * S_user
2. Pixel Conversion:     x_px = x_lp * S_eff
3. Typography Scale:     f_lp(k) = f_0 * r^k
```

### 11.2 Quantization Quick Guide

```
Text sizes:    round to 0.25 px
Text position: round to 0.5 px
Everything else: round to whole px
```

### 11.3 Safe Scaling Factors

For cleanest rendering, prefer factors that yield whole pixels:
- 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0

Avoid if possible:
- 1.1, 1.33, 1.75 (produce fractional results)

---

*Scaling Mathematics Version 1.0.0 - Generated 2025-12-27*
