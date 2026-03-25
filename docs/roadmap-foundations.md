# Roadmap From Foundations

Date: 2026-03-22

## What `ROADMAP.md` really is

`ROADMAP.md` is the repo's declared future-state ledger.

It does three jobs at once:

- it states ambition,
- it marks what the project thinks is already done,
- it exposes where implementation debt still lives.

So this document should not be read as a neutral snapshot. It is a planning
artifact that mixes aspiration, completion claims, and milestone framing.

## Step 1. Identify the central tension

The roadmap's central tension is the same one that appears elsewhere in the
repo:

- the project has a very large conceptual scope,
- but only part of that scope is fully implemented today.

The roadmap is valuable because it does not hide that tension. It names it.

## Step 2. What it says about the repo's identity

The roadmap makes clear that OpenPerception sees itself as more than:

- a CVD simulator,
- a token package,
- or a docs collection.

It wants to become a broad visual-accessibility system spanning:

- CVD,
- neurodivergence,
- visual processing differences,
- validators,
- integrations,
- standards work.

That ambition is important context for almost every other document.

## Step 3. Where the document is strongest

The roadmap is strongest when it distinguishes:

- completed infrastructure,
- in-progress work,
- deferred work,
- and spec-only territory.

That last category is especially useful. It prevents readers from mistaking
every specification file for a near-term implementation promise.

## Step 4. Where the roadmap now shows drift

Because the repo has continued to evolve, some roadmap wording should now be
read carefully.

Examples:

- the validator framework is listed as "in progress," which is true at the
  system level but hides that contrast and CVD validators already exist,
- web examples expansion has moved forward materially,
- newer experimental palette and foundations work are not yet reflected here.

So the roadmap is still directionally useful, but it is not a full live mirror
of the repo's newest state.

## Step 5. How to read it well

The right way to use this roadmap is:

- as a strategic map,
- not as the sole source of implementation truth.

For implementation truth, pair it with:

- `docs/current-work-inventory.md`
- `CHANGELOG.md`
- the actual `tools/`, `examples/`, and `docs/` trees

That combination tells you both where the repo is trying to go and what is
already real.

## Bottom line

`ROADMAP.md` is the repo's ambition ledger. It is broad, useful, and honest
about major gaps, but it should always be read alongside current implementation
artifacts because the project has already moved beyond parts of its last stated
milestone picture.
