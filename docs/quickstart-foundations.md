# Quickstart From Foundations

Date: 2026-03-22

## What `quickstart.md` really is

`docs/quickstart.md` is the repo's shortest operational path.

Its job is not to explain all of OpenPerception. Its job is to get a person
from zero context to:

- installed simulation tooling,
- a first CVD output image,
- first validator runs,
- and awareness of the next documents to read.

So this guide is the onboarding bridge between the repo's large theory surface
and a user's first working command.

## Step 1. Identify the core reduction

The quickstart deliberately compresses a large system into one initial use
case:

- clone repo,
- install DaltonLens-Python,
- simulate,
- daltonize,
- run validators.

That is a very specific sequence, and it reveals something important about the
repo's practical center of gravity:

- the simulation engine is the first live subsystem,
- validation is the first policy subsystem,
- the broader documentation comes after the user sees something working.

## Step 2. Why submodules come first

The quickstart begins with `--recursive` because the algorithm lane is not
optional decoration here.

Without the DaltonLens submodules, the repo loses:

- the Python simulation backbone,
- the C implementation lane,
- a large part of its executable evidence.

So the quickstart quietly teaches a structural truth: OpenPerception is not
just a token repo with some docs attached.

## Step 3. What it chooses as the first successful outcome

The first "win" in this guide is not:

- generating CSS,
- loading GTK,
- building Sphinx,
- or reading the full spec.

It is:

- simulate a color-vision deficiency on an image,
- save the result,
- confirm the toolchain is alive.

That is a good choice because it gives immediate evidence that the repo's core
claim is operational, not merely rhetorical.

## Step 4. Why validation appears so early

The quickstart moves into `make contrast-check` and `make separation-check`
very quickly.

That sequencing matters.

It says the repo's output is not complete when a palette exists or a demo
renders. The output becomes meaningful when it is checked against accessibility
constraints.

So the quickstart teaches the repo's culture as much as its commands:

- build,
- inspect,
- validate.

## Step 5. What it leaves out intentionally

The guide does not try to teach:

- the full validator architecture,
- the mathematics of OKLCH,
- the full range of UVAS invariants,
- GTK, Sphinx, Pandoc, or TeX integrations in detail.

That omission is correct.

A quickstart should optimize for momentum, not completeness.

## Step 6. Where it reflects the current repo best

The document is especially well aligned with the present implementation because
it points at subsystems that definitely exist and run:

- `algorithms/DaltonLens-Python`
- `tools/contrast_check.py`
- `tools/separation_check.py`
- the Makefile test and setup flow

That makes it a stronger starting document than some of the more ambitious
specs, which are broader but less fully implemented.

## Step 7. Relationship to the rest of the docs

The quickstart should be read as the repo's "entry corridor."

After it, the natural branching paths are:

- `docs/simulator-guide.md` for the algorithm lane,
- `docs/contrast-guide.md` and `docs/oklch-guide.md` for token reasoning,
- `specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md` for the constitutional layer,
- platform guides for delivery into GTK, Sphinx, TeX, and browser examples.

## Bottom line

`docs/quickstart.md` is the repo's momentum document. It reduces a large
architecture into the first reproducible proof that the simulation and
validation stack is alive, and that makes it one of the most practically
important documents in the project.
