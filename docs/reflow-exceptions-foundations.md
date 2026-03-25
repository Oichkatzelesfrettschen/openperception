# Reflow Exceptions From Foundations

Date: 2026-03-22

## What `REFLOW_EXCEPTIONS_2D.md` really is

`specs/REFLOW_EXCEPTIONS_2D.md` is the repo's exception-discipline spec for
two-dimensional content.

Its purpose is not to weaken reflow requirements. It is to say precisely when
single-axis reflow cannot preserve meaning and what obligations still remain in
those cases.

That is a very important distinction.

## Step 1. Identify the conceptual move

The document's key move is:

- accept that some content is inherently two-dimensional,
- but tightly constrain the scope of that exemption.

This prevents a common failure mode where teams declare large regions
"special-case" and quietly drop accessibility obligations altogether.

## Step 2. What it gets right

The spec is strongest where it insists:

- only the exempt content region is exempt,
- surrounding chrome and controls must still reflow,
- the content still needs zoom, pan, reset, and alternative access paths.

That is exactly the right kind of exception handling.

## Step 3. Why this matters in OpenPerception

This repo touches several content types that can plausibly need 2D treatment:

- games,
- diagrams,
- tables,
- visualizations,
- possibly simulation or charting surfaces.

Without an exception policy, the layout system could become either:

- unrealistically rigid,
- or too permissive to be meaningful.

This spec keeps the middle ground.

## Step 4. Relationship to layout and scaling

This document is a boundary spec within the spatial stack:

- `LAYOUT_SYSTEM.md` defines normal reflow expectations,
- reflow exceptions define where those expectations narrow,
- `SCALING_MATHEMATICS.md` and related specs still govern the chrome around the
  exempt region.

So this is not a separate system. It is a scoped carveout inside the larger
layout contract.

## Step 5. What remains future work

There is currently no general repo validator that can automatically determine:

- which regions qualify for 2D exemption,
- whether required affordances exist,
- whether surrounding controls still reflow correctly.

So the spec is currently a strong review and design guideline rather than an
enforced rule.

## Bottom line

`specs/REFLOW_EXCEPTIONS_2D.md` is the repo's exception-discipline spec for
two-dimensional content. It is valuable because it prevents the reflow contract
from becoming either naive or meaningless, even though enforcement is still
manual and aspirational.
