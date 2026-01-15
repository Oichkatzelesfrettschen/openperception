# Contributing to OpenPerception

Thank you for your interest in contributing to OpenPerception. This document provides guidelines for contributing to the project.

---

## Code of Conduct

Be respectful, inclusive, and constructive. This project focuses on accessibility - we expect contributors to embody those values in their interactions.

---

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment:

```bash
# Python development
cd algorithms/DaltonLens-Python
pip install -e ".[dev]"

# C development
cd algorithms/libDaltonLens
mkdir build && cd build
cmake ..
make
```

---

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/add-new-algorithm`
- `fix/contrast-calculation-bug`
- `docs/update-quickstart`
- `refactor/simplify-color-conversion`

### Commit Messages

Follow Conventional Commits:

```
type(scope): short description

Longer explanation if needed.

Closes #123
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Code Quality

Before submitting:

```bash
# Python
ruff check .
black --check .
pytest -v

# C
cmake --build . --target test
```

All checks must pass. Warnings are treated as errors.

---

## Pull Request Process

1. **Create a focused PR**: One feature or fix per PR
2. **Update documentation**: Include relevant doc changes
3. **Add tests**: New features need test coverage
4. **Pass CI**: All checks must be green
5. **Request review**: Tag maintainers for review

### PR Template

```markdown
## Summary
Brief description of changes.

## Changes
- Change 1
- Change 2

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Lint checks pass
- [ ] CI is green
```

---

## Code Standards

### Python

- Use Black for formatting (88 char line limit)
- Use ruff for linting
- Add type hints for public APIs
- Document with docstrings (NumPy style)

```python
def simulate_cvd(
    image: np.ndarray,
    deficiency: Deficiency,
    severity: float = 1.0,
) -> np.ndarray:
    """
    Simulate color vision deficiency on an image.

    Parameters
    ----------
    image : np.ndarray
        Input image in sRGB color space, shape (H, W, 3).
    deficiency : Deficiency
        Type of CVD to simulate.
    severity : float, optional
        Severity from 0.0 (normal) to 1.0 (full dichromacy).

    Returns
    -------
    np.ndarray
        Simulated image in sRGB color space.
    """
```

### C

- 4-space indentation
- K&R brace style
- Document public API in header file
- No external dependencies

```c
/**
 * Simulate CVD on an image in-place.
 *
 * @param deficiency Type of color vision deficiency
 * @param severity Severity from 0.0 to 1.0
 * @param image RGBA image data (modified in-place)
 * @param width Image width in pixels
 * @param height Image height in pixels
 * @param stride Bytes per row
 */
void dl_simulate_cvd(
    enum DLDeficiency deficiency,
    float severity,
    unsigned char *image,
    size_t width,
    size_t height,
    size_t stride
);
```

### Documentation

- Use Markdown for all documentation
- Follow WHY/WHAT/HOW structure for explanations
- Include code examples for APIs
- Keep specifications evidence-based (cite sources)

---

## Testing Guidelines

### Python Tests

- Use pytest for all tests
- Store ground truth images in `tests/images/`
- Test multiple deficiency types and severities
- Document test rationale

```python
def test_brettel_protan_full():
    """Test Brettel simulation of full protanopia."""
    simulator = Simulator_Brettel1997()
    result = simulator.simulate_cvd(input_img, Deficiency.PROTAN, 1.0)
    expected = load_ground_truth("brettel_protan_1.0.png")
    np.testing.assert_array_almost_equal(result, expected, decimal=5)
```

### C Tests

- Compare against Python ground truth
- Allow tolerance for floating-point differences
- Test edge cases (null pointers, zero dimensions)

---

## Adding New Features

### New Algorithm

1. Research the algorithm and gather citations
2. Implement in Python first with tests
3. Port to C if performance-critical
4. Add to `simulate.py` following `Simulator` base class
5. Document in README and update specs

### New Tool

1. Add to `tools/` directory
2. Add Makefile target
3. Document usage in `docs/`
4. Add to CLAUDE.md common tasks

### New Research Area

1. Create directory under `research/`
2. Add compendium to `papers/`
3. Update `specs/EVIDENCE_MATRIX.md`
4. Update `MASTER_INDEX.md`

---

## Research Contributions

We welcome research contributions:

- **Paper summaries**: Add to compendiums in `papers/`
- **Evidence citations**: Update `specs/EVIDENCE_MATRIX.md`
- **Specification updates**: Propose changes with evidence

All claims should be backed by peer-reviewed research where possible.

---

## Reporting Issues

### Bug Reports

Include:
- Operating system and version
- Python/compiler version
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternatives considered
- Supporting research (if applicable)

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License (or the specific license of the component you're modifying).

---

## Questions?

Open an issue or discussion for questions about contributing.
