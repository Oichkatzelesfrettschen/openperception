# DaltonLens-Python Requirements

This file documents the editable-install and validation expectations for the
`algorithms/DaltonLens-Python/` submodule as used from the root repo.

## Required

- Python with `pip`
- NumPy
- Pillow

Editable install:

```bash
python3 -m pip install -e algorithms/DaltonLens-Python
```

## Testing

```bash
cd algorithms/DaltonLens-Python
python3 -m pytest tests/ -v --tb=short
```

## Metadata Caveat

The local submodule `pyproject.toml` does not currently declare
`requires-python`.

That means:

- the package may work across a broader range of interpreters
- but this repo does not currently expose that floor in machine-readable
  packaging metadata

Until that is fixed, the safest path is to validate the editable install using
the same interpreter you use for the root repo tooling.
