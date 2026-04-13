# OpenPerception Architecture

This document describes the high-level architecture and component relationships in OpenPerception.

---

## System Overview

```
+------------------------------------------------------------------+
|                        OpenPerception                             |
+------------------------------------------------------------------+
|                                                                   |
|  +-------------------+     +-------------------+                  |
|  |   Research &      |     |   Specifications  |                  |
|  |   Evidence Base   |     |   & Standards     |                  |
|  +-------------------+     +-------------------+                  |
|          |                         |                              |
|          v                         v                              |
|  +-------------------+     +-------------------+                  |
|  |  papers/          |     |  specs/           |                  |
|  |  research/        |     |  EVIDENCE_MATRIX  |                  |
|  +-------------------+     +-------------------+                  |
|          |                         |                              |
|          +------------+------------+                              |
|                       |                                           |
|                       v                                           |
|  +--------------------------------------------------+            |
|  |              Core Algorithms                      |            |
|  +--------------------------------------------------+            |
|  |                                                   |            |
|  |  +-------------------+   +-------------------+    |            |
|  |  | DaltonLens-Python |   |   libDaltonLens  |    |            |
|  |  |     (Python)      |   |       (C)        |    |            |
|  |  +-------------------+   +-------------------+    |            |
|  |          |                       |               |            |
|  +----------|-----------------------|---------------+            |
|             |                       |                             |
|             v                       v                             |
|  +--------------------------------------------------+            |
|  |              Design System                        |            |
|  +--------------------------------------------------+            |
|  |                                                   |            |
|  |  +-------------+  +-------------+  +----------+  |            |
|  |  | tokens/     |  | gtk4/       |  | examples/|  |            |
|  |  | (JSON/CSS)  |  | (Demo App)  |  | (Code)   |  |            |
|  |  +-------------+  +-------------+  +----------+  |            |
|  |                                                   |            |
|  +--------------------------------------------------+            |
|             |                                                     |
|             v                                                     |
|  +--------------------------------------------------+            |
|  |              Development Tools                    |            |
|  +--------------------------------------------------+            |
|  |                                                   |            |
|  |  +----------------+  +----------------+           |            |
|  |  | tools/         |  | Makefile       |           |            |
|  |  | (Validators)   |  | (Orchestration)|           |            |
|  |  +----------------+  +----------------+           |            |
|  |                                                   |            |
|  +--------------------------------------------------+            |
|                                                                   |
+------------------------------------------------------------------+
```

---

## Component Details

### 1. Research & Evidence Base

**Location**: `papers/`, `research/`

**Purpose**: Catalog and organize academic research supporting accessibility decisions.

**Contents**:
- 7 research compendiums (400+ papers)
- Domain-specific research directories
- Citation metadata and DOIs

**Data Flow**:
- Research informs specifications
- Citations linked via EVIDENCE_MATRIX.md
- Compendiums updated as new research emerges

---

### 2. Specifications & Standards

**Location**: `specs/`

**Purpose**: Define measurable accessibility criteria and validation frameworks.

**Key Documents**:
| Document | Purpose |
|----------|---------|
| UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md | Core 5-pillar framework |
| VALIDATORS_FRAMEWORK.md | Testing requirements |
| EVIDENCE_MATRIX.md | Research citation mapping |
| TYPOGRAPHY_SYSTEM.md | Font/text rules |
| LAYOUT_SYSTEM.md | Spatial organization |

**Dependencies**:
- Informed by research compendiums
- Drives algorithm requirements
- Defines tool validation criteria

---

### 3. Core Algorithms

**Location**: `algorithms/`

#### DaltonLens-Python

**Structure**:
```
daltonlens/
|-- __init__.py
|-- simulate.py     # CVD simulation (Brettel, Vienot, Machado)
|-- convert.py      # Color space conversions
|-- generate.py     # Test image generation
|-- cmfs.py         # Cone matching functions
|-- geometry.py     # Math utilities
|-- main.py         # CLI entry point
+-- utils.py        # Helpers
```

**Key Classes**:
- `Simulator` (abstract base)
- `Simulator_Brettel1997` -- dichromat half-plane projection (Brettel 1997)
- `Simulator_Vienot1999` -- efficient dichromat projection (Vienot 1999)
- `Simulator_Machado2009` -- anomalous trichromacy (severity dial)
- `Simulator_Vischeck` -- Brettel with original GIMP matrices
- `Simulator_Achromat` -- rod monochromacy (BT.709 Y = all-gray)
- `Simulator_BCM` -- blue-cone monochromacy (SmithPokorny75 3x3 matrix)
- `Simulator_AutoSelect` -- routes to best simulator per deficiency type

