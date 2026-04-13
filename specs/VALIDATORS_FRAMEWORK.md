# Validators and Automated Checks Framework

**Version:** 1.0.0
**Purpose:** Automated enforcement of UVAS invariants and soft constraints

---

## Implementation Status

| Gate | ID | Status | Location |
|------|----|--------|----------|
| CONTRAST | GATE-002 | **Implemented** | `tools/validators/contrast.py` |
| CVD | GATE-003 | **Implemented** | `tools/validators/cvd.py` |
| ACHROMAT | GATE-007 | **Implemented** | `tools/validators/achromat.py` |
| Base ABC | -- | **Implemented** | `tools/validators/base.py` |
| SEIZURE | GATE-001 | Partial (v0.3.0) | `tools/validators/seizure.py` |
| SPATIAL | GATE-004 | Partial | `tools/validators/spatial.py` |
| TEMPORAL/DEPTH | GATE-005 | Partial | `tools/validators/temporal_depth.py` |
| COGNITIVE | GATE-006 | Partial | `tools/validators/cognitive.py` |
| Unified CLI | -- | **Implemented** | `tools/validate.py` |

---

## 1. Validator Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      VALIDATION PIPELINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ASSET          CONTENT-TYPE         VALIDATOR          RESULT  │
│  INPUT          DETECTION            DISPATCH           OUTPUT  │
│                                                                  │
│  ┌────────┐     ┌──────────┐        ┌──────────┐      ┌──────┐ │
│  │ Video  │────>│ Temporal │───────>│ SEIZURE  │─────>│BLOCK │ │
│  │ .mp4   │     │ content  │        │ GATE     │      │/PASS │ │
│  └────────┘     └──────────┘        └──────────┘      └──────┘ │
│                                                                  │
│  ┌────────┐     ┌──────────┐        ┌──────────┐      ┌──────┐ │
│  │ Theme  │────>│ Color    │───────>│ CONTRAST │─────>│BLOCK │ │
│  │ .json  │     │ palette  │        │ GATE     │      │/PASS │ │
│  └────────┘     └──────────┘        └──────────┘      └──────┘ │
│                                                                  │
│  ┌────────┐     ┌──────────┐        ┌──────────┐      ┌──────┐ │
│  │ Palette│────>│ Semantic │───────>│ CVD      │─────>│WARN  │ │
│  │ .json  │     │ colors   │        │ GATE     │      │/PASS │ │
│  └────────┘     └──────────┘        └──────────┘      └──────┘ │
│                                                                  │
│  ┌────────┐     ┌──────────┐        ┌──────────┐      ┌──────┐ │
│  │ Layout │────>│ UI       │───────>│ SPATIAL  │─────>│WARN  │ │
│  │ .tsx   │     │ components│       │ GATE     │      │/PASS │ │
│  └────────┘     └──────────┘        └──────────┘      └──────┘ │
│                                                                  │
│  ┌────────┐     ┌──────────┐        ┌──────────┐      ┌──────┐ │
│  │ Scene  │────>│ 3D       │───────>│ DEPTH    │─────>│WARN  │ │
│  │ .unity │     │ mechanic │        │ GATE     │      │/PASS │ │
│  └────────┘     └──────────┘        └──────────┘      └──────┘ │
│                                                                  │
│  ┌────────┐     ┌──────────┐        ┌──────────┐      ┌──────┐ │
│  │ Nav    │────>│ Menu     │───────>│ COGNITIVE│─────>│WARN  │ │
│  │ .json  │     │ structure│        │ GATE     │      │/PASS │ │
│  └────────┘     └──────────┘        └──────────┘      └──────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Gate Definitions

### SEIZURE_GATE (BLOCKING)

**Severity:** BLOCKING (CI/CD will fail)
**Applies to:** Videos, animations, shaders, particle systems, UI transitions

```yaml
seizure_gate:
  id: GATE-001
  severity: BLOCKING
  checks:
    - name: flash_frequency
      rule: "count(luminance_transitions > 10%) <= 3 per second"
      threshold: 3
      unit: "flashes/second"
      source: "WCAG 2.3.1"

    - name: red_flash_saturation
      rule: "NOT (R >= 0.8 AND (R - G - B) >= 0.8) during flash"
      threshold: 0.8
      unit: "proportion of max"
      source: "ISO 9241-391"

    - name: flash_area
      rule: "combined_flash_area < 25% of 10-degree FOV"
      threshold: 25
      unit: "% of 341x256 px"
      source: "WCAG 2.3.1"

    - name: pattern_oscillation
      rule: "light_dark_pairs < 5 if oscillating"
      threshold: 5
      unit: "pairs"
      source: "ITU-R BT.1702-3"

    - name: cumulative_exposure
      rule: "flash_sequence_duration < 5 seconds"
      threshold: 5
      unit: "seconds"
      source: "Ofcom"

  tools:
    - name: "EA IRIS"
      url: "https://github.com/electronicarts"
      license: "BSD"

    - name: "PEAT"
      url: "https://trace.umd.edu/peat/"
      license: "Free for web"

    - name: "Apple VideoFlashingReduction"
      url: "https://github.com/apple/VideoFlashingReduction"
      license: "Open source"

    - name: "Harding FPA"
      url: "https://hardingtest.com/"
      license: "Commercial"

  error_message: |
    SEIZURE SAFETY VIOLATION
    This content may trigger seizures in susceptible individuals.
    Violation: {check_name}
    Measured: {measured_value}
    Threshold: {threshold_value}

    REQUIRED ACTION: Reduce flash frequency, desaturate red, or reduce flash area.
```

### CONTRAST_GATE (BLOCKING)

**Severity:** BLOCKING
**Applies to:** Theme files, stylesheets, color definitions

```yaml
contrast_gate:
  id: GATE-002
  severity: BLOCKING
  checks:
    - name: text_normal_contrast
      rule: "contrast_ratio(foreground, background) >= 4.5"
      threshold: 4.5
      unit: "ratio"
      source: "WCAG 1.4.3"
      applies_to: "text < 18pt"

    - name: text_large_contrast
      rule: "contrast_ratio(foreground, background) >= 3.0"
      threshold: 3.0
      unit: "ratio"
      source: "WCAG 1.4.3"
      applies_to: "text >= 18pt OR text >= 14pt bold"

    - name: ui_component_contrast
      rule: "contrast_ratio(component, adjacent) >= 3.0"
      threshold: 3.0
      unit: "ratio"
      source: "WCAG 1.4.11"
      applies_to: "buttons, form controls, icons"

    - name: focus_indicator_contrast
      rule: "contrast_ratio(focus, adjacent) >= 3.0"
      threshold: 3.0
      unit: "ratio"
      source: "WCAG 2.4.7"

    - name: focus_indicator_thickness
      rule: "outline_width >= 2"
      threshold: 2
      unit: "px"

  tools:
    - name: "WebAIM Contrast Checker"
      url: "https://webaim.org/resources/contrastchecker/"

    - name: "APCA Calculator"
      url: "https://www.myndex.com/APCA/"

    - name: "axe DevTools"
      url: "https://www.deque.com/axe/"

    - name: "Lighthouse"
      url: "chrome://inspect"

  error_message: |
    CONTRAST VIOLATION
    Text or UI components do not meet minimum contrast requirements.
    Element: {element_selector}
    Foreground: {fg_color}
    Background: {bg_color}
    Measured ratio: {measured_ratio}
    Required ratio: {required_ratio}

    REQUIRED ACTION: Increase lightness difference between foreground and background.
```

### CVD_GATE (WARNING)

