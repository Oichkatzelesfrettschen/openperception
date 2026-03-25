# Pandoc Guide From Foundations

Date: 2026-03-22

## What `pandoc-guide.md` really is

`docs/pandoc-guide.md` is the repo's document-export bridge.

It answers a practical need:

- how do Markdown documents inherit the OpenPerception design system when they
  are rendered into standalone HTML or PDF artifacts?

This makes it a publishing-layer companion to the Sphinx and TeX guides.

## Step 1. Identify the architectural choice

The guide makes a strong architectural choice:

- keep content in Markdown,
- keep presentation in templates and shared CSS,
- let exported documents inherit the token system rather than restyling them by
  hand.

That is exactly the kind of separation the repo wants elsewhere too:

- semantics in source,
- presentation in controlled token-driven layers.

## Step 2. What it preserves from the core system

The Pandoc lane preserves several important repo-level behaviors:

- consistent surfaces and text colors,
- token-driven headings and notices,
- CVD-aware variant switching,
- black-and-white print fallback.

That last point is especially important. The print stylesheet forces a
high-contrast monochrome path, which is a very practical acknowledgement that
"accessible output" sometimes means giving up brand color entirely.

## Step 3. Why this guide matters

The guide shows that OpenPerception is not confined to interactive UI.

It also wants:

- reports,
- specs,
- exported documents,
- printable artifacts

to remain aligned with the same accessibility logic.

That expands the scope of the project from interface skinning into document
production discipline.

## Step 4. Where it is slightly out of sync

Like the OKLCH guide, the Pandoc guide has a small variant-label mismatch:

- it documents `achromat`
- the broader current repo convention is `mono`

That is not a conceptual problem, but it is an implementation detail worth
keeping explicit.

There is also a subtle platform warning embedded in the guide:

- not every HTML-to-PDF engine respects the modern CSS path equally well.

That is why WeasyPrint is preferred over wkhtmltopdf.

## Step 5. What the guide is really teaching

Under the surface, this guide teaches three things:

1. token-driven publishing is possible,
2. print output is a different accessibility environment than screen output,
3. exported docs still need explicit variant and contrast thinking.

So even though the guide looks like a templating how-to, it is really another
instance of the repo's broader rule:

- do not let presentation drift away from validated semantics.

## Bottom line

`docs/pandoc-guide.md` is the repo's Markdown-to-artifact publishing bridge. It
extends the token system into standalone HTML and PDF outputs, and it does so
in a way that preserves both brand structure and practical monochrome fallback.
