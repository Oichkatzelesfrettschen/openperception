# In-Browser Contrast Checker

Use the interactive checker to validate contrast and see token swatches per variant.

Files:
- `examples/contrast/index.html`

Run locally:
- Serve the repo (to avoid file:// CORS issues) with: `python3 -m http.server` and open `http://localhost:8000/examples/contrast/`
- Switch variants from the dropdown (sets `data-cvd`)
- Test standard pairs or custom foreground/background hex

Notes:
- The checker computes WCAG contrast in sRGB.
- Swatches are read from computed CSS variables of `tokens/color-tokens.css`.

