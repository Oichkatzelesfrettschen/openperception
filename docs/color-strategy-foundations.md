# Color Strategy From Foundations

Date: 2026-03-22

## What `COLOR-STRATEGY.md` really is

`COLOR-STRATEGY.md` is not the current OpenPerception production token spec.
It is a semantic recoloring strategy for a specific dark MATE theme lineage:

- dark-theme-first,
- desktop-theme-oriented,
- semantic hue remapping,
- explicitly tuned around a dark background.

So the correct way to read it is:

- not as the canonical token source of truth,
- but as a worked example of semantic recoloring under accessibility
  constraints.

## Step 1. Start from its stated premise

The document says Synthesis Dark is a semantic color system, not a simple color
replacement.

That means the basic object being preserved is not exact hue; it is role.

This gives four foundational rules:

1. preserve semantic family,
2. preserve or re-establish luminance hierarchy,
3. reduce red/green conflicts,
4. optimize against a specific dark surface.

## Step 2. Identify the transformation model

The document is built around a mapping function:

`original semantic family -> target semantic family`

Examples:

- blue -> indigo/violet
- green -> teal
- yellow -> warm yellow
- orange -> peach
- red -> soft red
- purple -> mauve

So the strategy is not "pick pretty colors." It is:

- classify the source hue family,
- assign a safer target family,
- then preserve role through controlled transformation.

## Step 3. Why luminance is central

The document's strongest technical idea is that distinction should come more
from brightness hierarchy than from hue difference alone.

That aligns well with the rest of this repo:

- `docs/contrast-guide.md`
- `tools/contrast_check.py`
- monochrome/CVD-safe reasoning in the design docs

In other words, `COLOR-STRATEGY.md` belongs to the same family of thought as
the production token system even if its palette is different.

## Step 4. What it optimizes for

The strategy is optimized for:

- desktop theming,
- dark surfaces,
- semantic recoloring of an existing icon/theme world,
- preserving intuitive meaning.

It is not primarily optimized for:

- web product branding,
- multi-theme token interchange,
- broad research taxonomy,
- the current indigo/magenta production palette.

## Step 5. How it relates to our newer work

There is a clean bridge from `COLOR-STRATEGY.md` to the new experimental work:

- both care about semantics over raw hue,
- both care about luminance ordering,
- both reject naive red/green dependence,
- both accept that color needs non-color backup cues.

But the newer pack work adds:

- explicit CVD variant lanes,
- repo-integrated validation scripts,
- a tertiary family for high-gravity emphasis,
- side-by-side comparison artifacts.

## Step 6. What to keep

The parts of `COLOR-STRATEGY.md` worth preserving as living principles are:

- semantic mapping over direct substitution,
- luminance-first role separation,
- explicit folder/icon recoloring logic,
- shape backup for colorblind safety.

## Step 7. What not to over-apply

The parts that should stay scoped to its original context are:

- the exact Catppuccin-like palette choices,
- hardcoded assumptions about `#232530`,
- MATE-specific folder recoloring rules as if they were universal,
- treating the document as the main repo token contract.

## Bottom line

`COLOR-STRATEGY.md` is best understood as a theme-specific semantic remapping
playbook, not the repo's universal color law. Its foundations are compatible
with the rest of OpenPerception, but its concrete palette is one branch, not
the trunk.
