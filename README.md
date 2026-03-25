# OpenPerception

**Visual Accessibility Research and Tools for Color Vision Deficiency, Neurodivergence, and Inclusive Design**

OpenPerception is a comprehensive research repository and toolkit for understanding and accommodating diverse visual perception. It provides production-ready algorithms, design systems, and evidence-based specifications for creating accessible visual experiences.

---

## Overview

This repository contains:

- **CVD Simulation Algorithms**: Production-ready implementations of Brettel, Vienot, and Machado color vision deficiency simulation algorithms
- **Design Token System**: CVD-aware color tokens with variants for protanopia, deuteranopia, tritanopia, and achromatopsia
- **Accessibility Specifications**: Comprehensive framework covering safety, perceptibility, discriminability, comprehensibility, and controllability
- **Depth Accessibility Guidance**: Stereo-independent depth documentation for users with and without stereopsis
- **Research Compendiums**: 400+ cataloged academic papers on visual accessibility
- **Development Tools**: Contrast checkers, color separation validators, and OKLCH utilities

---

## Quick Start

### Prerequisites

- Python 3.8+
- CMake 3.16+ (for C library)
- NumPy and Pillow (for Python package)
- Git LFS (for paper corpus PDFs)

### Install DaltonLens-Python

```bash
cd algorithms/DaltonLens-Python
pip install -e .
```

### Run CVD Simulation

```python
from daltonlens import simulate, convert
import numpy as np
from PIL import Image

# Load image
img = np.array(Image.open("input.png"))

# Simulate deuteranopia (green-weak)
simulator = simulate.Simulator_Brettel1997()
simulated = simulator.simulate_cvd(img, simulate.Deficiency.DEUTAN, severity=1.0)
```

### Build libDaltonLens (C)

```bash
cd algorithms/libDaltonLens
mkdir build && cd build
cmake ..
make
./tests/test_simulation
```

### Run Development Tools

```bash
# Start development server
make serve

# Check WCAG contrast ratios
make contrast-check

# Generate OKLCH tokens
make oklch
```

### Research Corpus Notes

The canonical paper corpus lives under `papers/downloads/`. Non-paper dataset
support assets live under `datasets/source_assets/`. PDF artifacts in both
lanes are stored with Git LFS. After cloning, run:

```bash
git lfs pull
```

Integrity checks:

```bash
python3 tools/check_paper_corpus.py
python3 tools/check_source_assets.py
```

The paper-corpus check now also fails if tracked literature PDFs appear
directly under `papers/` instead of a topic lane inside `papers/downloads/`.

Visual showcase artifacts now live under `artifacts/blender_showcase/`, with a
tracked spec plus retained render and `.blend` snapshots for the palette lane.

---

## Repository Structure

```
openperception/
|-- algorithms/
|   |-- DaltonLens-Python/     # Python CVD simulation package
|   +-- libDaltonLens/         # C library (public domain)
|-- artifacts/
|   +-- blender_showcase/     # Tracked Blender scene and render snapshots
|-- datasets/
|   |-- source_assets/         # Non-paper reference assets for datasets/tools
|   +-- ishihara-plate-learning/  # Color blindness test learning tool
|-- docs/                       # User guides and tutorials
|-- examples/                   # Code examples and demos
|-- gtk4/                       # GTK4 accessibility demo
|-- papers/                     # Research paper compendiums
|   |-- downloads/             # Canonical topic-lane paper cache
|-- python-packages/
|   +-- sphinx-brand-theme/    # Custom Sphinx documentation theme
|-- research/                   # Domain research (CVD, neurodivergence, etc.)
|-- specs/                      # Technical specifications
|-- templates/                  # Document templates
|-- tex/                        # LaTeX resources
|-- tokens/                     # Design token definitions
+-- tools/                      # Development utilities
```

---

## Components

### DaltonLens-Python

Research and development package implementing multiple CVD simulation algorithms:

