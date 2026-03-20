# Display Adaptation Layer (DAL)

> **Status:** SPECIFICATION ONLY -- not yet targeted for implementation

**Version:** 1.0.0
**Purpose:** Enable UVAS+ to adapt semantics to display physics without becoming a GPU driver

---

## 1. Overview

The Display Adaptation Layer separates **meaning** from **display constraints**. It allows the same accessibility guarantees to hold across:

- 10 Hz e-ink to 480 Hz OLED
- 76 DPI legacy monitors to 192+ DPI retina displays
- VRR gaming monitors to fixed-refresh industrial CRTs
- Emissive (LCD/OLED) to reflective (e-ink) technologies

**Design principle:** Same semantics, different render caps.

---

## 2. Three Temporal Phenomena (Category Separation)

These are **distinct domains** and must not be conflated:

### 2.1 Refresh Rate (Display Capability)

**Definition:** How often the display can present new frames (Hz).

| Category | Range | Examples |
|----------|-------|----------|
| Ultra-low | 1-15 Hz | E-ink, some industrial |
| Low | 15-30 Hz | Legacy monitors, power-saving |
| Standard | 30-75 Hz | Most desktop monitors |
| High | 75-165 Hz | Gaming monitors |
| Ultra-high | 165-480 Hz | Competitive gaming, VR |

**What it affects:** Smoothness, latency, motion portrayal
**What it does NOT affect:** Content safety (flashes are time-based, not frame-based)

### 2.2 Content Flicker (Your Pixels)

**Definition:** How often your rendered pixels oscillate in luminance.

This is the **seizure-risk domain**. UVAS+ controls this directly.

| Risk Band | Frequency | Notes |
|-----------|-----------|-------|
| High risk | 10-25 Hz | Peak photosensitive seizure trigger band |
| Moderate risk | 3-10 Hz, 25-50 Hz | Sensitive individuals affected |
| Low risk | < 3 Hz, > 50 Hz | Generally safe |

**UVAS+ invariant:** Content flash rate <= 3 Hz (conservative floor)

### 2.3 Hardware Flicker (PWM/VRR/Dithering)

**Definition:** Luminance modulation from display hardware, not your content.

| Source | Mechanism | Mitigation |
|--------|-----------|------------|
| PWM dimming | Rapid on/off cycling for brightness control | User override: flicker-sensitive mode |
| VRR brightness flicker | Frame-rate variation causing brightness shifts | Avoid rapid frame-time changes |
| Temporal dithering | Frame-to-frame bit toggling for color depth | Reduce high-frequency spatial patterns |
| Overdrive artifacts | Response time compensation glitches | Avoid rapid alternating high-contrast |

**UVAS+ can only:** Reduce stimuli that aggravate these; offer user overrides.
**UVAS+ cannot:** Fix monitor firmware.

---

## 3. DAL Architecture

```
+------------------+     +------------------+     +------------------+
|  UVAS+ Tokens    | --> |  DAL Transform   | --> |  Render Caps     |
|  (logical units) |     |  (display-aware) |     |  (device-specific)|
+------------------+     +------------------+     +------------------+
        |                        |                        |
        v                        v                        v
   motion.duration          S_eff scaling           max_animation_hz
   spacing.base             quantization            min_motion_step_px
   font.body_lp             reflow validation       palette_variant
```

---

## 4. DAL Inputs

### 4.1 System-Queryable (Runtime Detection)

```yaml
dal_inputs:
  dpi_physical:
    type: number
    source: "OS/toolkit API"
    fallback: 96
    note: "May be unreliable; user override recommended"

  scale_user:
    type: number
    source: "OS accessibility settings"
    range: [0.5, 4.0]
    common_values: [1.0, 1.25, 1.5, 2.0]
    note: "Windows DPI scaling / macOS display scaling / Wayland fractional"

  refresh_rate_hz:
    type: number
    source: "Display API"
    fallback: 60
    note: "For VRR displays, use minimum or current rate"

  vrr_enabled:
    type: boolean
    source: "Display API / user setting"
    fallback: false
    note: "Adaptive-Sync / FreeSync / G-Sync detection"

  display_technology:
    type: enum
    values: ["unknown", "lcd", "oled", "eink", "crt", "projection"]
    source: "EDID parsing / user selection"
    fallback: "unknown"
```

### 4.2 User Overrides (Explicit Settings)

```yaml
user_overrides:
  eink_mode:
    type: boolean
    default: false
    effect: "Disables animations, increases dwell times, uses persistent states"
    trigger: "User selection or e-ink display detection"

  flicker_sensitive_mode:
    type: boolean
    default: false
    effect: "Reduces luminance modulation, avoids high-area contrast changes"
    trigger: "User selection (vestibular/migraine/photosensitive)"

  vrr_safe_mode:
    type: boolean
    default: false
    effect: "Maintains stable frame timing, reduces camera shake"
    trigger: "User selection or VRR-related discomfort"

  reduced_motion:
    type: boolean
    default: false
    effect: "Minimizes or disables all motion, instant transitions"
    trigger: "prefers-reduced-motion media query or user selection"

  high_refresh_mode:
    type: boolean
    default: false
    effect: "Unlocks animations above 60 Hz, enables smoother motion"
    trigger: "User selection on capable displays"
```

