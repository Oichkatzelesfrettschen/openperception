# Pandoc Template Guide

This guide covers the OpenPerception Pandoc template system for producing
brand-consistent HTML documents and PDFs from Markdown source files.

---

## WHY

Writing docs in Markdown keeps content separate from presentation.
The Pandoc templates wire OpenPerception's design tokens directly into
the output, so contrast ratios and CVD-friendly colors are inherited
automatically without manual CSS overrides.

---

## Template Files

| File | Purpose |
|------|---------|
| `templates/pandoc/brand.html` | Pandoc HTML5 template (title, date, body slots) |
| `templates/pandoc/brand.css` | Screen stylesheet using design token CSS variables |
| `templates/pandoc/brand-print.css` | Print/PDF overrides (forces high-contrast black-and-white) |

The HTML template links `tokens/color-tokens.css` (design tokens) and
`brand.css` (layout). The template uses relative paths; run pandoc from
the repository root or adjust paths for your output directory.

---

## Prerequisites

```bash
# Install Pandoc (Arch/Manjaro)
sudo pacman -S pandoc

# Verify
pandoc --version

# PDF via WeasyPrint (recommended; pure Python, no Java)
pip install weasyprint

# PDF via wkhtmltopdf (alternative; requires wkhtmltopdf binary)
sudo pacman -S wkhtmltopdf
```

---

## HTML Output

```bash
# From repository root
pandoc -s -t html5 \
  --template templates/pandoc/brand.html \
  -M title="My Document" \
  -M date="2026-02-26" \
  -o out.html \
  README.md
```

Open `out.html` in a browser. CSS token variables resolve to the
default (normal vision) palette unless you set a CVD variant (see below).

### Multiple Source Files

```bash
# Concatenate sections in order
pandoc -s -t html5 \
  --template templates/pandoc/brand.html \
  -M title="Full Spec" \
  -o out.html \
  docs/quickstart.md docs/simulator-guide.md docs/contrast-guide.md
```

---

## PDF Output

### Via WeasyPrint (recommended)

```bash
# Step 1: produce HTML
pandoc -s -t html5 \
  --template templates/pandoc/brand.html \
  -M title="My Document" \
  -o out.html README.md

# Step 2: convert to PDF
weasyprint out.html out.pdf
```

WeasyPrint respects `@media print` rules in `brand-print.css`, which
forces black-and-white output suitable for physical printing. The print
stylesheet is loaded automatically via `brand.css`.

### Via wkhtmltopdf (alternative)

```bash
pandoc -s -t html5 \
  --template templates/pandoc/brand.html \
  -M title="My Document" \
  -o out.html README.md

wkhtmltopdf out.html out.pdf
```

Note: wkhtmltopdf uses an older WebKit engine and may not support all
CSS custom properties (design tokens) correctly. Test the output before
relying on it for production documents.

---

## Metadata Variables

The template supports these Pandoc metadata variables:

| Variable | Effect |
|----------|--------|
| `title` | Rendered in `<title>` tag and `<h1 class="title">` |
| `date` | Rendered below the title in `<div class="date">` |

Pass via `-M key=value` on the command line, or add a YAML front matter
block to your Markdown:

```markdown
---
title: CVD Simulation Report
date: 2026-02-26
---

## Introduction
...
```

---

## CVD Variant Switching

The design token stylesheet exports separate CSS custom properties per
CVD variant. Switch variants by setting the `data-cvd` attribute on the
`<html>` or `<body>` element.

For a static HTML document, add the attribute directly:

```html
<!-- In the generated out.html, find and edit: -->
<html data-cvd="deutan">
```

Or post-process with sed:

```bash
# Generate for deuteranopia simulation
sed -i 's/<html>/<html data-cvd="deutan">/' out.html
```

| `data-cvd` value | Variant |
|------------------|---------|
| (not set) | Normal vision |
| `protan` | Protanopia/protanomaly |
| `deutan` | Deuteranopia/deuteranomaly |
| `tritan` | Tritanopia/tritanomaly |
| `achromat` | Achromatopsia |

---

## CSS Classes

The stylesheet provides a few utility classes for HTML output:

| Class | Use |
|-------|-----|
| `.notice` | Callout box with subtle magenta background |
| `.btn` | Generic button style |
| `.btn-primary` | Filled primary-brand button |

Use these in raw HTML blocks inside Markdown:

```markdown
<div class="notice">
This feature requires Python 3.8 or later.
</div>
```

---

## Design Token Integration

`brand.css` consumes the following token CSS variables from
`tokens/color-tokens.css`:

| Variable | Used for |
|----------|---------|
| `--surface` | Page background |
| `--surface-subtle` | Header, code blocks, table headers |
| `--text` | Body text |
| `--text-muted` | Date, blockquotes |
| `--border` | Borders |
| `--link` | Hyperlink color |
| `--indigo-700` | Document title |
| `--indigo-500` | Blockquote left border |
| `--brand-primary` | Primary button background |
| `--brand-primary-strong` | Primary button border |
| `--magenta-200` | Notice box background |

If you edit `tokens/color-tokens.json`, run `make oklch` to regenerate
CSS, then re-render your HTML to pick up the changes.

---

## Troubleshooting

**CSS variables not resolved (design tokens show as literal text)**
- Ensure `tokens/color-tokens.css` is served or present relative to the HTML file.
- Browsers require HTTP (not `file://`) for cross-directory stylesheets; use `make serve`.

**PDF output uses wrong colors**
- `brand-print.css` forces black-and-white under `@media print`. This is intentional.
- If you need a color PDF, remove or override the `@media print` block.

**Pandoc: template not found**
- Verify the `--template` path is correct relative to your working directory.
- Example from repo root: `--template templates/pandoc/brand.html`

**wkhtmltopdf: CSS custom properties not applied**
- wkhtmltopdf does not support CSS custom properties (variables). Use WeasyPrint instead.
