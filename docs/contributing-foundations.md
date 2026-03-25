# Contributing From Foundations

Date: 2026-03-22

## What `CONTRIBUTING.md` really is

`CONTRIBUTING.md` is the repo's participation contract.

It tells contributors:

- how to enter the project,
- what quality bars exist,
- how changes should be shaped,
- and what kinds of evidence and tests are expected.

So this document is governance, not just etiquette.

## Step 1. Identify the repo values it encodes

The contribution guide encodes several repo values very clearly:

- accessibility is both subject matter and collaboration norm,
- evidence matters,
- tests matter,
- documentation matters,
- cross-language quality matters for both Python and C.

That alignment is important. The guide is not just telling people how to open a
PR; it is telling them what kind of project this is.

## Step 2. What it does well

The strongest parts of the guide are its insistence on:

- focused pull requests,
- documentation updates,
- tests for new work,
- and explicit coding standards for both Python and C.

That is a strong fit for a repo where algorithm correctness and claims
credibility matter.

## Step 3. What it reveals about architecture

The contribution guide also quietly reveals the repo's structure:

- Python algorithm lane,
- C library lane,
- tools and validators lane,
- research and specification lane.

That makes it a useful orientation document even for readers who are not yet
planning to contribute code.

## Step 4. Where it is slightly behind current reality

A few details now need to be read with current-state awareness:

- the guide describes quality tooling, but some newer experimental palette and
  foundations-doc workflows are not yet mentioned,
- it is centered on the major established lanes rather than the newest
  experimental work,
- its setup steps emphasize algorithm subdirectories more than the repo-root
  workflows now used in several newer tasks.

None of that breaks the document. It just means it still reflects the more
established core of the project.

## Bottom line

`CONTRIBUTING.md` is the repo's participation contract. It does a good job of
encoding the project's quality and evidence culture, but it will eventually
need light expansion to mention the newer experimental and documentation-heavy
workflows now present in the repo.
