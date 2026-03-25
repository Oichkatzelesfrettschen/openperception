# Daltonization Guide From Foundations

Date: 2026-03-22

## What `daltonization-guide.md` really is

`docs/daltonization-guide.md` is the repo's image-remediation note.

It is not about token selection first. It is about what to do when a finished
image or chart already exists and we need to alter that image so a CVD viewer
can distinguish more of its content.

That places it beside, not above:

- token design,
- contrast validation,
- CVD separation checks.

## Step 1. Start with the core distinction

The most important move in the guide is the split between:

- simulation,
- daltonization.

Simulation asks:

- what does the original look like to a given viewer model?

Daltonization asks:

- how can we transform the image so that viewer loses less usable
  information?

That distinction matters because the repo uses simulation for validation, but
daltonization for intervention.

## Step 2. Why this belongs in the repo

OpenPerception is not only a token library. It also touches charts, rendered
artifacts, and documentation assets.

That means some accessibility problems arise after the palette is chosen:

- an imported figure,
- a screenshot,
- a legacy chart,
- a static image generated elsewhere.

Daltonization exists for that layer of the problem.

## Step 3. What the implementation actually contains

The guide maps well to the vendored implementation in
`algorithms/DaltonLens-Python/daltonlens/daltonize.py`.

That file currently exposes:

- `daltonize_fidaner`
- `daltonize_simple`
- `daltonize` as a dispatcher

The Fidaner path does four concrete steps:

1. simulate the chosen deficiency,
2. convert original and simulated images into linear RGB,
3. compute the lost-color error,
4. shift that error into channels that remain more usable and add it back.

So the guide's explanation is not hand-wavy. It reflects real code in the
repo.

## Step 4. What the Fidaner method is really doing

The easiest way to read the default method is:

- detect information that vanished under simulation,
- re-encode part of that information elsewhere.

For protan and deutan cases, the current implementation pushes lost
red/green structure toward green/blue channels. For tritan, it pushes lost
blue/yellow structure toward red/green channels.

This is why daltonization is always a compromise:

- it is trying to preserve the original image,
- while also making hidden distinctions visible through another route.

## Step 5. What the simple method means

The simple method is best understood as a pragmatic approximation.

It does not run the full simulation-and-error pipeline. It directly enhances
channel distinctions in a cheaper way.

That makes it useful when:

- speed matters,
- visual fidelity is less critical,
- a rough improvement is good enough.

So the guide is right to present it as lighter-weight rather than equivalent in
quality.

## Step 6. What daltonization does not solve

This guide becomes much clearer when we say what it is not for.

Daltonization does not eliminate the need for:

- good base token design,
- readable labels,
- contrast validation,
- shapes, hatching, icons, or text redundancy.

It is a repair or enhancement tool, not a universal replacement for accessible
design.

That is especially important in this repo, where the foundation documents
already insist that color must not carry meaning alone.

## Step 7. Relationship to the validator stack

Daltonization is adjacent to the validator stack, but not the same thing.

- contrast validators answer whether text and surfaces remain readable,
- CVD separation validators answer whether token families stay far enough apart,
- daltonization changes an image so more of its encoded differences survive.

So this guide should be read as part of the repo's rendering and remediation
toolbox, not as a semantic-token policy document.

## Step 8. Why DaltonLens matters here

The presence of vendored DaltonLens code means this guide is backed by a
serious algorithmic lane, not just a design aspiration.

That matters for two reasons:

- OpenPerception can explain its image-adjustment claims against real source,
- the repo can evolve simulation and remediation together instead of treating
  them as unrelated features.

## Bottom line

`docs/daltonization-guide.md` is the repo's practical guide to post hoc image
remediation for CVD viewers. It is well grounded in the vendored DaltonLens
implementation, but it should always be read as a complement to accessible
palette design and validator enforcement, not a substitute for them.
