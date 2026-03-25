# Colorblind-Friendly Design Guide From Foundations

Date: 2026-03-22

## What `colorblind-friendly-design-guide.md` really is

`docs/colorblind-friendly-design-guide.md` is the practical handbook layer.

It is downstream from:

- UVAS,
- the validators framework,
- the token system,
- the simulation and contrast tooling.

So this guide should be read as the operational translation layer:

- from principle to palette,
- from validator to component pattern,
- from research to everyday design work.

## Step 1. Identify its core simplification

The guide does something very important: it narrows the huge theoretical
surface into a manageable everyday design grammar.

Its grammar is:

- one primary family,
- one accent family,
- strong neutrals,
- explicit CVD variants,
- non-color redundancy.

That compression is necessary. Without it, the repo would be technically rich
but hard to use.

## Step 2. Why indigo/gray/magenta was chosen

The guide's base choice is not arbitrary branding. It encodes a design
judgment:

- indigo is more stable than many reds/greens under common CVD cases,
- magenta can stay distinct if separated by lightness and tuned per variant,
- gray provides reliable structure and text contrast.

This was the production baseline before the new experimental packs were added.

## Step 3. What it gets right

The strongest parts of the guide are:

- color is never the only cue,
- contrast targets are explicit,
- variant handling is concrete,
- component behavior is tied to interaction rules,
- charts are treated as a first-class accessibility problem.

This makes the guide much more than a palette sheet. It is a small practical
design system.

## Step 4. Where it is now slightly behind current work

The guide still assumes the production pair:

- indigo,
- magenta.

That was correct for the production token source, but the new experimental
findings show:

- the current strong indigo/magenta pair gets too close under protan,
- an indigo/mauve alternative improves separation materially,
- burgundy works well as a tertiary family.

So the guide is still useful, but it now represents the production baseline,
not the end of the discussion.

## Step 5. How to read it after the new experimental work

Use the guide for:

- the interaction rules,
- the redundancy rules,
- the charting rules,
- the implementation checklist,
- the variant-switching mechanics.

Treat the exact color family recommendation as:

- production default guidance,
- not a closed question.

That lets the document remain true without pretending the new experimental lane
does not exist.

## Step 6. Relationship to the red-theme work

The guide also helps explain why the red-theme triage landed where it did.

Because the guide prioritizes:

- stable primaries,
- lightness separation,
- non-color redundancy,

it naturally resists making "all red, all the time" the default product UI.

That does not invalidate a red theme. It just pushes it into:

- tertiary emphasis,
- atmosphere,
- separate theme pack,

rather than the baseline semantic stack.

## Bottom line

`colorblind-friendly-design-guide.md` is the practical day-to-day handbook for
the current production lane. The new experimental packs do not replace its core
principles; they challenge only part of its concrete palette recommendation.
