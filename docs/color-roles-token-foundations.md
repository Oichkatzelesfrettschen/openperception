# Color Roles Token From Foundations

Date: 2026-03-22

## What `color-roles.json` really is

`specs/tokens/semantic/color-roles.json` is the repo's semantic-color contract
in machine-readable form.

It is trying to describe color not as a palette ramp, but as a mapping between:

- meanings,
- color candidates,
- redundancy channels,
- and validation expectations.

So this file is not equivalent to `tokens/color-tokens.json`. It is a semantic
policy layer above any specific production palette.

## Step 1. Identify the conceptual move

The key move is to bind each semantic role to more than color:

- pattern,
- icon,
- shape,
- animation,
- sound cue,
- contrast expectations.

That is fully aligned with the repo's recurring principle that color must not
carry meaning alone.

## Step 2. What it gets right

This token spec is strongest where it encodes:

- redundancy directly in the role definition,
- CVD validation thresholds as role relationships,
- role semantics instead of raw brand families.

That makes it much more interesting than a normal design-token file.

## Step 3. Where it diverges from the current repo lane

This file should be read carefully because it is more aspirational than current
production truth.

Examples:

- it uses `protan-safe`, `deutan-safe`, and `tritan-safe` naming rather than
  the repo's current authored variant lanes,
- it encodes a red/green danger-vs-ally worldview that is semantically rich but
  also exactly the kind of pairing the repo treats cautiously under CVD,
- it is not the live source of truth for the production CSS token outputs.

So this is best understood as a future semantic contract, not a currently wired
runtime file.

## Bottom line

`specs/tokens/semantic/color-roles.json` is the repo's machine-readable
semantic-color contract. It is conceptually strong because it treats meaning as
multi-channel, but it remains more like future architecture than live token
infrastructure today.
