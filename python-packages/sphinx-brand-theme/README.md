# sphinx-brand-theme

Minimal Sphinx theme binding CVD-friendly brand tokens (indigo, gray, magenta).

Install (editable):

```
pip install -e python-packages/sphinx-brand-theme
```

Local package expectations for this repo are documented in `REQUIREMENTS.md`.

Use in `conf.py`:

```
import sphinx_brand_theme
html_theme = 'brand_theme'
html_theme_path = [sphinx_brand_theme.get_html_theme_path()]
```

Ensure `_static` has `color-tokens.css` if not using the packaged copy.
