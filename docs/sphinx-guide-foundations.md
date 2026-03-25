# Sphinx Guide From Foundations

Date: 2026-03-22

## What `sphinx-guide.md` really is

`docs/sphinx-guide.md` is the repo's documentation-site integration note.

Its role is simple but important:

- take the token and accessibility work,
- bind it into a Sphinx theme,
- make published docs inherit the same visual system as the rest of the repo.

So this guide is not about accessibility theory first. It is about carrying the
theory into a documentation renderer.

## Step 1. Identify the translation

The guide translates between:

- OpenPerception token CSS,
- Sphinx theme configuration,
- static site output.

That translation matters because a design system does not become real until it
survives the publishing layer.

## Step 2. What grounds it in the repo

The guide is backed by two concrete implementation paths:

- `sphinx/brand_theme/` as a local theme folder,
- `python-packages/sphinx-brand-theme/` as a packaged reusable theme.

That means it supports both:

- repo-local experimentation,
- and broader reuse outside the example tree.

This dual path makes the guide more than a one-off setup note.

## Step 3. What it is really preserving

The deepest purpose of the guide is preservation of invariants.

When docs move into Sphinx, the project still wants:

- branded surfaces,
- readable link treatments,
- visible focus,
- CVD variant switching,
- and alignment with the shared token vocabulary.

Without that bridge, documentation could quietly drift back to a generic theme
that ignores the repo's core accessibility principles.

## Step 4. Why this guide is intentionally minimal

The Sphinx guide is short because most of the complexity already lives
elsewhere:

- token generation,
- CSS definitions,
- theme packaging,
- Sphinx's own build system.

Its job is only to show the join points.

That is appropriate. A platform-bridge guide should be brief if the underlying
artifacts are already clear.

## Step 5. Where it sits relative to the current palette work

Like the GTK and OKLCH lanes, the Sphinx guide currently reflects the
production token pack more directly than the experimental palette packs.

That means the guide is still accurate for the main shipping path, but the repo
would need additional work if experimental mauve/burgundy or red/mahogany
themes are meant to become first-class Sphinx options.

## Bottom line

`docs/sphinx-guide.md` is the repo's Sphinx delivery note. It ensures the
accessibility-aware token system can cross into published documentation, and it
shows that OpenPerception treats docs as part of the product surface, not as an
unrelated afterthought.
