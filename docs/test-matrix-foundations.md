# Test Matrix From Foundations

Date: 2026-03-22

## What `TEST_MATRIX.md` really is

`specs/TEST_MATRIX.md` is the repo's validation-environment contract.

It answers a question that many specs avoid:

- across what real hardware and platform conditions would these accessibility
  claims actually need to hold?

That makes it one of the most reality-facing documents in the spec cluster.

## Step 1. Identify the core move

The strongest move in this document is boundary-based testing.

It emphasizes:

- edge DPI values,
- varied scaling factors,
- low and high refresh rates,
- emissive and reflective displays,
- platform-specific windowing models.

That is a much healthier testing mindset than validating only a comfortable
96-DPI, 60-Hz desktop middle.

## Step 2. Why this matters

OpenPerception makes cross-platform and cross-display claims. A project cannot
seriously make those claims if it tests only:

- one monitor density,
- one zoom level,
- one rendering stack.

This matrix is valuable because it turns that implicit obligation into explicit
test coverage intent.

## Step 3. What it gets right

The document is strongest where it treats:

- display physics,
- platform windowing behavior,
- and validator accuracy

as part of one test landscape.

That is important because accessibility failures can come from any of those
layers, not just from token values.

## Step 4. Relationship to implementation reality

Like many large specs here, the test matrix is ahead of the current repo.

The repo does not yet have automated coverage across the full matrix it
describes. So this document functions primarily as:

- a test strategy,
- a future validation plan,
- and a statement of what serious coverage would require.

## Step 5. Why it is still useful now

Even without full automation, this matrix is useful because it prevents false
confidence.

It makes clear how much environmental breadth would need to be exercised before
the repo could honestly claim robust display-wide guarantees.

## Bottom line

`specs/TEST_MATRIX.md` is the repo's validation-environment contract. It is a
strong reality check on the project's cross-platform ambitions, even though the
actual automated test coverage remains far smaller than the matrix it defines.
