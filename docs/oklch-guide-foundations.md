# OKLCH Guide From Foundations

Date: 2026-03-22

## What `oklch-guide.md` really is

`docs/oklch-guide.md` is the repo's palette-geometry note.

It explains why OpenPerception does not rely on naive hue manipulation when it
wants structured token families. Its purpose is to give designers and
maintainers a perceptual coordinate system that behaves more predictably than
HSL or ad hoc hex tweaking.

In repo terms, it sits between:

- source tokens in `tokens/color-tokens.json`
- generated artifacts from `tools/gen_oklch_tokens.py`
- downstream validation work such as contrast and separation checks

## Step 1. Identify the conceptual move

The key move in the OKLCH guide is:

- stop treating color as raw RGB triples,
- move into a space where lightness is closer to human perception,
- reason about families by lightness, chroma, and hue separately.

That is why the guide matters. It gives the repo a design language for talking
about palette structure without pretending RGB coordinates are intuitive.

## Step 2. Why this matters in OpenPerception specifically

This repo is not only trying to make a pleasant palette. It is trying to make
a palette that survives:

- accessibility checks,
- CVD accommodation,
- theme variation,
- cross-format export into CSS, GTK, TeX, and documentation artifacts.

For that kind of work, a perceptual coordinate system is not cosmetic. It is a
stability aid.

## Step 3. What the generator actually does

The guide talks about generated OKLCH artifacts, and the current implementation
is straightforward:

- `tools/gen_oklch_tokens.py` reads `tokens/color-tokens.json`
- it computes OKLCH tuples for hex values
- it writes `tokens/color-oklch-map.json`
- it writes `tokens/color-tokens-oklch.css`

This means the guide is grounded, but also narrower than it may first appear.

The present generator is built around the production ramps:

- `indigo`
- `magenta`
- `gray`

So the guide currently describes the production token lane more directly than
the newer experimental token packs.

## Step 4. What it gets right

The guide's strongest claim is that perceptual lightness should be treated as a
first-class design parameter.

That helps with:

- predictable ramp construction,
- more reliable dark/light pairing,
- fewer accidental brightness jumps,
- better reasoning about accessible surfaces and accents.

This is one reason the repo could reach the later experimental conclusion that
an indigo/mauve/burgundy lane is structurally cleaner than a tighter
indigo/magenta pairing under some simulated deficiencies.

## Step 5. Where the document is slightly behind the repo

There is one visible doc drift in the variant table:

- the guide says `data-cvd="achromat"`
- the generated selectors and broader repo convention use `mono`

That matters because this guide is describing an implementation interface, not
only a concept.

There is also a broader scope mismatch:

- the guide reads like a general OKLCH architecture note,
- but the generator is still keyed to the production source-of-truth token set.

So the correct interpretation is:

- the color-space explanation is general,
- the current artifact generation is still production-pack specific.

## Step 6. What the guide does not claim

OKLCH is helpful, but it is not magic.

The guide should not be read as claiming that OKLCH alone guarantees:

- CVD-safe separation,
- universal readability,
- semantic clarity,
- success under monochrome conditions.

That is why the repo still needs:

- contrast checks,
- separation checks,
- explicit variants,
- non-color redundancy.

OKLCH helps construct better candidates. It does not remove the need to test
them.

## Step 7. Relationship to experimental palette work

The experimental palette lane extends the logic of this guide even though the
main generator does not yet own those packs.

In other words:

- the OKLCH guide explains the design math well,
- the experimental tokens prove that the same logic can support alternate hue
  families,
- the implementation debt is that the generator still centers the original
  production ramps.

## Bottom line

`docs/oklch-guide.md` is the repo's perceptual palette-construction note. Its
theory remains solid, but its artifact examples still describe the production
token lane more directly than the newer experimental packs, and its achromat
labeling should now be read as `mono` in current repo terms.
