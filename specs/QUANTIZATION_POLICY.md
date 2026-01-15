# Quantization Policy

**Version:** 1.0.0
**Purpose:** Define hysteresis quantization and snap-class rules to prevent jitter during scaling and animation
**Companion to:** SCALING_MATHEMATICS.md

---

## 1. The Problem: Pixel Jitter

### 1.1 What Happens Without Hysteresis

When continuous values oscillate near a rounding boundary, the quantized result flips back and forth:

```
Frame 1: x = 15.49 -> round() -> 15 px
Frame 2: x = 15.51 -> round() -> 16 px
Frame 3: x = 15.49 -> round() -> 15 px
Frame 4: x = 15.52 -> round() -> 16 px
```

Result: **visible jitter** even though the actual change is sub-perceptual.

### 1.2 When Jitter Manifests

| Scenario | Cause | Severity |
|----------|-------|----------|
| Fractional scaling (1.25x, 1.75x) | Values land near boundaries | HIGH |
| DPI transitions | Moving between monitors | HIGH |
| Animated elements | Continuous position/size updates | MEDIUM |
| Responsive layout | Width-dependent calculations | MEDIUM |
| Scroll-triggered changes | Layout recalc on scroll | LOW |

### 1.3 The Solution: Hysteresis Quantization

**Hysteresis** adds a "dead zone" around the last quantized value. The result only changes when the new value exceeds a threshold band, preventing oscillation.

---

## 2. Hysteresis Quantizer Algorithm

### 2.1 Core Algorithm

```python
class HysteresisQuantizer:
    """
    Quantizer with memory that prevents jitter near boundaries.

    The hysteresis band creates a "sticky" zone around the last output.
    Only when the input moves outside this zone does the output change.
    """

    def __init__(self, precision: float = 1.0, hysteresis: float = 0.2):
        """
        Args:
            precision: Quantization step (e.g., 1.0 for whole pixels)
            hysteresis: Half-width of dead zone (e.g., 0.2 px)
        """
        self.precision = precision
        self.hysteresis = hysteresis
        self._last_output: dict[str, float] = {}  # Key -> last quantized value

    def quantize(self, value: float, key: str) -> float:
        """
        Quantize with hysteresis.

        Args:
            value: Raw continuous value
            key: Unique identifier for this value (e.g., "button.width")

        Returns:
            Quantized value with jitter suppression
        """
        # Standard quantization candidate
        candidate = round(value / self.precision) * self.precision

        # If we have no history, just return the candidate
        if key not in self._last_output:
            self._last_output[key] = candidate
            return candidate

        last = self._last_output[key]

        # Check if the raw value is within hysteresis band of last output
        lower_bound = last - (self.precision / 2) - self.hysteresis
        upper_bound = last + (self.precision / 2) + self.hysteresis

        if lower_bound <= value <= upper_bound:
            # Stay with last output (suppress jitter)
            return last
        else:
            # Value moved outside band; update
            self._last_output[key] = candidate
            return candidate

    def reset(self, key: str = None):
        """Clear quantization history (e.g., on layout reset)."""
        if key is None:
            self._last_output.clear()
        else:
            self._last_output.pop(key, None)
```

### 2.2 Visualization

```
      |<-- hysteresis -->|<-- precision -->|<-- hysteresis -->|
      |                  |                 |                  |
------+------------------+-----------------+------------------+------
     14.3              14.5              15.5              15.7

If last output = 15.0:
  - Values in [14.3, 15.7] continue returning 15.0
  - Values < 14.3 snap to 14.0 or lower
  - Values > 15.7 snap to 16.0 or higher
```

### 2.3 Key Properties

| Property | Value | Rationale |
|----------|-------|-----------|
| Default hysteresis | 0.2 px | Larger than typical floating-point noise |
| Never exceeds | 0.4 px | Keeps perceived accuracy |
| Per-key state | Required | Different elements have different histories |
| Reset on layout | Recommended | Prevents stale state after major changes |

---

## 3. Snap Class Hierarchy

### 3.1 Metric Classes

Not all metrics should be quantized the same way. Define **snap classes** by metric type:

| Snap Class | Precision | Hysteresis | Rationale |
|------------|-----------|------------|-----------|
| `stroke` | 1.0 px | 0.2 px | Strokes must be crisp; sub-pixel causes blur |
| `layout` | 1.0 px | 0.2 px | Box model requires whole pixels for alignment |
| `icon` | 1.0 px | 0.2 px | Bitmap icons need pixel-perfect edges |
| `spacing` | 1.0 px | 0.2 px | Rhythm consistency |
| `touch-target` | 1.0 px | 0.0 px | Safety-critical; always use ceiling, no hysteresis |
| `text-size` | 0.25 px | 0.1 px | Font engines handle subpixel; finer precision OK |
| `text-position` | 0.5 px | 0.15 px | Subpixel positioning improves kerning |

### 3.2 Implementation

