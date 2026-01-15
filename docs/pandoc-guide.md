# Pandoc Theme Preset (Brand + CVD)

Files:
- `templates/pandoc/brand.html` — template
- `templates/pandoc/brand.css` — styles using tokens
 - `templates/pandoc/brand-print.css` — print/PDF overrides

Usage (HTML):
- Serve tokens or ensure relative paths are correct. From repo root:
  - `pandoc -s -t html5 --template templates/pandoc/brand.html -o out.html README.md`
- Optionally add metadata: `-M title="My Doc" -M date="2025-10-31"`

Usage (PDF via wkhtmltopdf/weasyprint):
- Add the print stylesheet: `-c templates/pandoc/brand.css -c templates/pandoc/brand-print.css`
- Example with wkhtmltopdf: `wkhtmltopdf out.html out.pdf`

Notes:
- The template links `tokens/color-tokens.css` then `brand.css`.
- Switch CVD variants by setting `<html data-cvd="...">` or post-process.
- For PDF via wkhtmltopdf/weasyprint, ensure CSS files are discoverable or inline them.
