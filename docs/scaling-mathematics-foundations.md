# Scaling Mathematics From Foundations

Date: 2026-03-22

## What `SCALING_MATHEMATICS.md` really is

`specs/SCALING_MATHEMATICS.md` is the repo's unit-system spec.

Its job is to make scaling predictable across:

- device density,
- user zoom and scaling,
- typography,
- layout,
- and quantization boundaries.

So this is not merely a sizing guide. It is the mathematical substrate for much
of the repo's future spatial and rendering consistency.

## Step 1. Identify the key move

The key move is to define a canonical logical unit:

- logical pixels anchored to a 96-DPI reference,
- transformed by an effective scale equation,
- then quantized according to context.

This is the kind of move that turns "responsive design" into a real system
rather than a collection of ad hoc breakpoints.

## Step 2. Why this matters

Many accessibility guarantees depend on sizing:

- touch targets,
- text size,
- line length,
- spacing,
- reflow behavior.

Without a clear unit system, those guarantees become inconsistent across
devices and platforms.

This spec tries to solve that at the root.

## Step 3. What it gets right

The document is especially strong where it:

- defines a simple effective-scale formula,
- ties logical units to practical examples,
- distinguishes quantization contexts,
- explains why whole-pixel and fractional rounding rules differ by artifact
  type.

That combination of abstraction and implementation-minded detail is very good.

## Step 4. Relationship to other specs

This spec is infrastructural for several other documents:

- `DISPLAY_ADAPTATION_LAYER.md` uses its scaling logic directly,
- `TYPOGRAPHY_SYSTEM.md` depends on it for font-size behavior,
- `LAYOUT_SYSTEM.md` depends on it for spacing and reflow consistency.

So while it may look narrower than UVAS, it is actually one of the core
mechanical documents under the whole stack.

## Step 5. What remains unimplemented

As with several neighboring specs, the math is clearer than the current
runtime.

The repo does not yet have a full shared implementation of:

- logical-pixel conversion,
- context-aware quantization,
- scale-aware layout validation,
- broad cross-platform rendering enforcement.

That means the spec currently acts as a design reference more than a consumed
library contract.

## Bottom line

`specs/SCALING_MATHEMATICS.md` is the repo's unit-system spec. It is one of the
most important hidden-foundation documents because many future layout,
typography, and display-adaptation guarantees depend on it, even though the
corresponding runtime machinery is still mostly absent.
