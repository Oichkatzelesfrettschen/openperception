# LaTeX Render Rules From Foundations

Date: 2026-03-22

## What `RENDER_RULES.md` really is

`specs/renderers/latex/RENDER_RULES.md` is the repo's prose contract for
accessible LaTeX output.

It explains how UVAS ideas should survive in academic and technical documents:

- typography,
- figures,
- tables,
- equations,
- code listings,
- hyperlinking,
- and PDF accessibility features.

So this document is a renderer policy note, not a generic LaTeX style guide.

## Step 1. What it does well

The guide is strongest where it keeps accessibility concerns visible in
traditionally neglected areas:

- figure alt text,
- CVD-safe figures,
- code listing readability,
- heading hierarchy,
- line-length and spacing floors.

That is the right way to treat technical publishing in this repo.

## Step 2. Relationship to the TeX guide

This file differs from `docs/tex-pgfplots-guide.md` in a useful way:

- the guide in `docs/` is practical user-facing workflow,
- this renderer spec is the normative LaTeX output contract.

Together they form a good prose-spec pair.

## Bottom line

`specs/renderers/latex/RENDER_RULES.md` is the repo's normative LaTeX renderer
policy. It extends the project's accessibility thinking into academic and print
publishing rather than leaving that surface to conventional defaults.
