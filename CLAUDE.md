# OpenPerception - Claude Project Memory

This file provides context for AI assistants working on the OpenPerception repository.

---

## Project Overview

OpenPerception is a visual accessibility research and tools repository focused on:
- Color Vision Deficiency (CVD) simulation and accommodation
- Neurodivergent-friendly design patterns
- Evidence-based accessibility specifications
- Production-ready algorithm implementations

---

## Repository Layout

```
openperception/
|-- algorithms/           # Core algorithm implementations
|   |-- DaltonLens-Python/   # Python CVD package (pip installable)
|   +-- libDaltonLens/       # C library (public domain, zero deps)
|-- datasets/             # Learning tools and test data
|-- docs/                 # User-facing guides
|-- examples/             # Code examples (viz, simulator, contrast)
|-- gtk4/                 # GTK4 demo application
|-- papers/               # Research paper compendiums (400+ papers)
|-- python-packages/      # Additional Python packages
|-- research/             # Domain research by topic
|-- specs/                # Technical specifications
|-- tokens/               # Design token definitions
+-- tools/                # Development utilities
```

---

## Build Instructions

### DaltonLens-Python

```bash
cd algorithms/DaltonLens-Python
pip install -e .

# Run tests
pytest -v tests/
```

### libDaltonLens (C)

```bash
cd algorithms/libDaltonLens
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make

# Run tests (requires ground truth images)
./tests/test_simulation
```

### Development Tools

```bash
# From repository root
make serve              # Start dev server on port 8000
make contrast-check     # Validate WCAG contrast ratios
make separation-check   # Check CVD color separation
make oklch              # Generate OKLCH tokens
```

### Documentation

```bash
make sphinx-install-theme   # Install custom Sphinx theme
make sphinx-example-html    # Build example documentation
```

---

## Standards and Conventions

### Python

- **Style**: Black formatter, 88 character line limit
- **Linting**: Ruff for fast, comprehensive linting
- **Types**: Type hints encouraged but not enforced
- **Imports**: isort with Black-compatible settings
- **Tests**: pytest with ground truth image comparison

### C

- **Style**: 4-space indentation, K&R braces
- **Compiler flags**: `-Wall -Wextra -Werror` in CI
- **Dependencies**: Zero external dependencies (single-file library)
- **Tests**: Compare against DaltonLens-Python ground truth

### Documentation

- **Format**: Markdown with GitHub-flavored extensions
- **Structure**: WHY/WHAT/HOW pattern for explanations
- **References**: Academic citations in specs/REFERENCES_BIBLIOGRAPHY.md

---

## Key Files

### Core Algorithms

| File | Purpose |
|------|---------|
| `algorithms/DaltonLens-Python/daltonlens/simulate.py` | CVD simulation algorithms |
| `algorithms/DaltonLens-Python/daltonlens/convert.py` | Color space conversions |
| `algorithms/libDaltonLens/libDaltonLens.c` | C implementation |
| `algorithms/libDaltonLens/libDaltonLens.h` | Public API |

### Specifications

| File | Purpose |
|------|---------|
| `specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md` | Core accessibility framework |
| `specs/VALIDATORS_FRAMEWORK.md` | Testing and validation |
| `specs/EVIDENCE_MATRIX.md` | Research citation matrix |

### Configuration

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python tooling configuration |
| `.editorconfig` | Editor settings |
| `Makefile` | Build orchestration |

---

## Testing

### Python Tests

```bash
cd algorithms/DaltonLens-Python
pytest -v tests/test_simulate.py   # Algorithm tests
pytest -v tests/test_generate.py   # Image generation tests
```

Ground truth images are stored in `tests/images/` for regression testing.

### C Tests

```bash
cd algorithms/libDaltonLens/build
./tests/test_simulation
```

Compares C output against Python ground truth with tolerance of 1 byte difference per channel.

### Integration Tests

```bash
make contrast-check      # Should report all passing
make separation-check    # Should report adequate separation
```

---

## Common Tasks

### Add a New CVD Algorithm

1. Implement in `daltonlens/simulate.py` following `Simulator` base class
2. Add ground truth images to `tests/images/`
3. Add test case to `tests/test_simulate.py`
4. Update C implementation if needed

### Update Color Tokens

1. Edit `tokens/color-tokens.json` (source of truth)
2. Run `make oklch` to regenerate OKLCH variants
3. Run `make contrast-check` to validate WCAG compliance
4. Update CSS files in `gtk4/` if needed

### Add Research Paper

1. Add entry to appropriate compendium in `papers/`
2. Update `specs/EVIDENCE_MATRIX.md` if it supports a claim
3. Update `MASTER_INDEX.md` if adding new compendium

---

## Known Issues

See `docs/KNOWN_ISSUES.md` for current gaps and limitations.

Key items:
- Validator framework specified but not fully implemented
- Performance TODO in simulate.py (CoblisV2 array allocation, intentional design decision)

