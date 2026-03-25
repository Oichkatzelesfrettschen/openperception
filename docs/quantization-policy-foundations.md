# Quantization Policy From Foundations

Date: 2026-03-22

## What `QUANTIZATION_POLICY.md` really is

`specs/QUANTIZATION_POLICY.md` is the repo's anti-jitter spec.

It focuses on a subtle but very real problem:

- continuous values become unstable when repeatedly rounded near boundaries,
- and that instability becomes visible as jitter, blur, or rhythm collapse.

So this document is a rendering-stability policy, not just a math appendix.

## Step 1. Identify the key insight

The key insight is that rounding is not stateless if we care about perception.

A naive `round()` can be mathematically fine and visually wrong. The spec
responds by introducing:

- hysteresis,
- snap classes,
- context-specific quantization rules,
- transition-aware behavior.

That is a very strong engineering move.

## Step 2. Why this matters

If OpenPerception wants scaling, motion, and layout to feel stable across:

- fractional DPI,
- animation,
- responsive changes,
- and runtime transitions,

then it cannot rely on generic rounding everywhere.

This spec recognizes that rendering stability is itself an accessibility issue.

## Step 3. What it gets right

The document is particularly strong where it:

- separates snap classes by artifact type,
- treats touch-target quantization as safety-critical,
- scales precision with DPI,
- and carries state per key rather than globally.

That combination shows serious thought about how UI geometry actually behaves.

## Step 4. Relationship to neighboring specs

This spec plays a supporting but essential role in the scaling cluster:

- scaling mathematics defines the ideal value,
- quantization policy defines how that ideal becomes a stable raster value,
- DPI transition contract defines how those values behave during scale changes.

Without this policy, the larger scaling architecture would still feel shaky in
practice.

## Step 5. What is still missing

The repo does not yet have a shared implementation that applies these snap-class
rules across its actual render targets.

So the spec currently acts as:

- design guidance,
- future library behavior,
- and a reference for how to avoid common fractional-scaling bugs.

## Bottom line

`specs/QUANTIZATION_POLICY.md` is the repo's anti-jitter spec. It is one of the
most technically grounded documents in the scaling cluster because it focuses on
the point where mathematically correct values can still become perceptually bad
output.
