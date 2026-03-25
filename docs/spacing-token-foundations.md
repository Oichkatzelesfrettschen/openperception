# Spacing Token From Foundations

Date: 2026-03-22

## What `spacing.json` really is

`specs/tokens/layout/spacing.json` is the repo's spatial token payload.

It turns the larger layout and scaling specs into concrete token families for:

- spacing,
- radii,
- strokes,
- grid behavior,
- focus outlines,
- breakpoints,
- density modes.

So this file is the layout-system contract in tokenized form.

## Step 1. What it does well

The file is strongest where it combines:

- primitive scales,
- semantic aliases,
- responsive grid values,
- accessibility-critical interactive minima.

That makes it more than a spacing table. It is a compact spatial design system.

## Step 2. Why it matters

This token file shows how the repo wants to make layout accessibility
implementable:

- touch-target minimums become tokens,
- focus geometry becomes tokens,
- density modes become structured values rather than ad hoc CSS choices.

That is exactly the kind of machine-readable contract a real system needs.

## Step 3. Relationship to the larger specs

This file operationalizes ideas from:

- `LAYOUT_SYSTEM.md`
- `SCALING_MATHEMATICS.md`
- and parts of the broader UVAS structure thinking

It is one of the clearer examples of the repo moving from prose spec to token
payload.

## Bottom line

`specs/tokens/layout/spacing.json` is the repo's spatial token payload. It is a
useful bridge between abstract layout accessibility rules and something a
renderer could actually consume.
