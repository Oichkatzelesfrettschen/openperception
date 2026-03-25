# Font Families Token From Foundations

Date: 2026-03-22

## What `font-families.json` really is

`specs/tokens/typography/font-families.json` is the repo's font decision matrix
in token form.

It maps use-case categories to:

- preferred families,
- alternates,
- platform stacks,
- accessibility overrides,
- and fallback strategies.

This makes it the practical companion to the stricter font contract file.

## Step 1. Relationship to the font contract

The clean way to read the typography token pair is:

- `font-contract.json` defines what a good font must satisfy,
- `font-families.json` proposes concrete families that likely satisfy those
  requirements in different contexts.

That is a healthy separation of evaluation from selection.

## Step 2. What it reveals

This file shows that the repo wants typography to serve different semantic
surfaces:

- UI sans,
- long-form sans,
- reading serif,
- monospace,
- accessibility overrides for dyslexia, low vision, and cognitive load.

That breadth reinforces that OpenPerception is not only a color project.

## Bottom line

`specs/tokens/typography/font-families.json` is the repo's font decision matrix
in token form. It complements the font contract by translating abstract
typographic requirements into actionable family choices and platform stacks.
