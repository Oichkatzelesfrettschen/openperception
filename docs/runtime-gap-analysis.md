# Runtime Gap Analysis

Date: 2026-03-22

## What the lacunae actually are

OpenPerception has a serious declared system for:

- evidence and claims,
- axis conflicts,
- scaling and quantization,
- reflow and layout,
- typography,
- display adaptation,
- and validator governance.

The current runtime is much narrower.

Today the executable core is mainly:

- CVD simulation in `algorithms/DaltonLens-Python`
- C implementation in `algorithms/libDaltonLens`
- WCAG contrast enforcement in [contrast.py](/home/eirikr/Github/openperception/tools/validators/contrast.py)
- token separation enforcement in [cvd.py](/home/eirikr/Github/openperception/tools/validators/cvd.py)
- supporting standalone checks in `tools/contrast_check.py` and `tools/separation_check.py`
- palette experimentation and reporting in `tools/experimental_palette_report.py`
- semantic-role-aware CVD validation in `tools/validators/cvd.py`
- first-class semantic role runtime tokens in `tokens/semantic-role-tokens.json`
- first-pass temporal/depth policy validation in `tools/validators/temporal_depth.py`
- first-pass cognitive/navigation validation in `tools/validators/cognitive.py`
- typography, profile composition, and scaling helpers surfaced through `tools/validate.py`

That means the repo's main gap is not lack of ideas. It is lack of runtime
realization for most of the declared architecture.

## Lacunae

1. Evidence is structured in [EVIDENCE_MATRIX.md](/home/eirikr/Github/openperception/specs/EVIDENCE_MATRIX.md), but only a seeded subset is now machine-linked in [CLAIMS_RUNTIME_REGISTRY.json](/home/eirikr/Github/openperception/specs/CLAIMS_RUNTIME_REGISTRY.json); most claims remain outside runtime coverage.
2. Axis conflict handling is no longer purely prose: a first machine-readable profile manifest and composition helper now exist, but seam-resolution is still not wired into validators or renderer/runtime consumers.
3. Scaling, quantization, display adaptation, and DPI transition policy now have a first shared runtime helper, but they still lack display detection, transition handling, and downstream consumer integration.
4. Reflow and layout rules are specified, but runtime still only has an early rendered slice; exact focus clipping, deeper overlap measurement, and 2D exception handling are still outside enforcement even after viewport, main-layout, narrow-viewport column-fit, swatch-grid, wrapping-row, first Chromium-backed overflow checks, and first focus-visibility checks.
5. Typography contracts and font tokens are no longer purely aspirational: a first verifier now exists, but rendering-based disambiguation, broader output coverage, and shared integration still remain missing.
6. Temporal safety and display-mode motion rules are specified, but only first seizure and temporal policy validator subsets exist; motion and richer temporal analysis remain unimplemented.
7. Cognitive load and navigation are no longer spec-only, but runtime enforcement is still limited to static HTML and early renderer-backed checks rather than full task-flow or deeper viewport-state analysis, even though visible-control burden and declared panel and metric-group burden are now tracked.
8. The validator framework declared a unified CLI, but until this pass there was no single entrypoint exposing what is implemented versus still partial.

## Executed In This Pass

The gap list is now partially built out and executed in repo code:

