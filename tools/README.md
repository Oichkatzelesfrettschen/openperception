# Tools

Development and validation utilities for OpenPerception.

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `contrast_check.py` | WCAG contrast ratio validation for color tokens | `python tools/contrast_check.py` |
| `separation_check.py` | CVD color separation validation | `python tools/separation_check.py` |
| `gen_oklch_tokens.py` | Generate OKLCH color token variants | `python tools/gen_oklch_tokens.py` |
| `okcolor.py` | OKLCH color space utilities (library) | Imported by other scripts |
| `devserver.py` | Development HTTP server for examples | `python tools/devserver.py` |

## Validators

Automated enforcement gates implementing `specs/VALIDATORS_FRAMEWORK.md`:

| Module | Gate | Description |
|--------|------|-------------|
| `validators/base.py` | -- | `ValidatorGate` ABC, `GateResult`, `Severity`, `Status` |
| `validators/contrast.py` | GATE-002 | WCAG 2.1 AA/AAA contrast ratio enforcement |
| `validators/cvd.py` | GATE-003 | CVD color separation validation |

## Tests

```bash
# Run all tools tests (27 tests)
python -m pytest tools/tests/ -v
```

## Other Files

| File | Description |
|------|-------------|
| `PEAT_1.6_Seizure_Analysis.zip` | Photosensitive Epilepsy Analysis Tool (reference binary) |
