# Contrast Guide From Foundations

Date: 2026-03-22

## What `contrast-guide.md` really is

`docs/contrast-guide.md` is the repo's shortest path from accessibility law to
an enforceable numeric floor.

It sits below:

- `specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md`
- `specs/VALIDATORS_FRAMEWORK.md`

and directly above:

- `tools/contrast_check.py`
- `tools/validators/contrast.py`

So this guide is not primarily theory. It is the operational note that turns
"make text readable" into a concrete threshold and a repeatable command.

## Step 1. Identify the fundamental reduction

The key reduction in the contrast guide is:

- start with complex human visual variation,
- reduce that to luminance contrast floors,
- expose those floors as a simple pass/fail gate.

That move is narrow, but it is powerful.

Contrast is not the whole accessibility problem, yet it is one of the few
parts that can be measured robustly and automated cleanly.

## Step 2. Why the formula matters

The guide includes the WCAG luminance-ratio formula because the repo's
contrast machinery is based on that exact abstraction:

- convert sRGB to linear light,
- compute relative luminance,
- compare lighter and darker values,
- classify against AA and related thresholds.

That is why the guide is useful even though it is short. It points directly to
the arithmetic that the validator actually enforces.

## Step 3. What it is really validating

The guide can look like it is "checking colors," but what it actually checks
is more specific:

- foreground/background readability,
- token-pair safety floors,
- whether authored semantic roles are usable as text or UI surfaces.

That makes it a foundational gate for:

- body text,
- labels,
- controls,
- chart annotations,
- status elements with text overlays.

## Step 4. What it does well

The strongest thing about this guide is its restraint.

It does not pretend contrast solves:

- hue confusion,
- chart category discrimination,
- monochrome semantics,
- motion or temporal issues.

Instead it says: here is one strict thing we can test every time.

That makes it a dependable enforcement note rather than a vague accessibility
essay.

## Step 5. What it leaves out by design

The guide is intentionally incomplete.

It does not cover:

- Oklab or Oklch separation,
- simulated CVD pair collapse,
- non-color redundancy,
- shape, label, or pattern obligations.

Those are handled elsewhere in the repo.

So the correct reading is:

- contrast is necessary,
- contrast is not sufficient.

That distinction is especially important for the newer red-theme and
experimental palette work, where many pairings can pass WCAG while still being
semantically brittle under CVD simulation.

## Step 6. How it fits the current implementation

This guide is one of the best aligned docs in the repo because it matches real
tooling closely.

Its claims map directly onto:

- `tools/contrast_check.py`
- `tools/validators/contrast.py`
- the `make contrast-check` workflow

So unlike some higher-level specs, this document is already mostly runtime law
and not just aspiration.

## Step 7. Relationship to the other guides

The contrast guide is the simplest member of a three-part stack:

- `contrast-guide.md` answers "can this pair be read at all?"
- `oklch-guide.md` answers "can we reason about palette structure
  perceptually?"
- `daltonization-guide.md` answers "how do images change when we need to help
  CVD viewers directly?"

That makes the contrast guide the floor, not the full house.

## Bottom line

`docs/contrast-guide.md` is the repo's numeric readability floor: narrow,
practical, and closely aligned with the tooling that already exists. It should
be treated as the minimum gate, never as the whole accessibility story.
