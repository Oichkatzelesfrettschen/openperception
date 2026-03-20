import sphinx_brand_theme


project = 'Brand + CVD Sphinx Example'
extensions = []
templates_path = ['_templates']
exclude_patterns = []

html_theme = 'brand_theme'
html_theme_path = [sphinx_brand_theme.get_html_theme_path()]
html_static_path = ['_static']
html_css_files = ['brand.css', 'color-tokens.css']

