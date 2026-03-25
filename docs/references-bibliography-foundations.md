# References Bibliography From Foundations

Date: 2026-03-22

## What `REFERENCES_BIBLIOGRAPHY.md` really is

`specs/REFERENCES_BIBLIOGRAPHY.md` is the repo's citation spine.

Its job is to consolidate the external references that the UVAS+ spec family
depends on:

- standards,
- toolkit docs,
- research papers,
- platform documentation,
- algorithm sources.

So this document is not itself a theory note. It is the cross-spec citation
infrastructure.

## Step 1. Why this matters

A repo with many interlocking specs can become hard to audit if sources are
scattered everywhere.

The bibliography helps by centralizing:

- where claims come from,
- which source families are being relied on,
- and which external domains form the project's evidentiary base.

That makes the spec family easier to maintain and inspect.

## Step 2. What it does well

The document is strongest where it combines:

- standards references,
- research references,
- toolkit/platform references,
- and implementation-oriented documentation links.

That breadth is appropriate because OpenPerception spans both normative
accessibility law and low-level rendering behavior.

## Step 3. Relationship to the evidence matrix

This bibliography and the evidence matrix are complementary:

- the bibliography centralizes source inventory,
- the evidence matrix turns selected sources into structured claims.

That division is healthy. It keeps citation storage separate from claim
normalization.

## Step 4. What the document is not

This is not a guarantee that every citation is equally strong, current, or
enforced in code.

It is best read as:

- the source backbone for the spec family,
- not a direct implementation status report.

## Bottom line

`specs/REFERENCES_BIBLIOGRAPHY.md` is the repo's citation spine. It is valuable
because it keeps the expanding spec family tethered to auditable external
sources, even though the repo still needs stronger end-to-end links from
bibliography to enforceable validators and artifacts.
