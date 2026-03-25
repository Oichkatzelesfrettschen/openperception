# Logical Pixels Token From Foundations

Date: 2026-03-22

## What `logical-pixels.json` really is

`specs/tokens/units/logical-pixels.json` is the tokenized form of the repo's
unit system.

It packages:

- the logical-pixel definition,
- effective-scale math,
- quantization contexts,
- spacing and typography scales,
- platform mappings,
- and test profiles

into one machine-readable contract.

## Step 1. Relationship to the scaling math spec

This file is effectively the data payload companion to
`SCALING_MATHEMATICS.md`.

The prose spec explains the model. This JSON expresses that model in a form
that future code could consume directly.

That pairing is strong architecture.

## Step 2. Why it matters

If the repo ever wants shared runtime scaling behavior, it will need exactly
this kind of token surface:

- reference constants,
- quantization rules,
- platform mappings,
- invariant statements,
- common test cases.

So even though the current repo does not yet centrally consume this file, it is
an important design artifact.

## Bottom line

`specs/tokens/units/logical-pixels.json` is the tokenized unit-system contract.
It is one of the clearest examples of the repo trying to make its abstract
scaling math executable in principle, even though the corresponding runtime
engine is still missing.
