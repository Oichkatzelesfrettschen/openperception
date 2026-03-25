# TeX PGFPlots Guide From Foundations

Date: 2026-03-22

## What `tex-pgfplots-guide.md` really is

`docs/tex-pgfplots-guide.md` is the scientific-figure delivery note.

Its purpose is not just to color LaTeX figures nicely. It exists to show how
the repo's accessibility rules survive in plots, charts, and papers where color
alone is notoriously brittle.

This makes it one of the most important downstream guides in the whole project.

## Step 1. Start from the real plotting problem

Plots fail accessibility very easily because they often rely on:

- hue-only legend distinctions,
- thin lines,
- tiny markers,
- poor grayscale behavior,
- and unlabeled series.

The TeX guide responds by treating a figure not as "colored decoration" but as
a semantic encoding problem.

## Step 2. What the style package actually does

The guide is backed by `tex/brandpalette.sty`, which defines:

- named brand and variant colors,
- plot cycle lists,
- marker and dash patterns,
- hatch styles for bars and filled regions,
- a `mono` mode,
- and axis/grid styling.

So the guide is grounded in a reusable package, not just a prose recommendation.

## Step 3. Why non-color encoding is central here

This guide is one of the clearest expressions of the repo's core doctrine:

- color must not carry meaning alone.

In plot terms that becomes:

- markers,
- dashes,
- line widths,
- hatch fills,
- direct labels,
- grayscale survivability.

That is exactly the right move for charts, where semantic collapse under CVD or
printing is otherwise very common.

## Step 4. How variants work in this lane

The guide mirrors the broader token system with:

- `default`
- `protan`
- `deutan`
- `tritan`
- `mono`

That is useful because it keeps the figure lane conceptually aligned with the
CSS and GTK lanes, even though the actual implementation is native TeX.

This is a strong sign of architectural coherence across output formats.

## Step 5. What it reveals about the repo

The existence of this guide and package tells us something important:

OpenPerception is not only building interface themes. It is also trying to
control the accessibility properties of:

- academic figures,
- report charts,
- print-oriented technical artifacts.

That broadens the repo from a UI system into a visual communication system.

## Step 6. Relationship to current experimental palettes

Right now the TeX package still encodes the production indigo/magenta/gray lane
and its tuned variants.

So, just like GTK and Sphinx, the TeX lane has not yet been extended to the
experimental mauve/burgundy or red/mahogany packs.

That is implementation debt, not a conceptual limitation. The architecture is
already suitable for multiple theme families.

## Bottom line

`docs/tex-pgfplots-guide.md` is the repo's figure-accessibility note. It shows
how OpenPerception carries its core principles into scientific and technical
plots by combining controlled color variants with explicit non-color encodings
and grayscale-safe fallbacks.
