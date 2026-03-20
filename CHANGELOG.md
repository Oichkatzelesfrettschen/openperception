# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Repository infrastructure (git, .gitignore, .gitattributes)
- MIT License for root project
- README.md with project overview and quick start guide
- CLAUDE.md project memory for AI assistants
- CONTRIBUTING.md with contribution guidelines
- ARCHITECTURE.md documenting component relationships
- ROADMAP.md with project goals and milestones
- .editorconfig for editor consistency
- pyproject.toml with ruff/black configuration
- .clang-format for C code consistency
- GitHub Actions CI/CD workflows (python-tests, lint, c-build)
- docs/KNOWN_ISSUES.md documenting current gaps
- docs/quickstart.md with 5-minute getting started guide
- Validator framework base class (`tools/validators/base.py` -- ValidatorGate ABC)
- GATE-002 CONTRAST validator (`tools/validators/contrast.py`)
- GATE-003 CVD validator (`tools/validators/cvd.py`)
- Tools test suite (`tools/tests/` -- 27 tests)
- `.gitmodules` for submodule tracking (was missing)
- `.pre-commit-config.yaml` with ruff, black, and standard hooks
- `requirements-dev.txt` for development dependencies
- Daltonization module (`daltonize.py` -- Fidaner and Simple methods)
- CLI fully implemented (`main.py` -- simulate, daltonize, info subcommands)

### Research Updates (2026-03-19)
- Updated CVD_RESEARCH_REPORT.md with 2025-2026 findings: simulation accuracy study, gene therapy trial results, NVIDIA daltonization, WCAG 3.0/APCA status
- Created dyslexia visual processing research file (`research/neurodivergence/dyslexia/DYSLEXIA_VISUAL_PROCESSING_RESEARCH.md`)
- Updated colorblindness algorithms compendium with 5 new papers (simulation accuracy, ChromATA, NVIDIA daltonization, DL daltonization, Swin Transformer)
- Updated achromatopsia/BCM compendium with AGTC/MeiraGTx trial results, BGTF-027 Phase 1, treatment window study
- Updated ADHD compendium with retinal fundus biomarker study (95.5-96.9% AUROC), AI detection methods
- Updated cognitive load compendium with multimodal fNIRS+eye-tracking prediction (F1=0.87), intrinsic vs. extraneous load differentiation
- Updated seizure compendium with PSE tool validation framework, PEAT retirement confirmation, platform adoption status
- Added APCA reference and cross-references to papers/ in REFERENCES_BIBLIOGRAPHY.md
- Updated DETECTION_TOOLS.md with 2025-2026 validation research and platform adoption

### Changed
- Enhanced Makefile with test and lint targets
- Updated MASTER_INDEX.md organization and statistics
- Marked CLI subcommands and daltonization as completed in ROADMAP.md
- Updated KNOWN_ISSUES.md to reflect actual examples/ state (8 files, not empty)
- Renamed CVD_RESEARCH_REPORT_2024.md to CVD_RESEARCH_REPORT.md (content covers 2023-2026)
- Added implementation status table to VALIDATORS_FRAMEWORK.md
- Added "SPECIFICATION ONLY" headers to 4 aspirational spec files
- Added "Deferred Items" section to ROADMAP.md with milestone targets
- CI: coverage threshold enforced (--cov-fail-under=70), tools tests added, link check blocking, clang-format blocking
- Pre-commit: added mypy, bandit, conventional-commits hooks
- Fixed pyproject.toml known-first-party (removed non-package "tools")

### Fixed
- Performance TODO in simulate.py documented as intentional design decision
- 7 accuracy debt items resolved (false doc claims corrected)
- GitHub URL placeholders annotated in CHANGELOG

---

## [0.1.0] - 2026-01-15 (Pre-infrastructure)

### Components Present

#### DaltonLens-Python v0.1.6
- Brettel et al. (1997) CVD simulation
- Vienot et al. (1999) fast simulation
- Machado et al. (2009) severity model
- Vischeck reference compatibility
- Color space conversions (sRGB, Linear RGB, LMS)
- Test image generation (RGB spans, Ishihara patterns)

#### libDaltonLens (Public Domain)
- Single-file C implementation
- Brettel and Vienot algorithms
- Zero external dependencies
- SVG filter port

#### Design System
- Color token definitions (JSON, CSS)
- OKLCH color space support
- Five CVD variant stylesheets
- GTK4 demo application

#### Specifications
- UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md
- VALIDATORS_FRAMEWORK.md
- EVIDENCE_MATRIX.md
- 11 additional specification documents

#### Research
- 7 paper compendiums (400+ papers cataloged)
- 5 research domain categories
- CVD, neurodivergence, cognitive load, seizures, visual impairments

#### Tools
- contrast_check.py - WCAG contrast validation
- separation_check.py - CVD color separation
- gen_oklch_tokens.py - OKLCH token generation
- okcolor.py - OKLCH utilities
- devserver.py - Development HTTP server

---

## Version History Notes

This changelog was created as part of repository infrastructure setup. Prior work existed without formal version tracking. The [0.1.0] section documents the state of components that existed before infrastructure was added.

Future versions will follow semantic versioning:
- MAJOR: Breaking API changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

---

<!-- Update these URLs when repository is published to GitHub -->
[Unreleased]: https://github.com/openperception/openperception/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/openperception/openperception/releases/tag/v0.1.0
