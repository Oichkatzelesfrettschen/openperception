# Quickstart Guide

Get from zero to a working CVD simulation in five minutes.

---

## 1. Clone the Repository

```bash
git clone --recursive https://github.com/openperception/openperception.git
cd openperception
```

The `--recursive` flag pulls the algorithm submodules (DaltonLens-Python, libDaltonLens).

---

## 2. Set Up the Python Package

```bash
# Install DaltonLens-Python in editable mode
pip install -e algorithms/DaltonLens-Python

# Verify installation
python -c "from daltonlens import simulate; print('OK')"
```

For a complete development environment (linting, testing, pre-commit):

```bash
make install-dev
```

---

## 3. Simulate Color Vision Deficiency

### Python API

```python
from PIL import Image
import numpy as np
from daltonlens import convert, simulate

# Load any RGB image
image = np.array(Image.open("my_image.png"))

# Simulate deuteranopia (green-blind, most common CVD)
model = convert.LMSModel_sRGB_SmithPokorny75()
sim = simulate.Simulator_Brettel1997(model)
result = sim.simulate_cvd(image, simulate.Deficiency.DEUTAN, severity=1.0)

Image.fromarray(result).save("simulated_deutan.png")
```

### Command Line

```bash
# Simulate protanopia
daltonlens-python input.png output.png --deficiency protan

# All three deficiency types
for deficiency in protan deutan tritan; do
    daltonlens-python input.png sim_${deficiency}.png --deficiency $deficiency
done
```

---

## 4. Daltonize (Correct for CVD)

Daltonization enhances images so CVD users can distinguish colors:

```python
from daltonlens import daltonize, simulate

result = daltonize.daltonize(image, simulate.Deficiency.DEUTAN)
Image.fromarray(result).save("daltonized.png")
```

```bash
# Command line
daltonlens-python input.png output.png --filter daltonize --deficiency deutan
```

---

## 5. Validate Contrast Ratios

```bash
# Check WCAG contrast for all color token pairs
make contrast-check

# Check CVD color separation
make separation-check
```

---

## 6. Run Tests

```bash
# All tests
make test

# Python tests only (with coverage)
make coverage

# C library tests
make test-c
```

---

## 7. Explore Further

| Guide | Topic |
|-------|-------|
| `docs/simulator-guide.md` | All 8 simulation algorithms, severity, examples |
| `docs/contrast-guide.md` | WCAG formulas, token workflow |
| `docs/oklch-guide.md` | OKLCH color space and token generation |
| `specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md` | Full accessibility framework |
| `papers/colorblindness_algorithms_compendium.md` | Academic literature survey |

---

## Common Issues

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'daltonlens'` | Run `pip install -e algorithms/DaltonLens-Python` |
| `ModuleNotFoundError: No module named 'Geometry3D'` | Optional; only needed for Ishihara plate generation |
| C build fails | Run `make build-c` from repo root; requires cmake |
| Submodules empty | Run `git submodule update --init --recursive` |