**Deficiency enum**:
- `PROTAN` (0) / `DEUTAN` (1) / `TRITAN` (2) -- dichromacies
- `ACHROMAT` (3) -- rod monochromacy (achromatopsia); Simulator_Achromat
- `BCM` (4) -- blue-cone monochromacy; Simulator_BCM

**Data Flow**:
```
Input Image (sRGB uint8)
    |
    v
sRGB_to_linearRGB()     # Gamma decode
    |
    v
linearRGB_to_LMS()      # To cone response space
    |
    v
simulate_cvd()          # Project to dichromat plane
    |
    v
LMS_to_linearRGB()      # Back to RGB
    |
    v
linearRGB_to_sRGB()     # Gamma encode
    |
    v
Output Image (sRGB uint8)
```

#### libDaltonLens (C)

**Structure**:
```
libDaltonLens/
|-- libDaltonLens.c     # Implementation
|-- libDaltonLens.h     # Public API
|-- tests/
|   |-- test_simulation.c
|   |-- stb_image.h         # Vendored
|   |-- stb_image_write.h   # Vendored
|   +-- sokol_time.h        # Vendored
+-- svg/                    # SVG filter port
```

**API**:
```c
enum DLDeficiency {
    DLDeficiency_Protan,
    DLDeficiency_Deutan,
    DLDeficiency_Tritan,
    DLDeficiency_Achromat,  /* Rod monochromacy (achromatopsia)  */
    DLDeficiency_BCM        /* Blue-cone monochromacy             */
};

/* Automatic dispatch: best algorithm per deficiency type */
void dl_simulate_cvd(enum DLDeficiency deficiency, float severity,
    unsigned char *srgba_image, size_t width, size_t height, size_t bytesPerRow);

/* Named algorithm variants */
void dl_simulate_cvd_brettel1997(enum DLDeficiency, float severity, ...);
void dl_simulate_cvd_vienot1999(enum DLDeficiency, float severity, ...);
void dl_simulate_cvd_machado2009(enum DLDeficiency, float severity, ...);
void dl_simulate_cvd_achromat(float severity, ...);
void dl_simulate_cvd_bcm(float severity, ...);
```

**Design Principles**:
- Zero external dependencies
- Single-file inclusion
- Public domain license
- Pixel-accurate against Python implementation

---

### 4. Design System

**Location**: `tokens/`, `gtk4/`, `examples/`

#### Token System

**Files**:
- `color-tokens.json` - Source of truth
- `color-tokens.css` - CSS custom properties
- `color-oklch-map.json` - OKLCH mappings
- `color-tokens-oklch.css` - OKLCH variants

**Generation Flow**:
```
color-tokens.json
    |
    +---> gen_oklch_tokens.py
    |         |
    |         v
    |     color-oklch-map.json
    |     color-tokens-oklch.css
    |
    +---> Manual curation
              |
              v
          brand_*.css (5 variants)
```

#### GTK4 Demo

**Location**: `gtk4/`

**Components**:
- `demo.py` - Application with runtime theme switching
- `brand_default.css` - Standard color vision
- `brand_protan.css` - Red-weak variant
- `brand_deutan.css` - Green-weak variant
- `brand_tritan.css` - Blue-weak variant
- `brand_mono.css` - Grayscale variant

---

### 5. Development Tools

**Location**: `tools/`, `Makefile`

#### Python Tools

| Tool | Purpose |
|------|---------|
| `contrast_check.py` | WCAG contrast validation |
| `separation_check.py` | CVD color separation |
| `gen_oklch_tokens.py` | OKLCH token generation |
| `okcolor.py` | sRGB/OKLCH conversion |
| `devserver.py` | HTTP development server |

#### Makefile Targets

| Target | Purpose |
|--------|---------|
| `serve` | Start dev server |
| `contrast-check` | Run contrast validator |
| `separation-check` | Run separation validator |
| `oklch` | Generate OKLCH tokens |
| `sphinx-install-theme` | Install docs theme |
| `sphinx-example-html` | Build example docs |
| `test-python` | Run Python tests |
| `test-c` | Run C tests |
| `lint` | Run linters |
| `clean` | Remove build artifacts |