---

## 5. DAL Outputs (Render Caps)

### 5.1 Temporal Caps

```yaml
render_caps:
  max_animation_hz:
    description: "Maximum frame rate for animated content"
    formula: "min(refresh_rate_hz, 60) unless high_refresh_mode"
    eink_override: 1  # Static only
    flicker_sensitive_override: 30

  max_luminance_modulation_hz:
    description: "Maximum frequency for brightness changes"
    invariant_ceiling: 3  # WCAG/seizure safety
    note: "Content luminance oscillations above this are BLOCKED"

  min_transition_duration_ms:
    description: "Minimum time for state transitions"
    standard: 150
    eink_override: 500
    reduced_motion_override: 0  # Instant

  preferred_transition_durations:
    short_ms: 150
    medium_ms: 300
    long_ms: 500
    eink_multiplier: 3.0
    note: "All durations in milliseconds, not frames"
```

### 5.2 Spatial Caps

```yaml
  min_motion_step_px:
    description: "Minimum movement per frame to avoid smearing"
    formula: "max(1, round(velocity_px_per_sec / refresh_rate_hz))"
    eink_override: 4  # Coarse steps for slow panels

  quantization_text_px:
    description: "Rounding precision for text sizes"
    standard: 0.25
    low_dpi_override: 0.5
    high_dpi_threshold: 144
    high_dpi_value: 0.125

  quantization_stroke_px:
    description: "Rounding precision for strokes/borders"
    value: 1.0  # Always whole pixels

  quantization_layout_px:
    description: "Rounding precision for layout metrics"
    value: 1.0  # Always whole pixels at raster stage
```

### 5.3 Visual Mode Caps

```yaml
  palette_variant:
    description: "Color palette adaptation"
    values:
      full: "Standard CVD-safe palette"
      reduced: "High-contrast subset for low color depth"
      monochrome: "Grayscale with pattern encoding"
      eink: "Optimized for bistable displays"
    default: "full"
    eink_override: "eink"

  pattern_encoding_required:
    description: "Force non-color encoding channels"
    eink: true
    monochrome: true
    standard: false
    note: "When true, all categorical data must use shape/pattern/texture"
```

---

## 6. Scaling Pipeline

### 6.1 Effective Scale Calculation

```
S_eff = (DPI_phys / DPI_ref) * S_user

Where:
  DPI_ref = 96 (canonical reference)
  DPI_phys = physical display DPI
  S_user = user scaling factor (1.0 = 100%)
```

### 6.2 Logical Unit Conversion

```
x_px = x_lp * S_eff

Where:
  x_lp = size in logical pixels
  x_px = size in physical pixels
```

### 6.3 Quantization Application

```
x_px_final = Q(x_px, context)

Where Q is the quantizer:
  - Text: round to nearest quantization_text_px
  - Strokes: round to nearest whole pixel
  - Layout: round to nearest whole pixel
```

### 6.4 Complete Pipeline

```
[Token lp] --> [Scale by S_eff] --> [Quantize] --> [Layout/Reflow] --> [Render]
```

---

## 7. Display Mode Profiles

### 7.1 Standard Profile (Default)

```yaml
profile_standard:
  applies_when: "No overrides active, refresh >= 30 Hz"
  caps:
    max_animation_hz: 60
    max_luminance_modulation_hz: 3
    min_transition_duration_ms: 150
    palette_variant: "full"
    pattern_encoding_required: false
```

### 7.2 E-ink Profile

```yaml
profile_eink:
  applies_when: "eink_mode = true OR display_technology = 'eink'"
  caps:
    max_animation_hz: 1  # Effectively static
    max_luminance_modulation_hz: 0.5
    min_transition_duration_ms: 500
    palette_variant: "eink"
    pattern_encoding_required: true
  behaviors:
    - "Disable blinking cursors"
    - "Disable animated loaders (use progress text)"
    - "Disable shimmer effects"
    - "Increase hover/focus dwell time"
    - "Use explicit state change indicators"
```

### 7.3 Flicker-Sensitive Profile

```yaml
profile_flicker_sensitive:
  applies_when: "flicker_sensitive_mode = true"
  caps:
    max_animation_hz: 30
    max_luminance_modulation_hz: 1
    min_transition_duration_ms: 300
    palette_variant: "reduced"
    pattern_encoding_required: false
  behaviors:
    - "Reduce large-area contrast changes"
    - "Avoid rapid alternating patterns"
    - "Use longer fade durations"
    - "Disable camera shake effects"
    - "Reduce particle/sparkle effects"
```

