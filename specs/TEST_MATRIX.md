# Display Test Matrix

**Version:** 1.0.0
**Purpose:** Cross-platform display testing requirements for UVAS+ validation

---

## 1. Overview

This matrix defines the test configurations required to validate UVAS+ guarantees
across the full range of display hardware and software environments.

**Testing Philosophy:**
- Test at spec boundaries, not just comfortable midpoints
- Include legacy and edge-case hardware
- Validate both visual correctness AND validator accuracy
- Document "what we can't control" explicitly

---

## 2. DPI Test Values

| DPI | Description | Example Hardware | Priority |
|-----|-------------|------------------|----------|
| 72 | Legacy Mac (pre-Retina) | Classic Mac displays | LOW |
| 76 | Ultra-low density | Old CRTs, industrial displays | MEDIUM |
| 96 | Windows reference | Standard desktop monitors | HIGH |
| 110 | Common laptop | Most 15" laptops at 1080p | HIGH |
| 120 | Midrange density | 24" 4K monitors | MEDIUM |
| 144 | High density | Surface devices, high-end laptops | HIGH |
| 192 | Retina/HiDPI | MacBook Pro, high-end 4K | HIGH |
| 220 | Ultra-high | 5K iMac, premium displays | MEDIUM |
| 288 | Extreme | 8K displays, medical imaging | LOW |

**Rationale:**
- 96 DPI is the Windows/CSS reference point (1 DIP = 1/96 inch)
- macOS historically used 72 DPI then doubled to 144 DPI for Retina
- Testing at boundaries (76, 288) catches edge cases

---

## 3. Scale Factor Test Values

| Scale | S_eff at 96 DPI | S_eff at 144 DPI | Use Case | Priority |
|-------|-----------------|------------------|----------|----------|
| 0.5x  | 0.50 | 0.75 | Extreme density | LOW |
| 1.0x  | 1.00 | 1.50 | Standard | HIGH |
| 1.25x | 1.25 | 1.875 | Common Windows default | HIGH |
| 1.5x  | 1.50 | 2.25 | Laptops/HiDPI | HIGH |
| 1.75x | 1.75 | 2.625 | Fractional edge case | MEDIUM |
| 2.0x  | 2.00 | 3.00 | WCAG 200% zoom requirement | HIGH |
| 2.5x  | 2.50 | 3.75 | High accessibility need | MEDIUM |
| 3.0x  | 3.00 | 4.50 | Low vision support | MEDIUM |
| 4.0x  | 4.00 | 6.00 | WCAG 400% reflow requirement | HIGH |

**Test Combinations (minimum required):**

```
Priority HIGH combinations:
- 96 DPI @ 1.0x, 1.25x, 1.5x, 2.0x, 4.0x
- 144 DPI @ 1.0x, 1.5x, 2.0x
- 110 DPI @ 1.0x, 1.25x, 2.0x

Priority MEDIUM combinations:
- 76 DPI @ 1.0x, 2.0x
- 192 DPI @ 1.0x, 0.5x, 2.0x
- Any DPI @ 1.75x (fractional stress test)
```

---

## 4. Refresh Rate Test Values

| Hz | Display Type | Content Type | Priority |
|----|--------------|--------------|----------|
| 1-5 | E-ink (standard) | Static, page-flip | HIGH |
| 10 | E-ink (fast) | Simple animations | HIGH |
| 15 | Legacy video | Slideshow, basic UI | LOW |
| 24 | Film content | Video playback | MEDIUM |
| 30 | Console/old displays | Gaming, video | MEDIUM |
| 60 | Standard LCD/OLED | General use | HIGH |
| 75 | Common gaming | Smooth UI, gaming | MEDIUM |
| 90 | Mobile high-refresh | Phone/tablet gaming | MEDIUM |
| 120 | High-refresh gaming | Fast motion, esports | HIGH |
| 144 | Gaming standard | Competitive gaming | MEDIUM |
| 165 | High-end gaming | Enthusiast | LOW |
| 240 | Pro gaming | Esports | MEDIUM |
| 360 | Ultra high-refresh | Competitive esports | LOW |
| 480 | Extreme | Research, specialty | LOW |

