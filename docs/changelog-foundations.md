# Changelog From Foundations

Date: 2026-03-22

## What `CHANGELOG.md` really is

`CHANGELOG.md` is the repo's formal memory of change.

Unlike the roadmap, which points forward, the changelog tries to capture:

- what was added,
- what changed,
- what was fixed,
- and what state existed before formal release tracking.

That makes it one of the repo's most important truth-maintenance documents.

## Step 1. Why it matters in this repo

OpenPerception has several overlapping layers:

- repo-owned algorithm lanes,
- new validators,
- specs,
- docs,
- examples,
- research compendiums,
- theme and token work.

In a repo like that, the changelog is not cosmetic. It is one of the few places
that can explain how the current mixture came to exist.

## Step 2. What it gets right

The changelog does two especially valuable things:

- it records the infrastructure formalization of a repo that already had
  substantial prior content,
- it preserves the difference between newly added project scaffolding and
  previously existing algorithm or research material.

That helps later readers avoid the false impression that everything appeared at
once.

## Step 3. What kind of document it is not

This is not a complete implementation audit.

A changelog records notable deltas, not all current facts.

So if a reader wants to know:

- what is currently implemented,
- what examples exist,
- what docs now have foundations companions,

the changelog alone is insufficient.

## Step 4. Where drift now exists

Because we added substantial work in this pass, the current `Unreleased`
section is now incomplete relative to the repo.

For example, it does not yet include:

- the experimental mauve/burgundy token lane,
- the experimental red/mahogany lane,
- palette comparison example work,
- the new foundations-note document family,
- the unified color-scheme scope note.

That is normal for active work, but it means the changelog now carries a fresh
update debt.

## Step 5. How to use it correctly

Use the changelog for:

- release-oriented history,
- major deltas,
- understanding when infrastructure and governance arrived,
- spotting update debt when new work has landed but is not yet recorded.

Pair it with:

- `docs/current-work-inventory.md`
- `ROADMAP.md`
- and actual repo inspection

if you need a full current-state picture.

## Bottom line

`CHANGELOG.md` is the repo's formal memory of change, but it now needs a fresh
`Unreleased` update to reflect the new experimental palette and foundations
work that has landed in this pass.
