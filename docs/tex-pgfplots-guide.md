# TeX/Ti*k*Z/PGFPlots Guide (Brand + CVD)

This guide shows how to use the brand palette (indigo, gray, magenta) in LaTeX documents and pgfplots figures with CVD-safe defaults: color+non-color encodings (markers, dashes, hatch patterns) and robust grayscale fallback.

Files:
- `tex/brandpalette.sty` — package with color defs, cycle lists, and bar patterns
- `tex/example-pgfplots.tex` — minimal working example

## Requirements
- TeX distribution with `pgfplots` (>= 1.18 recommended)
- `tikz` libraries: `patterns`, `arrows.meta`
- For modern fonts, use `lualatex` or `xelatex` (optional)

## Quick Start

- Add to preamble:
  - `\usepackage{pgfplots}` then `\usepackage{brandpalette}`
  - `\pgfplotsset{compat=1.18}`
  - Select variant: `\brandsetup[variant=default]` or `protan|deutan|tritan|mono`
  - Apply brand plot styles: `\brandapplyplotstyles`

- Use pgfplots as usual; cycle list provides color+dash+marker. Bar charts get hatch fills via style names, e.g., `\addplot+[brandbarA]`.

## Variants
- `default` — standard brand colors
- `protan`, `deutan` — adjusted to preserve Indigo vs Magenta separability
- `tritan` — indigo shifted violet, magenta slightly redder, higher chroma
- `mono` — grayscale-only; relies on shapes, dashes, patterns

Switch with: `\brandsetup[variant=tritan]`.

## Non-color Encodings
- Lines: solid, dashed, dotted, dash-dot variations, increasing line widths
- Markers: `*` `square*` `triangle*` `diamond*` cycling
- Bars/areas: hatch patterns (north east lines, dots, crosshatch)
- Direct labels: use `nodes near coords`, `every node near coord/.append style={...}`

## Print/Grayscale
- Use `mono` variant for grayscale. You can also test by printing or converting the resulting PDF to grayscale.
- Ensure any distinctions remain visible with markers and hatch patterns.

## Compile
- `lualatex tex/example-pgfplots.tex` (or `pdflatex`)

## Tips
- Prefer direct labeling over legends for multi-line plots
- Increase `line width` for emphasis series instead of relying on color alone
- Use `mark repeat` to avoid clutter in dense plots
