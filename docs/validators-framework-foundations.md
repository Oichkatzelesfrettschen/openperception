# Validators Framework From Foundations

Date: 2026-03-22

## What `VALIDATORS_FRAMEWORK.md` really is

`specs/VALIDATORS_FRAMEWORK.md` is the enforcement bridge between UVAS and
actual code.

If UVAS is the constitutional layer, the validators framework is the proposed
judicial system:

- what gets checked,
- what blocks,
- what warns,
- what tool or algorithm should perform the check.

## Step 1. Its main structural move

The framework turns accessibility requirements into named gates.

That is important because the repo needs more than principles. It needs
machine-actionable decisions like:

- pass,
- warn,
- fail,
- block merge,
- emit recommendation.

This is how the repo moves from design philosophy to operational practice.

## Step 2. Severity is the real backbone

The most important architectural idea in the validator framework is not the
ASCII diagram. It is the severity model.

The framework distinguishes:

- blocking gates,
- warning gates.

That lets the repo express different kinds of truth:

- seizure safety and contrast are floors,
- CVD discriminability may initially be advisory,
- future spatial or cognitive checks may mature from warnings into blockers.

That makes the framework evolvable.

## Step 3. What is actually implemented

Current repo state:

- `tools/validators/base.py` exists
- `tools/validators/contrast.py` exists
- `tools/validators/cvd.py` exists

So the framework is partially implemented, not hypothetical.

But only two gates are actually operational today:

- GATE-002 contrast
- GATE-003 CVD

Everything else remains framework-level intent.

## Step 4. Where the code is narrower than the framework

This is the crucial practical point.

The framework describes a richer validation world than the code currently
executes.

Examples:

- The framework describes simulated delta-E thresholds per deficiency.
- The current CVD validator checks authored Oklab separation for primary/accent
  token pairs only.

- The framework imagines content-type dispatch across video, layout, scene, and
  navigation assets.
- The current repo validators operate on token JSON only.

- The framework names specific external tools for flash and temporal analysis.
- No such gate is implemented yet in `tools/validators/`.

So the framework should be read as:

- partly real,
- partly target architecture.

## Step 5. Why this still matters now

Even with partial implementation, the framework is valuable because it makes
implementation debt legible.

It tells us:

- what missing gates exist,
- which ones are supposed to block,
- what their inputs and outputs should look like,
- where repo growth should go next.

Without this document, missing validators would feel like accidental omissions.
With it, they become tracked incompleteness.

## Step 6. Relationship to current experimental work

The new experimental palette work uses the same enforcement spirit:

- explicit validator script,
- measurable outputs,
- no silent hand-waving about accessibility.

But it still sits below the full framework ambition.

In particular, the palette reports do not yet implement:

- simulated semantic-role matrix checking,
- seizure/flash analysis,
- spatial density or cognitive checks,
- unified CLI dispatch.

## Bottom line

`VALIDATORS_FRAMEWORK.md` is the enforcement blueprint. It explains how the
repo intends to turn UVAS into gates, and it makes the current difference
between "implemented law" and "declared law" explicit.