**Critical Test Scenarios:**

1. **Flash safety at all rates:**
   - 10 Hz: 3 flashes/sec = 30% of frames flash (dangerous!)
   - 60 Hz: 3 flashes/sec = 5% of frames flash (safe margin)
   - 480 Hz: 3 flashes/sec = 0.6% of frames flash (very safe)

2. **Animation timing consistency:**
   - 300ms fade should take 300ms regardless of refresh rate
   - Motion tokens in ms, not frames

3. **VRR behavior:**
   - Test at VRR lower bound (typically 40-48 Hz)
   - Test rapid frame rate changes

---

## 5. Display Type Test Matrix

### 5.1 Emissive Displays

| Type | Characteristics | Test Focus |
|------|-----------------|------------|
| LCD (IPS) | Wide viewing angle, color accuracy | Contrast, color |
| LCD (VA) | High contrast, narrow angle | Contrast viewing angle |
| LCD (TN) | Fast response, poor color | Response time, color shift |
| OLED | Perfect black, PWM dimming | PWM flicker, burn-in |
| Mini-LED | Local dimming zones | Zone halo, HDR handling |
| MicroLED | Perfect black, no PWM | Reference behavior |

**OLED-Specific Tests:**
- PWM flicker at low brightness (many OLEDs use ~240 Hz PWM)
- Dark content sustained luminance
- Color shift at angle

### 5.2 Reflective Displays

| Type | Refresh | Test Focus |
|------|---------|------------|
| E-ink (standard) | 1-5 Hz | Ghosting, full refresh |
| E-ink (fast mode) | 10 Hz | Partial update artifacts |
| E-ink (color) | <1 Hz | Color accuracy, refresh time |
| E-paper (DES) | Variable | Bistability, persistence |

**E-ink-Specific Tests:**
- Animation degradation at slow refresh
- Ghosting under rapid update
- High ambient light readability

### 5.3 Legacy Displays

| Type | Characteristics | Test Focus |
|------|-----------------|------------|
| CRT | Phosphor persistence, flicker | Interlace artifacts, flicker |
| Plasma | Phosphor, subfield drive | Motion artifacts, burn-in |
| Projector (DLP) | Rainbow effect, refresh | Motion, color wheel artifacts |
| Projector (LCD) | Pixel grid, response | Sharpness, response time |

**CRT-Specific Considerations:**
- 75 Hz minimum to avoid visible flicker
- Interlaced modes (480i, 1080i) need special handling
- Curved screen geometry affects layout

---

## 6. Windowing System Test Matrix

### 6.1 Linux/Unix

| System | Scaling Model | Test Focus |
|--------|---------------|------------|
| X11 | xrandr DPI, toolkit-specific | Inconsistent scaling, bitmap fonts |
| Wayland (native) | Integer scale + compositor | Fractional blur, XWayland apps |
| Wayland (fractional-v1) | Overscale + downsample | Crisp text, app support |

**Wayland Fractional Scaling Tests:**
- 1.25x scale: Check for blur in native vs XWayland apps
- Font hinting at fractional scales
- Multi-monitor with different scales

### 6.2 Windows

| Version | Scaling Model | Test Focus |
|---------|---------------|------------|
| Windows 10 | Per-monitor DPI awareness | DPI change handling |
| Windows 11 | Per-monitor V2 | High scale correctness |
| Legacy apps | System DPI awareness | Bitmap scaling, blur |

**Windows-Specific Tests:**
- DPI awareness mode (unaware, system, per-monitor, per-monitor v2)
- Virtualization blur on unaware apps
- Mixed DPI multi-monitor

### 6.3 macOS

| Feature | Behavior | Test Focus |
|---------|----------|------------|
| Retina | 2x integer scaling | Point vs pixel confusion |
| Non-Retina | 1x scaling | Font rendering differences |
| External display | May differ from built-in | Mixed scale handling |