### 7.4 VRR-Safe Profile

```yaml
profile_vrr_safe:
  applies_when: "vrr_safe_mode = true AND vrr_enabled = true"
  caps:
    max_animation_hz: 60  # Cap to stable rate
    max_luminance_modulation_hz: 3
    min_transition_duration_ms: 150
    palette_variant: "full"
  behaviors:
    - "Maintain stable frame timing"
    - "Avoid rapid frame-time variation"
    - "Smooth velocity changes"
    - "Disable motion blur that varies with frame time"
```

### 7.5 Reduced Motion Profile

```yaml
profile_reduced_motion:
  applies_when: "reduced_motion = true OR prefers-reduced-motion"
  caps:
    max_animation_hz: 0  # No animation
    max_luminance_modulation_hz: 0
    min_transition_duration_ms: 0  # Instant
    palette_variant: "full"
  behaviors:
    - "Instant state transitions"
    - "No parallax scrolling"
    - "Static backgrounds"
    - "No auto-playing video/animation"
    - "Progress indicators: text/numeric only"
```

---

## 8. Profile Composition

When multiple overrides are active, compose restrictively:

```python
def compose_profiles(active_profiles: List[Profile]) -> RenderCaps:
    """Take most restrictive value for each cap."""
    return RenderCaps(
        max_animation_hz=min(p.max_animation_hz for p in active_profiles),
        max_luminance_modulation_hz=min(p.max_luminance_modulation_hz for p in active_profiles),
        min_transition_duration_ms=max(p.min_transition_duration_ms for p in active_profiles),
        # Pattern encoding required if ANY profile requires it
        pattern_encoding_required=any(p.pattern_encoding_required for p in active_profiles),
    )
```

**Example:** User has both `flicker_sensitive_mode` and `reduced_motion`:
- `max_animation_hz`: min(30, 0) = 0
- `max_luminance_modulation_hz`: min(1, 0) = 0
- `min_transition_duration_ms`: max(300, 0) = 0 (instant wins for reduced motion)

---

## 9. What UVAS+ Can and Cannot Guarantee

### 9.1 CAN Guarantee (Controlled)

| Domain | Guarantee | Mechanism |
|--------|-----------|-----------|
| Content flash rate | <= 3 Hz | FLASH_GATE validator |
| Semantic invariants | Always enforced | Token system + validators |
| Time-based motion | Frame-rate independent | Duration tokens in ms |
| Reflow correctness | No clipping/overlap | Layout validation |
| Dual-channel encoding | Non-color fallback exists | VIZ_GATE validator |
| Profile-based fallbacks | Display-appropriate behavior | DAL profiles |

### 9.2 CANNOT Fully Guarantee (Hardware-Dependent)

| Domain | Limitation | Mitigation |
|--------|------------|------------|
| PWM flicker | Monitor firmware | Flicker-sensitive mode reduces stimuli |
| VRR brightness flicker | Monitor/driver | VRR-safe mode stabilizes frame timing |
| Overdrive artifacts | Monitor response time | Avoid rapid high-contrast alternation |
| E-ink ghosting | Panel technology | Extended dwell times, contrast limits |
| Subpixel rendering | OS/font engine | Quantization rules, hinting respect |

---

## 10. Implementation Checklist

### 10.1 Runtime Detection

- [ ] Query DPI from OS/toolkit
- [ ] Query refresh rate from display API
- [ ] Detect VRR capability
- [ ] Parse EDID for display technology (when available)
- [ ] Respect `prefers-reduced-motion` media query
- [ ] Provide user settings UI for overrides

### 10.2 Token System Integration

- [ ] All motion tokens in milliseconds (not frames)
- [ ] All size tokens in logical pixels (lp)
- [ ] Scaling pipeline implemented (lp -> S_eff -> Q -> px)
- [ ] Quantizers applied per context (text/stroke/layout)

### 10.3 Validator Integration

- [ ] FLASH_GATE operates on time domain
- [ ] VRR_FLICKER_GATE checks frame-time stability
- [ ] EINK_MODE_GATE validates static-only rendering
- [ ] All gates respect active profile caps

---

## 11. References

- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) - Flash thresholds
- [Microsoft DIP Model](https://learn.microsoft.com/en-us/windows/win32/learnwin32/dpi-and-device-independent-pixels) - Device-independent pixels
- [Wayland Fractional Scaling](https://wayland.app/protocols/fractional-scale-v1) - Compositor scaling
- [VESA Adaptive-Sync](https://www.vesa.org/) - VRR specification
- [IEEE Spectrum E-ink](https://spectrum.ieee.org/e-paper-display-modos) - E-ink refresh rates
- [Epilepsy Action Guidelines](https://www.epilepsy.org.uk/info/seizure-triggers/photosensitive-epilepsy) - Photosensitive triggers

---

*Display Adaptation Layer Version 1.0.0 - Generated 2025-12-27*
