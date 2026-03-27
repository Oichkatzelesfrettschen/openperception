# sphinx-brand-theme Requirements

This file documents the local packaging expectations for the Sphinx theme lane.

## Required

- Python 3.8+ according to package metadata in `pyproject.toml`
- `pip`
- a Sphinx documentation project that will consume the theme

Editable install:

```bash
make venv
```

## Verification

The repo currently validates this lane indirectly through importable package
layout and documentation usage. If you are actively modifying the theme, also
build the example Sphinx docs with the repo-selected interpreter:

```bash
make sphinx-example-html
```

Exact repo example-docs expectation:

- Sphinx 9.1.0 from `requirements-dev.txt`

Direct package-only install, if you do not want the full repo dev environment:

```bash
python3 -m pip install -e python-packages/sphinx-brand-theme
python3 -m pip install Sphinx==9.1.0
```

## Notes

- the package metadata floor (`>=3.8`) is intentionally narrower than the root
  repo tooling floor (`>=3.10`)
- example-doc verification follows the repo dev environment, not just the
  package metadata
- the theme package does not auto-install a complete docs toolchain for every
  consumer project
- keep `README.md`, `pyproject.toml`, and this file aligned when the package
  metadata changes
