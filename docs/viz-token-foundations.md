# Viz Token From Foundations

Date: 2026-03-22

## What `viz-tokens.json` really is

`specs/tokens/viz/viz-tokens.json` is the repo's visualization contract in
token form.

It defines:

- chart palettes,
- non-color redundancy channels,
- typography floors,
- line and marker dimensions,
- legend and annotation limits,
- export expectations,
- and validation rules.

So this is one of the most complete downstream token specs in the repo.

## Step 1. What it gets especially right

The file is strongest where it treats charts as semantic encodings rather than
as decorative graphics.

Its core rule is excellent:

- every visual category must use at least two channels.

That is a direct continuation of the repo's broader non-color redundancy
principle.

## Step 2. Relationship to the rest of the repo

This file connects several otherwise separate ideas:

- color accessibility,
- chart readability,
- typography minimums,
- cognitive load,
- export discipline.

That makes it a particularly rich integration point.

## Step 3. Where it differs from the current production lane

Like some other token specs, the viz tokens describe a broader or alternate
palette universe than the current production token CSS files.

So this file should be read as a visualization contract and recommendation set,
not as a verbatim mirror of the shipping brand palette.

## Bottom line

`specs/tokens/viz/viz-tokens.json` is the repo's chart and data-graphics
contract. It is one of the clearest expressions of OpenPerception's idea that
accessible visualization requires both color discipline and explicit non-color
encoding.
