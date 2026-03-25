# UVAS From Foundations

Date: 2026-03-22

## What `UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md` really is

`specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md` is the normative theory document
for the repo.

It is trying to define the governing law of OpenPerception in one place:

- what the end state is,
- what counts as measurable accessibility,
- how human limits map to UI constraints,
- what must be invariant,
- what can be user-tunable.

So this document is not implementation code and not a simple design guide. It
is the repo's constitutional layer.

## Step 1. Identify the key move

The most important move in UVAS is right at the beginning:

- reject vague "acceptable to everyone" language,
- replace it with measurable pillars.

Those pillars are:

1. safety,
2. perceptibility,
3. discriminability,
4. comprehensibility,
5. controllability.

That shift is foundational because it turns accessibility from taste or
aspiration into explicit constraints.

## Step 2. Understand its ontology

UVAS is doing three mappings at once:

1. human functional limits,
2. UI meaning primitives,
3. rendering degrees of freedom.

That is the document's deepest idea.

It says accessibility is not just "use better colors." It is a relation between:

- what changes in the human channel,
- what the interface must communicate,
- what parameters the system can vary.

This is why the spec spans chromatic, luminance, spatial, temporal, depth, and
cognitive axes instead of only color.

## Step 3. Why invariants vs dials matters

The spec's second major structural idea is to split requirements into:

- invariants: non-negotiable floors,
- dials: user-tunable bounded controls.

This is a strong design move because it avoids two bad extremes:

- "everything must be fixed"
- "everything is user preference"

Instead:

- seizure safety is not optional,
- contrast floors are not optional,
- motion intensity, text scale, and color profile are tunable.

That is the right general model for an accessibility system.

## Step 4. What is implemented vs what is aspirational

The document itself is honest here:

- GATE-002 contrast exists,
- GATE-003 CVD exists,
- most invariants remain specification-only.

This is the biggest practical thing to understand about UVAS:

- it is ahead of the current codebase.

That is not a defect, but it does mean the spec must be read as partly
normative and partly roadmap.

## Step 5. Where the implementation diverges

There are important gaps between UVAS and current code.

Examples:

- UVAS speaks in terms of six full axes and many invariants.
- Current code only enforces a small subset.

- UVAS frames CVD discriminability in terms of simulated delta-E thresholds.
- Current `tools/validators/cvd.py` uses Oklab distance on authored token pairs,
  not a full simulated semantic-role matrix.

- UVAS imagines seizure, spatial, temporal/depth, and cognitive gates.
- Those are not implemented yet.

So UVAS is the repo's intended law, but not yet its complete runtime.

## Step 6. What to keep in mind when using it

Use UVAS for:

- deciding what classes of accessibility the repo is supposed to cover,
- understanding the repo's philosophical scope,
- judging whether a proposed feature belongs here,
- identifying validator gaps.

Do not use UVAS alone for:

- assuming a feature is already enforced,
- inferring exact token values,
- inferring that a stated gate is already in CI.

## Step 7. Relationship to the newer palette work

The new experimental palette work fits UVAS well because it follows the same
logic:

- measurable contrast,
- discriminability concerns,
- non-color redundancy,
- explicit variant handling.

But UVAS is broader than palette work. It also claims temporal, spatial, depth,
and cognitive territory that the current experimental palette artifacts do not
touch.

## Bottom line

UVAS is the repo's constitutional document: broad, principled, and partially
ahead of implementation. It tells us what OpenPerception wants to become, and
therefore where current implementation debt still exists.