**Severity:** WARNING (PR comments, but doesn't block)
**Applies to:** Palette definitions, semantic color roles

```yaml
cvd_gate:
  id: GATE-003
  severity: WARNING
  checks:
    - name: protan_discriminability
      rule: "deltaE_2000(color_a_simulated, color_b_simulated) >= 10"
      threshold: 10
      unit: "CIEDE2000"
      simulation: "Brettel 1997 protan"
      applies_to: "semantic role pairs (danger-ally, focus-disabled, etc.)"

    - name: deutan_discriminability
      rule: "deltaE_2000(color_a_simulated, color_b_simulated) >= 10"
      threshold: 10
      unit: "CIEDE2000"
      simulation: "Brettel 1997 deutan"

    - name: tritan_discriminability
      rule: "deltaE_2000(color_a_simulated, color_b_simulated) >= 8"
      threshold: 8
      unit: "CIEDE2000"
      simulation: "Brettel 1997 tritan"

    - name: non_color_redundancy
      rule: "every semantic role has pattern OR icon OR label"
      threshold: "exists"
      unit: "boolean"

  tools:
    - name: "DaltonLens"
      url: "https://daltonlens.org"

    - name: "colour-science"
      url: "https://colour-science.org"

    - name: "Color Oracle"
      url: "https://colororacle.org"

  warning_message: |
    CVD DISCRIMINABILITY WARNING
    Colors may be confusable for users with color vision deficiency.
    Role A: {role_a} ({color_a})
    Role B: {role_b} ({color_b})
    Delta-E under {cvd_type}: {delta_e}
    Minimum recommended: {threshold}

    RECOMMENDATION: Increase lightness contrast or add non-color redundancy.
```

### SPATIAL_GATE (WARNING)

**Severity:** WARNING
**Applies to:** UI components, layout definitions

```yaml
spatial_gate:
  id: GATE-004
  severity: WARNING
  checks:
    - name: touch_target_size
      rule: "min(width, height) >= 44"
      threshold: 44
      unit: "CSS px"
      source: "WCAG 2.5.5"

    - name: touch_target_spacing
      rule: "spacing_between_targets >= 8"
      threshold: 8
      unit: "px"

    - name: text_minimum_size
      rule: "font_size >= 16"
      threshold: 16
      unit: "px"

    - name: line_height
      rule: "line_height >= 1.5 * font_size"
      threshold: 1.5
      unit: "multiplier"
      source: "WCAG 1.4.12"

    - name: paragraph_spacing
      rule: "margin_bottom >= 2 * font_size"
      threshold: 2.0
      unit: "multiplier"

    - name: letter_spacing
      rule: "letter_spacing >= 0.12 * font_size"
      threshold: 0.12
      unit: "em"

    - name: word_spacing
      rule: "word_spacing >= 0.16 * font_size"
      threshold: 0.16
      unit: "em"

  warning_message: |
    SPATIAL ACCESSIBILITY WARNING
    Element: {element_selector}
    Issue: {check_name}
    Measured: {measured_value}
    Minimum: {threshold}

    RECOMMENDATION: {recommendation}
```

### DEPTH_GATE (WARNING)

**Severity:** WARNING
**Applies to:** 3D scenes, gameplay mechanics

```yaml
depth_gate:
  id: GATE-005
  severity: WARNING
  checks:
    - name: monocular_cue_static
      rule: "essential_depth_info.has_static_monocular_cue == true"
      applies_to: "depth-critical gameplay elements"

    - name: monocular_cue_order
      rule: "essential_depth_info.has_occlusion_or_order_cue == true"

    - name: monocular_cue_scale
      rule: "essential_depth_info.has_size_or_perspective_cue == true"

    - name: monocular_cue_edge
      rule: "essential_depth_info.has_outline_or_lighting_cue == true"

    - name: stereo_not_required
      rule: "gameplay_completable_with_stereo_disabled == true"

    - name: reduced_motion_depth_path
      rule: "reduced_motion_preserves_depth_meaning == true"

  warning_message: |
    DEPTH CUE WARNING
    Element: {element_name}
    Issue: Essential depth information lacks sufficient stereo-independent cues.
    Available cues: {cue_list}
    Missing: {missing_cues}

    RECOMMENDATION: Add static monocular cues first (occlusion/order, size/perspective,
    outline/lighting). Motion parallax may reinforce depth, but reduced-motion and
    stereo-disabled paths must preserve the same meaning.
```

### COGNITIVE_GATE (WARNING)

**Severity:** WARNING
**Applies to:** Navigation structures, HUD layouts, text content

```yaml
cognitive_gate:
  id: GATE-006
  severity: WARNING
  checks:
    - name: navigation_item_count
      rule: "menu_items <= 9"
      threshold: 9
      unit: "items"
      source: "Miller's Law"

    - name: nesting_depth
      rule: "max_nesting_depth <= 3"
      threshold: 3
      unit: "levels"

    - name: progressive_disclosure
      rule: "complex_content.has_summary_view == true"

    - name: reading_level
      rule: "flesch_kincaid_grade <= 9"
      threshold: 9
      unit: "grade level"
      source: "WCAG 3.1.5 (AAA)"

    - name: concurrent_notifications
      rule: "visible_notifications <= 3"
      threshold: 3
      unit: "items"

  warning_message: |
    COGNITIVE LOAD WARNING
    Location: {location}
    Issue: {check_name}
    Measured: {measured_value}
    Recommended maximum: {threshold}

    RECOMMENDATION: {recommendation}
```

### ACHROMAT_GATE (WARNING)

**Severity:** WARNING
**Applies to:** The `mono` token variant (achromatopsia / rod monochromacy simulation)

WHY: Rod monochromacy leaves no colour discrimination at all; the only perceptual
channel is luminance contrast. GATE-002 validates the default/CVD variants but does
not specifically audit the mono variant. GATE-007 fills that gap using the same BT.709
relative luminance formula as Simulator_Achromat and dl_simulate_cvd_achromat, keeping
the simulation and the validator internally consistent.

```yaml
achromat_gate:
  id: GATE-007
  severity: WARNING
  checks:
    - name: brand_primary_on_surface
      rule: "contrast_ratio(mono.brand.primary, mono.brand.surface) >= 4.5"
      threshold: 4.5
      unit: "ratio"
      source: "WCAG 1.4.3 (BT.709 luminance, consistent with GATE-002)"

    - name: brand_text_on_surface
      rule: "contrast_ratio(mono.brand.text, mono.brand.surface) >= 4.5"
      threshold: 4.5
      unit: "ratio"
      source: "WCAG 1.4.3"

    - name: brand_link_on_surface
      rule: "contrast_ratio(mono.brand.link, mono.brand.surface) >= 4.5"
      threshold: 4.5
      unit: "ratio"
      source: "WCAG 1.4.3"

    - name: viz_categorical_collapse
      rule: "categorical[0] != categorical[1] OR marker/dash redundancy present"
      source: "WCAG 1.4.1 (non-color redundancy for charts)"

  warning_message: |
    ACHROMAT (MONO) CONTRAST WARNING
    Token: {token_name}
    Foreground: {fg_color}
    Background: {bg_color}
    Measured ratio: {measured_ratio}
    Required ratio: 4.5:1 (WCAG AA) or 3.0:1 (large text / non-text UI)

    RECOMMENDATION: Darken the foreground token in the mono variant, or
    run "make mono-tokens" to re-derive all mono values from BT.709 luminance.
```

---

## 3. Implementation Guides

### JavaScript/TypeScript Validator

```typescript
// validators/seizure-check.ts
import { analyzeFlashRate, analyzeRedSaturation, analyzeFlashArea } from './flash-analysis';

export interface SeizureCheckResult {
  passed: boolean;
  violations: SeizureViolation[];
  warnings: SeizureWarning[];
}

export interface SeizureViolation {
  check: string;
  measured: number;
  threshold: number;
  timestamp?: number;
  frame?: number;
  severity: 'BLOCKING';
}

export async function checkSeizureSafety(videoPath: string): Promise<SeizureCheckResult> {
  const flashRate = await analyzeFlashRate(videoPath);
  const redSaturation = await analyzeRedSaturation(videoPath);
  const flashArea = await analyzeFlashArea(videoPath);

  const violations: SeizureViolation[] = [];

  // Check flash frequency
  for (const segment of flashRate.segments) {
    if (segment.flashesPerSecond > 3) {
      violations.push({
        check: 'flash_frequency',
        measured: segment.flashesPerSecond,
        threshold: 3,
        timestamp: segment.startTime,
        severity: 'BLOCKING'
      });
    }
  }

  // Check red flash saturation
  for (const flash of redSaturation.redFlashes) {
    if (flash.rValue >= 0.8 && (flash.rValue - flash.gValue - flash.bValue) >= 0.8) {
      violations.push({
        check: 'red_flash_saturation',
        measured: flash.rValue,
        threshold: 0.8,
        frame: flash.frame,
        severity: 'BLOCKING'
      });
    }
  }

  // Check flash area
  for (const flash of flashArea.flashEvents) {
    if (flash.areaPercent > 25) {
      violations.push({
        check: 'flash_area',
        measured: flash.areaPercent,
        threshold: 25,
        frame: flash.frame,
        severity: 'BLOCKING'
      });
    }
  }

  return {
    passed: violations.length === 0,
    violations,
    warnings: []
  };
}
```

### Python Validator

```python
# validators/contrast_check.py
from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class ContrastResult:
    passed: bool
    violations: List['ContrastViolation']

@dataclass
class ContrastViolation:
    check: str
    element: str
    foreground: str
    background: str
    measured_ratio: float
    required_ratio: float
    severity: str = 'BLOCKING'

def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Calculate relative luminance per WCAG 2.1"""
    def channel(c: int) -> float:
        c_srgb = c / 255
        if c_srgb <= 0.04045:
            return c_srgb / 12.92
        return ((c_srgb + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

def contrast_ratio(fg: Tuple[int, int, int], bg: Tuple[int, int, int]) -> float:
    """Calculate contrast ratio per WCAG 2.1"""
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def check_contrast(
    colors: List[dict],
    content_type: str = 'text_normal'
) -> ContrastResult:
    """Check color pairs against WCAG contrast requirements"""

    thresholds = {
        'text_normal': 4.5,
        'text_large': 3.0,
        'ui_component': 3.0,
        'focus_indicator': 3.0
    }

    required = thresholds.get(content_type, 4.5)
    violations = []

    for color_pair in colors:
        fg = tuple(color_pair['foreground'])
        bg = tuple(color_pair['background'])
        ratio = contrast_ratio(fg, bg)

        if ratio < required:
            violations.append(ContrastViolation(
                check=f'{content_type}_contrast',
                element=color_pair.get('element', 'unknown'),
                foreground=f'rgb{fg}',
                background=f'rgb{bg}',
                measured_ratio=round(ratio, 2),
                required_ratio=required
            ))

    return ContrastResult(
        passed=len(violations) == 0,
        violations=violations
    )
```

### CVD Simulation Validator

```python
# validators/cvd_check.py
import numpy as np
from colour import delta_E
from typing import Tuple, List

# Brettel 1997 simulation matrices (linearized sRGB space)
BRETTEL_PROTAN = np.array([
    [0.11238, 0.88762, 0.00000],
    [0.11238, 0.88762, 0.00000],
    [0.00401, -0.00401, 1.00000]
])

BRETTEL_DEUTAN = np.array([
    [0.29275, 0.70725, 0.00000],
    [0.29275, 0.70725, 0.00000],
    [-0.02234, 0.02234, 1.00000]
])

BRETTEL_TRITAN = np.array([
    [1.00000, 0.14461, -0.14461],
    [0.00000, 0.85924, 0.14076],
    [0.00000, 0.85924, 0.14076]
])

def srgb_to_linear(srgb: np.ndarray) -> np.ndarray:
    """Convert sRGB to linear RGB (gamma decode)"""
    return np.where(
        srgb <= 0.04045,
        srgb / 12.92,
        ((srgb + 0.055) / 1.055) ** 2.4
    )

def linear_to_srgb(linear: np.ndarray) -> np.ndarray:
    """Convert linear RGB to sRGB (gamma encode)"""
    return np.where(
        linear <= 0.0031308,
        12.92 * linear,
        1.055 * (linear ** (1/2.4)) - 0.055
    )

def simulate_cvd(rgb: np.ndarray, cvd_type: str) -> np.ndarray:
    """Simulate CVD using Brettel 1997"""
    matrices = {
        'protan': BRETTEL_PROTAN,
        'deutan': BRETTEL_DEUTAN,
        'tritan': BRETTEL_TRITAN
    }

    linear = srgb_to_linear(rgb / 255.0)
    simulated = np.dot(linear, matrices[cvd_type].T)
    simulated = np.clip(simulated, 0, 1)
    return linear_to_srgb(simulated) * 255

def check_cvd_discriminability(
    color_pairs: List[Tuple[str, np.ndarray, str, np.ndarray]],
    cvd_type: str = 'protan',
    threshold: float = 10.0
) -> dict:
    """Check if color pairs remain distinguishable under CVD simulation"""

    results = {
        'passed': True,
        'warnings': []
    }

    for role_a, color_a, role_b, color_b in color_pairs:
        sim_a = simulate_cvd(color_a, cvd_type)
        sim_b = simulate_cvd(color_b, cvd_type)

        # Convert to Lab for delta-E calculation
        # (simplified - use colour-science library for accurate Lab conversion)
        de = np.sqrt(np.sum((sim_a - sim_b) ** 2))  # Euclidean approximation

        if de < threshold:
            results['passed'] = False
            results['warnings'].append({
                'role_a': role_a,
                'role_b': role_b,
                'cvd_type': cvd_type,
                'delta_e': round(de, 2),
                'threshold': threshold,
                'recommendation': 'Increase lightness contrast or add non-color redundancy'
            })

    return results
```

---

## 4. CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/accessibility-validation.yml
name: Accessibility Validation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  seizure-safety:
    name: Seizure Safety Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install EA IRIS
        run: |
          pip install ea-iris

      - name: Check Video Assets
        run: |
          for video in assets/videos/*.mp4; do
            echo "Checking $video..."
            iris-cli analyze "$video" --strict --output json > results.json
            if [ $(jq '.violations | length' results.json) -gt 0 ]; then
              echo "SEIZURE SAFETY VIOLATION in $video"
              jq '.violations' results.json
              exit 1
            fi
          done

      - name: Check Animation Files
        run: |
          python scripts/check_animations.py animations/

  contrast-validation:
    name: Contrast Validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Dependencies
        run: npm ci

      - name: Check Theme Contrast
        run: |
          npx ts-node scripts/contrast-check.ts themes/*.json

      - name: Run axe-core
        run: |
          npx axe-cli http://localhost:3000 --tags wcag2a,wcag2aa

  cvd-simulation:
    name: CVD Discriminability
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install colour-science
        run: pip install colour-science numpy

      - name: Validate Palettes
        run: |
          python scripts/cvd_validate.py palettes/semantic-roles.json

  spatial-checks:
    name: Spatial Accessibility
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check Touch Targets
        run: |
          npx ts-node scripts/touch-target-audit.ts components/**/*.tsx

  report:
    name: Generate Report
    needs: [seizure-safety, contrast-validation, cvd-simulation, spatial-checks]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Generate Accessibility Report
        run: |
          echo "# Accessibility Validation Report" > report.md
          echo "" >> report.md
          echo "| Check | Status |" >> report.md
          echo "|-------|--------|" >> report.md
          echo "| Seizure Safety | ${{ needs.seizure-safety.result }} |" >> report.md
          echo "| Contrast | ${{ needs.contrast-validation.result }} |" >> report.md
          echo "| CVD Simulation | ${{ needs.cvd-simulation.result }} |" >> report.md
          echo "| Spatial | ${{ needs.spatial-checks.result }} |" >> report.md

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: accessibility-report
          path: report.md
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: contrast-check
        name: Contrast Validation
        entry: npx ts-node scripts/contrast-check.ts
        language: system
        files: \.(json|css|scss)$
        types: [file]

      - id: flash-check
        name: Flash Safety Lint
        entry: python scripts/flash_lint.py
        language: system
        files: \.(mp4|webm|gif)$
        types: [file]
```

---

## 5. Tool Integration Matrix

| Gate | Tool Options | License | Integration |
|------|--------------|---------|-------------|
| SEIZURE | EA IRIS | BSD | CLI, Python |
| SEIZURE | PEAT | Free (web) | CLI |
| SEIZURE | Apple VideoFlashingReduction | Open | Swift, Python |
| SEIZURE | Harding FPA | Commercial | Professional |
| CONTRAST | axe-core | MIT | npm, Browser |
| CONTRAST | WebAIM API | Free | HTTP API |
| CONTRAST | Lighthouse | Apache 2.0 | Chrome, CLI |
| CVD | DaltonLens | MIT | C, Python |
| CVD | colour-science | BSD | Python |
| CVD | Color Oracle | MIT | Java |
| SPATIAL | axe-core | MIT | npm |
| COGNITIVE | Flesch-Kincaid | Public | Various |

---

## 6. Error Handling and Reporting

### Violation Report Format

```json
{
  "report_version": "1.0.0",
  "timestamp": "2025-12-27T10:00:00Z",
  "summary": {
    "total_checks": 42,
    "passed": 38,
    "blocked": 2,
    "warnings": 2
  },
  "blocking_violations": [
    {
      "gate": "SEIZURE_GATE",
      "check": "flash_frequency",
      "file": "assets/videos/explosion.mp4",
      "location": "00:02:15 - 00:02:17",
      "measured": 8.5,
      "threshold": 3,
      "unit": "flashes/second",
      "action_required": "Reduce flash frequency below 3/second or reduce flash area below 25%"
    }
  ],
  "warnings": [
    {
      "gate": "CVD_GATE",
      "check": "protan_discriminability",
      "file": "palettes/game-colors.json",
      "roles": ["danger", "ally"],
      "measured_delta_e": 7.2,
      "threshold": 10,
      "recommendation": "Add icon or pattern redundancy to distinguish danger from ally"
    }
  ]
}
```

---

## 7. Typography Gate (UVAS+ Extension)

### TYPOGRAPHY_GATE (WARNING)

**Severity:** WARNING
**Applies to:** CSS files, design tokens, font definitions

```yaml
typography_gate:
  id: GATE-007
  severity: WARNING
  checks:
    - name: body_text_size
      rule: "font_size >= 16px"
      threshold: 16
      unit: "px"
      source: "WCAG 1.4.4"

    - name: line_height
      rule: "line_height >= 1.5"
      threshold: 1.5
      unit: "multiplier"
      source: "WCAG 1.4.12"

    - name: line_length
      rule: "max_width <= 80ch"
      threshold: 80
      unit: "characters"

    - name: letter_spacing
      rule: "letter_spacing >= 0"
      threshold: 0
      unit: "em"

    - name: all_caps_length
      rule: "uppercase_only_text <= 50 chars"
      threshold: 50
      unit: "characters"

    - name: font_disambiguation
      rule: "font_passes_confusion_test(['Il1', '0Oo', 'rnm'])"
      threshold: "all pairs distinct"

  tools:
    - name: "fonttools"
      url: "https://github.com/fonttools/fonttools"
      use: "Font metric extraction"

    - name: "Puppeteer/Playwright"
      use: "Rendered text measurement"

  warning_message: |
    TYPOGRAPHY WARNING
    Element: {element}
    Issue: {check_name}
    Measured: {measured_value}
    Threshold: {threshold}

    RECOMMENDATION: {recommendation}
```

### Typography Validator (Python)

```python
# validators/typography_check.py
from dataclasses import dataclass
from typing import List, Optional
import re

@dataclass
class TypographyViolation:
    check: str
    element: str
    measured: float
    threshold: float
    severity: str = 'WARNING'

def parse_css_value(value: str) -> tuple[float, str]:
    """Parse CSS value like '16px' or '1.5em' into (number, unit)"""
    match = re.match(r'([\d.]+)(px|em|rem|pt|ch|%)?', value.strip())
    if match:
        return float(match.group(1)), match.group(2) or ''
    return 0, ''

def check_typography(css_rules: dict) -> List[TypographyViolation]:
    """Validate typography rules against UVAS requirements"""
    violations = []

    # Check font-size
    if 'font-size' in css_rules:
        size, unit = parse_css_value(css_rules['font-size'])
        if unit == 'px' and size < 16:
            violations.append(TypographyViolation(
                check='body_text_size',
                element=css_rules.get('selector', 'unknown'),
                measured=size,
                threshold=16
            ))

    # Check line-height
    if 'line-height' in css_rules:
        height, unit = parse_css_value(css_rules['line-height'])
        if height < 1.5 and unit == '':  # Unitless line-height
            violations.append(TypographyViolation(
                check='line_height',
                element=css_rules.get('selector', 'unknown'),
                measured=height,
                threshold=1.5
            ))

    # Check max-width for text containers
    if 'max-width' in css_rules:
        width, unit = parse_css_value(css_rules['max-width'])
        if unit == 'ch' and width > 80:
            violations.append(TypographyViolation(
                check='line_length',
                element=css_rules.get('selector', 'unknown'),
                measured=width,
                threshold=80
            ))

    # Check negative letter-spacing
    if 'letter-spacing' in css_rules:
        spacing, unit = parse_css_value(css_rules['letter-spacing'])
        if spacing < 0:
            violations.append(TypographyViolation(
                check='letter_spacing',
                element=css_rules.get('selector', 'unknown'),
                measured=spacing,
                threshold=0
            ))

    return violations
```

---

## 8. Layout Gate (UVAS+ Extension)

### LAYOUT_GATE (WARNING)

**Severity:** WARNING
**Applies to:** UI components, layout files, responsive designs

```yaml
layout_gate:
  id: GATE-008
  severity: WARNING
  checks:
    - name: touch_target_size
      rule: "min(width, height) >= 44px"
      threshold: 44
      unit: "CSS px"
      source: "WCAG 2.5.5"

    - name: touch_target_spacing
      rule: "gap_between_adjacent_targets >= 8px"
      threshold: 8
      unit: "px"

    - name: focus_indicator_present
      rule: "focusable_element.has_focus_style == true"
      threshold: "exists"

    - name: focus_indicator_contrast
      rule: "focus_outline_contrast >= 3.0"
      threshold: 3.0
      unit: "ratio"
      source: "WCAG 2.4.7"

    - name: nav_depth
      rule: "menu_nesting_depth <= 4"
      threshold: 4
      unit: "levels"

    - name: nav_items_per_level
      rule: "items_per_nav_level <= 9"
      threshold: 9
      unit: "items"
      source: "Miller's Law"

    - name: heading_hierarchy
      rule: "no_skipped_heading_levels"
      threshold: "pass"

  tools:
    - name: "axe-core"
      url: "https://github.com/dequelabs/axe-core"
      use: "DOM accessibility audit"

    - name: "Playwright/Puppeteer"
      use: "Element bounding box measurement"

  warning_message: |
    LAYOUT WARNING
    Element: {element}
    Issue: {check_name}
    Measured: {measured_value}
    Threshold: {threshold}

    RECOMMENDATION: {recommendation}
```

### REFLOW_GATE (WARNING)

**Severity:** WARNING
**Applies to:** Responsive layouts at zoom levels

```yaml
reflow_gate:
  id: GATE-009
  severity: WARNING
  test_scales: [1.0, 1.25, 1.5, 2.0]
  checks:
    - name: no_horizontal_scroll
      rule: "document.scrollWidth <= viewport.width"
      source: "WCAG 1.4.10"

    - name: no_truncation
      rule: "truncated_elements.all(e => e.has_accessible_expansion)"

    - name: no_overlap
      rule: "interactive_elements.no_bounding_box_intersections"

    - name: touch_targets_scaled
      rule: "min_target_size >= 44px at all scales"

    - name: reading_order_preserved
      rule: "dom_order == visual_order"

  warning_message: |
    REFLOW WARNING at {scale}x zoom
    Issue: {check_name}
    Details: {details}

    RECOMMENDATION: Implement responsive reflow.
```

### Layout Validator (TypeScript)

```typescript
// validators/layout-check.ts
interface LayoutViolation {
  check: string;
  element: string;
  measured: number;
  threshold: number;
  severity: 'WARNING' | 'BLOCKING';
}

interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

function boxesOverlap(a: BoundingBox, b: BoundingBox): boolean {
  return !(
    a.x + a.width < b.x ||
    b.x + b.width < a.x ||
    a.y + a.height < b.y ||
    b.y + b.height < a.y
  );
}

export function checkTouchTargets(
  elements: Array<{ selector: string; box: BoundingBox }>
): LayoutViolation[] {
  const violations: LayoutViolation[] = [];

  for (const el of elements) {
    const minDimension = Math.min(el.box.width, el.box.height);
    if (minDimension < 44) {
      violations.push({
        check: 'touch_target_size',
        element: el.selector,
        measured: minDimension,
        threshold: 44,
        severity: 'WARNING'
      });
    }
  }

  // Check for overlaps
  for (let i = 0; i < elements.length; i++) {
    for (let j = i + 1; j < elements.length; j++) {
      if (boxesOverlap(elements[i].box, elements[j].box)) {
        violations.push({
          check: 'element_overlap',
          element: `${elements[i].selector} / ${elements[j].selector}`,
          measured: 0,
          threshold: 0,
          severity: 'WARNING'
        });
      }
    }
  }

  return violations;
}

export function checkHeadingHierarchy(
  headings: Array<{ tag: string; text: string }>
): LayoutViolation[] {
  const violations: LayoutViolation[] = [];
  let lastLevel = 0;

  for (const h of headings) {
    const level = parseInt(h.tag.replace('H', ''), 10);
    if (lastLevel > 0 && level > lastLevel + 1) {
      violations.push({
        check: 'heading_hierarchy',
        element: `${h.tag}: "${h.text.substring(0, 30)}..."`,
        measured: level,
        threshold: lastLevel + 1,
        severity: 'WARNING'
      });
    }
    lastLevel = level;
  }

  return violations;
}
```

---

## 9. Visualization Gate (UVAS+ Extension)

### VIZ_GATE (WARNING)

**Severity:** WARNING (color-only encoding is BLOCKING)
**Applies to:** Charts, graphs, data visualizations

```yaml
viz_gate:
  id: GATE-010
  severity: WARNING
  checks:
    - name: color_only_encoding
      rule: "every_category.has_non_color_channel"
      threshold: "true"
      severity_override: BLOCKING
      source: "WCAG 1.4.1"

    - name: legend_item_count
      rule: "legend_items <= 8"
      threshold: 8
      unit: "items"

    - name: annotation_density
      rule: "annotations_per_panel <= 5"
      threshold: 5
      unit: "annotations"

    - name: line_stroke_width
      rule: "line_stroke_width >= 1.0pt"
      threshold: 1.0
      unit: "pt"

    - name: text_minimum_size
      rule: "chart_text_size >= 8pt at export"
      threshold: 8
      unit: "pt"

    - name: contrast_text_on_background
      rule: "text_contrast >= 4.5"
      threshold: 4.5
      unit: "ratio"

  tools:
    - name: "colour-science"
      url: "https://colour-science.org"
      use: "CVD simulation, delta-E calculation"

    - name: "matplotlib accessibility"
      use: "Built-in accessibility checks"

  warning_message: |
    VISUALIZATION WARNING
    Chart: {chart_id}
    Issue: {check_name}
    Measured: {measured_value}
    Threshold: {threshold}

    RECOMMENDATION: {recommendation}
```

### Visualization Validator (Python)

```python
# validators/viz_check.py
from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np

@dataclass
class VizViolation:
    check: str
    chart_id: str
    measured: Any
    threshold: Any
    severity: str = 'WARNING'

def check_color_encoding(
    categories: List[Dict],
) -> List[VizViolation]:
    """
    Check that every category has non-color encoding.

    Each category dict should have:
    - 'name': category name
    - 'color': hex color
    - 'marker': marker shape (optional)
    - 'linestyle': line style (optional)
    - 'pattern': hatch pattern (optional)
    - 'label': text label (optional)
    """
    violations = []

    for cat in categories:
        has_non_color = any([
            cat.get('marker'),
            cat.get('linestyle') and cat.get('linestyle') != 'solid',
            cat.get('pattern'),
            cat.get('label')
        ])

        if not has_non_color:
            violations.append(VizViolation(
                check='color_only_encoding',
                chart_id=cat.get('chart_id', 'unknown'),
                measured=f"Category '{cat['name']}' has color only",
                threshold="color + non-color channel required",
                severity='BLOCKING'
            ))

    return violations

def check_legend_size(
    legend_items: int,
    chart_id: str
) -> List[VizViolation]:
    """Check legend doesn't exceed cognitive limit."""
    violations = []

    if legend_items > 8:
        violations.append(VizViolation(
            check='legend_item_count',
            chart_id=chart_id,
            measured=legend_items,
            threshold=8,
            severity='WARNING'
        ))

    return violations

def check_stroke_width(
    strokes: List[Dict],
    chart_id: str
) -> List[VizViolation]:
    """Check line stroke widths meet minimum."""
    violations = []

    for stroke in strokes:
        if stroke.get('width', 0) < 1.0:
            violations.append(VizViolation(
                check='line_stroke_width',
                chart_id=chart_id,
                measured=stroke.get('width'),
                threshold=1.0,
                severity='WARNING'
            ))

    return violations

def check_text_sizes(
    text_elements: List[Dict],
    export_dpi: int,
    chart_id: str
) -> List[VizViolation]:
    """Check all text meets minimum size at export resolution."""
    violations = []

    for text in text_elements:
        size_pt = text.get('size_pt', 0)
        if size_pt < 8:
            violations.append(VizViolation(
                check='text_minimum_size',
                chart_id=chart_id,
                measured=size_pt,
                threshold=8,
                severity='WARNING'
            ))

    return violations
```

---

## 10. Temporal Safety Validators (Display Adaptation Layer)

### 10.1 FLASH_GATE — Seizure-Safe Flash Limits (Enhanced)

**Purpose:** Prevent content-induced photosensitive seizures using time-domain (not frame-count) analysis.

**Category:** BLOCKING (CI will fail on violation)

**Key Difference from SEIZURE_GATE:** FLASH_GATE operates in the time domain and is frame-rate independent. It works identically whether content is displayed at 10 Hz or 480 Hz.

**Evidence:**
- W3C WCAG 2.2 Success Criterion 2.3.1: "No more than three flashes in any one-second period"
- Epilepsy Action: Photosensitive epilepsy risk peaks at 10-25 Hz frequency band
- ISO 9241-391:2016: Reduction of photosensitive seizures
- International Guidelines for Photosensitive Epilepsy (2024 PMC review)

```yaml
flash_gate:
  id: GATE-T01
  severity: BLOCKING
  domain: time  # NOT frame-count
  checks:
    - name: flash_rate_per_second
      rule: "flashes_per_second <= 3"
      threshold: 3
      unit: "flashes/second"
      source: "WCAG 2.3.1"
      note: "Counted in 1-second sliding windows, independent of display refresh rate"

    - name: high_risk_frequency_band
      rule: "NO sustained luminance oscillation in 10-25 Hz band"
      band_hz: [10, 25]
      severity_override: BLOCKING
      source: "Epilepsy Action, ISO 9241-391"
      note: "Use FFT spectral analysis on luminance signal"

    - name: flash_luminance_delta
      rule: "qualifying_flash_delta >= 10%"
      threshold: 0.10
      unit: "relative luminance"
      note: "A flash is a pair of opposing changes ≥10% where darker state < 0.80"

    - name: flash_area_limit
      rule: "combined_flash_area < 25% of viewport"
      threshold: 25
      unit: "percent"
      source: "WCAG 2.3.1"

    - name: red_flash_special_case
      rule: "red_saturation_during_flash < 0.8"
      threshold: 0.8
      note: "Red flashes are higher risk; R/(R+G+B) > 0.8 triggers stricter limits"

  implementation:
    analysis_method: "sliding_window_1_second"
    spectral_analysis: "FFT for 10-25 Hz detection"
    frame_rate_independent: true

  tools:
    - name: "EA IRIS"
      url: "https://github.com/electronicarts"
    - name: "PEAT"
      url: "https://trace.umd.edu/peat/"
    - name: "Apple VideoFlashingReduction"
      url: "https://github.com/apple/VideoFlashingReduction"
```

**Python Implementation:**

```python
# validators/flash_gate.py
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class FlashViolation:
    type: str
    time_sec: float
    measured: float
    threshold: float
    severity: str = 'BLOCKING'
    message: str = ''

class FlashGate:
    """
    Time-domain flash analysis (frame-rate independent).

    Works identically whether content is 10 Hz or 480 Hz because we
    analyze in time, not frame counts.
    """

    MAX_FLASHES_PER_SECOND = 3
    HIGH_RISK_BAND_HZ = (10, 25)
    MIN_FLASH_DELTA = 0.10
    DARK_STATE_MAX = 0.80
    MAX_FLASH_AREA_RATIO = 0.25

    def validate_sequence(
        self,
        luminance_values: np.ndarray,
        timestamps_sec: np.ndarray
    ) -> List[FlashViolation]:
        """
        Validate luminance sequence for flash violations.

        Args:
            luminance_values: Per-frame average luminance [0,1]
            timestamps_sec: Timestamp for each frame in seconds
        """
        violations = []
        duration = timestamps_sec[-1] - timestamps_sec[0]

        # Sliding 1-second window
        window_sec = 1.0
        step_sec = 0.1  # 100ms step

        t = timestamps_sec[0]
        while t + window_sec <= timestamps_sec[-1]:
            # Get frames in this window
            mask = (timestamps_sec >= t) & (timestamps_sec < t + window_sec)
            window_lum = luminance_values[mask]
            window_times = timestamps_sec[mask]

            # Count flashes in window
            flash_count = self._count_flashes(window_lum)

            if flash_count > self.MAX_FLASHES_PER_SECOND:
                violations.append(FlashViolation(
                    type='FLASH_RATE_EXCEEDED',
                    time_sec=t,
                    measured=flash_count,
                    threshold=self.MAX_FLASHES_PER_SECOND,
                    message=f'{flash_count} flashes/sec at t={t:.2f}s (max: 3)'
                ))

            # Spectral analysis for high-risk band
            if len(window_lum) >= 4:
                dominant_freq = self._analyze_frequency(window_lum, window_times)
                if self.HIGH_RISK_BAND_HZ[0] <= dominant_freq <= self.HIGH_RISK_BAND_HZ[1]:
                    violations.append(FlashViolation(
                        type='HIGH_RISK_FREQUENCY',
                        time_sec=t,
                        measured=dominant_freq,
                        threshold=self.HIGH_RISK_BAND_HZ,
                        message=f'{dominant_freq:.1f}Hz in seizure-risk band (10-25Hz)'
                    ))

            t += step_sec

        return violations

    def _count_flashes(self, luminance: np.ndarray) -> int:
        """Count qualifying flash transitions."""
        flashes = 0
        in_bright = None

        for i in range(1, len(luminance)):
            delta = luminance[i] - luminance[i-1]

            if abs(delta) >= self.MIN_FLASH_DELTA:
                darker = min(luminance[i], luminance[i-1])
                if darker < self.DARK_STATE_MAX:
                    currently_bright = delta > 0
                    if in_bright is not None and currently_bright != in_bright:
                        flashes += 1
                    in_bright = currently_bright

        return flashes

    def _analyze_frequency(
        self,
        luminance: np.ndarray,
        times: np.ndarray
    ) -> float:
        """FFT-based dominant frequency detection."""
        if len(luminance) < 4:
            return 0.0

        # Estimate sample rate from timestamps
        dt = np.mean(np.diff(times))
        fs = 1.0 / dt if dt > 0 else 60.0

        # FFT
        fft = np.fft.rfft(luminance - np.mean(luminance))
        freqs = np.fft.rfftfreq(len(luminance), 1/fs)

        # Find dominant frequency (skip DC)
        magnitudes = np.abs(fft)[1:]
        freqs = freqs[1:]

        if len(magnitudes) > 0:
            return freqs[np.argmax(magnitudes)]
        return 0.0
```

---

### 10.2 VRR_FLICKER_GATE — Variable Refresh Rate Safety

**Purpose:** Reduce content patterns that aggravate VRR-induced brightness modulation and overdrive artifacts.

**Category:** WARNING (advisory, promotes flicker-safe mode)

**Context:** VRR (Adaptive-Sync, FreeSync, G-SYNC) dynamically varies refresh rate. This can cause:
- Brightness flicker at lower VRR ranges
- Overdrive artifacts (ghosting, coronas)
- PWM interaction on OLED panels

We cannot fix monitor hardware, but we CAN reduce provocative content patterns.

**Evidence:**
- VESA Adaptive-Sync Whitepaper (2014)
- User reports of VRR-related visual discomfort
- OLED PWM dimming interactions

```yaml
vrr_flicker_gate:
  id: GATE-T02
  severity: WARNING
  checks:
    - name: large_area_luminance_delta
      rule: "per_frame_luminance_swing < 30%"
      threshold: 0.30
      unit: "relative luminance delta"
      area_threshold: 0.40
      note: "Large-area (>40% viewport) rapid brightness changes aggravate VRR flicker"

    - name: rapid_alternation_pattern
      rule: "no A-B-A-B patterns over 2 cycles"
      threshold: 2
      unit: "cycles"
      note: "Alternating high-contrast frames interact poorly with VRR timing"

    - name: vrr_low_range_awareness
      rule: "reduce_modulation_when_vrr_active"
      note: "VRR's lower refresh range (e.g., 48-60 Hz) is most prone to flicker"

  vrr_safe_mode:
    max_luminance_delta: 0.15  # Halved from normal
    min_transition_frames: 3
    avoid_patterns:
      - alternating_high_contrast
      - rapid_brightness_pulse
      - camera_shake
    prefer_eased_transitions: true

  warning_message: |
    VRR FLICKER WARNING
    Content pattern may cause flicker on VRR displays.
    Pattern: {pattern_type}
    Measured delta: {measured_delta}
    Threshold: {threshold}

    RECOMMENDATION: Add intermediate frames to smooth transitions.
    Enable VRR-safe mode for flicker-sensitive users.
```

**Python Implementation:**

```python
# validators/vrr_flicker_gate.py
from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class VRRWarning:
    type: str
    frame: int
    measured: float
    threshold: float
    suggestion: str

class VRRFlickerGate:
    """
    Detects content patterns that interact poorly with VRR displays.
    """

    MAX_AREA_LUMINANCE_DELTA = 0.30
    LARGE_AREA_THRESHOLD = 0.40  # 40% of viewport
    MAX_ALTERNATION_CYCLES = 2

    def validate_sequence(
        self,
        frames: List[np.ndarray],
        vrr_active: bool = True
    ) -> List[VRRWarning]:
        """Check frame sequence for VRR-aggravating patterns."""
        if not vrr_active:
            return []

        warnings = []

        # Check large-area luminance swings
        for i in range(1, len(frames)):
            avg_lum_prev = self._large_area_luminance(frames[i-1])
            avg_lum_curr = self._large_area_luminance(frames[i])
            delta = abs(avg_lum_curr - avg_lum_prev)

            if delta > self.MAX_AREA_LUMINANCE_DELTA:
                warnings.append(VRRWarning(
                    type='VRR_LUMINANCE_SWING',
                    frame=i,
                    measured=delta,
                    threshold=self.MAX_AREA_LUMINANCE_DELTA,
                    suggestion='Add intermediate frames to smooth transition'
                ))

        # Detect A-B-A-B alternation patterns
        alternation_count = self._count_alternations(frames)
        if alternation_count >= self.MAX_ALTERNATION_CYCLES:
            warnings.append(VRRWarning(
                type='VRR_RAPID_ALTERNATION',
                frame=0,
                measured=alternation_count,
                threshold=self.MAX_ALTERNATION_CYCLES,
                suggestion='Replace A-B-A-B pattern with gradual transition'
            ))

        return warnings

    def _large_area_luminance(self, frame: np.ndarray) -> float:
        """Compute luminance of largest uniform region."""
        # Simplified: use mean luminance
        return np.mean(frame)

    def _count_alternations(self, frames: List[np.ndarray]) -> int:
        """Count A-B-A-B alternation cycles."""
        if len(frames) < 4:
            return 0

        alternations = 0
        for i in range(len(frames) - 2):
            sim_02 = self._similarity(frames[i], frames[i+2])
            sim_01 = self._similarity(frames[i], frames[i+1])

            if sim_02 > 0.95 and sim_01 < 0.70:
                alternations += 1

        return alternations

    def _similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Frame similarity (1.0 = identical)."""
        diff = np.abs(a.astype(float) - b.astype(float))
        return 1.0 - (np.mean(diff) / 255.0)

    def get_safe_mode_config(self) -> Dict:
        """Return VRR-safe mode configuration."""
        return {
            'max_luminance_delta': 0.15,
            'min_transition_frames': 3,
            'prefer_eased_transitions': True,
            'avoid_patterns': [
                'alternating_high_contrast',
                'rapid_brightness_pulse',
                'camera_shake'
            ]
        }
```

---

### 10.3 EINK_MODE_GATE — Electrophoretic Display Adaptation

**Purpose:** Validate content appropriateness for e-ink and slow-refresh displays.

**Category:** ADVISORY (enables graceful degradation)

**Context:** E-ink displays have fundamentally different characteristics:
- Slow refresh (typically 1-10 Hz for full refresh)
- Partial refresh faster but with ghosting
- Persistence (image stays without power)
- High contrast in ambient light
- No backlight flicker

Content must adapt to work well on these displays.

**Evidence:**
- IEEE Spectrum: E-paper display technology advances
- E-ink panel specifications (10 Hz modern high-speed)
- Persistence-based display semantics

```yaml
eink_mode_gate:
  id: GATE-T03
  severity: ADVISORY
  checks:
    - name: animation_duration
      rule: "animation_duration >= 200ms"
      threshold: 200
      unit: "ms"
      note: "Faster animations look broken on e-ink"

    - name: continuous_animation
      rule: "no infinite loop animations"
      forbidden: true
      alternatives: "state-change icons, progress bars with text"

    - name: blinking_elements
      rule: "no blinking cursors or pulsing highlights"
      forbidden: true
      alternatives: "solid cursor, persistent border highlight"

    - name: smooth_scroll
      rule: "prefer page-flip over smooth scroll"
      alternatives: "paginated navigation with clear indicators"

    - name: feedback_dwell_time
      rule: "transient_feedback_duration >= 2000ms"
      threshold: 2000
      unit: "ms"
      note: "E-ink users need longer feedback visibility"

  forbidden_patterns:
    - continuous_animation
    - blinking_cursor
    - loading_spinner
    - shimmer_effect
    - pulsing_highlight
    - smooth_scroll

  eink_alternatives:
    continuous_animation: "state-change icons or text updates"
    blinking_cursor: "solid cursor with underline"
    loading_spinner: "progress bar with percentage text"
    shimmer_effect: "solid placeholder shapes"
    pulsing_highlight: "persistent highlight with border"
    smooth_scroll: "page-flip navigation with clear indicators"

  profile:
    max_refresh_hz: 10
    prefer_state_changes: true
    avoid_continuous_motion: true
    dwell_time_multiplier: 2.0
    use_page_navigation: true
```

**Python Implementation:**

```python
# validators/eink_mode_gate.py
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class EinkIssue:
    type: str
    element: str
    severity: str  # 'ERROR' or 'WARNING'
    suggestion: str

class EinkModeGate:
    """
    Validate content for e-ink display compatibility.
    """

    MIN_ANIMATION_MS = 200
    MIN_FEEDBACK_DWELL_MS = 2000

    FORBIDDEN_PATTERNS = {
        'continuous_animation': 'Use state-change icons or text updates',
        'blinking_cursor': 'Use solid cursor with underline',
        'loading_spinner': 'Use progress bar with percentage text',
        'shimmer_effect': 'Use solid placeholder shapes',
        'pulsing_highlight': 'Use persistent highlight with border',
        'smooth_scroll': 'Use page-flip navigation with indicators'
    }

    def validate_content(
        self,
        animations: List[Dict],
        feedback_elements: List[Dict],
        detected_patterns: List[str],
        eink_mode: bool = True
    ) -> List[EinkIssue]:
        """Validate UI content for e-ink appropriateness."""
        if not eink_mode:
            return []

        issues = []

        # Check animation durations
        for anim in animations:
            duration = anim.get('duration_ms', 0)
            if duration < self.MIN_ANIMATION_MS:
                issues.append(EinkIssue(
                    type='ANIMATION_TOO_FAST',
                    element=anim.get('name', 'unknown'),
                    severity='WARNING',
                    suggestion=f'Increase duration to ≥{self.MIN_ANIMATION_MS}ms'
                ))

            if anim.get('loops') == 'infinite' or anim.get('is_continuous'):
                issues.append(EinkIssue(
                    type='CONTINUOUS_ANIMATION',
                    element=anim.get('name', 'unknown'),
                    severity='ERROR',
                    suggestion='Replace with state-based feedback'
                ))

        # Check forbidden patterns
        for pattern in detected_patterns:
            if pattern in self.FORBIDDEN_PATTERNS:
                issues.append(EinkIssue(
                    type='FORBIDDEN_PATTERN',
                    element=pattern,
                    severity='ERROR',
                    suggestion=self.FORBIDDEN_PATTERNS[pattern]
                ))

        # Check feedback dwell times
        for feedback in feedback_elements:
            duration = feedback.get('duration_ms', 0)
            if duration < self.MIN_FEEDBACK_DWELL_MS:
                issues.append(EinkIssue(
                    type='SHORT_FEEDBACK',
                    element=feedback.get('name', 'unknown'),
                    severity='WARNING',
                    suggestion=f'Increase to ≥{self.MIN_FEEDBACK_DWELL_MS}ms for e-ink visibility'
                ))

        return issues

    def get_eink_profile(self) -> Dict:
        """Return complete e-ink adaptation profile."""
        return {
            'display_type': 'e-ink',
            'max_refresh_hz': 10,
            'constraints': {
                'prefer_state_changes': True,
                'avoid_continuous_motion': True,
                'dwell_time_multiplier': 2.0,
                'use_page_navigation': True
            },
            'adaptations': {
                'animations': 'disabled_or_minimal',
                'transitions': 'instant_or_fade_500ms',
                'scrolling': 'page_flip',
                'cursors': 'solid_persistent',
                'loading': 'progress_bar_with_text',
                'highlights': 'border_based'
            },
            'benefits': [
                'Excellent battery (persistence)',
                'Excellent sunlight readability',
                'Reduced eye strain (no backlight)',
                'Zero flicker (reflective)'
            ]
        }
```

---

### 10.4 TEMPORAL_STABILITY_GATE — Frame Pacing and Motion Consistency

**Purpose:** Validate temporal consistency of animations and visual updates to prevent perceptual jitter, stuttering, and motion-induced discomfort.

**Category:** WARNING (degrades UX and can trigger vestibular sensitivity)

**Context:** Even when content is flash-safe and VRR-compatible, inconsistent frame timing creates perceptual problems:
- Frame pacing jitter causes stuttering even at high frame rates
- Inconsistent animation timing feels "laggy" or "broken"
- Erratic motion patterns can trigger vestibular sensitivity
- E-ink displays require state-change semantics, not continuous oscillation

**Evidence:**
- Digital Foundry: Frame pacing analysis methodology
- WCAG 2.1 SC 2.3.3: Animation from Interactions (AAA)
- Vestibular Disorders Association: Motion sensitivity triggers
- ISO 9241-112:2017: Dialogue principles (temporal consistency)

```yaml
temporal_stability_gate:
  id: GATE-T04
  severity: WARNING
  checks:
    - name: frame_pacing_variance
      rule: "frame_time_deviation <= 10% of intended_period"
      threshold: 0.10
      unit: "ratio"
      note: "Jitter beyond 10% creates visible stuttering"

    - name: animation_cadence_consistency
      rule: "animation_step_variance <= 15% of mean_step"
      threshold: 0.15
      unit: "ratio"
      note: "Animation keyframe timing should be consistent"

    - name: motion_predictability
      rule: "motion_direction_reversals <= 2 per animation"
      threshold: 2
      unit: "reversals"
      note: "Erratic direction changes trigger vestibular discomfort"

    - name: oscillation_avoidance
      rule: "no value oscillation without damping"
      forbidden: true
      note: "Values should converge, not oscillate indefinitely"

    - name: eink_state_semantics
      rule: "prefer discrete state changes over continuous updates"
      context: "eink_mode"
      note: "E-ink displays should see step functions, not gradients"

  motion_quality_metrics:
    target_frame_time_ms: 16.67  # 60 Hz reference
    acceptable_jitter_ms: 1.67   # 10% of 16.67ms
    max_dropped_frames_consecutive: 2
    animation_easing_required: true

  vestibular_safety:
    max_parallax_ratio: 0.5
    max_zoom_speed: 2.0  # stops/second
    max_rotation_speed: 45  # degrees/second
    require_reduce_motion_support: true

  eink_constraints:
    prefer_state_changes: true
    min_state_dwell_ms: 500
    avoid_oscillation: true
    use_discrete_steps: true
```

**Python Implementation:**

```python
# validators/temporal_stability_gate.py
import numpy as np
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class StabilityIssueType(Enum):
    FRAME_JITTER = "frame_jitter"
    CADENCE_VARIANCE = "cadence_variance"
    ERRATIC_MOTION = "erratic_motion"
    UNDAMPED_OSCILLATION = "undamped_oscillation"
    EINK_CONTINUOUS_UPDATE = "eink_continuous_update"
    VESTIBULAR_TRIGGER = "vestibular_trigger"

@dataclass
class TemporalStabilityIssue:
    type: StabilityIssueType
    location: str
    measured: float
    threshold: float
    severity: str
    suggestion: str

class TemporalStabilityGate:
    """
    Validate temporal consistency and motion quality.

    Ensures animations and visual updates are smooth, predictable,
    and appropriate for the display type (including e-ink).
    """

    # Frame pacing thresholds
    MAX_JITTER_RATIO = 0.10  # 10% of intended frame period
    MAX_CADENCE_VARIANCE = 0.15  # 15% step variance

    # Motion quality
    MAX_DIRECTION_REVERSALS = 2
    OSCILLATION_DAMPING_THRESHOLD = 0.1  # Must decay to 10%

    # Vestibular safety
    MAX_PARALLAX_RATIO = 0.5
    MAX_ZOOM_SPEED = 2.0  # stops/sec
    MAX_ROTATION_SPEED = 45.0  # deg/sec

    # E-ink constraints
    EINK_MIN_DWELL_MS = 500

    def validate_frame_pacing(
        self,
        frame_times_ms: np.ndarray,
        target_period_ms: float = 16.67
    ) -> List[TemporalStabilityIssue]:
        """
        Validate frame timing consistency.

        Args:
            frame_times_ms: Timestamps of each rendered frame
            target_period_ms: Expected frame period (e.g., 16.67ms for 60Hz)
        """
        issues = []

        if len(frame_times_ms) < 3:
            return issues

        # Calculate inter-frame intervals
        intervals = np.diff(frame_times_ms)
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)

        # Check jitter against target
        jitter_ratio = std_interval / target_period_ms

        if jitter_ratio > self.MAX_JITTER_RATIO:
            issues.append(TemporalStabilityIssue(
                type=StabilityIssueType.FRAME_JITTER,
                location="frame_timing",
                measured=jitter_ratio,
                threshold=self.MAX_JITTER_RATIO,
                severity="WARNING",
                suggestion=f"Frame jitter {jitter_ratio:.1%} exceeds {self.MAX_JITTER_RATIO:.0%} threshold. "
                           "Ensure consistent render loop timing."
            ))

        # Check for dropped frames (intervals > 2x target)
        dropped_frames = np.sum(intervals > target_period_ms * 2)
        if dropped_frames > 0:
            dropped_ratio = dropped_frames / len(intervals)
            if dropped_ratio > 0.05:  # More than 5% dropped
                issues.append(TemporalStabilityIssue(
                    type=StabilityIssueType.FRAME_JITTER,
                    location="frame_drops",
                    measured=dropped_ratio,
                    threshold=0.05,
                    severity="WARNING",
                    suggestion=f"{dropped_frames} frames dropped ({dropped_ratio:.1%}). "
                               "Optimize render performance."
                ))

        return issues

    def validate_animation_cadence(
        self,
        keyframe_times_ms: np.ndarray,
        keyframe_values: np.ndarray
    ) -> List[TemporalStabilityIssue]:
        """
        Validate animation keyframe timing consistency.

        Animation should progress at consistent rate without stuttering.
        """
        issues = []

        if len(keyframe_times_ms) < 3:
            return issues

        # Calculate progress steps
        time_steps = np.diff(keyframe_times_ms)
        value_steps = np.diff(keyframe_values)

        # Velocity at each step
        velocities = value_steps / time_steps
        mean_velocity = np.mean(np.abs(velocities))
        velocity_variance = np.std(np.abs(velocities)) / mean_velocity if mean_velocity > 0 else 0

        if velocity_variance > self.MAX_CADENCE_VARIANCE:
            issues.append(TemporalStabilityIssue(
                type=StabilityIssueType.CADENCE_VARIANCE,
                location="animation_velocity",
                measured=velocity_variance,
                threshold=self.MAX_CADENCE_VARIANCE,
                severity="WARNING",
                suggestion=f"Animation velocity variance {velocity_variance:.1%} exceeds threshold. "
                           "Use consistent easing or linear interpolation."
            ))

        return issues

    def validate_motion_predictability(
        self,
        position_sequence: np.ndarray,
        time_sequence_ms: np.ndarray
    ) -> List[TemporalStabilityIssue]:
        """
        Validate that motion is predictable and not erratic.

        Erratic motion (sudden direction changes) triggers vestibular discomfort.
        """
        issues = []

        if len(position_sequence) < 3:
            return issues

        # Calculate velocity
        dt = np.diff(time_sequence_ms) / 1000.0  # Convert to seconds
        dx = np.diff(position_sequence, axis=0) if position_sequence.ndim > 1 else np.diff(position_sequence)
        velocity = dx / dt[:, np.newaxis] if position_sequence.ndim > 1 else dx / dt

        # Count direction reversals
        if velocity.ndim > 1:
            # 2D motion: check angle changes
            angles = np.arctan2(velocity[:, 1], velocity[:, 0]) if velocity.shape[1] >= 2 else np.zeros(len(velocity))
            angle_changes = np.abs(np.diff(angles))
            # Normalize to [-pi, pi]
            angle_changes = np.minimum(angle_changes, 2 * np.pi - angle_changes)
            reversals = np.sum(angle_changes > np.pi / 2)  # > 90 degree change
        else:
            # 1D motion: sign changes
            sign_changes = np.diff(np.sign(velocity))
            reversals = np.sum(sign_changes != 0)

        if reversals > self.MAX_DIRECTION_REVERSALS:
            issues.append(TemporalStabilityIssue(
                type=StabilityIssueType.ERRATIC_MOTION,
                location="motion_path",
                measured=reversals,
                threshold=self.MAX_DIRECTION_REVERSALS,
                severity="WARNING",
                suggestion=f"{reversals} direction reversals detected (max: {self.MAX_DIRECTION_REVERSALS}). "
                           "Smooth motion path or add easing at direction changes."
            ))

        return issues

    def validate_oscillation_damping(
        self,
        value_sequence: np.ndarray,
        target_value: float
    ) -> List[TemporalStabilityIssue]:
        """
        Validate that oscillating values converge (are damped).

        Undamped oscillation is disorienting and inappropriate for e-ink.
        """
        issues = []

        if len(value_sequence) < 6:
            return issues

        # Find oscillation peaks
        deviations = value_sequence - target_value
        peaks = []
        for i in range(1, len(deviations) - 1):
            if (deviations[i] > deviations[i-1] and deviations[i] > deviations[i+1]) or \
               (deviations[i] < deviations[i-1] and deviations[i] < deviations[i+1]):
                peaks.append(abs(deviations[i]))

        if len(peaks) >= 3:
            # Check if peaks are decreasing (damped)
            peak_ratios = [peaks[i+1] / peaks[i] for i in range(len(peaks)-1) if peaks[i] > 0]

            if peak_ratios and np.mean(peak_ratios) > 0.9:
                # Not damping fast enough
                issues.append(TemporalStabilityIssue(
                    type=StabilityIssueType.UNDAMPED_OSCILLATION,
                    location="value_oscillation",
                    measured=np.mean(peak_ratios),
                    threshold=0.9,
                    severity="WARNING",
                    suggestion="Oscillation not damping sufficiently. "
                               "Add damping factor or use critically-damped spring."
                ))

        return issues

    def validate_eink_appropriateness(
        self,
        update_times_ms: np.ndarray,
        update_values: np.ndarray,
        eink_mode: bool = False
    ) -> List[TemporalStabilityIssue]:
        """
        Validate content for e-ink display semantics.

        E-ink should see discrete state changes, not continuous updates.
        """
        issues = []

        if not eink_mode or len(update_times_ms) < 2:
            return issues

        # Check for continuous updates (too many small changes)
        intervals = np.diff(update_times_ms)
        value_changes = np.abs(np.diff(update_values))

        # Count rapid small updates
        rapid_small_updates = np.sum(
            (intervals < self.EINK_MIN_DWELL_MS) & (value_changes < 0.1)
        )

        if rapid_small_updates > 3:
            issues.append(TemporalStabilityIssue(
                type=StabilityIssueType.EINK_CONTINUOUS_UPDATE,
                location="update_pattern",
                measured=rapid_small_updates,
                threshold=3,
                severity="WARNING",
                suggestion=f"{rapid_small_updates} rapid small updates detected. "
                           "For e-ink, batch updates into discrete state changes with "
                           f"minimum {self.EINK_MIN_DWELL_MS}ms dwell time."
            ))

        # Check for oscillation in values
        if len(update_values) >= 4:
            # Simple oscillation detection: alternating direction
            directions = np.sign(np.diff(update_values))
            direction_changes = np.sum(np.diff(directions) != 0)

            if direction_changes >= 2:
                issues.append(TemporalStabilityIssue(
                    type=StabilityIssueType.EINK_CONTINUOUS_UPDATE,
                    location="value_oscillation",
                    measured=direction_changes,
                    threshold=2,
                    severity="WARNING",
                    suggestion="Value oscillation detected. E-ink displays should receive "
                               "monotonic updates converging to final state."
                ))

        return issues

    def validate_vestibular_safety(
        self,
        parallax_ratio: Optional[float] = None,
        zoom_speed: Optional[float] = None,
        rotation_speed: Optional[float] = None
    ) -> List[TemporalStabilityIssue]:
        """
        Validate motion parameters for vestibular sensitivity.

        Aggressive parallax, zoom, and rotation can trigger motion sickness.
        """
        issues = []

        if parallax_ratio is not None and parallax_ratio > self.MAX_PARALLAX_RATIO:
            issues.append(TemporalStabilityIssue(
                type=StabilityIssueType.VESTIBULAR_TRIGGER,
                location="parallax",
                measured=parallax_ratio,
                threshold=self.MAX_PARALLAX_RATIO,
                severity="WARNING",
                suggestion=f"Parallax ratio {parallax_ratio:.2f} exceeds {self.MAX_PARALLAX_RATIO}. "
                           "Reduce parallax effect or respect prefers-reduced-motion."
            ))

        if zoom_speed is not None and zoom_speed > self.MAX_ZOOM_SPEED:
            issues.append(TemporalStabilityIssue(
                type=StabilityIssueType.VESTIBULAR_TRIGGER,
                location="zoom",
                measured=zoom_speed,
                threshold=self.MAX_ZOOM_SPEED,
                severity="WARNING",
                suggestion=f"Zoom speed {zoom_speed:.1f} stops/sec exceeds {self.MAX_ZOOM_SPEED}. "
                           "Slow zoom transitions or add easing."
            ))

        if rotation_speed is not None and rotation_speed > self.MAX_ROTATION_SPEED:
            issues.append(TemporalStabilityIssue(
                type=StabilityIssueType.VESTIBULAR_TRIGGER,
                location="rotation",
                measured=rotation_speed,
                threshold=self.MAX_ROTATION_SPEED,
                severity="WARNING",
                suggestion=f"Rotation speed {rotation_speed:.0f} deg/sec exceeds {self.MAX_ROTATION_SPEED}. "
                           "Slow rotation or respect prefers-reduced-motion."
            ))

        return issues

    def get_reduced_motion_profile(self) -> dict:
        """Return configuration for prefers-reduced-motion users."""
        return {
            'animations': 'instant_or_fade_only',
            'transitions': {
                'max_duration_ms': 150,
                'allowed_types': ['opacity', 'color'],
                'forbidden_types': ['transform', 'motion-path']
            },
            'parallax': 'disabled',
            'auto_play': 'disabled',
            'carousel': 'static_with_controls',
            'zoom': {
                'max_speed': 0.5,
                'easing': 'ease-out'
            },
            'scroll_animations': 'disabled'
        }
```

**Test Cases:**

```python
def test_frame_pacing_detects_jitter():
    """Frame jitter beyond 10% is flagged."""
    gate = TemporalStabilityGate()

    # Simulate jittery frame times (target: 16.67ms)
    jittery_frames = np.array([0, 16, 34, 50, 68, 83, 100, 115, 133])
    issues = gate.validate_frame_pacing(jittery_frames, target_period_ms=16.67)

    assert len(issues) > 0
    assert issues[0].type == StabilityIssueType.FRAME_JITTER

def test_smooth_frames_pass():
    """Consistent frame pacing passes validation."""
    gate = TemporalStabilityGate()

    # Smooth 60Hz frames
    smooth_frames = np.arange(0, 170, 16.67)
    issues = gate.validate_frame_pacing(smooth_frames, target_period_ms=16.67)

    assert len(issues) == 0

def test_oscillation_damping_required():
    """Undamped oscillation is flagged."""
    gate = TemporalStabilityGate()

    # Undamped oscillation around target=0
    values = np.array([10, -9, 8, -8, 7, -7, 7, -7, 7, -7])  # Not converging
    issues = gate.validate_oscillation_damping(values, target_value=0)

    assert len(issues) > 0
    assert issues[0].type == StabilityIssueType.UNDAMPED_OSCILLATION

def test_eink_prefers_state_changes():
    """E-ink mode flags continuous small updates."""
    gate = TemporalStabilityGate()

    # Rapid small updates (bad for e-ink)
    times = np.array([0, 50, 100, 150, 200, 250])  # 50ms intervals
    values = np.array([0.0, 0.02, 0.04, 0.06, 0.08, 0.10])  # Small increments

    issues = gate.validate_eink_appropriateness(times, values, eink_mode=True)

    assert len(issues) > 0
    assert issues[0].type == StabilityIssueType.EINK_CONTINUOUS_UPDATE
```

---

## 11. Extended Tool Integration Matrix

| Gate | Tool Options | License | Integration |
|------|--------------|---------|-------------|
| SEIZURE | EA IRIS | BSD | CLI, Python |
| SEIZURE | PEAT | Free (web) | CLI |
| CONTRAST | axe-core | MIT | npm, Browser |
| CONTRAST | APCA-W3 | W3C | npm |
| CVD | DaltonLens | MIT | C, Python |
| CVD | colour-science | BSD | Python |
| SPATIAL | axe-core | MIT | npm |
| COGNITIVE | Flesch-Kincaid | Public | Various |
| **TYPOGRAPHY** | fonttools | MIT | Python |
| **TYPOGRAPHY** | postcss | MIT | npm |
| **LAYOUT** | axe-core | MIT | npm |
| **LAYOUT** | Playwright | Apache 2.0 | npm, Python |
| **REFLOW** | Puppeteer | Apache 2.0 | npm |
| **VIZ** | colour-science | BSD | Python |
| **VIZ** | matplotlib | PSF | Python |

---

## 11. GitHub Actions (Extended)

```yaml
# .github/workflows/uvas-plus-validation.yml
name: UVAS+ Full Validation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  typography-validation:
    name: Typography Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Check Font Contracts
        run: |
          pip install fonttools
          python scripts/font_contract_check.py fonts/
      - name: Check CSS Typography
        run: |
          npm install postcss
          npx ts-node scripts/typography-lint.ts styles/**/*.css

  layout-validation:
    name: Layout & Reflow Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Playwright
        run: |
          npm install playwright
          npx playwright install chromium
      - name: Check Touch Targets
        run: |
          npx ts-node scripts/touch-target-audit.ts
      - name: Reflow Test at 200%
        run: |
          npx ts-node scripts/reflow-test.ts --scales 1.0,1.5,2.0
      - name: Heading Hierarchy
        run: |
          npx ts-node scripts/heading-audit.ts

  viz-validation:
    name: Visualization Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: pip install colour-science matplotlib numpy
      - name: Check Color Encoding
        run: |
          python scripts/viz_color_encoding_check.py charts/
      - name: Check CVD Safety
        run: |
          python scripts/viz_cvd_check.py palettes/viz-palette.json

  full-report:
    name: Generate UVAS+ Report
    needs: [typography-validation, layout-validation, viz-validation]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Generate Report
        run: |
          echo "# UVAS+ Validation Report" > report.md
          echo "| Gate | Status |" >> report.md
          echo "|------|--------|" >> report.md
          echo "| Typography | ${{ needs.typography-validation.result }} |" >> report.md
          echo "| Layout | ${{ needs.layout-validation.result }} |" >> report.md
          echo "| Visualization | ${{ needs.viz-validation.result }} |" >> report.md
      - uses: actions/upload-artifact@v4
        with:
          name: uvas-plus-report
          path: report.md
```

---

*Framework Version 1.1.0 - Updated 2025-12-27 with UVAS+ Typography, Layout, Visualization gates*
