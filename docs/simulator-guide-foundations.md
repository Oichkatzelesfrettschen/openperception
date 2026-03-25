# Simulator Guide From Foundations

Date: 2026-03-22

## What `simulator-guide.md` really is

`docs/simulator-guide.md` is the repo's algorithm-access guide.

It explains how OpenPerception exposes the simulation lane in a form that
developers can actually use:

- through Python,
- through the CLI,
- through browser-facing examples,
- and through named model choices.

This makes it the practical front door to the DaltonLens-backed evidence
stack.

## Step 1. Start from the repo's deepest need

OpenPerception makes claims about accessibility under color-vision
deficiency. Those claims need a model layer that can answer:

- what would a viewer with a given deficiency actually see?

The simulator guide exists because without that model layer, the repo would be
reduced to guesswork and style preference.

## Step 2. Why multiple simulators exist

The guide lists several simulator classes because the repo is not built around
one universal algorithm.

Different models emphasize different tradeoffs:

- Brettel 1997 as the strongest general reference,
- Vienot 1999 as a simpler fast path,
- Machado 2009 for severity modeling,
- legacy Coblis variants as historical comparison rather than preferred truth.

This matters because the guide is quietly teaching epistemic discipline:

- not every simulation is equally grounded,
- model choice affects what conclusions are trustworthy.

## Step 3. What the guide is really exposing

At first glance, the guide looks like API documentation. But structurally it is
doing more than that.

It exposes the simulation pipeline as a chain:

- sRGB input,
- linear RGB conversion,
- LMS projection,
- deficiency-specific transform,
- conversion back to output RGB.

That is exactly the bridge between the high-level accessibility mission and the
actual image-processing math in the vendored algorithm code.

## Step 4. Why severity is important

The severity section is one of the most important conceptual parts of the
guide.

It separates:

- full dichromacy,
- partial anomalous trichromacy.

That means the repo is not limited to a crude "blind or not blind" model. It
admits a continuum, which is far closer to the real human landscape.

This is also why the guide correctly points people to Machado 2009 when
severity below `1.0` is important.

## Step 5. How the browser example fits

The mention of `examples/simulator/index.html` is especially useful because it
shows a second delivery path:

- heavyweight, algorithm-backed simulation in Python,
- lightweight approximation through SVG color-matrix filters in the browser.

These are not equivalent. The browser version is a convenient preview, while
the Python simulator is the more serious validation path.

That distinction is worth keeping explicit.

## Step 6. What the guide does not claim

The simulator guide should not be read as saying:

- simulation alone guarantees accessibility,
- simulated appearance is the same thing as semantic usability,
- SVG filters are full substitutes for the algorithmic simulator.

Simulation shows one kind of perceptual transformation. The repo still needs:

- contrast checks,
- separation thresholds,
- non-color redundancy,
- platform-specific implementation discipline.

## Step 7. Relationship to the broader repo

The simulator guide is the practical companion to:

- `docs/daltonlens-python-foundations.md`
- `docs/daltonization-guide.md`
- `tools/validators/cvd.py`
- `examples/simulator/index.html`

Taken together, those pieces show the full loop:

- simulate,
- inspect,
- validate,
- optionally remediate.

## Bottom line

`docs/simulator-guide.md` is the repo's practical guide to the CVD modeling
engine. It turns the DaltonLens algorithm lane into an everyday tool, while
also teaching that model choice and severity modeling matter for any serious
accessibility claim.
