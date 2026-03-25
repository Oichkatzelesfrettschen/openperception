# Daltonization Guide

Daltonization adjusts the colors in an image so that people with color vision
deficiency (CVD) can distinguish colors that would otherwise look identical or
nearly identical to them.

---

## Simulation vs. Daltonization

| Goal | Tool |
|------|------|
| Show what a CVD viewer sees | `simulate_cvd()` -- no modification to original |
| Adjust image so CVD viewers can distinguish colors | `daltonize()` -- modifies the image |

Simulation is for testing and diagnosis. Daltonization produces a modified
image intended for CVD viewers to consume directly.

For the repo's broader distinction between simulation, daltonization,
recognition aids, and reconstructive color models, see the
[Color support accommodation taxonomy](/home/eirikr/Github/openperception/docs/color-support-accommodation-taxonomy.md).

---

## Quick Start

```python
import numpy as np
from PIL import Image
from daltonlens import daltonize
from daltonlens.simulate import Deficiency

img = np.array(Image.open("chart.png"))

# Correct for deuteranopia (green-blind, ~5% of males)
corrected = daltonize.daltonize(img, Deficiency.DEUTAN)

Image.fromarray(corrected).save("chart_daltonized.png")
```

---

## Deficiency Types

| Constant | Condition | Prevalence |
|----------|-----------|------------|
| `Deficiency.PROTAN` | Protanopia/protanomaly (red) | ~1% males |
| `Deficiency.DEUTAN` | Deuteranopia/deuteranomaly (green) | ~5% males |
| `Deficiency.TRITAN` | Tritanopia/tritanomaly (blue-yellow) | ~0.01% all |

---

## Methods

### `daltonize_fidaner` -- Error Diffusion (default)

Based on Fidaner et al. (2006). The algorithm:

1. Simulates the CVD view of the image.
2. Computes the error: `original - simulated`.
3. Shifts the error to color channels the viewer CAN perceive.
4. Adds the shifted error back to the original.

This preserves the overall appearance for normal-vision viewers while
making previously-confused colors distinguishable to CVD viewers.

```python
corrected = daltonize.daltonize_fidaner(
    img,
    Deficiency.PROTAN,
    severity=1.0,   # 0.0 = no correction, 1.0 = full correction
)
```

The `severity` parameter scales how much error is diffused. Use values
below 1.0 for subtle correction that minimizes visible change.

### `daltonize_simple` -- Channel Enhancement

A lightweight method that enhances saturation and shifts hues in the
channels affected by the deficiency. Faster than Fidaner and suitable
for real-time use.

```python
corrected = daltonize.daltonize_simple(
    img,
    Deficiency.DEUTAN,
    strength=1.0,   # 0.0 = no change, 1.0 = full enhancement
)
```

### `daltonize` -- Dispatch Function

Convenience wrapper that selects the method via a string argument:

```python
corrected = daltonize.daltonize(img, Deficiency.DEUTAN, method="fidaner")
corrected = daltonize.daltonize(img, Deficiency.DEUTAN, method="simple")
```

---

## Method Comparison

| | Fidaner | Simple |
|---|---------|--------|
| Algorithm | Error-diffusion (Fidaner 2006) | Channel enhancement |
| Quality | Higher -- preserves luminance | Lower -- may shift hues |
| Speed | Slower (requires simulation pass) | Faster |
| Parameter | `severity` (0.0-1.0) | `strength` (0.0-1.0) |
| Best for | Offline processing, high quality | Real-time, lightweight |

---

## CLI Usage

The `daltonlens` CLI supports daltonization via the `--filter daltonize` flag:

```bash
# Daltonize for deuteranopia (default: fidaner method)
python -m daltonlens input.png output.png --filter daltonize --deficiency deutan

# Adjust severity
python -m daltonlens input.png output.png --filter daltonize --deficiency protan --severity 0.7
```

---

## Batch Processing

```python
from pathlib import Path
import numpy as np
from PIL import Image
from daltonlens import daltonize
from daltonlens.simulate import Deficiency

input_dir = Path("images/original")
output_dir = Path("images/daltonized")
output_dir.mkdir(exist_ok=True)

for img_path in input_dir.glob("*.png"):
    img = np.array(Image.open(img_path))
    corrected = daltonize.daltonize(img, Deficiency.DEUTAN)
    Image.fromarray(corrected).save(output_dir / img_path.name)
```

---

## How It Works (Fidaner Detail)

The error-diffusion matrices shift lost color information to channels the
CVD viewer can still perceive:

- **Protan** (missing L-cones): error shifted to G and B channels
- **Deutan** (missing M-cones): error shifted to R and B channels
- **Tritan** (missing S-cones): error shifted to R and G channels

This means the luminance contrast that encoded color information is
preserved but expressed through a different channel pairing.

---

## Limitations

- Daltonization improves distinguishability but cannot fully compensate
  for all color confusion pairs, especially with complex natural images.
- The Fidaner method uses Brettel1997 simulation internally by default;
  you can pass a custom `simulator` argument for other models.
- Neither method guarantees WCAG contrast compliance. Use the GATE-002
  CONTRAST validator (`tools/validators/contrast.py`) to verify contrast
  ratios independently.

---

## Related

- `algorithms/DaltonLens-Python/daltonlens/daltonize.py` -- source
- `algorithms/DaltonLens-Python/tests/test_daltonize.py` -- tests
- `docs/quickstart.md` -- getting started overview
- `tools/validators/cvd.py` -- GATE-003 CVD color separation validator
- `specs/REFERENCES_BIBLIOGRAPHY.md` -- academic references
