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
- `Simulator_Brettel1997`
- `Simulator_Vienot1999`
- `Simulator_Machado2009`
- `Simulator_Vischeck`

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
enum DLDeficiency { DL_PROTAN, DL_DEUTAN, DL_TRITAN };

void dl_simulate_cvd(
    enum DLDeficiency deficiency,
    float severity,
    unsigned char *srgba_image,
    size_t width, size_t height, size_t bytesPerRow
);
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
| (contrast_check, separation_check) |
+------------------------------------+
      |
      | (pass/fail + metrics)
      v
+------------------------------------+
|        Developer Feedback          |
+------------------------------------+
```

### Token Generation Pipeline

```
+------------------+
| color-tokens.json|  (Manual edit)
+------------------+
         |
         v
+------------------+
| gen_oklch_tokens |
+------------------+
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
