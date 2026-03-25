# Examples

Interactive and script-based examples demonstrating OpenPerception features.
All HTML examples can be opened directly in a browser or served via `make serve`
from the repository root (starts a dev server on port 8000).

---

## HTML Examples

### `simulator/index.html` -- CVD Simulator

Interactive browser tool for simulating color vision deficiency.
Drop in or link an image and toggle between protan, deutan, tritan, and normal
views in real time. Uses the design tokens from `tokens/` for UI colors.

**Open:** `http://localhost:8000/examples/simulator/`

---

### `contrast/index.html` -- Contrast and Tokens Checker

Displays the full color token palette with WCAG contrast ratios computed
against common background colors. Useful for verifying that color choices
pass AA/AAA contrast requirements before committing to a design.

**Open:** `http://localhost:8000/examples/contrast/`

---

### `ui/variant-toggle.html` -- CVD Variant Toggle

Demonstrates the CSS variant-switching system. The `data-cvd` attribute on
`<html>` drives which CVD stylesheet is active. Includes a toggle UI so you
can switch between `default`, `protan`, `deutan`, `tritan`, and `mono` at
runtime without a page reload.

**Open:** `http://localhost:8000/examples/ui/variant-toggle.html`

---

### `ui/palette-compare.html` -- Current, Accessible, and Red Theme Packs

Renders the production pack, the experimental mauve/burgundy accessibility
pack, and the atmosphere-first red/mahogany theme side by side, using the same
authored variant and optional simulated CVD filter for all lanes.

**Open:** `http://localhost:8000/examples/ui/palette-compare.html`

---

## Script Examples

### `viz/matplotlib_palette.py` -- Matplotlib CVD-Aware Palette

Generates a Matplotlib `cycler` from the design tokens, with a `variant`
parameter that selects the CVD-safe color set:

```
variant: 'default' | 'protan' | 'deutan' | 'tritan' | 'mono'
```

Reads `tokens/color-tokens.json` at runtime. Import and call `get_cycler(variant)`
to use in any Matplotlib figure.

```bash
python examples/viz/matplotlib_palette.py
```

---

### `viz/d3-scale.js` -- D3 Categorical Scale

Drop-in replacement for `d3.scaleOrdinal` that uses CVD-aware brand tokens
instead of D3's default color scheme. Pass `variant` to select the palette.

```js
import { getCVDScale } from './examples/viz/d3-scale.js';
const color = getCVDScale('deutan');  // returns d3.scaleOrdinal
```

---

### `viz/chartjs.config.js` -- Chart.js 4 Config

A Chart.js dataset color config that applies CVD-safe colors AND non-color
encodings (dash patterns, marker shapes) so charts remain distinguishable
for both CVD and monochrome viewers.

```js
import { buildDatasetConfig } from './examples/viz/chartjs.config.js';
const datasets = buildDatasetConfig(rawData, 'protan');
```

---

## Shared Utilities

### `shared/auto-dev.js`

Injects a hot-reload `<script>` tag during local development (detects
`localhost`) so HTML examples refresh when files change. Safe to include in
production pages -- it no-ops when not on localhost.

### `shared/query-variant.js`

Reads a `?variant=` URL query parameter and sets `document.documentElement.dataset.cvd`
accordingly. Lets you deep-link to a specific CVD view, e.g.:

```
http://localhost:8000/examples/contrast/?variant=protan
```

---

## Running All Examples

```bash
# From repository root
make serve          # Starts HTTP server on port 8000

# Then open in browser:
# http://localhost:8000/examples/simulator/
# http://localhost:8000/examples/contrast/
# http://localhost:8000/examples/ui/variant-toggle.html
```