```python
SNAP_CLASSES = {
    "stroke": {"precision": 1.0, "hysteresis": 0.2},
    "layout": {"precision": 1.0, "hysteresis": 0.2},
    "icon": {"precision": 1.0, "hysteresis": 0.2},
    "spacing": {"precision": 1.0, "hysteresis": 0.2},
    "touch-target": {"precision": 1.0, "hysteresis": 0.0, "round_fn": "ceil"},
    "text-size": {"precision": 0.25, "hysteresis": 0.1},
    "text-position": {"precision": 0.5, "hysteresis": 0.15},
}

def quantize_by_class(value: float, snap_class: str, key: str,
                      quantizer: HysteresisQuantizer) -> float:
    """Apply class-appropriate quantization."""
    config = SNAP_CLASSES.get(snap_class, SNAP_CLASSES["layout"])

    # Touch targets use ceiling for safety
    if config.get("round_fn") == "ceil":
        import math
        return math.ceil(value / config["precision"]) * config["precision"]

    # Others use hysteresis quantizer
    quantizer.precision = config["precision"]
    quantizer.hysteresis = config["hysteresis"]
    return quantizer.quantize(value, key)
```

### 3.3 Token to Snap Class Mapping

```yaml
token_snap_classes:
  # Spacing tokens
  spacing.*: spacing
  gap.*: spacing
  padding.*: layout
  margin.*: layout

  # Typography tokens
  font.size.*: text-size
  line.height.*: text-size
  letter.spacing: text-position

  # Interactive tokens
  touch.target.*: touch-target
  button.min.*: touch-target

  # Visual tokens
  border.width.*: stroke
  outline.width.*: stroke
  divider.width: stroke

  # Icon tokens
  icon.size.*: icon

  # Layout tokens
  container.*: layout
  grid.*: layout
  column.*: layout
```

---

## 4. High-DPI Adjustments

### 4.1 DPI-Dependent Precision

At higher DPIs, finer quantization is invisible and improves accuracy:

| DPI Range | stroke.precision | text-size.precision | hysteresis |
|-----------|------------------|---------------------|------------|
| < 96 | 1.0 px | 0.5 px | 0.3 px |
| 96-143 | 1.0 px | 0.25 px | 0.2 px |
| 144-191 | 0.5 px | 0.25 px | 0.15 px |
| >= 192 | 0.5 px | 0.125 px | 0.1 px |

### 4.2 Rationale

- At 192 DPI (2x), a 0.5 px error is physically 0.25 px at 96 DPI equivalent
- Finer precision at high DPI maintains the same perceived accuracy
- Hysteresis scales proportionally to maintain anti-jitter effectiveness

### 4.3 Implementation

```python
def get_dpi_adjusted_snap_class(snap_class: str, dpi: float) -> dict:
    """Return precision/hysteresis adjusted for DPI."""
    base = SNAP_CLASSES[snap_class].copy()

    if dpi >= 192:
        scale = 0.5
    elif dpi >= 144:
        scale = 0.75
    else:
        scale = 1.0

    # Only adjust if base precision is 1.0 or higher
    if base["precision"] >= 1.0:
        base["precision"] *= scale

    base["hysteresis"] *= scale
    return base
```

---

## 5. Quantization During Transitions

### 5.1 Scale Change Events

When scale changes (DPI transition, user zoom), quantization must be handled carefully:

```python
class TransitionQuantizer(HysteresisQuantizer):
    """Extended quantizer with transition awareness."""

    def on_scale_change(self, old_scale: float, new_scale: float):
        """
        Handle scale transition.

        Strategy: Reset history for elements that will visibly move,
        but smooth the transition for others.
        """
        ratio = new_scale / old_scale

        if abs(ratio - 1.0) > 0.25:
            # Major scale change (>25%): reset all history
            self.reset()
        else:
            # Minor change: scale the history values
            for key in self._last_output:
                self._last_output[key] *= ratio
```

### 5.2 Animation Quantization

During animations, disable hysteresis for the animated property:

```python
def animate_value(start: float, end: float, progress: float,
                  snap_class: str, key: str, quantizer: HysteresisQuantizer) -> float:
    """
    Animate with appropriate quantization.

    During animation (0 < progress < 1): no hysteresis (smooth motion)
    At rest (progress = 0 or 1): full hysteresis (stable positioning)
    """
    raw = start + (end - start) * progress

    if 0 < progress < 1:
        # Animation in progress: use simple rounding, no hysteresis
        config = SNAP_CLASSES[snap_class]
        return round(raw / config["precision"]) * config["precision"]
    else:
        # At rest: use full hysteresis
        return quantize_by_class(raw, snap_class, key, quantizer)
```

---

## 6. Edge Cases

### 6.1 Touch Target Safety

Touch targets are **never** subject to hysteresis downward:

```python
def quantize_touch_target(value_lp: float, s_eff: float) -> float:
    """
    Touch targets always round UP (ceiling).

    44 lp minimum is an accessibility invariant.
    Rounding down could create non-compliant targets.
    """
    import math
    min_lp = 44
    value_px = max(value_lp, min_lp) * s_eff
    return math.ceil(value_px)  # Always ceiling
```

