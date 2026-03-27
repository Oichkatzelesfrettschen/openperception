# Task Ledger

This file is the repo's live task tracker for the current audit and
implementation tranche.

Status markers:

- `[x]` done in the current audited state
- `[ ]` not yet complete

Current tranche focus:

- reconcile repo claims with runtime reality
- refine installation requirements module by module
- convert loose governance prose into repo-native, checkable files
- keep every newly introduced warning or ambiguity visible as tracked debt

## Phase 1. Baseline And Governance

- [x] T001 Reconfirm clean worktree and baseline branch state on `main`.
- [x] T002 Inventory repo-wide install and requirements surfaces under `README.md`,
  `Makefile`, `pyproject.toml`, and module `README.md` files.
- [x] T003 Audit loose placeholder and TODO language across repo-owned docs.
- [x] T004 Confirm that `docs/KNOWN_ISSUES.md` was referenced but missing.
- [x] T005 Inspect `tools/validate.py` and current validator runtime behavior.
- [x] T006 Confirm that repo-owned root tooling uses Python 3.10+ syntax in
  `tools/`.
- [x] T007 Create the live debt register in `docs/KNOWN_ISSUES.md`.
- [x] T008 Create the live 100-step task tracker in `docs/task-ledger.md`.
- [x] T009 Add a governance verifier under `tools/task_governance.py`.
- [x] T010 Add a CLI wrapper in `tools/check_task_governance.py`.
- [x] T011 Add governance tests in `tools/tests/test_check_task_governance.py`.
- [x] T012 Add a fast repo-integrity entrypoint to `Makefile`.
- [x] T013 Wire the governance check into `Makefile` help and phony targets.
- [x] T014 Add a dedicated CI or default `make check` lane for all integrity verifiers.
- [ ] T015 Expand governance checks to cover additional strategic docs.
- [ ] T016 Add machine-readable task metadata if markdown proves too weak.
- [ ] T017 Add issue aging fields so stale debt can be detected automatically.
- [ ] T018 Add owners or maintainers for high-risk debt items.
- [ ] T019 Add due-date or milestone mapping for critical debt items.
- [ ] T020 Reconcile governance docs after each major tranche automatically.

## Phase 2. Installation Requirements And Reproducibility

- [x] T021 Add a repo-root install guide in `REQUIREMENTS.md`.
- [x] T022 Split core vs optional toolchains in `REQUIREMENTS.md`.
- [x] T023 Add `docs/module-requirements/daltonlens-python.md`.
- [x] T024 Add `docs/module-requirements/libdaltonlens.md`.
- [x] T025 Add `python-packages/sphinx-brand-theme/REQUIREMENTS.md`.
- [x] T026 Add `artifacts/blender_showcase/REQUIREMENTS.md`.
- [x] T027 Update `README.md` to point at `REQUIREMENTS.md`.
- [x] T028 Update module readmes to point at their local `REQUIREMENTS.md` files.
- [x] T029 Separate root-tooling Python requirements from subpackage support claims.
- [x] T030 Document Git LFS requirements for `papers/downloads/` and `datasets/source_assets/`.
- [x] T031 Document optional Chromium and Playwright expectations for rendered audits.
- [x] T032 Document optional Blender and Octane expectations for showcase regeneration.
- [x] T033 Verify editable install flows for each Python package in a fresh environment.
- [x] T034 Add exact Sphinx version expectations for `python-packages/sphinx-brand-theme`.
- [ ] T035 Add OS package hints for Linux contributors who need `cmake`, `cppcheck`,
  and browser dependencies.
- [x] T036 Add contributor instructions for Playwright browser bootstrap if required.
- [ ] T037 Add a reproducible environment bootstrap script if the docs remain too manual.
- [ ] T038 Add machine-checkable install smoke tests for root and module lanes.
- [ ] T039 Validate build docs on a second host profile.
- [x] T040 Close any remaining mismatch between docs and actual install commands.

## Phase 3. Claim Audit And Source Validation

- [x] T041 Create a claims-audit source index in `docs/external_sources/repo_claims_audit_sources.md`.
- [x] T042 Create a repo audit note in `docs/repo-audit-2026-03-26.md`.
- [x] T043 Test the hypothesis that the top-level `Python 3.8+` root claim is accurate.
- [x] T044 Refute that claim for repo-owned root tooling using Python syntax evidence.
- [x] T045 Validate the WCAG contrast minimum used by the contrast gate.
- [x] T046 Validate the stereoblindness prevalence source used by the depth lane.
- [x] T047 Downgrade or rewrite claims that lack exact support.
- [x] T048 Audit every numbered or thresholded claim in `README.md`.
- [x] T049 Audit every completed-state claim in `ROADMAP.md`.
- [x] T050 Audit every statistics claim in `MASTER_INDEX.md`.
- [ ] T051 Audit research-count claims in paper compendiums for reproducible counting.
- [ ] T052 Add source-index references for roadmap-level standards claims.
- [ ] T053 Add source-index references for major depth-accommodation claims not yet indexed.
- [ ] T054 Add source-index references for major color-support taxonomy claims not yet indexed.
- [ ] T055 Add an overclaim phrase linter for unsupported certainty words.
- [x] T056 Add a stats generator for local corpus counts instead of hardcoded prose counts.
- [x] T057 Reconcile cache counts between `MASTER_INDEX.md` and actual files.
- [x] T058 Audit README language for "production-ready" assertions lane by lane.
- [x] T059 Audit package support claims against packaging metadata.
- [x] T060 Publish a second audit note after the next reconciliation pass.

