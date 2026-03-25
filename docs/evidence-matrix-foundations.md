# Evidence Matrix From Foundations

Date: 2026-03-22

## What `EVIDENCE_MATRIX.md` really is

`specs/EVIDENCE_MATRIX.md` is the repo's claims registry.

It is the closest thing OpenPerception has to a structured constitution of
evidence:

- what the project believes,
- which axis each belief belongs to,
- what kind of evidence supports it,
- and whether the claim acts like a hard floor, a comfort preference, or a
  tradeoff.

So this document is not only bibliography and not only specification. It is the
binding layer between research and policy.

## Step 1. Identify the key move

The matrix takes a difficult problem:

- a large number of heterogeneous research findings across color, vision,
  seizure safety, cognition, and layout

and normalizes them into one repeatable schema.

That is a very important move because it turns "we read a lot of papers" into
"we have structured, inspectable claims."

## Step 2. Why this matters in this repo

OpenPerception makes broad promises. Without a claims registry, those promises
would be hard to audit.

The evidence matrix gives the repo a way to say:

- this claim belongs to this axis,
- it affects these UI primitives,
- it has this kind of evidentiary status,
- it implies this threshold or constraint.

That makes the repo more rigorous than a loose research compendium alone.

## Step 3. What it gets right

The matrix is strongest where it distinguishes:

- hard safety constraints,
- softer comfort constraints,
- model-based implementation assumptions.

That distinction is crucial.

For example:

- seizure limits should be treated very differently from aesthetic comfort
  preferences,
- simulation-pipeline requirements are not the same kind of claim as clinical
  prevalence,
- layout and cognitive guidance should not masquerade as absolute law without
  saying so.

## Step 4. What it is not

The evidence matrix is not an implementation ledger.

A claim being present here does not mean:

- the validator exists,
- the threshold is enforced in CI,
- the product surface actually satisfies it today.

This is the same declared-law versus implemented-law split we already saw in
UVAS and the validators framework.

## Step 5. Why it is foundational

This file is foundational because many of the repo's other specs implicitly
depend on it:

- UVAS uses its thresholds and invariants,
- overlap and seam maps rely on its axis framing,
- future validators are supposed to enforce parts of it,
- roadmap items assume its claims are the evidence basis for implementation.

So if UVAS is the constitution, the evidence matrix is the cited case law.

## Step 6. Where the debt still is

The matrix creates a powerful structure, but it also exposes debt very clearly:

- many claims have no corresponding validator yet,
- some claims depend on secondary or mixed-strength evidence,
- the repo still lacks a full machine-readable enforcement path from matrix
  entry to validation artifact.

That is not a flaw in the document. It is the implementation backlog made
legible.

## Bottom line

`specs/EVIDENCE_MATRIX.md` is the repo's claims registry. It is one of the most
important foundations documents because it turns broad research into structured,
auditable assertions, even though much of the enforcement logic still remains
to be built.
