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
- GitHub Actions CI/CD workflows
- docs/KNOWN_ISSUES.md documenting current gaps

### Changed
- Enhanced Makefile with test and lint targets
- Updated MASTER_INDEX.md organization

### Fixed
- (Pending) CLI NotImplementedError in main.py
- (Pending) Performance TODO in simulate.py
- (Pending) FIXME verification in convert.py

---

## [0.1.0] - 2024-XX-XX (Pre-infrastructure)

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

[Unreleased]: https://github.com/username/openperception/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/username/openperception/releases/tag/v0.1.0