### 6.2 Zero-Crossing Values

For values that can cross zero (e.g., margins, positions):

```python
def quantize_signed(value: float, precision: float, hysteresis: float,
                    key: str, last_output: dict) -> float:
    """Handle signed values crossing zero."""
    candidate = round(value / precision) * precision

    if key not in last_output:
        last_output[key] = candidate
        return candidate

    last = last_output[key]

    # Special handling for zero crossing: always allow it
    if (last > 0 and value < -hysteresis) or (last < 0 and value > hysteresis):
        last_output[key] = candidate
        return candidate

    # Standard hysteresis otherwise
    band = precision / 2 + hysteresis
    if abs(value - last) <= band:
        return last
    else:
        last_output[key] = candidate
        return candidate
```

### 6.3 Layout Dependency Chains

When element A's size affects element B's position, quantization order matters:

```
[Parent Container]
    |
    +-- [Child A: width = f(parent)]  <- Quantize first
    |
    +-- [Child B: left = A.right + gap]  <- Quantize after A
```

**Rule:** Quantize in layout tree order (parent before children, earlier siblings before later).

---

## 7. Validator Integration

### 7.1 QUANTIZATION_CONSISTENCY Gate

```yaml
quantization_consistency_gate:
  id: GATE-Q01
  severity: WARNING
  checks:
    - name: jitter_detection
      rule: "No element changes quantized position more than twice in 500ms without user input"
      threshold: 2
    - name: hysteresis_application
      rule: "All animated layouts use hysteresis quantization"
    - name: touch_target_ceiling
      rule: "Touch targets use ceiling, never floor or round"
```

### 7.2 Jitter Detection Algorithm

```python
class JitterDetector:
    """Detect quantization jitter in running application."""

    def __init__(self, window_ms: float = 500, max_flips: int = 2):
        self.window_ms = window_ms
        self.max_flips = max_flips
        self._history: dict[str, list[tuple[float, float]]] = {}  # key -> [(time, value)]

    def record(self, key: str, value: float, timestamp_ms: float):
        """Record a quantized value."""
        if key not in self._history:
            self._history[key] = []

        history = self._history[key]

        # Prune old entries
        history = [(t, v) for t, v in history if timestamp_ms - t < self.window_ms]
        history.append((timestamp_ms, value))
        self._history[key] = history

    def check_jitter(self, key: str) -> bool:
        """Returns True if jitter detected for key."""
        if key not in self._history:
            return False

        history = self._history[key]
        if len(history) < 3:
            return False

        # Count direction changes
        values = [v for _, v in history]
        flips = 0
        for i in range(2, len(values)):
            if (values[i] - values[i-1]) * (values[i-1] - values[i-2]) < 0:
                flips += 1

        return flips >= self.max_flips
```

---

## 8. Testing Requirements

### 8.1 Hysteresis Unit Tests

```python
def test_hysteresis_suppresses_jitter():
    """Values oscillating within band return same result."""
    q = HysteresisQuantizer(precision=1.0, hysteresis=0.2)

    results = []
    for value in [15.4, 15.6, 15.4, 15.5, 15.6, 15.4]:
        results.append(q.quantize(value, "test"))

    # Should be stable after first quantization
    assert results[0] == 15.0  # or 16.0 depending on initial
    assert all(r == results[0] for r in results)

def test_hysteresis_allows_large_changes():
    """Values outside band do update."""
    q = HysteresisQuantizer(precision=1.0, hysteresis=0.2)

    q.quantize(15.5, "test")  # Should be 16
    result = q.quantize(14.0, "test")  # Far outside band

    assert result == 14.0  # Should have updated

def test_touch_targets_use_ceiling():
    """Touch targets never round down."""
    for value in [43.1, 43.5, 43.9, 44.0, 44.1]:
        result = quantize_touch_target(value, 1.0)
        assert result >= 44, f"{value} should round to at least 44"
```

### 8.2 Visual Jitter Test

Manual/automated test:

1. Set scale to 1.25x (known fractional stress point)
2. Apply small random perturbations (±0.1 lp) to element positions
3. Record rendered pixel positions over 100 frames
4. Assert: no element oscillates between two values more than 2 times

---

## 9. Quick Reference

### 9.1 Snap Class Cheat Sheet

```
Strokes/borders:    Round to 1 px, hysteresis 0.2 px
Layout metrics:     Round to 1 px, hysteresis 0.2 px
Touch targets:      CEILING to 1 px, NO hysteresis
Text sizes:         Round to 0.25 px, hysteresis 0.1 px
Text positions:     Round to 0.5 px, hysteresis 0.15 px
```

### 9.2 When to Reset Hysteresis

- DPI change (window moved to different monitor)
- User scale change (> 25%)
- Layout mode change (compact/comfortable/spacious)
- Window resize (major dimension change)

### 9.3 When NOT to Use Hysteresis

- Touch target sizing (safety-critical; always ceiling)
- User-initiated animation (smooth motion expected)
- Scroll position (user controls precisely)

---

*Quantization Policy Version 1.0.0 - Created 2025-12-27*