## Phase 4. Build, Validation, And Runtime Integrity

- [x] T061 Run `python3 tools/validate.py` and record live warning surfaces.
- [x] T062 Run `python3 tools/check_claims_registry.py`.
- [x] T063 Run targeted validator tests under `tools/tests/test_validate.py`.
- [x] T064 Add `tools/check_task_governance.py` to a broader default check lane.
- [x] T065 Add `tools/check_source_cache_links.py` to the broader default check lane.
- [x] T066 Add `tools/check_paper_corpus.py` to the broader default check lane.
- [x] T067 Add `tools/check_source_assets.py` to the broader default check lane.
- [x] T068 Add a `make check` umbrella target once scope is settled.
- [ ] T069 Ensure every verifier error points to one exact file and task or issue row.
- [x] T070 Add JSON output mode to repo-governance verifiers for future automation.
- [x] T071 Audit whether `tools/validate.py` should fail on warnings for selected profiles.
- [x] T072 Decide whether rendered audits belong in default or optional validation.
- [ ] T073 Add benchmark or performance smoke coverage where docs claim performance intent.
- [ ] T074 Add a validator summary doc that maps runtime warnings to debt IDs.
- [ ] T075 Add a typography debt issue row for the current TYPE-001 warning.
- [ ] T076 Add CVD borderline-separation debt issue rows for the current GATE-003 warnings.
- [ ] T077 Add cognitive reading-level debt issue rows for the current GATE-006 warnings.
- [ ] T078 Add regression fixtures for any validator bug uncovered during the tranche.
- [x] T079 Confirm the Makefile help text stays synchronized with real targets.
- [ ] T080 Review whether root lint targets are too broad or too narrow.

## Phase 5. Research Corpus, Cache, And Provenance Discipline

- [x] T081 Reconfirm the canonical literature lane is `papers/downloads/`.
- [x] T082 Reconfirm the canonical non-paper asset lane is `datasets/source_assets/`.
- [x] T083 Audit whether every source-cache doc links to a live research-facing note.
- [x] T084 Audit whether every high-value research note links back to a source cache doc.
- [ ] T085 Add a verifier for unresolved provenance placeholders in source docs.
- [ ] T086 Audit topic-lane README coverage under `papers/downloads/`.
- [ ] T087 Audit whether each cached topic has a corresponding source-notes lane.
- [ ] T088 Reconcile legacy migration closeout docs with current file layout.
- [x] T089 Add checks for stale cache counts in `MASTER_INDEX.md`.
- [ ] T090 Verify that each repaired paper cited in docs resolves to the canonical path.
- [ ] T091 Audit the Ishihara source-asset lane for downstream references.
- [ ] T092 Add a small machine-readable registry for source-cache doc ownership.
- [ ] T093 Add a source-index doc for any remaining uncached but repeatedly cited external source.
- [ ] T094 Verify that all provenance docs use stable ASCII-only filenames.
- [ ] T095 Review whether any cached HTML traces should be upgraded to PDFs if now accessible.
- [ ] T096 Add periodic revalidation tasks for key web standards sources.
- [ ] T097 Add a migration playbook for future research-local artifacts.
- [ ] T098 Add a paper-count generation script if prose counts keep drifting.
- [x] T099 Audit whether bibliography files are canonical and non-duplicative.
- [x] T100 Cut the next tranche from the remaining open items and rebaseline this ledger.

## Phase 6. Blender And Octane Cleanliness

- [x] T101 Reproduce the live Octane and Blender startup warnings under the
  current host configuration.
- [x] T102 Isolate the Blender startup-script warning to the local
  `blendermcp_autostart.py` loader path.
- [x] T103 Confirm a clean Octane headless path exists with `--factory-startup`
  plus an `OctaneServer` preflight.
- [x] T104 Add a repo-owned Octane headless probe under `tools/`.
- [x] T105 Add tests and Makefile coverage for the Octane probe lane.
- [x] T106 Update showcase requirements and tool docs to point at the clean
  Octane path instead of a naive raw launch.
- [x] T107 Move full showcase regeneration behind the repo-owned
  `tools/render_blender_showcase.py` driver and `make showcase-render`.
- [x] T108 Re-run the real-physics showcase refinement tranche only through the
  cleaned Octane path so the canonical `.png` and `.blend` are regenerated
  without startup-warning debt.
