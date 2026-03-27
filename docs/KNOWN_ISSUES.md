# Known Issues

This file is the repo's live debt register. It lists current issues that are
real, reproducible, and still unresolved after the latest audit pass.

Issue classes:

- implementation gap: behavior does not yet meet the intended standard
- documentation gap: docs overstate, understate, or omit something important
- tooling gap: local setup or validation depends on undeclared prerequisites
- evidence gap: a claim exists without enough primary-source or runtime support

## KI-001 Root Tooling Python Floor Is Underspecified

- class: documentation gap
- status: open
- affected files: `README.md`, `REQUIREMENTS.md`, `pyproject.toml`, `tools/`
- problem: top-level docs previously said `Python 3.8+`, but the repo-owned
  root tooling uses PEP 604 union syntax such as `Path | None`, which requires
  Python 3.10+.
- consequence: contributors can follow the old claim and then hit syntax
  errors before reaching the real validation surface.
- current handling: root requirements now state `Python 3.10+` for repo-owned
  tooling and note that the current audit pass was run on Python 3.14.3.

## KI-002 `DaltonLens-Python` Metadata Does Not Declare A Machine-Readable Python Floor

- class: tooling gap
- status: open
- affected files: `algorithms/DaltonLens-Python/pyproject.toml`,
  `docs/module-requirements/daltonlens-python.md`
- problem: the local package metadata does not currently expose
  `requires-python`, so compatibility claims for the editable package are not
  machine-checkable from packaging metadata alone.
- consequence: downstream tooling cannot reliably infer the supported Python
  range for that package.
- current handling: the module requirements doc now calls this out explicitly
  instead of silently implying broader support.

## KI-003 Full Python Test Lane Depends On A Local Dev Environment

- class: tooling gap
- status: open
- affected files: `Makefile`, `requirements-dev.txt`,
  `docs/module-requirements/daltonlens-python.md`
- problem: the full `DaltonLens-Python` test lane requires a local virtual
  environment and the `Geometry3D` dependency for Ishihara generation tests.
- consequence: running `make test-python` against a bare system Python can fail
  even when the repo itself is healthy.
- current handling: `make venv` now provisions the preferred local environment,
  and the missing dependency is declared in `requirements-dev.txt`.

## KI-004 Strategic Docs Still Need Ongoing Reconciliation

- class: documentation gap
- status: open
- affected files: `ROADMAP.md`, `docs/current-work-inventory.md`,
  `CHANGELOG.md`, `MASTER_INDEX.md`
- problem: some strategic docs are snapshots or ambition ledgers, while others
  describe current runtime state; they drift unless explicitly reconciled.
- consequence: readers can mistake a strategic milestone or stale count for a
  verified current-state claim.
- current handling: `README.md`, `ROADMAP.md`, and `MASTER_INDEX.md` were
  reconciled in the March 26 audit pass, machine-checkable repo counts now live
  in `docs/generated/repo_stats.json` and `docs/generated/repo_stats.md`, and
  `docs/task-ledger.md` continues to track the remaining strategic-doc burn-down
  work.

## KI-005 Optional Artifact Tooling Is Still Partly Host-Managed

- class: tooling gap
- status: open
- affected files: `REQUIREMENTS.md`, `artifacts/blender_showcase/REQUIREMENTS.md`,
  `.github/workflows/python-tests.yml`, `tools/rendered_spatial_check.py`,
  `tools/rendered_cognitive_check.py`
- problem: Blender showcase regeneration still depends on local Blender or
  Octane Blender tooling that the repo documents but does not auto-install.
- consequence: a clean clone is not enough to run every optional artifact lane
  without additional host setup.
- current handling: requirements docs now split core vs optional toolchains,
  `make playwright-install` provisions the browser-backed audit lane locally,
  GitHub Actions now requires `make check-rendered` on a dedicated Ubuntu
  runner, and Blender host tooling remains explicitly manual.

## KI-006 Claims-To-Evidence Coverage Is Still Partial

- class: evidence gap
- status: open
- affected files: `specs/CLAIMS_RUNTIME_REGISTRY.json`,
  `docs/external_sources/`, `docs/repo-audit-2026-03-26.md`
- problem: some repo narrative claims have been audited and downgraded, but not
  every high-level statement is yet paired with a source index or offline
  verifier.
- consequence: some statements remain directionally true but not yet fully
  machine-backed.
- current handling: the 100-step tranche in `docs/task-ledger.md` includes a
  dedicated claim-verification burn-down phase.
