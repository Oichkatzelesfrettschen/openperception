# DPI Transition Contract From Foundations

Date: 2026-03-22

## What `DPI_TRANSITION_CONTRACT.md` really is

`specs/DPI_TRANSITION_CONTRACT.md` is the repo's continuity spec for scale
changes.

It is concerned with a very practical and often messy problem:

- what happens when effective scale changes at runtime because the user zooms,
  drags a window between displays, docks a laptop, or changes a system scaling
  setting?

So this document is not about static layout correctness. It is about preserving
accessibility while the coordinate system itself is moving.

## Step 1. Identify the key move

The strongest move in this spec is that it treats DPI transitions as stateful
events, not as simple rerenders.

That means the contract is not only:

- recompute sizes,
- rerender at new scale.

It is also:

- preserve focus,
- preserve scroll position,
- preserve selection and interaction state,
- avoid clipping, overlap, blur, and visible disruption.

That is exactly the right framing.

## Step 2. Why this matters

A lot of scaling systems look correct when rendered from scratch but fail
during transitions.

This spec recognizes that accessible systems must remain usable while changing
scale, not only after change is complete.

That is especially important for:

- multi-monitor workflows,
- laptop docking,
- low-vision zoom use,
- and desktop environments with mixed DPI outputs.

## Step 3. What the document does well

The spec is strongest where it combines:

- platform-specific notifications,
- explicit failure modes,
- state-preservation requirements,
- example algorithms for scroll and focus restoration.

That gives it a concrete implementation feel even though it remains spec-only.

## Step 4. Relationship to the scaling stack

This document depends on the rest of the scaling cluster:

- `SCALING_MATHEMATICS.md` defines the unit logic,
- `QUANTIZATION_POLICY.md` helps avoid visual jitter,
- `SCALING_AUTHORITY_MATRIX.md` prevents double-scaling confusion,
- `LAYOUT_SYSTEM.md` defines what reflow success should mean.

So the transition contract is best understood as the runtime event policy above
those lower-level rules.

## Step 5. What remains aspirational

There is no current repo subsystem that comprehensively implements this across
toolkits.

The spec provides strong guidance, but not a shared runtime abstraction for:

- DPI change callbacks,
- focus-path restoration,
- proportional scroll preservation,
- cross-platform transition testing.

So this remains an architecture target rather than present behavior.

## Bottom line

`specs/DPI_TRANSITION_CONTRACT.md` is the repo's continuity spec for scale
changes. It is one of the clearest examples of OpenPerception treating
accessibility as a dynamic runtime problem rather than a static rendering
problem, even though the actual implementation layer is still absent.