**macOS-Specific Tests:**
- 72 pt/inch legacy compatibility
- Retina @2x asset loading
- External non-Retina display handling

---

## 7. Test Assertions

### 7.1 Scaling Correctness

```python
def test_scaling_correctness(config: TestConfig):
    """
    Verify S_eff calculation produces correct pixel sizes.
    """
    s_eff = (config.dpi_physical / 96.0) * config.scale_factor

    for token_name, token_lp in TOKENS.items():
        expected_px = token_lp * s_eff
        actual_px = render_and_measure(token_name, config)

        # Allow for quantization
        assert abs(actual_px - round(expected_px)) <= 1, \
            f"{token_name}: expected ~{expected_px}px, got {actual_px}px"
```

### 7.2 Touch Target Validity

```python
def test_touch_targets_at_scale(config: TestConfig):
    """
    Verify 44lp touch targets remain >= 44px at any scale.
    """
    s_eff = (config.dpi_physical / 96.0) * config.scale_factor

    for element in INTERACTIVE_ELEMENTS:
        measured_px = measure_element_size(element, config)
        min_dimension = min(measured_px.width, measured_px.height)

        # 44lp minimum, scaled
        threshold_px = 44 * s_eff

        assert min_dimension >= threshold_px - 1, \
            f"{element}: {min_dimension}px < {threshold_px}px threshold"
```

### 7.3 Reflow at 200%/400%

```python
def test_reflow_at_scale(scale: float):
    """
    WCAG 1.4.10: No horizontal scroll at 320px equivalent width.
    WCAG 1.4.4: Text resizable to 200% without loss.
    """
    config = TestConfig(scale_factor=scale)
    viewport = ViewportConfig(width=320 * scale, height=800 * scale)

    render_page(config, viewport)

    # Check no horizontal overflow
    content_width = measure_content_width()
    assert content_width <= viewport.width, \
        f"Horizontal overflow: {content_width} > {viewport.width}"

    # Check no truncated text without expansion
    truncated = find_truncated_text()
    for element in truncated:
        assert has_accessible_expansion(element), \
            f"Truncated text without expansion: {element}"

    # Check no overlapping interactive elements
    overlaps = find_overlapping_interactives()
    assert len(overlaps) == 0, \
        f"Overlapping elements: {overlaps}"
```

### 7.4 Flash Safety at All Refresh Rates

```python
def test_flash_safety_refresh_independent(content: VideoContent):
    """
    Flash rate measured in time domain, not frames.
    """
    for refresh_hz in [10, 30, 60, 120, 240, 480]:
        # Simulate content at different refresh rates
        frames = resample_to_refresh_rate(content, refresh_hz)
        timestamps = generate_timestamps(len(frames), refresh_hz)

        # Run flash gate
        violations = flash_gate.validate_sequence(
            extract_luminance(frames),
            timestamps
        )

        # Violations should be identical regardless of refresh rate
        # (same content, same time-domain analysis)
        assert violations == expected_violations_for_content(content), \
            f"Flash detection varied with refresh rate {refresh_hz}"
```

### 7.5 E-ink Mode Graceful Degradation

```python
def test_eink_mode_degradation():
    """
    E-ink mode disables problematic patterns.
    """
    config = TestConfig(eink_mode=True)

    # Continuous animations should be disabled
    for animation in CONTINUOUS_ANIMATIONS:
        assert not is_animation_active(animation, config), \
            f"Continuous animation {animation} active in e-ink mode"

    # Loading spinners replaced with progress bars
    for spinner in LOADING_SPINNERS:
        replacement = get_eink_replacement(spinner, config)
        assert replacement.type == 'progress_bar', \
            f"Spinner not replaced: {spinner}"

    # Scroll behavior is page-flip
    scroll_behavior = get_scroll_behavior(config)
    assert scroll_behavior == 'page_flip', \
        f"Smooth scroll in e-ink mode: {scroll_behavior}"
```

---

## 8. CI/CD Integration

### 8.1 Test Tiers

**Tier 1 (Every PR):**
- 96 DPI @ 1.0x, 2.0x
- Flash safety (60 Hz reference)
- Touch target minimum
- Contrast validation

