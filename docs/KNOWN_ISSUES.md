# Known Issues

This file is the repo's live debt register. It lists current issues that are
real, reproducible, and still unresolved after the latest audit pass.

Issue classes:

- implementation gap: behavior does not yet meet the intended standard
- documentation gap: docs overstate, understate, or omit something important
- tooling gap: local setup or validation depends on undeclared prerequisites
- evidence gap: a claim exists without enough primary-source or runtime support

Each entry carries an `opened: YYYY-MM-DD` field so stale issues can be detected
by date comparison (T127).  Issues not resolved within one major tranche should
receive an explicit resolution-path update.

High-risk entries (implementation gap class) carry an `owner:` field and a
`milestone:` field so they can be assigned and prioritized against ROADMAP
version targets (T018, T019).

## KI-001 Root Tooling Python Floor Is Underspecified

- class: documentation gap
- status: open
- opened: 2026-03-26
- owner: unassigned
- milestone: ongoing (docs updated; no further milestone gate required)
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
- status: mitigated
- opened: 2026-03-26
- owner: unassigned
- milestone: v0.2.0+ (PEP 621 migration deferred to this version)
- affected files: `algorithms/DaltonLens-Python/setup.cfg`,
  `algorithms/DaltonLens-Python/pyproject.toml`,
  `docs/module-requirements/daltonlens-python.md`
- problem: the local `pyproject.toml` does not have a `[project]` table
  with `requires-python`, so PEP 621-aware tooling reading only
  `pyproject.toml` cannot infer the Python floor.
- consequence: downstream tooling that reads only `pyproject.toml` cannot
  reliably infer the supported Python range for that package.
- current handling: `setup.cfg` declares `python_requires = >=3.12`, which
  setuptools reads during build and editable install. Full PEP 621 migration
  (consolidating `setup.cfg` into `pyproject.toml [project]`) is deferred to
  v0.2.0+. The module requirements doc calls out the floor explicitly.

## KI-003 Full Python Test Lane Depends On A Local Dev Environment

- class: tooling gap
- status: open
- opened: 2026-03-26
- owner: unassigned
- milestone: v0.2.0 (CI/CD hardening; Geometry3D install documented, venv provisioned)
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
- opened: 2026-03-26
- owner: unassigned
- milestone: ongoing (reconciled each major tranche; no fixed version gate)
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
- opened: 2026-03-26
- owner: unassigned
- milestone: v0.3.0+ (rendered-audit policy stabilized; Blender/Octane remain host-managed)
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
- opened: 2026-03-26
- owner: unassigned
- milestone: ongoing (Phase 9 closed T053, T054, T093; remaining gaps deferred)
- affected files: `specs/CLAIMS_RUNTIME_REGISTRY.json`,
  `docs/external_sources/`, `docs/repo-audit-2026-03-26.md`
- problem: some repo narrative claims have been audited and downgraded, but not
  every high-level statement is yet paired with a source index or offline
  verifier.
- consequence: some statements remain directionally true but not yet fully
  machine-backed.
- current handling: the 100-step tranche in `docs/task-ledger.md` includes a
  dedicated claim-verification burn-down phase.

## KI-007 GATE-003 Borderline Separation In Mono Variant

- class: implementation gap
- status: resolved
- opened: 2026-04-10
- resolved: 2026-04-12
- owner: unassigned (requires token design judgment)
- milestone: v0.3.0 (validator expansion tranche)
- affected files: `tokens/color-tokens.json` (mono variant),
  `tools/validators/cvd.py`, `tools/validators/achromat.py`
- problem: GATE-003 (CVD) reports `mono/primary-vs-accent` at Oklab distance
  0.178, in the borderline range [0.15, 0.20). This is because `primaryStrong`
  (#374151, gray-700) and `accentStrong` (#6B7280, gray-500) are adjacent gray
  ramp stops.
- consequence: in a monochromatic rendering, primary and accent are
  distinguishable only by luminance contrast (10.3:1 vs 4.8:1 on white), not
  by hue or chroma. Non-color redundancy (marker/dash series) is present and
  compensates for chart elements, but UI components relying solely on these two
  semantic colors to convey different states would lose that distinction.
- current handling: GATE-003 emits a WARN (non-blocking). GATE-007 (ACHROMAT)
  verifies that each color individually has adequate contrast on white. Marker
  and dash redundancy is present in the mono viz token variant.
- resolution path: allocate more separated gray stops for primaryStrong and
  accentStrong in the mono variant (e.g., gray-900 for primaryStrong, gray-500
  for accentStrong). Requires re-evaluating GATE-002 (CONTRAST) for any new
  assignments and running `make validate` to confirm both gates pass.

## KI-008 GATE-007 Low Contrast Between Mono Viz Categorical Pair

- class: implementation gap
- status: resolved
- opened: 2026-04-10
- resolved: 2026-04-12
- owner: unassigned (requires token design judgment; resolve alongside KI-007)
- milestone: v0.3.0 (validator expansion tranche; resolve together with KI-007)
- affected files: `tokens/color-tokens.json` (mono variant, viz.categorical),
  `tools/validators/achromat.py`
- problem: GATE-007 (ACHROMAT) reports `mono/viz.categorical[0-1]` contrast
  at 2.13:1, which is below the 3.0:1 WARN threshold. Both categorical[0]
  (#374151, gray-700) and categorical[1] (#6B7280, gray-500) are the same
  pair as primaryStrong and accentStrong -- adjacent gray ramp stops.
- consequence: in monochromatic rendering, categorical series 0 and 1 are
  indistinguishable by luminance contrast alone without non-color redundancy
  (marker shape or line dash pattern). Charts that use color alone to
  distinguish series 0 from 1 will fail for achromatopsia viewers.
- current handling: GATE-007 emits a WARN (non-blocking). Marker and dash
  redundancy is defined in the mono viz token variant and must be applied.
  GATE-003 also flags this pair under KI-007.
- resolution path: assign a more separated gray stop to categorical[0] or
  categorical[1] in the mono variant (e.g., gray-900 / gray-400), then
  re-run `make validate` to confirm GATE-007 and GATE-002 both pass.
- resolution: categorical[0] moved to gray-900 (#111827) and categorical[1]
  moved to gray-400 (#9CA3AF) in `tokens/color-tokens.json`. GATE-007
  `mono/viz.categorical[0-1]` contrast is now 6.99:1 (was 2.13:1). GATE-003
  `mono/primary-vs-accent` Oklab distance is now 0.341 (was 0.178). Both
  gates PASS. `make validate` confirmed clean.