---

## Architecture Notes

### CVD Simulation Pipeline

```
Input Image (sRGB)
    |
    v
Linear RGB (gamma decode)
    |
    v
LMS Color Space (cone responses)
    |
    v
CVD Projection (Brettel/Vienot/Machado)
    |
    v
LMS (simulated)
    |
    v
Linear RGB
    |
    v
sRGB (gamma encode)
    |
    v
Output Image
```

### Design Token Flow

```
color-tokens.json (source of truth)
    |
    +-> gen_oklch_tokens.py -> color-oklch-map.json
    |                       -> color-tokens-oklch.css
    |
    +-> Manual edit -> brand_*.css (GTK4 variants)
```

---

## External Dependencies

### Python

- NumPy: Array operations
- Pillow: Image I/O
- pytest: Testing (dev only)
- ruff/black: Linting/formatting (dev only)

### C

- None (zero-dependency single-file library)
- Test dependencies (vendored): stb_image, stb_image_write, sokol_time

---

## CI/CD

GitHub Actions workflows in `.github/workflows/`:

- `python-tests.yml`: Run pytest on Python package
- `c-build.yml`: Build and test C library
- `lint.yml`: Run ruff and format checks

All workflows treat warnings as errors.

---

## Troubleshooting

### System Resource Issues (Claude CLI Crashes)

**Symptom**: Claude CLI crashes with `ThreadPoolBuildError: IOError(Os { code: 11, kind: WouldBlock })` or SIGABRT signal

**Root Cause**: System resource exhaustion - combination of:
1. Thread count exceeding ulimit (multiple Claude instances)
2. High swap usage (25GB+) causing memory pressure
3. Aggressive swappiness setting (150 default on some systems)
4. Rayon thread pool initialization requiring resources not available

**Prevention Measures** (applied 2026-01-29):

```bash
# Check system health
system-health                    # Shows memory, swap, threads, Claude instances

# Before intensive operations
free -h                          # Ensure >4GB available RAM
ps aux | grep claude | wc -l     # Close unnecessary Claude sessions
```

**Configuration Applied**:

1. **Swappiness reduced to 10** (from 150):
   ```bash
   # Temporary
   sudo sysctl vm.swappiness=10

   # Permanent (in /etc/sysctl.d/99-swappiness.conf)
   vm.swappiness=10
   vm.vfs_cache_pressure=50
   ```

2. **Rayon thread limit** (in ~/.zshrc):
   ```bash
   export RAYON_NUM_THREADS=2
   ```

3. **Optimized ulimit values** (in /etc/security/limits.conf):
   ```bash
   # System: AMD Ryzen 5 5600X3D (12 threads), 31GB RAM
   # Previous: nproc=4096 (insufficient, caused thread exhaustion)
   # Optimized: nproc=16384 (4x increase, allows 10+ Claude instances)

   eirikr  soft  nproc   16384     # Max user processes/threads
   eirikr  hard  nproc   32768     # Emergency headroom
   eirikr  soft  nofile  524288    # File descriptors (adequate)
   eirikr  hard  nofile  1048576   # Doubled for safety
   ```

   **Rationale**:
   - Previous limit (4096) caused crashes with current thread usage (4464)
   - New soft limit (16384) provides 4x headroom for development workload
   - Hard limit (32768) allows emergency expansion
   - Still <1% of kernel limit (4,194,304) - safe from runaway processes

   **Verification** (requires logout/login):
   ```bash
   verify-ulimits              # Run verification script
   ulimit -u                   # Should show 16384
   ulimit -Hu                  # Should show 32768
   ```

4. **Monitoring installed**:
   - `~/.local/bin/system-health` - System dashboard
   - `~/.local/bin/memory-monitor` - Cron job alerts (every 5 minutes)
   - Alerts when available RAM <2GB or threads >80% of ulimit

**Recovery After Crash**:

```bash
# Verify repository integrity
cd /home/eirikr/Github/openperception
git fsck --full                  # Should report no errors
git status                       # Verify clean working tree

# Test build artifacts
cd algorithms/libDaltonLens/build
./test_simulation               # Should show GOOD for all tests

# Test Python package
cd algorithms/DaltonLens-Python
python3 -c "from daltonlens import simulate; print('OK')"
```

**Emergency Memory Reclaim** (use with caution):

```bash
# Drop filesystem caches (safe, non-destructive)
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches

# Reclaim swap (ONLY if free RAM > swap usage + 2GB safety margin)
sudo swapoff -a && sudo swapon -a
```

**Verified After 2026-01-29 Crash**:
- Repository integrity: CLEAN (git fsck passed)
- Build artifacts: FUNCTIONAL (C tests pass, Python imports)
- Data loss: NONE
- Working tree: CLEAN

**Quick Reference**: See `~/openperception-troubleshooting.md` for command cheat sheet

---

## Contact

For questions about this repository, see CONTRIBUTING.md or open an issue.
