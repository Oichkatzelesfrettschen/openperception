# Scaling Authority Matrix From Foundations

Date: 2026-03-22

## What `SCALING_AUTHORITY_MATRIX.md` really is

`specs/SCALING_AUTHORITY_MATRIX.md` is the repo's anti-double-scaling spec.

Its central question is:

- who is allowed to own scale on each platform or toolkit?

That may sound narrow, but it is critical. Without a single authority, all the
repo's careful scaling math can be destroyed by duplicated scaling at different
layers.

## Step 1. Identify the core design rule

The document's core rule is simple and strong:

- only one layer should own scaling,
- all other layers should operate inside that authority's coordinate system.

This is one of the healthiest architectural ideas in the entire scaling stack.

## Step 2. Why it matters

Double-scaling is a subtle but destructive class of failure:

- UIs become too large or blurry,
- assets are loaded at wrong resolutions,
- platform APIs are misunderstood,
- environmental overrides stack unpredictably.

This spec exists to prevent that class of error systematically.

## Step 3. What it gets right

The matrix is particularly useful because it is not generic. It names real
platforms and toolkits and states:

- where authority should live,
- which APIs expose scale,
- what coordinate system each stack expects.

That practical specificity makes it far more useful than an abstract note about
"device independence."

## Step 4. Relationship to the rest of the scaling cluster

This document is the ownership layer within the larger system:

- `SCALING_MATHEMATICS.md` says how scaling should work,
- authority matrix says who gets to apply it,
- `DPI_TRANSITION_CONTRACT.md` says what happens when it changes,
- `QUANTIZATION_POLICY.md` says how to keep motion and rounding stable.

That makes this spec surprisingly central.

## Step 5. What remains unresolved

Even though the matrix is detailed, the repo does not yet have a common runtime
adapter that encodes these rules into actual toolkit integrations.

So today it mainly serves as:

- design guidance,
- implementation guardrail,
- documentation against future scaling mistakes.

## Bottom line

`specs/SCALING_AUTHORITY_MATRIX.md` is the repo's ownership map for scaling. It
is a high-value preventative spec because it names one of the easiest ways for
cross-platform accessibility work to fail before users even see the product.
