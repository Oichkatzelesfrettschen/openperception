# Contrast Validation Guide

This guide explains WCAG contrast requirements and how OpenPerception validates them.

---

## WHY

Low contrast causes text and UI elements to be unreadable for users with low vision,
color vision deficiency, or viewing displays in bright environments.
WCAG 2.1 defines minimum contrast ratios that ensure basic legibility.

---

## WCAG Contrast Levels

| Level | Ratio | Applies to |
|-------|-------|-----------|
| AA Normal | 4.5:1 | Body text (< 18pt or < 14pt bold) |
| AA Large | 3.0:1 | Large text (>= 18pt or >= 14pt bold), UI components |
| AAA Normal | 7.0:1 | Enhanced body text |
| AAA Large | 4.5:1 | Enhanced large text |

---

## Contrast Ratio Formula

```
contrast = (L_lighter + 0.05) / (L_darker + 0.05)

where L = relative_luminance = 0.2126 R + 0.7152 G + 0.0722 B
(R, G, B are linearized sRGB channels)
```

---

## Command-Line Check

```bash
# Check all token pairs across all variants
python tools/contrast_check.py

# Or via Makefile
make contrast-check
```

Output shows each pair's ratio and WCAG level (AA/AA Large/FAIL).

---

## Python API

```python
from tools.contrast_check import contrast_ratio, relative_luminance

# Check a specific pair
ratio = contrast_ratio("#1a1a2e", "#e8f4f8")
print(f"Contrast ratio: {ratio:.2f}:1")  # e.g. 12.34:1
```

---

## Validator Gate (GATE-002)

The ContrastGate integrates with the validator pipeline:

```python
import sys
sys.path.insert(0, "tools")
from validators.contrast import ContrastGate

gate = ContrastGate()
result = gate.validate()
print(result)
if not result.passed:
    raise SystemExit(1)
```

---

## Token Workflow

1. Edit `tokens/color-tokens.json` (source of truth)
2. Run `make contrast-check` to validate all pairs
3. Fix any FAIL entries by adjusting lightness
4. Run `make oklch` to regenerate OKLCH variants

---

## Common Failures

| Problem | Cause | Fix |
|---------|-------|-----|
| Gray text on white | Gray too light | Use gray-700 or darker |
| Colored button label | Saturation reduces contrast | Use high-L foreground |
| Accent on surface | Accent too similar in luminance | Darken or lighten accent |
