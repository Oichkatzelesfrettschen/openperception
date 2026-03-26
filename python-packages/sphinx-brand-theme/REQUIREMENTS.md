# sphinx-brand-theme Requirements

This file documents the local packaging expectations for the Sphinx theme lane.

## Required

- Python 3.8+ according to package metadata in `pyproject.toml`
- `pip`
- a Sphinx documentation project that will consume the theme

Editable install:

```bash
python3 -m pip install -e python-packages/sphinx-brand-theme
```

## Verification

The repo currently validates this lane indirectly through importable package
layout and documentation usage. If you are actively modifying the theme, also
build the example Sphinx docs:

```bash
make sphinx-example-html
```

## Notes

- the theme package does not auto-install a complete docs toolchain for every
  consumer project
- keep `README.md`, `pyproject.toml`, and this file aligned when the package
  metadata changes