- **Brettel et al. (1997)**: Dichromat simulation with opponent-color projection
- **Vienot et al. (1999)**: Fast digital simulation method
- **Machado et al. (2009)**: Severity-parameterized model
- **Vischeck**: Reference implementation compatibility

```python
from daltonlens.simulate import Simulator_Brettel1997, Deficiency

simulator = Simulator_Brettel1997()
result = simulator.simulate_cvd(image, Deficiency.PROTAN, severity=0.8)
```

### libDaltonLens

Single-file, dependency-free C library for embedded applications:

```c
#include "libDaltonLens.h"

// Simulate CVD in-place
dl_simulate_cvd(DL_DEFICIENCY_DEUTAN, 1.0f,
                image_data, width, height, stride);
```

### Design Token System

CVD-aware color tokens in multiple formats:

- `tokens/color-tokens.css` - CSS custom properties
- `tokens/color-tokens.json` - JSON definitions
- `tokens/color-oklch-map.json` - OKLCH color space mappings

Five accessibility variants:
- `brand_default.css` - Standard color vision
- `brand_protan.css` - Red-weak optimized
- `brand_deutan.css` - Green-weak optimized
- `brand_tritan.css` - Blue-weak optimized
- `brand_mono.css` - Grayscale/achromatopsia

### Specifications

Comprehensive accessibility framework in `specs/`:

- **UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md** - Core 5-pillar specification
- **VALIDATORS_FRAMEWORK.md** - Testing and validation framework
- **EVIDENCE_MATRIX.md** - Research citation matrix
- **TYPOGRAPHY_SYSTEM.md** - Accessible typography rules
- **LAYOUT_SYSTEM.md** - Responsive layout guidelines

Applied guidance in `docs/`:

- **harmonized-depth-accommodation-guide.md** - Shared depth-cue strategy for stereo-capable and stereoblind users

---

## Development

### Running Tests

```bash
# Python tests
cd algorithms/DaltonLens-Python
pytest -v

# C tests
cd algorithms/libDaltonLens/build
./tests/test_simulation
```

### Code Quality

```bash
# Lint Python code
ruff check .

# Format Python code
black .

# Check contrast ratios
make contrast-check
```

### Documentation

```bash
# Install Sphinx theme
make sphinx-install-theme

# Build documentation
make sphinx-example-html
```

---

## Research Areas

### Color Vision Deficiency

- Protanopia/Protanomaly (red-weak)
- Deuteranopia/Deuteranomaly (green-weak)
- Tritanopia/Tritanomaly (blue-weak)
- Achromatopsia (complete color blindness)
- Blue Cone Monochromacy

### Neurodivergence

- ADHD visual processing
- Autism spectrum visual perception
- Dyslexia and visual stress
- Cognitive load optimization

### Safety

- Photosensitive epilepsy prevention
- Pattern sensitivity guidelines
- Flash rate limitations

### Visual Impairments

- Stereoblindness and reduced stereopsis
- Low vision and contrast sensitivity
- Visual field loss
- Nystagmus and oculomotor instability

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

Individual components have their own licenses:
- **libDaltonLens**: Public Domain
- **DaltonLens-Python**: BSD 2-Clause
- **Ishihara Plate Learning**: AGPL-3.0

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

---

## Acknowledgments

- Nicolas Burrus for the original DaltonLens implementations
- The color vision research community for foundational algorithms
- Contributors to the accessibility specifications

---

## References

Key papers informing this work:

- Brettel, H., Vienot, F., & Mollon, J. D. (1997). Computerized simulation of color appearance for dichromats.
- Vienot, F., Brettel, H., & Mollon, J. D. (1999). Digital video colourmaps for checking the legibility of displays by dichromats.
- Machado, G. M., Oliveira, M. M., & Fernandes, L. A. (2009). A physiologically-based model for simulation of color vision deficiency.

See `papers/` directory for comprehensive research compendiums.