- Added [validator_registry.py](/home/eirikr/Github/openperception/tools/validator_registry.py) to declare implemented gates, spec-only gates, and broader runtime areas in one place.
- Added [validate.py](/home/eirikr/Github/openperception/tools/validate.py) as the unified validator CLI for the implemented gate subset.
- Added [runtime_gap_report.py](/home/eirikr/Github/openperception/tools/runtime_gap_report.py) to emit a runnable declared-vs-runtime gap report.
- Added tests in [test_validate.py](/home/eirikr/Github/openperception/tools/tests/test_validate.py) so the new control point is verified.
- Added [CLAIMS_RUNTIME_REGISTRY.json](/home/eirikr/Github/openperception/specs/CLAIMS_RUNTIME_REGISTRY.json) as the first machine-readable claims-to-validator/artifact registry.
- Added [claims_registry.py](/home/eirikr/Github/openperception/tools/claims_registry.py), [claims_coverage_report.py](/home/eirikr/Github/openperception/tools/claims_coverage_report.py), and [check_claims_registry.py](/home/eirikr/Github/openperception/tools/check_claims_registry.py) so evidence coverage is queryable and integrity-checked in runtime tooling.
- Added [axis-profiles.json](/home/eirikr/Github/openperception/specs/tokens/profiles/axis-profiles.json) and [profile_resolver.py](/home/eirikr/Github/openperception/tools/profile_resolver.py) so axis/display profiles can now be composed and cross-axis conflicts surfaced in runtime tooling.
- Added [scaling.py](/home/eirikr/Github/openperception/tools/scaling.py) as the first shared scaling and quantization runtime helper, including effective-scale math, snap-class quantization, hysteresis, and touch-target floor enforcement.
- Added [semantic-role-tokens.json](/home/eirikr/Github/openperception/tokens/semantic-role-tokens.json) and [semantic_tokens.py](/home/eirikr/Github/openperception/tools/semantic_tokens.py) so chromatic validation can consume first-class runtime semantic role data rather than relying only on derived mappings.
- Added [temporal_depth.py](/home/eirikr/Github/openperception/tools/validators/temporal_depth.py) as the first partial runtime for `GATE-005`, validating motion-token safety and display-profile compatibility.
- Added [cognitive.py](/home/eirikr/Github/openperception/tools/validators/cognitive.py) as the first partial runtime for `GATE-006`, validating navigation size, nesting, summary views, notification density, density-region budgets, primary action density, visible-control burden, declared panel and metric-group burden, HUD complexity, and approximate reading level on repo-owned HTML.
- Added [rendered_cognitive_check.py](/home/eirikr/Github/openperception/tools/rendered_cognitive_check.py) as the first browser-backed `GATE-006` expansion, using Playwright and a local HTTP server to measure first-screen visible controls, regions, clusters, and notifications at fixed viewport sizes.
- Expanded [cvd.py](/home/eirikr/Github/openperception/tools/validators/cvd.py) and [semantic-role-tokens.json](/home/eirikr/Github/openperception/tokens/semantic-role-tokens.json) so runtime chromatic validation now covers warning-vs-info and progress-vs-disabled in addition to the earlier semantic pairs.
- Expanded [CLAIMS_RUNTIME_REGISTRY.json](/home/eirikr/Github/openperception/specs/CLAIMS_RUNTIME_REGISTRY.json) so `GATE-003`, `GATE-004`, `GATE-005`, and `GATE-006` now have evidence-linked runtime claims instead of relying mostly on prose.
- Added [test_claims_coverage_report.py](/home/eirikr/Github/openperception/tools/tests/test_claims_coverage_report.py) so the seeded claims registry is verified.
- Added [seizure.py](/home/eirikr/Github/openperception/tools/validators/seizure.py) as a first executable subset of `GATE-001`, with frame-sequence manifest input and checks for flash frequency, red flash, flash area, and cumulative exposure.
- Added [test_seizure.py](/home/eirikr/Github/openperception/tools/tests/test_seizure.py) to verify pass/fail behavior for the first seizure-gate subset.
- Added [spatial.py](/home/eirikr/Github/openperception/tools/validators/spatial.py) as a first executable subset of `GATE-004`, now including token minima, focus affordances, HTML hygiene, explicit button target minima checks, and first static reflow heuristics like viewport/meta checks, main-layout responsiveness, narrow-viewport column fit, media-query or adaptive-grid markers, swatch-grid adaptation, and wrapping control rows.
- Added [rendered_spatial_check.py](/home/eirikr/Github/openperception/tools/rendered_spatial_check.py) as the first browser-backed `GATE-004` expansion, using Playwright and a local HTTP server to measure real page, main-container, known-row overflow, and first focus-visibility risk at fixed viewport sizes.
- Expanded the example HTML surfaces in [variant-toggle.html](/home/eirikr/Github/openperception/examples/ui/variant-toggle.html) and [palette-compare.html](/home/eirikr/Github/openperception/examples/ui/palette-compare.html) so they now expose density-region, primary-action, and declared panel/metric-group markers that the cognitive and spatial gates can inspect honestly.
- Added [typography.py](/home/eirikr/Github/openperception/tools/validators/typography.py) as a first executable typography verifier over font contracts, example body-text rules, and non-color link distinction.
- Expanded [cvd.py](/home/eirikr/Github/openperception/tools/validators/cvd.py) beyond `primary-vs-accent` so it now checks derived semantic-role pairs like danger-vs-ally and interactable-vs-disabled, plus first-pass redundancy backups from `viz` markers and dashes.
- Expanded [validate.py](/home/eirikr/Github/openperception/tools/validate.py) so the unified validator now reports auxiliary runtime surfaces for typography, profile resolution, and scaling.
- Fixed a real example-surface bug in [variant-toggle.html](/home/eirikr/Github/openperception/examples/ui/variant-toggle.html) where a duplicate `class` attribute broke the intended focus-ring wiring on a focusable card.

This closes one meaningful infrastructural gap: the repo can now execute a
runtime slice of every declared validator family from a single entrypoint
instead of leaving one entire gate family stranded in prose.

## Priority Gap List

P0:
- Keep `GATE-002` and `GATE-003` accessible via the unified CLI and use that as the single runtime validator entrypoint.
- Expand the seeded claims-to-validator/artifact registry beyond the current initial subset so the evidence system becomes broadly actionable.

P1:
- Expand `GATE-001` from frame sequences into pattern-oscillation and direct video analysis.
- Expand `GATE-004` from static token/CSS/example checks into rendered reflow and overlap audits.
- Expand the new typography verifier into rendering-based disambiguation and broader output coverage.
- Integrate the new profile resolver with validator and renderer/runtime surfaces.
- Integrate the new scaling helper with validators, profile composition, and downstream renderers.
- Expand semantic-role chromatic validation from the current runtime role subset into broader first-class semantic token coverage.
- Expand the new temporal/depth gate from token/profile policy into rendered motion-path and depth-cue analysis.
- Expand the new cognitive gate from static HTML/profile checks into task-flow, density, and renderer-aware HUD analysis.

P2:
- Build a reusable scaling and quantization runtime library from the scaling specs.
- Add profile composition for display adaptation and motion modes.

## Commands

```bash
python tools/validate.py
python tools/validate.py --json
python tools/validate.py --seizure-manifest path/to/manifest.json
python tools/runtime_gap_report.py
python tools/runtime_gap_report.py --format markdown
python tools/claims_coverage_report.py
python tools/check_claims_registry.py
python tools/validators/cognitive.py
python tools/validators/typography.py
python tools/profile_resolver.py --profiles standard,reduced-motion
python tools/scaling.py --lp 44 --dpi 144 --scale 1.25 --snap-class touch-target
python tools/validators/temporal_depth.py
```
