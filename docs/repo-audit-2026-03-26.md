# Repo Audit - 2026-03-26

This document records the current tranche's audit hypotheses, local checks, and
selected source-backed outcomes.

## Honest Assessment

OpenPerception is not one thing. It is currently a hybrid of:

- upstream CVD algorithm packages
- repo-owned validator and research-governance tooling
- broad accessibility specifications
- curated research and provenance infrastructure
- experimental and applied visualization lanes

The strongest parts are:

- paper and source-asset provenance discipline
- validator scaffolding and runtime reporting
- applied documentation around color support and depth accommodation

The weakest parts are:

- strategic docs drifting away from current runtime state
- uneven installation documentation across module boundaries
- some high-level claims that were more precise than the repo could currently
  prove
- a Blender showcase lane that still depends on host-specific bootstrap

## Hypotheses

### HYP-001 The top-level `Python 3.8+` claim is accurate for repo-owned root tooling

- status: refuted
- local evidence: repo-owned tooling under `tools/` uses syntax such as
  `Path | None`
- source evidence: PEP 604 union syntax shipped in Python 3.10, so that syntax
  is not valid on Python 3.8 or 3.9
- action: root docs now say Python 3.10+ for repo-owned tooling and note the
  currently audited interpreter

### HYP-002 The contrast gate is aligned with WCAG contrast-minimum guidance

- status: supported
- local evidence: `tools/validate.py` enforces 4.5:1 for normal text pairs
- source evidence: WCAG 2.1 Understanding SC 1.4.3 uses 4.5:1 as the minimum
  contrast ratio for normal text
- action: keep the gate, but continue auditing surrounding prose for overclaim

### HYP-003 The depth-accommodation stereoblindness prevalence claim has a valid primary source

- status: supported
- local evidence: the repo's stereoblindness source cache already records the
  Chopin et al. synthesis as the prevalence anchor
- source evidence: Chopin, Bavelier, and Levi 2019 remains the primary source
  used for the roughly 7 percent prevalence figure in adults under 60
- action: keep the claim source-backed and continue separating source-backed
  statements from synthesis statements

### HYP-004 The validator framework is only aspirational and not meaningfully implemented

- status: refuted in the strong form
- local evidence: `python3 tools/validate.py` currently executes gates for
  contrast, CVD, spatial, temporal-depth, and cognitive checks, plus auxiliary
  runtime surfaces
- nuance: the validator framework is still incomplete because it returns live
  warnings and some broader ambitions remain spec-only
- action: strategic docs should describe it as a partial implemented runtime,
  not as pure aspiration

### HYP-005 Strategic-doc counts and milestone language still match the current tree

- status: partially refuted
- local evidence: `MASTER_INDEX.md` had stale markdown counts and `ROADMAP.md`
  still described already-implemented validators as deferred or in-progress
- action: rewrite strategic docs to use measured counts, narrower completion
  language, and more honest milestone framing

### HYP-006 The documented dev-environment bootstrap is reproducible on a fresh host profile

- status: supported after remediation
- local evidence: the repo can now bootstrap a fresh virtual environment,
  install the editable theme and DaltonLens package, and build the example
  Sphinx docs using repo-owned commands
- nuance: rendered browser audits still require an explicit Playwright browser
  install step for local development even though CI can provision them
- action: keep rendered audits opt-in locally, but require them in CI on a
  dedicated Ubuntu runner

## Current Runtime Findings

Executed on this audit pass:

- `python3 tools/validate.py`
- `python3 tools/check_claims_registry.py`
- `python3 -m pytest tools/tests/test_validate.py tools/tests/test_check_claims_registry.py -q`

Observed current runtime result after remediation:

- `python3 tools/validate.py --strict-warnings` now passes
- the remaining practical setup gap is environment bootstrap for the full
  `DaltonLens-Python` test lane
- strategic docs now use narrower completion language, and repo counts now come
  from generated stats instead of hand-written totals
- rendered browser audits remain optional locally but are now suitable for a
  dedicated CI runner that provisions Chromium explicitly

That means the repo's current debt is no longer in the implemented validator
surface itself. It is now mostly in environment reproducibility, broader
claim-audit coverage, and strategic-doc reconciliation.

## Conclusion

The repo is strongest when it behaves like a disciplined research-and-validation
system. It gets weaker when roadmap or README language outruns what can be
defended by runtime checks, packaging metadata, or primary sources. This audit
pass corrects some of that drift, but it does not claim the reconciliation work
is complete.
