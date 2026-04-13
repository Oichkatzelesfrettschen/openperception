# OpenPerception Requirements

This file is the repo-wide installation and environment guide.

Use it as the source of truth for contributor setup. Module-specific
requirements live in the root doc lane or next to the relevant local package:

- `docs/module-requirements/daltonlens-python.md`
- `docs/module-requirements/libdaltonlens.md`
- `python-packages/sphinx-brand-theme/REQUIREMENTS.md`
- `artifacts/blender_showcase/REQUIREMENTS.md`

## Scope

OpenPerception mixes several lanes:

- repo-owned Python tooling under `tools/`
- the upstream `DaltonLens-Python` package under `algorithms/DaltonLens-Python/`
- the upstream `libDaltonLens` C library under `algorithms/libDaltonLens/`
- the local Sphinx theme under `python-packages/sphinx-brand-theme/`
- optional local rendered-audit and Blender artifact lanes

Those lanes do not all share the same dependency floor, so this document keeps
them separate instead of pretending one command provisions everything.

## Core Repo Tooling

Required for the root repo checks and most documentation and validator work:

- Git
- Git LFS
- Python 3.10+ for repo-owned tooling in `tools/`
- `pip`

Current audited interpreter:

- Python 3.14.3

Why the root floor is 3.10+:

- repo-owned tooling uses PEP 604 union syntax such as `Path | None`
- that syntax is not valid on Python 3.8 or 3.9

## Core Setup

```bash
make venv
```

Optional local theme package:

The `venv` target installs:

- `requirements-dev.txt`
- editable `algorithms/DaltonLens-Python`
- editable `python-packages/sphinx-brand-theme`
- Sphinx for the example docs lane
- Playwright Python bindings for the rendered-audit lane

Pull tracked binary artifacts after clone:

```bash
git lfs pull
```

## Core Verification

Fast repo integrity:

```bash
make integrity-check
```

Accessibility runtime validator:

```bash
make validate
```

Targeted tests:

```bash
make test-tools
make test-python
make check
```

Optional docs build:

```bash
make sphinx-example-html
```

## Optional Toolchains

### C build lane

Needed for `algorithms/libDaltonLens/`:

- CMake 3.16+
- a C compiler supported by your platform

**Linux OS packages** (Debian/Ubuntu family):

```bash
sudo apt-get install cmake build-essential
```

**Arch/CachyOS** (pacman):

```bash
sudo pacman -S cmake base-devel
```

Optional static analysis (cppcheck is run in CI):

```bash
# Debian/Ubuntu
sudo apt-get install cppcheck

# Arch/CachyOS
sudo pacman -S cppcheck
```

See `docs/module-requirements/libdaltonlens.md`.

### Rendered audits

Needed for:

- `tools/rendered_spatial_check.py`
- `tools/rendered_cognitive_check.py`

Requirements:

- local Chromium-capable Playwright environment

**Linux OS packages** (Debian/Ubuntu family):

```bash
# system libraries Playwright's bundled Chromium needs
sudo apt-get install libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 \
    libgbm1 libasound2
```

On Arch/CachyOS these are generally pulled in by the chromium package.

Bootstrap commands:

```bash
make venv
make playwright-install
```

Policy:

- `make check` does not run rendered audits by default on local hosts
- `make check-rendered` is the explicit local lane once Chromium is installed
- CI now runs `make check-rendered` on a dedicated Ubuntu runner that installs Chromium

### Blender showcase

Needed for:

- `artifacts/blender_showcase/`
- `tools/blender_palette_showcase_scene.py`

Requirements:

- Blender
- Octane Blender if you want the current preferred render path
- Blender MCP only if you want live agent-driven scene control

See `artifacts/blender_showcase/REQUIREMENTS.md`.

## Known Gaps

- `algorithms/DaltonLens-Python/pyproject.toml` does not have a `[project]`
  table with `requires-python`; the floor is declared in `setup.cfg` and
  full PEP 621 migration is deferred to v0.2.0+ (see KI-002).
- optional toolchains are documented here but not auto-installed.
- the root repo prefers a local `.venv` because Linux hosts enforce PEP 668
  for the system Python.
- some strategic docs still need ongoing reconciliation with runtime state; see
  `docs/KNOWN_ISSUES.md` and `docs/task-ledger.md`.
- a reproducible environment bootstrap script is still a manual process; see
  T037 in `docs/task-ledger.md`.