---

## Data Flow Diagrams

### CVD Simulation Pipeline

```
User Application
      |
      | (image data)
      v
+------------------+
| DaltonLens-Python|  or  +---------------+
| (research/dev)   |      | libDaltonLens |
+------------------+      | (production)  |
      |                   +---------------+
      |                         |
      | (simulated image)       |
      v                         v
+------------------------------------+
|        Design Validation           |
| (contrast_check, separation_check, |
|  GATE-007 achromat luminance check)|
+------------------------------------+
      |
      | (pass/fail + metrics)
      v
+------------------------------------+
|        Developer Feedback          |
+------------------------------------+
```

**Dichromacy pipeline** (Brettel/Vienot/Machado, protan/deutan/tritan):
```
sRGB -> linear RGB -> LMS -> CVD projection -> LMS -> linear RGB -> sRGB
```

**Achromatopsia pipeline** (Simulator_Achromat / dl_simulate_cvd_achromat):
```
sRGB -> linear RGB --(BT.709)--> Y -> (Y, Y, Y) -> sRGB
Y = 0.2126*R + 0.7152*G + 0.0722*B  (ITU-R BT.709-6 / WCAG 2.1)
```
BT.709 photopic weights are chosen for consistency with GATE-002 (CONTRAST).

**Blue-cone monochromacy pipeline** (Simulator_BCM / dl_simulate_cvd_bcm):
```
sRGB -> linear RGB --(BCM 3x3)--> gamut-fix -> severity blend -> sRGB
BCM = linearRGB_from_LMS @ A  (SmithPokorny75)
  A replaces L,M rows with white_lms[i]*bt709; keeps S row unchanged
```
The full LMS roundtrip is precomputed to a single 3x3 operation per pixel.

### Token Generation Pipeline

```
+------------------+
| color-tokens.json|  (Manual edit: default/protan/deutan/tritan variants)
+------------------+
         |
         +------------------+
         |                  |
         v                  v
+------------------+  +--------------------+
| gen_oklch_tokens |  | gen_mono_tokens.py |
+------------------+  | (BT.709 luminance  |
         |            |  projection for     |
         |            |  achromat / mono)   |
         |            +--------------------+
         |
    +----+----+
    |         |
    v         v
+-------+  +-------+
| .json |  | .css  |  (OKLCH variants)
+-------+  +-------+
         |
         v
+------------------+
| contrast_check   |  (Validation)
+------------------+
         |
    +----+----+
    |         |
    v         v
  PASS      FAIL -> iterate on colors
```

---

## Extension Points

### Adding New Algorithm

1. Implement `Simulator` subclass in `simulate.py`
2. Add conversion matrices to `convert.py` if needed
3. Generate ground truth images
4. Add tests to `test_simulate.py`
5. (Optional) Port to C in `libDaltonLens.c`

### Adding New Validator

1. Create tool in `tools/validators/`
2. Implement against specs in `specs/VALIDATORS_FRAMEWORK.md`
3. Add Makefile target
4. Document in CLAUDE.md

### Adding New Design Token Variant

1. Define colors in `color-tokens.json`
2. Run `make oklch` to generate derivatives
3. Create `brand_<variant>.css` in `gtk4/`
4. Run `make contrast-check` to validate
5. Update demo.py if needed

---

## Dependencies

### Runtime

| Component | Dependencies |
|-----------|--------------|
| DaltonLens-Python | NumPy, Pillow |
| libDaltonLens | None |
| GTK4 Demo | PyGObject, GTK4 |
| Tools | Python 3.8+ |

### Development

| Purpose | Tools |
|---------|-------|
| Python Lint | ruff, black |
| Python Test | pytest |
| C Build | CMake 3.16+ |
| Documentation | Sphinx |
| CI/CD | GitHub Actions |

---

## Security Considerations

- No network access in core algorithms
- No file system access except explicit I/O
- No user input parsing in library code
- Vendored dependencies audited for vulnerabilities

---

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|------------|-------|
| CVD Simulation | O(pixels) | Linear in image size |
| Color Conversion | O(1) | Per-pixel constant time |
| Contrast Check | O(tokens) | Linear in token count |

Memory usage:
- Python: 3x image size (input, intermediate, output)
- C: In-place, no additional allocation
