# Sphinx Theme (Brand + CVD)

Files:
- `sphinx/brand_theme/` — minimal theme
- `sphinx/brand_theme/static/brand.css` — uses CSS tokens

Usage in `conf.py` (packaged theme):

```
import sphinx_brand_theme
html_theme = 'brand_theme'
html_theme_path = [sphinx_brand_theme.get_html_theme_path()]
html_static_path = ['_static']
```

Install locally (editable):

```
pip install -e python-packages/sphinx-brand-theme
```

Usage in `conf.py` (local theme folder):

```
import os
html_theme = 'brand_theme'
html_theme_path = [os.path.abspath('sphinx')]
html_static_path = ['_static']
html_css_files = ['brand.css', 'color-tokens.css']
```

- Copy tokens CSS into `_static` or symlink if not using the packaged copy:
  - `cp tokens/color-tokens.css docs/_static/color-tokens.css`
  - `cp sphinx/brand_theme/static/brand.css docs/_static/brand.css`
- Build: `sphinx-build -b html docs _build/html`
- Switch CVD variant by setting `data-cvd` in `layout.html` or via a small JS toggle.

Notes:
- Keep links underlined and ensure focus is visible if you add interactive elements in docs.
