# DaltonLens-Python Requirements

This file documents the editable-install and validation expectations for the
`algorithms/DaltonLens-Python/` submodule as used from the root repo.

## Required

- Python with `pip`
- NumPy
- Pillow
- Geometry3D for the Ishihara plate generation tests
- OpenCV (`opencv-python-headless`) for the Ishihara plate generation tests

Repo-preferred editable install:

```bash
make venv
```

Direct editable install for a pre-existing writable virtual environment:

```bash
python3 -m pip install -e algorithms/DaltonLens-Python
```

## Testing

```bash
make test-python
```

Notes:

- the direct editable-install snippet assumes you are already inside a writable
  virtual environment
- it does not install the extra test-only dependencies by itself
- `make venv` is the supported path for root-repo and module verification on
  PEP 668 hosts

## Metadata Caveat

The local submodule `pyproject.toml` does not currently declare
`requires-python`.

That means:

- the package may work across a broader range of interpreters
- but this repo does not currently expose that floor in machine-readable
  packaging metadata

Until that is fixed, the safest path is to validate the editable install using
the same interpreter you use for the root repo tooling.
