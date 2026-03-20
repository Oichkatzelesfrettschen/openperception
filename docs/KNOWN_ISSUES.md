# Known Issues

This document tracks known limitations, bugs, and areas needing improvement in OpenPerception.

---

## Critical Issues

None currently. All critical issues have been resolved.

---

## Code Quality Issues

### Performance Note - Array Allocation (Documented)

**Location**: `algorithms/DaltonLens-Python/daltonlens/simulate.py` (CoblisV2Simulator.simulate_cvd)

**Description**: The CoblisV2 simulator allocates multiple intermediate arrays for clarity and debugging. This is a conscious design choice prioritizing readability over memory efficiency.

**Impact**: Higher memory usage during simulation (~50% more than optimal).

**Status**: Documented - intentional design decision

**Recommendation**: Use libDaltonLens (C) for performance-critical applications.

---

## Documentation Gaps

### Optional Dependency for Generate Tests

**Affected Area**: `algorithms/DaltonLens-Python/tests/test_generate.py`

**Description**: The Ishihara plate generation tests require the optional `Geometry3D` package.

**Impact**: 4 tests skip without this dependency. Core simulation tests (7/7) pass without it.

**Status**: Expected behavior - Geometry3D is optional

**Resolution**: Install with `pip install Geometry3D` if Ishihara generation is needed.

---

### Examples Documentation

**Affected Areas**: `examples/`

**Description**: 8 functional example files exist across 4 subdirectories:
- `examples/simulator/index.html` -- Interactive CVD simulator
- `examples/contrast/index.html` -- Contrast ratio checker
- `examples/viz/matplotlib_palette.py` -- Matplotlib palette visualization
- `examples/viz/d3-scale.js` -- D3.js scale configuration
- `examples/viz/chartjs.config.js` -- Chart.js configuration
- `examples/shared/auto-dev.js` -- Auto-reload development helper
- `examples/shared/query-variant.js` -- CVD variant query utility
- `examples/ui/variant-toggle.html` -- CVD variant toggle UI

**Impact**: Examples exist but lack a README or usage documentation.

**Status**: Documentation needed (v0.2.0)

---

### Specification Implementation Gap

**Description**: `specs/VALIDATORS_FRAMEWORK.md` defines 6 validation gates. GATE-002 (CONTRAST) and GATE-003 (CVD) are implemented in `tools/validators/`. GATE-001 (SEIZURE), GATE-004 (SPATIAL), GATE-005 (TEMPORAL/DEPTH), and GATE-006 (COGNITIVE) remain spec-only. The unified validator CLI is not yet implemented.

**Impact**: 4 of 6 gates and the unified CLI lack enforcement tooling.

**Status**: Remaining gates targeted for v0.3.0

---

## Infrastructure Issues

### No Automated Documentation Deployment

**Description**: Documentation must be built locally; no CI/CD deploys to GitHub Pages or similar.

**Impact**: Users must build docs themselves.

**Status**: Targeted for v0.2.0

---

### Limited Cross-Platform Testing

**Description**: CI/CD primarily tests Linux; macOS and Windows coverage is limited.

**Impact**: Potential platform-specific bugs may go undetected.

**Status**: Targeted for v0.2.0

---

## Third-Party Dependencies

### Vendored jQuery

**Location**: `datasets/ishihara-plate-learning/scripts/jquery.js`

**Description**: Older jQuery 1.x version is vendored in the Ishihara learning tool.

**Impact**: Potential security vulnerabilities in outdated library.

**Status**: Low priority - standalone educational tool

**Workaround**: Tool functions offline; no sensitive data handling.

---

### Vendored stb Libraries

**Location**: `algorithms/libDaltonLens/tests/`

**Description**: stb_image, stb_image_write, and sokol_time are vendored.

**Impact**: May fall behind upstream security patches.

**Status**: Monitor upstream for security updates

---

### PEAT Binary in Git

**Location**: `tools/PEAT_1.6_Seizure_Analysis.zip` (1.1 MB)

**Description**: The Photosensitive Epilepsy Analysis Tool binary is committed to the repository as a reference tool for GATE-001 SEIZURE validation research.

**Impact**: Inflates repository size. Binary files are not ideal for git.

**Status**: Acceptable for now; consider Git LFS or external hosting if more binaries are added

---

## Research Gaps

### Anomalous Trichromacy Models

**Description**: Current algorithms focus on dichromacy (complete deficiency). Anomalous trichromacy (partial deficiency) simulation uses simple interpolation.

**Impact**: Less accurate simulation for mild CVD.

**Status**: Research ongoing - see `research/colorblindness/algorithms/`

---

### Blue Cone Monochromacy

**Description**: BCM is documented in research but not implemented in simulation algorithms.

**Impact**: Cannot simulate this rare condition.

**Status**: Targeted for algorithm expansion (v0.4.0)

---

## Reporting New Issues

When reporting new issues:

1. Check this document first for known issues
2. Search existing GitHub issues
3. If new, create issue with:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Any error messages or logs

---

## Issue Resolution Process

1. **Triage**: Issues are reviewed and labeled
2. **Prioritize**: Assigned to milestone based on impact
3. **Investigate**: Root cause analysis
4. **Fix**: Implementation with tests
5. **Document**: Update this file and CHANGELOG.md
6. **Release**: Include in appropriate version

---

## Version Targets

| Issue | Target Version |
|-------|----------------|
| Examples documentation | v0.2.0 |
| Remaining validator gates (4 of 6) | v0.3.0 |
| Unified validator CLI | v0.3.0 |
| Documentation deployment | v0.2.0+ |
| Cross-platform CI | v0.2.0 |
| BCM simulation | v0.4.0 |

---

Last Updated: 2026-03-19
