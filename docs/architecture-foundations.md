# Architecture From Foundations

Date: 2026-03-22

## What `ARCHITECTURE.md` really is

`ARCHITECTURE.md` is the bridge document between evidence, algorithms, design
system, and tooling.

It answers:

- what the major subsystems are,
- how they depend on one another,
- how data and constraints flow through the repo.

## Step 1. Identify the stack layers

The architecture document defines five layers:

1. research and evidence,
2. specifications and standards,
3. core algorithms,
4. design system,
5. development tools.

This is the right mental model for the repo.

## Step 2. Read the dependency direction

The intended direction is:

`research -> specifications -> algorithms/design system -> tools/validation`

This matters because it prevents upside-down reasoning. The repo is not meant
to invent accessibility claims from style preference and then search for
justification later. It is meant to derive implementation from evidence.

## Step 3. Place the main algorithm components

The architecture document correctly identifies two core engines:

- `DaltonLens-Python`
- `libDaltonLens`

The first is the research/runtime Python lane.
The second is the portable C lane.

That split is important:

- Python supports experimentation and analysis,
- C supports embedding and minimal deployment.

## Step 4. Place the design system

The design system layer contains:

- token JSON/CSS,
- GTK demo assets,
- examples.

This means OpenPerception is not only about simulation. It also turns the
simulation and evidence work into concrete design outputs.

## Step 5. Place validation

The tools layer is what makes the whole stack operational.

Without it, the repo would be a research archive.
With it, the repo becomes an enforceable accessibility workspace.

The important takeaway is:

- validators are not auxiliary,
- they are how evidence becomes practice.

## Step 6. How the newer experimental work fits

The new experimental packs and walkthrough notes fit naturally into the
existing architecture:

- new palette notes live between specs and design system,
- new token packs live in design system,
- comparison examples live in examples,
- validation scripts live in tools.

So the recent work is additive, not architectural drift.

## Bottom line

`ARCHITECTURE.md` is the repo's dependency map. If `MASTER_INDEX.md` tells you
what knowledge is here, `ARCHITECTURE.md` tells you how that knowledge is
turned into tools, tokens, and validation.
