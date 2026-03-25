# Axis Overlap Map From Foundations

Date: 2026-03-22

## What `AXIS_OVERLAP_MAP.md` really is

`specs/AXIS_OVERLAP_MAP.md` is the repo's conflict cartography.

It exists because accessibility constraints do not live in isolation. A choice
that helps one group can pressure another constraint surface:

- higher contrast can aid low vision but increase glare discomfort,
- red can signal danger but becomes risky when flashing,
- motion can clarify urgency but overload attention.

This document maps those seams explicitly.

## Step 1. Identify the core conceptual move

The key move here is to shift from:

- isolated accessibility rules

to:

- interacting axes with conflicts and synergies.

That is a mature step. It treats accessibility as a systems problem rather than
as a list of disconnected checkboxes.

## Step 2. Why it matters

Most accessibility documentation stops at domain-specific guidance. This map
goes further by asking:

- where do those domains collide,
- where should a single integration point solve multiple problems,
- where are dials needed instead of single fixed values?

That is exactly the kind of reasoning a unified accessibility framework needs.

## Step 3. What the document does especially well

The strongest part of the overlap map is its seam thinking.

It does not only say "these axes intersect." It asks:

- where should the fix happen once,
- what should never be allowed in raw content,
- which gates belong at which integration point.

That makes it architecturally useful, not just conceptually interesting.

## Step 4. Why it pairs well with UVAS

UVAS defines the broad axes and invariants. The overlap map explains where
those abstractions become messy in practice.

That makes the two documents complementary:

- UVAS gives the categories,
- overlap map gives the conflict geometry.

Without this second document, UVAS would risk sounding cleaner than reality.

## Step 5. What is still aspirational here

Like other major specs, this map is ahead of implementation.

Its gates and seam-resolution logic imply a much broader runtime than the
current repo actually has. Right now we do not have:

- full temporal validators,
- full cognitive gates,
- full spatial and depth enforcement,
- full profile composition machinery.

So this document is best read as architecture guidance and integration intent.

## Step 6. Why it matters for current palette work

This map also helps explain why the recent palette and red-theme work landed the
way it did.

Examples:

- chromatic and luminance must cooperate,
- color meaning needs non-color backup,
- red cannot be treated only as a branding question because it intersects with
  temporal seizure safety and warning semantics.

So the overlap map is not separate from palette work; it quietly governs it.

## Bottom line

`specs/AXIS_OVERLAP_MAP.md` is the repo's conflict cartography. It is one of
the clearest signs that OpenPerception wants to solve accessibility as an
interacting system, even though most of the runtime enforcement implied by that
map remains future work.