**Tier 2 (Daily/Nightly):**
- Full DPI range @ key scales
- All refresh rates
- Reflow at 200%, 400%
- E-ink mode validation

**Tier 3 (Weekly/Release):**
- Cross-platform (Windows, macOS, Linux)
- Wayland fractional scaling
- Multi-monitor configurations
- Full test matrix

### 8.2 GitHub Actions Example

```yaml
name: Display Matrix Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  tier1-fast:
    name: Tier 1 (Fast Checks)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run scaling tests (96 DPI)
        run: pytest tests/scaling/ -k "dpi96" --quick
      - name: Run flash safety
        run: pytest tests/temporal/flash_gate_test.py
      - name: Run contrast validation
        run: pytest tests/contrast/

  tier2-extended:
    name: Tier 2 (Extended)
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Full DPI range tests
        run: pytest tests/scaling/ --full-dpi-range
      - name: Refresh rate independence
        run: pytest tests/temporal/ --all-refresh-rates
      - name: Reflow tests
        run: pytest tests/reflow/ --scales 1.0,2.0,4.0
      - name: E-ink mode tests
        run: pytest tests/eink/

  tier3-comprehensive:
    name: Tier 3 (Full Matrix)
    runs-on: ${{ matrix.os }}
    if: github.event_name == 'push' && contains(github.ref, 'release')
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        scale: [1.0, 1.25, 1.5, 2.0, 4.0]
    steps:
      - uses: actions/checkout@v4
      - name: Platform-specific tests
        run: pytest tests/ --scale ${{ matrix.scale }}
```

---

## 9. Known Limitations and Documented Gaps

### 9.1 What We Test and Guarantee

| Aspect | Guarantee | Validation Method |
|--------|-----------|-------------------|
| Scaling math | S_eff formula correctness | Unit tests |
| Touch targets | >= 44lp at all scales | Automated measurement |
| Flash safety | <= 3 flashes/sec | Time-domain analysis |
| Contrast | >= 4.5:1 for text | Color math |
| Reflow | No clipping at 200% | DOM analysis |

### 9.2 What We Cannot Control

| Aspect | Reason | Mitigation |
|--------|--------|------------|
| PWM flicker | Hardware behavior | Flicker-safe mode reduces stimuli |
| VRR artifacts | Monitor-dependent | VRR-safe mode reduces provocation |
| E-ink ghosting | Panel physics | Graceful degradation profile |
| Bitmap font rendering | OS/toolkit dependent | Recommend font stacks |
| Color accuracy | Uncalibrated displays | Design for delta-E tolerance |

### 9.3 Testing Hardware Availability

Not all tests can run in CI. Document hardware tests that require:
- Physical e-ink devices (reMarkable, Kindle)
- High refresh monitors (240+ Hz)
- OLED panels for PWM testing
- CRT for legacy validation

These should be part of release certification, not CI.

---

## 10. Test Result Format

```json
{
  "test_run": {
    "timestamp": "2025-12-27T12:00:00Z",
    "version": "1.0.0",
    "tier": 2
  },
  "matrix_coverage": {
    "dpi_values_tested": [76, 96, 110, 144, 192],
    "scales_tested": [1.0, 1.25, 1.5, 2.0, 4.0],
    "refresh_rates_tested": [10, 60, 120, 240],
    "display_types_tested": ["lcd", "oled", "eink_simulated"]
  },
  "results": {
    "scaling_correctness": {
      "passed": 42,
      "failed": 0,
      "skipped": 3
    },
    "touch_targets": {
      "passed": 28,
      "failed": 0,
      "warnings": 2
    },
    "flash_safety": {
      "passed": 15,
      "blocked": 0
    },
    "reflow": {
      "passed": 12,
      "failed": 0
    }
  },
  "summary": {
    "all_blocking_passed": true,
    "warnings": 2,
    "coverage_percent": 87
  }
}
```

---

*Test Matrix Version 1.0.0 - Created 2025-12-27*
