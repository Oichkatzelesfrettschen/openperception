# Display Adaptation Layer From Foundations

Date: 2026-03-22

## What `DISPLAY_ADAPTATION_LAYER.md` really is

`specs/DISPLAY_ADAPTATION_LAYER.md` is the repo's display-physics abstraction
spec.

Its purpose is ambitious:

- preserve semantic accessibility guarantees,
- while adapting output to real display constraints like DPI, refresh rate,
  panel technology, and motion limitations.

So this document is not about tokens alone. It is about how semantics survive
contact with hardware reality.

## Step 1. Identify the core discipline

The strongest move in this spec is its separation of three temporal phenomena:

- display refresh capability,
- content flicker,
- hardware flicker.

That separation is excellent because these concepts are often confused in
accessibility discussions.

The spec insists that:

- content safety is time-based,
- hardware artifacts are partly outside app control,
- the system should adapt what it can without pretending to be a monitor driver.

## Step 2. Why this matters

If OpenPerception wants to be more than a static token library, it needs some
way to reason about:

- e-ink versus OLED,
- low DPI versus retina,
- reduced-motion preferences,
- VRR and frame-timing instability.

The DAL spec is the repo's answer to that need.

## Step 3. What it does well

The spec is strongest where it defines:

- clear runtime inputs,
- user overrides,
- output caps,
- and a scaling pipeline.

That structure makes it feel like a real systems design, not just a set of
accessibility wishes.

In particular, the distinction between:

- queried display traits,
- user overrides,
- derived render caps

is a strong architectural pattern.

## Step 4. Relationship to scaling math

This spec depends heavily on the repo's broader scaling model.

Its `S_eff` and logical-pixel pipeline tie directly into
`specs/SCALING_MATHEMATICS.md`, which is effectively its mathematical
substructure.

That relationship matters because DAL is not only policy. It is policy plus a
unit system.

## Step 5. What remains speculative

This file is explicitly spec-only, and it should be read that way.

There is no current implementation path in the repo that fully realizes:

- runtime display detection,
- render-cap negotiation,
- mode switching across panel types,
- adaptation-aware validator flows.

So the DAL is a very useful design target, but not present runtime law.

## Step 6. Why it is still important now

Even without implementation, this spec sharpens the repo in two ways:

- it prevents confusion about what "accessible on different displays" would
  actually require,
- it keeps future work grounded in explicit transforms rather than vague
  platform exceptions.

That is valuable design debt reduction by itself.

## Bottom line

`specs/DISPLAY_ADAPTATION_LAYER.md` is the repo's display-physics abstraction
spec. It is one of the clearest systems-design documents in the project, but it
remains fully aspirational and should be read as a future architecture target
rather than current implementation.
