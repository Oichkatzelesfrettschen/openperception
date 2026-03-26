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

## KI-003 Unified Validation Still Returns Live Warnings

- class: implementation gap
- status: open
- affected files: `tools/validate.py`, `tools/validators/cvd.py`,
  `tools/validators/cognitive.py`, `tools/validators/typography.py`
- problem: the current runtime validator reports warnings for borderline CVD
  separations, reading-level burden, and typography checks.
- consequence: the repo has a functioning validator surface, but not a
  clean-pass accessibility baseline yet.
- current handling: warnings are treated as real debt and tracked in
  `docs/task-ledger.md`.

## KI-004 Strategic Docs Still Need Ongoing Reconciliation

- class: documentation gap
- status: open
- affected files: `ROADMAP.md`, `docs/current-work-inventory.md`,
  `CHANGELOG.md`, `MASTER_INDEX.md`
- problem: some strategic docs are snapshots or ambition ledgers, while others
  describe current runtime state; they drift unless explicitly reconciled.
- consequence: readers can mistake a strategic milestone or stale count for a
  verified current-state claim.
- current handling: `docs/task-ledger.md` now tracks reconciliation work as a
  first-class task lane, and `docs/repo-audit-2026-03-26.md` records the latest
  audit findings.

## KI-005 Optional Tooling Is Still Not Auto-Provisioned

- class: tooling gap
- status: open
- affected files: `REQUIREMENTS.md`, `artifacts/blender_showcase/REQUIREMENTS.md`,
  `tools/rendered_spatial_check.py`, `tools/rendered_cognitive_check.py`
- problem: rendered audits and Blender showcase regeneration depend on local
  browser and Blender tooling that the repo documents but does not auto-install.
- consequence: a clean clone is not enough to run every optional artifact lane
  without additional host setup.
- current handling: requirements docs now split core vs optional toolchains and
  show the exact commands needed for each lane.

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
