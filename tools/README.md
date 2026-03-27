# Tools

Development and validation utilities for OpenPerception.

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `contrast_check.py` | WCAG contrast ratio validation for color tokens | `python tools/contrast_check.py` |
| `separation_check.py` | CVD color separation validation | `python tools/separation_check.py` |
| `gen_oklch_tokens.py` | Generate OKLCH color token variants | `python tools/gen_oklch_tokens.py` |
| `experimental_palette_report.py` | Validate an experimental token pack by path (defaults to mauve/burgundy pack) | `python tools/experimental_palette_report.py [tokens/file.json]` |
| `validate.py` | Unified validator CLI for implemented gates, explicit spec-only gaps, and auxiliary runtime surfaces | `python tools/validate.py [--json] [--seizure-manifest file.json] [--rendered-audits]` |
| `runtime_gap_report.py` | Declared-vs-runtime gap report across validator and system areas | `python tools/runtime_gap_report.py [--format markdown]` |
| `claims_coverage_report.py` | Coverage report linking seeded evidence claims to validators and runtime artifacts | `python tools/claims_coverage_report.py [--format markdown]` |
| `check_claims_registry.py` | Integrity checker for claim statuses, gate links, and referenced files | `python tools/check_claims_registry.py` |
| `repo_stats.py` | Generate machine-checkable repo stats from tracked files | `python tools/repo_stats.py [--output-json file.json] [--output-md file.md]` |
| `check_repo_stats.py` | Validate checked-in repo stats against the current tracked tree | `python tools/check_repo_stats.py [--json]` |
| `check_task_governance.py` | Integrity checker for `docs/task-ledger.md`, `docs/KNOWN_ISSUES.md`, and loose TODO-language debt | `python tools/check_task_governance.py` |
| `rendered_spatial_check.py` | Browser-backed overflow and focus-visibility audit for repo-owned example pages using Playwright | `python tools/rendered_spatial_check.py [--page examples/ui/palette-compare.html] [--viewport 320x900]` |
| `rendered_cognitive_check.py` | Browser-backed first-screen cognitive density audit for repo-owned example pages using Playwright | `python tools/rendered_cognitive_check.py [--page examples/ui/palette-compare.html] [--viewport 320x900]` |
| `profile_resolver.py` | Compose axis/display profiles and surface cross-axis conflicts | `python tools/profile_resolver.py [--profiles standard,reduced-motion]` |
| `palette_showcase_spec.py` | Emit the repo-driven Blender showcase payload for the living accessibility concept scene | `python tools/palette_showcase_spec.py [--output file.json]` |
| `octane_headless_probe.py` | Ensure OctaneServer is up and verify a warning-clean OctaneBlender headless startup path | `python tools/octane_headless_probe.py [--blender-executable OctaneBlender] [--json]` |
| `blender_palette_showcase_scene.py` | Build and render the repo-driven living accessibility concept scene inside Blender | `blender --background --factory-startup --python tools/blender_palette_showcase_scene.py -- --spec artifacts/blender_showcase/openperception_palette_showcase_spec.json --output artifacts/blender_showcase/openperception_palette_showcase_render.png --blend-output artifacts/blender_showcase/openperception_palette_showcase_scene.blend` |
| `scaling.py` | Convert logical pixels to physical pixels with snap-class quantization, optionally annotated with profile composition | `python tools/scaling.py --lp 44 --dpi 144 --scale 1.25 --snap-class touch-target [--profiles standard,reduced-motion]` |
| `semantic_tokens.py` | Shared loader and validator for first-class runtime semantic role tokens | Imported by CVD and tests |
| `claims_registry.py` | Shared loader and summarizer for the claims-to-runtime registry | Imported by report tools |
| `okcolor.py` | OKLCH color space utilities (library) | Imported by other scripts |
| `devserver.py` | Development HTTP server for examples | `python tools/devserver.py` |

## Validators

Automated enforcement gates implementing `specs/VALIDATORS_FRAMEWORK.md`:

| Module | Gate | Description |
|--------|------|-------------|
| `validators/base.py` | -- | `ValidatorGate` ABC, `GateResult`, `Severity`, `Status` |
| `validators/contrast.py` | GATE-002 | WCAG 2.1 AA/AAA contrast ratio enforcement |
| `validators/cvd.py` | GATE-003 | CVD color separation validation for brand pairs, expanded first-class semantic-role pairs, and non-color redundancy backups |
| `validators/seizure.py` | GATE-001 | First-pass frame-sequence flash safety validation |
| `validators/spatial.py` | GATE-004 | Static spatial checks over layout tokens, button target minima, focus affordances, viewport/meta responsiveness, main-layout/mobile-column responsiveness, swatch-grid adaptation, and wrapping example rows |
| `validators/temporal_depth.py` | GATE-005 | First-pass motion-token and display-profile temporal policy validation |
| `validators/cognitive.py` | GATE-006 | First-pass nav-count, density budgets, primary action density, visible-control burden, declared panel/metric-group burden, summary-view, notification-density, HUD-complexity, and reading-level checks |
| `validators/typography.py` | TYPE-001 | First-pass typography verifier over font contracts and example body-text rules |
| `validator_registry.py` | -- | Shared registry for implemented/spec-only gates and broader runtime gap areas |

## Rendered Audit

`rendered_spatial_check.py` is intentionally separate from `validate.py` by
default. It launches Chromium headlessly through Playwright, serves the
requested root directory over local HTTP, and checks rendered overflow plus
focus visibility at fixed viewport sizes. Use `python tools/validate.py
--rendered-audits` when you want those browser-backed summaries included in the
auxiliary runtime section.

`rendered_cognitive_check.py` follows the same pattern for `GATE-006`. It
measures first-screen visible controls, regions, clusters, and notifications at
fixed viewport sizes so we can reason about actual on-screen burden without
making the unified validator depend on a browser by default.

## Blender And Octane

For Octane-first showcase work, do not treat a raw `OctaneBlender` invocation
as the canonical readiness check. Use `octane_headless_probe.py` or
`make octane-probe` first so the repo verifies the clean
`--factory-startup` plus `OctaneServer` path before a full scene regeneration.

## Tests

```bash
# Run all tools tests
python -m pytest tools/tests/ -v
```

## Other Files

| File | Description |
|------|-------------|
| `PEAT_1.6_Seizure_Analysis.zip` | Photosensitive Epilepsy Analysis Tool (reference binary) |
