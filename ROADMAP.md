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
- [x] Design token system with CVD variants
- [x] Comprehensive specifications (5-pillar framework)
- [x] Research paper compendiums (400+ papers)
- [x] Development tools (contrast check, OKLCH generation)
- [x] GTK4 demo application
- [x] Repository infrastructure (git, docs, CI/CD)
- [x] CLI interface (all subcommands implemented in main.py)

### In Progress

- [ ] Validator framework implementation
- [ ] Performance optimization (array allocation)
- [ ] Web-based examples expansion

---

## Short-Term Goals

### Infrastructure Hardening

- [ ] Complete all CI/CD pipelines
- [ ] Achieve 90%+ test coverage for Python package
- [ ] Add cross-platform build validation (Linux, macOS, Windows)
- [ ] Set up automated documentation deployment

### CLI Completion

- [ ] Implement all CLI subcommands
- [ ] Add batch processing support
- [ ] Create CLI integration tests
- [ ] Document CLI usage comprehensively

### Validator Implementation

- [ ] WCAG 2.1 AA/AAA contrast validator
- [ ] CVD color separation validator
- [ ] Photosensitive seizure safety validator (PEAT-based)
- [ ] Pattern sensitivity detector
- [ ] Unified validator CLI interface

---

## Medium-Term Goals

### Web Platform

- [ ] Interactive CVD simulator web application
- [ ] Real-time contrast checker with suggestions
- [ ] Color palette analyzer with CVD preview
- [ ] Design token customization tool

### Algorithm Expansion

- [ ] Daltonization (color correction) algorithms
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
| P0 (Critical) | Infrastructure | CI/CD, test coverage, CLI completion |
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

To propose roadmap changes:
1. Open an issue with the `roadmap` label
2. Provide evidence or use case justification
3. Discuss in issue comments
4. Submit PR to update this document if approved

---

## Milestones

### v0.2.0 - Infrastructure Complete
- All CI/CD pipelines operational
- 90%+ test coverage
- CLI fully implemented
- Documentation deployed

### v0.3.0 - Validators Live
- WCAG contrast validator
- CVD separation validator
- Seizure safety validator
- Unified CLI interface

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
