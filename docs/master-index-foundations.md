# Master Index From Foundations

Date: 2026-03-22

## What `MASTER_INDEX.md` really is

`MASTER_INDEX.md` is an inventory document.

Its primary job is not to define behavior. Its job is to answer:

- what research domains exist here,
- what paper collections exist here,
- what compendiums exist here,
- how the repository's evidence base is organized.

So this document should be read as:

- map,
- catalog,
- navigation aid,
- research coverage summary.

It should not be read as:

- implementation spec,
- token contract,
- algorithm reference,
- runtime architecture.

## Step 1. Identify the organizing principle

The organizing principle is domain grouping.

The document clusters material into:

- CVD,
- algorithms,
- visual impairments,
- neurodivergence,
- seizure safety,
- cognitive load.

That tells us OpenPerception is not just a "colorblindness repo." It is a
broader visual accessibility and perception research workspace.

## Step 2. Distinguish research from implementation

The master index mixes several layers:

1. research categories,
2. downloaded PDFs,
3. markdown compendiums,
4. directory layout,
5. topic-level reference summaries.

That is useful, but it also means the reader has to know which layer they are
looking at.

The safe interpretation is:

- categories = conceptual taxonomy,
- PDF collections = local corpus snapshot,
- compendium files = curated markdown summaries,
- directory structure = navigation,
- key references = fast topical entry points.

## Step 3. Check against the actual tree

The repo tree supports the document's broad claims:

- `papers/downloads/*` exists,
- `research/*` exists with domain subtrees,
- the named compendium files exist,
- the algorithm and docs lanes exist.

So `MASTER_INDEX.md` is substantially synchronized with the current repo shape.

## Step 4. Why this document matters

Without `MASTER_INDEX.md`, it is easy to mistake the repo for:

- only an algorithm package,
- only a token system,
- or only a design-doc collection.

The index corrects that by showing the repo's actual center of gravity:

- evidence-backed accessibility work spanning research, algorithms, tokens,
  docs, and examples.

## Step 5. What this document is missing

Because it is a research inventory, it does not foreground the newer
experimental theme and token work added in this pass.

That is not a flaw; it just means it is stable and slower-moving than the
implementation notes.

The newer implementation-facing complement is:

- `docs/current-work-inventory.md`

## Bottom line

`MASTER_INDEX.md` is the repo's research map. It tells you what domains and
corpora exist, not what the current product decisions are.
