# Known Issues From Foundations

Date: 2026-03-22

## What `KNOWN_ISSUES.md` really is

`docs/KNOWN_ISSUES.md` is the repo's explicit debt register.

It is where the project states:

- what is still incomplete,
- what is intentionally imperfect,
- what is acceptable for now,
- and what needs future implementation or cleanup.

This makes it one of the most important honesty documents in the repo.

## Step 1. Why this document matters

In a project with broad specifications and ambitious claims, a known-issues file
prevents a dangerous illusion:

- that the current implementation already matches the full conceptual scope.

So this document is not just housekeeping. It is a safeguard against
overclaiming.

## Step 2. What it gets right

The file is strongest where it distinguishes among different kinds of debt:

- intentional design tradeoffs,
- documentation gaps,
- implementation gaps,
- infrastructure gaps,
- third-party dependency concerns,
- research gaps.

That categorization is helpful because not all debt is the same kind of risk.

## Step 3. What it reveals about the repo

The known-issues list reinforces the same pattern we saw in UVAS and the
validators framework:

- core contrast and CVD pieces exist,
- many broader accessibility ambitions remain ahead of implementation,
- some vendor and tooling tradeoffs are accepted intentionally,
- research breadth exceeds current enforcement breadth.

This is a realistic and useful picture of the project.

## Step 4. Where the file now shows update debt

There is some fresh drift here too.

Examples:

- the examples-documentation issue is partly improved now that
  `examples/README.md` and additional example work exist,
- the new foundations-doc lane is not yet reflected,
- newer experimental palette work and comparison tooling are not yet surfaced as
  either capabilities or open integration debt.

That means the known-issues file is still valuable, but it is no longer a fully
current account of repo debt after this pass.

## Step 5. How to read it well

Use this file as:

- a debt index,
- a caution against assuming the specs are fully enforced,
- and a triage starting point.

Pair it with:

- `ROADMAP.md`
- `docs/current-work-inventory.md`
- `CHANGELOG.md`

to understand both declared debt and newly landed work that may not yet be
backfilled into the governance docs.

## Bottom line

`docs/KNOWN_ISSUES.md` is the repo's explicit debt register, and it remains one
of the best documents for understanding implementation gaps. It now deserves a
small refresh so its issue list matches the newer example, experimental palette,
and foundations-document work already present in the tree.
