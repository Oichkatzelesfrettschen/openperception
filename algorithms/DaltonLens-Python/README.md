# DaltonLens-Python

[![Unit Tests](https://github.com/DaltonLens/DaltonLens-Python/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/DaltonLens/DaltonLens-Python/actions/workflows/unit_tests.yml)

This python package is a companion to the desktop application [DaltonLens](https://github.com/DaltonLens/DaltonLens). Its main goal is to help the research and development of better color filters for people with color vision deficiencies. It also powers the Jupyter notebooks used for the technical posts of [daltonlens.org](https://daltonlens.org). The current features include:

* Simulate color vision deficiencies using the Viénot 1999, Brettel 1997 or Machado 2009 models.
* Provide conversion functions to/from sRGB, linear RGB and LMS
* Implement several variants of the LMS model
* Generate Ishihara-like test images

For a discussion about which CVD simulation algorithms are the most accurate see our [Review of Open Source Color Blindness Simulations](https://daltonlens.org/opensource-cvd-simulation/).

For more information about the math of the chosen algorithms see our article [Understanding CVD Simulation](https://daltonlens.org/understanding-cvd-simulation/).

## Install

`python3 -m pip install daltonlens`

## How to use

### From the command line

Invoke as a module (`python -m daltonlens`) or via the installed entry point (`daltonlens`):

```
python -m daltonlens [options] input_image output_image
```

**Positional arguments**

| Argument | Description |
|---|---|
| `input_image` | Image file to process (PNG, JPEG, or any Pillow-supported format). |
| `output_image` | Path to write the processed image. |

**Options**

| Option | Choices | Default | Description |
|---|---|---|---|
| `--deficiency`, `-d` | `protan`, `deutan`, `tritan`, `achromat`, `bcm` | `protan` | CVD type to simulate. See the deficiency table below. |
| `--model`, `-m` | `auto`, `vienot`, `brettel`, `machado`, `vischeck`, `coblisV1`, `coblisV2` | `auto` | Simulation algorithm. `auto` selects the best available model per deficiency type. |
| `--filter`, `-f` | `simulate`, `daltonize` | `simulate` | `simulate` renders the CVD view; `daltonize` shifts colors to improve CVD legibility. |
| `--severity`, `-s` | `0.0` to `1.0` | `1.0` | Severity of the deficiency. `0.0` is normal vision; `1.0` is complete dichromacy or monochromacy. |
| `--daltonize-method` | `fidaner`, `simple` | `fidaner` | Daltonization algorithm (only applies with `--filter daltonize`). |

**Deficiency types**

| Value | Name | Description |
|---|---|---|
| `protan` | Protanopia / Protanomaly | Reduced red cone response (L-cone). Most common inherited CVD. |
| `deutan` | Deuteranopia / Deuteranomaly | Reduced green cone response (M-cone). Affects ~6% of males. |
| `tritan` | Tritanopia / Tritanomaly | Reduced blue cone response (S-cone). Rare; often acquired. |
| `achromat` | Rod monochromacy (achromatopsia) | All cones non-functional; rod-only vision. Simulated via BT.709 luminance projection. |
| `bcm` | Blue-cone monochromacy | L and M cones absent; S-cone and rod vision only. Simulated via pre-computed LMS matrix (SmithPokorny75). |

**Simulation models**

| Value | Algorithm | Notes |
|---|---|---|
| `auto` | Automatic | Selects Vienot 1999 for protan/deutan, Brettel 1997 for tritan, Achromat for achromat, BCM for bcm. |
| `vienot` | Vienot 1999 | Standard dichromacy projection; good general purpose choice. |
| `brettel` | Brettel 1997 | Piecewise projection; most accurate for tritan. |
| `machado` | Machado 2009 | Continuous severity model; only supports protan/deutan/tritan. |
| `vischeck` | Vischeck | Legacy; included for comparison. |
| `coblisV1` | Coblis v1 | Legacy; deprecated. |
| `coblisV2` | Coblis v2 | Includes additional filters. |

**Examples**

```bash
# Simulate full deuteranopia (green-weak) using the auto-selected algorithm
python -m daltonlens input.png output.png --deficiency deutan

# Simulate 50% protanomaly with the Machado 2009 model
python -m daltonlens input.png output.png --deficiency protan --model machado --severity 0.5

# Simulate complete achromatopsia (rod monochromacy)
python -m daltonlens input.png output.png --deficiency achromat

# Simulate blue-cone monochromacy
python -m daltonlens input.png output.png --deficiency bcm

# Daltonize an image for a tritanope viewer
python -m daltonlens input.png output.png --deficiency tritan --filter daltonize

# Daltonize using the simpler algorithm variant
python -m daltonlens input.png output.png --filter daltonize --daltonize-method simple

# Batch: process all PNGs in a directory
python -m daltonlens --batch "images/*.png" --output-dir out/ --deficiency deutan

# Batch: recursive glob across subdirectories
python -m daltonlens --batch "images/**/*.jpg" --output-dir out/ --deficiency achromat
```

### From code

```python
from daltonlens import convert, simulate, generate
import PIL
import numpy as np

# Generate a test image that spans the RGB range
im = np.asarray(PIL.Image.open("test.png").convert('RGB'))

# Create a simulator using the Viénot 1999 algorithm.
simulator = simulate.Simulator_Vienot1999()

# Apply the simulator to the input image to get a simulation of protanomaly
protan_im = simulator.simulate_cvd (im, simulate.Deficiency.PROTAN, severity=0.8)
```
