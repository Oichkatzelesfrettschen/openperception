# OpenPerception Roadmap

This document outlines the development priorities and goals for OpenPerception.

---

## Vision

Create the most comprehensive, evidence-based toolkit for visual accessibility, enabling developers and designers to build inclusive experiences for people with color vision deficiency, neurodivergent conditions, and other visual processing differences.

---

## Current Status

### Completed

- [x] Core CVD simulation algorithms (Brettel, Vienot, Machado)
- [x] Python package (DaltonLens-Python)
- [x] C library (libDaltonLens)
- [x] Design token system with CVD variants (protan, deutan, tritan, mono)
- [x] Comprehensive specifications (5-pillar framework)
- [x] Research paper compendiums and curated local source cache
- [x] Development tools (contrast check, OKLCH generation, mono-token derivation)
- [x] GTK4 demo prototype
- [x] Repository infrastructure (git, docs, baseline GitHub Actions workflows)
- [x] CLI interface implemented in `algorithms/DaltonLens-Python/daltonlens/main.py`
- [x] Rod monochromacy (achromatopsia) simulation: `Simulator_Achromat`, `dl_simulate_cvd_achromat`
- [x] Blue cone monochromacy simulation: `Simulator_BCM`, `dl_simulate_cvd_bcm`
- [x] Machado2009 C port: `dl_simulate_cvd_machado2009` (anomalous trichromacy, protan/deutan/tritan)
- [x] GATE-007 ACHROMAT luminance contrast validator (`tools/validators/achromat.py`)
- [x] Systematic mono token derivation via BT.709 luminance projection (`tools/gen_mono_tokens.py`)

### In Progress

- [ ] Validator framework expansion and policy reconciliation
- [ ] Performance optimization (array allocation)
- [ ] Web-based examples expansion
- [ ] Governance and installation-requirements reconciliation

---

## Short-Term Goals

### Infrastructure Hardening

- [ ] Complete all CI/CD pipelines
- [x] Achieve 90%+ test coverage for Python package (90% achieved; simulate.py 97%)
- [ ] Add machine-checkable install smoke tests (T113)
- [ ] Add cross-platform build validation (Linux, macOS, Windows)
- [ ] Set up automated documentation deployment

### CLI Enhancements

- [x] Implement all CLI subcommands in `daltonlens/main.py`
- [x] Create CLI integration tests (direct-call tests in `test_cli_direct.py`, 83% coverage)
- [ ] Add batch processing support (T114)
- [ ] Document CLI usage comprehensively (T115)

### Validator Implementation

- [x] WCAG contrast validator
- [x] CVD color separation validator
- [ ] Photosensitive seizure safety validator (PEAT-based)
- [x] Spatial, temporal/depth, cognitive, and typography validators
- [ ] Unified validator CLI ergonomics and richer artifact-backed checks

---

## Medium-Term Goals

### Web Platform

- [ ] Interactive CVD simulator web application
- [ ] Real-time contrast checker with suggestions
- [ ] Color palette analyzer with CVD preview
- [ ] Design token customization tool

### Algorithm Expansion

- [x] Daltonization (color correction) algorithms (daltonize.py -- Fidaner, Simple)
- [ ] Anomalous trichromacy refined models
- [ ] Machine learning-based perceptual metrics
- [ ] Real-time video processing support

### Integration Libraries

- [ ] React component library
- [ ] Flutter widget package
- [ ] Unity plugin for game accessibility
- [ ] Figma plugin for design workflow

### Research Synthesis

- [ ] Meta-analysis of CVD simulation accuracy
- [ ] Neurodivergence design pattern catalog
- [ ] Cross-disability interaction study
- [ ] Automated literature monitoring

---

## Long-Term Goals

### Standards Contribution

- [ ] Propose additions to WCAG 3.0
- [ ] Collaborate with W3C Accessibility Guidelines WG
- [ ] Publish peer-reviewed validation studies
- [ ] Create industry adoption guide

### Advanced Features

- [ ] AI-powered accessibility audit
- [ ] Personalized accommodation profiles
- [ ] Cross-device synchronization
- [ ] Accessibility testing integration (Playwright, Cypress)

### Community Building

- [ ] Contributor documentation program
- [ ] Academic collaboration framework
- [ ] Industry partnership model
- [ ] Educational curriculum materials

---

## Deferred Items

The following items are tracked but explicitly deferred to future milestones:

### Deferred to v0.2.0+
- [ ] PEP 621 migration (setup.cfg to pyproject.toml consolidation)
- [ ] Sphinx API documentation generation
- [ ] GitHub Pages documentation deployment

### Deferred to v0.3.0+
- [ ] Daltonization C port
- [ ] GATE-001 SEIZURE validator implementation
- [ ] Pattern-sensitivity detector and richer seizure-manifest coverage
- [ ] Unified validator CLI and report ergonomics
- [ ] CI coverage badge in README
- [ ] PyPI publish workflow

### Deferred to v0.4.0+
- [ ] sRGB lookup table optimization for C library
- [ ] SIMD vectorization for C library
- [ ] Performance benchmark suite

### Spec-Only (no implementation timeline)
The following specs define aspirational architecture and have no current implementation target:
- `specs/TYPOGRAPHY_SYSTEM.md`
- `specs/LAYOUT_SYSTEM.md`
- `specs/DPI_TRANSITION_CONTRACT.md`
- `specs/DISPLAY_ADAPTATION_LAYER.md`
- `specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md` (INV-001 through INV-010 invariant enforcement)

---

## Non-Goals

The following are explicitly out of scope:

- Proprietary algorithms without open implementation
- Platform-specific solutions without cross-platform path
- Features without evidence-based justification
- Breaking backward compatibility without major version bump

---

## Priority Matrix

| Priority | Category | Items |
|----------|----------|-------|
| P0 (Critical) | Infrastructure | CI/CD hardening, test coverage, documentation |
| P1 (High) | Features | Validator framework, web simulator |
| P2 (Medium) | Expansion | Integration libraries, algorithm expansion |
| P3 (Low) | Future | AI features, standards contribution |

---

## Contributing to Roadmap

Roadmap items are driven by:

1. **User needs**: Issues and feature requests
2. **Research**: New findings in visual accessibility
3. **Standards**: Updates to WCAG and related guidelines
4. **Community**: Contributor proposals

For current live execution tracking and known debt, also read:

- `docs/task-ledger.md`
- `docs/KNOWN_ISSUES.md`

To propose roadmap changes:
1. Open an issue with the `roadmap` label
2. Provide evidence or use case justification
3. Discuss in issue comments
4. Submit PR to update this document if approved

---

## Aspirational Milestones

### v0.2.0 - Baseline Infrastructure Hardening
- Baseline GitHub Actions workflows operational
- 90%+ test coverage
- CLI fully implemented
- Documentation deployed

### v0.3.0 - Validator Expansion
- Seizure safety validator
- Unified CLI/report interface
- Rendered audits policy and browser bootstrap stabilized

### v0.4.0 - Web Platform
- Interactive simulator
- Contrast checker
- Palette analyzer

### v1.0.0 - Production Ready
- Stable API
- Comprehensive documentation
- Community governance
- Industry adoption

---

## References

- WCAG 2.1: https://www.w3.org/WAI/WCAG21/
- WCAG 3.0 Draft: https://www.w3.org/TR/wcag-3.0/
- ISO 9241-171: Accessibility guidance
- Section 508: US accessibility requirements
