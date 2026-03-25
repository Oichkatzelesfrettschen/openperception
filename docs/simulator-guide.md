# CVD Simulator Guide

This guide covers all CVD simulation methods available in OpenPerception.

---

## WHY

Color Vision Deficiency (CVD) affects approximately 8% of males and 0.5% of females.
Simulating CVD lets developers verify that their designs remain usable for all users
without requiring user testing at every iteration.

In the repo's color-support taxonomy, simulation is primarily a validation
mode, not itself an accommodation. See the
[Color support accommodation taxonomy](/home/eirikr/Github/openperception/docs/color-support-accommodation-taxonomy.md).

---

## Python API

### Install

```bash
pip install -e algorithms/DaltonLens-Python
```

### Quick example

```python
from PIL import Image
import numpy as np
from daltonlens import convert, simulate

# Load image
im = np.array(Image.open("input.png"))

# Choose a simulator (Brettel 1997 is the gold standard)
model = convert.LMSModel_sRGB_SmithPokorny75()
simulator = simulate.Simulator_Brettel1997(model)

# Simulate protanopia (full severity)
result = simulator.simulate_cvd(im, simulate.Deficiency.PROTAN, severity=1.0)

Image.fromarray(result).save("simulated.png")
```

---

## Available Simulators

| Class | Algorithm | Use Case |
|-------|-----------|----------|
| `Simulator_Brettel1997` | Brettel et al. 1997 | Gold standard, best for tritanopia |
| `Simulator_Vienot1999` | Vienot et al. 1999 | Faster, good for protan/deutan |
| `Simulator_Machado2009` | Machado et al. 2009 | Required for severity modeling |
| `Simulator_AutoSelect` | Auto-picks best | Recommended for general use |
| `Simulator_CoblisV2` | Coblis v2 | Legacy reference only |
| `Simulator_CoblisV1` | Coblis v1 | **Deprecated** - very poor accuracy |

---

## Deficiency Types

| Deficiency | Cone | Prevalence |
|-----------|------|-----------|
| `Deficiency.PROTAN` | L-cone (red) loss | ~1% males |
| `Deficiency.DEUTAN` | M-cone (green) loss | ~6% males |
| `Deficiency.TRITAN` | S-cone (blue) loss | ~0.01% all |

---

## Severity

Severity scales from `0.0` (normal vision) to `1.0` (complete dichromacy):

```python
# Anomalous trichromacy (partial, severity=0.5)
result = simulator.simulate_cvd(im, simulate.Deficiency.PROTAN, severity=0.5)
```

For severity < 1.0, use `Simulator_Machado2009` which models the physiological
difference between anomalous trichromacy and dichromacy correctly.

---

## CLI

```bash
# Simulate deuteranopia and save result
daltonlens-python input.png output.png --deficiency deutan

# Use specific model
daltonlens-python input.png output.png --model brettel --deficiency protan

# Anomalous trichromacy (50% severity)
daltonlens-python input.png output.png --model machado --deficiency protan --severity 0.5

# Daltonize (correct for CVD)
daltonlens-python input.png output.png --filter daltonize --deficiency deutan
```

---

## SVG Filters (browser)

For in-browser preview without Python, use the SVG filter example:

```html
<!-- Include the filter definitions -->
<svg class="filters" aria-hidden="true">
  <!-- see examples/simulator/index.html for filter matrices -->
</svg>

<!-- Apply to a container -->
<div style="filter: url(#protanopia)">
  <!-- content here -->
</div>
```

Open `examples/simulator/index.html` in a browser to see an interactive demo.

---

## Algorithm Pipeline

```
Input Image (sRGB uint8)
    |
    v  as_float32() / linearRGB_from_sRGB()
Linear RGB float32
    |
    v  LMS_from_linearRGB matrix
LMS Color Space
    |
    v  CVD Projection (Brettel/Vienot/Machado)
LMS (simulated)
    |
    v  linearRGB_from_LMS matrix
Linear RGB
    |
    v  sRGB_from_linearRGB() / as_uint8()
Output Image (sRGB uint8)
```

---

## References

- Brettel, H., Vienot, F., & Mollon, J. (1997). Computerized simulation of color appearance for dichromats.
- Vienot, F., Brettel, H., & Mollon, J. (1999). Digital video colourmaps for checking the legibility of displays by dichromats.
- Machado, G., Oliveira, M., & Fernandes, L. (2009). A physiologically-based model for simulation of color vision deficiency.
