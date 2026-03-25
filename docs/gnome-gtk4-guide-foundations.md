# GNOME GTK4 Guide From Foundations

Date: 2026-03-22

## What `gnome-gtk4-guide.md` really is

`docs/gnome-gtk4-guide.md` is the desktop-delivery note for the brand and CVD
system.

It answers a practical question:

- once the tokens and accessibility rules exist, how do they become a working
  GTK4/libadwaita application skin without patching the whole desktop?

So this guide is not mainly about color theory. It is about platform mapping.

## Step 1. Identify the design decision

The guide's first major decision is:

- apply CSS at the application layer,
- do not patch the global system theme.

That is an important architectural choice because it keeps OpenPerception:

- reversible,
- app-scoped,
- testable,
- easier to distribute as a library or example pack.

## Step 2. What it is mapping

The guide is translating one vocabulary into another:

- OpenPerception brand roles and variant logic,
- GTK and libadwaita color roles and widget classes.

That translation is the heart of the document.

Without it, the repo would have an accessibility-aware token language but no
clear way to land it in a real desktop UI stack.

## Step 3. How the local demo grounds it

The guide is backed by `gtk4/demo.py`, which does three useful things:

- loads a chosen CSS variant,
- builds a tiny GTK application,
- shows representative UI pieces like buttons, links, and paused chips.

That means this guide is not hypothetical. It has a runnable proof point.

The demo also reinforces core repo principles:

- links are visibly underlined,
- focus rings stay visible,
- paused state uses a hatch cue,
- CVD variants are swapped deliberately by file.

## Step 4. Why this guide matters

Desktop theming can easily drift into aesthetics-first customization. This
guide resists that by keeping the platform integration tied to accessibility
rules:

- redundant cues,
- visible focus,
- state labels and icons,
- monochrome survivability.

So even though it is a platform guide, it still carries the repo's central
ethic: do not let color carry meaning alone.

## Step 5. What its limits are

The GTK guide is intentionally focused.

It does not attempt to define:

- the full semantics of every widget state,
- automated desktop validation,
- cross-toolkit abstractions for Qt, Electron, or web frameworks,
- the entire brand system.

Instead it shows how one concrete desktop stack can consume the palette and
variant outputs responsibly.

## Step 6. Relationship to current palette work

Right now the GTK lane is tied to the production-generated brand CSS files:

- `gtk4/brand_default.css`
- `gtk4/brand_protan.css`
- `gtk4/brand_deutan.css`
- `gtk4/brand_tritan.css`
- `gtk4/brand_mono.css`

So, like the OKLCH generator, this guide reflects the production lane more
directly than the newer experimental mauve/burgundy and red/mahogany packs.

That does not make it outdated. It just means the desktop integration debt is
still ahead of us if we want experimental palettes to become first-class GTK
variants too.

## Step 7. Why it belongs in the foundations map

This guide is important because it proves OpenPerception is not only:

- research notes,
- token JSON,
- validators,
- or browser examples.

It also has a real desktop application path.

That widens the project from a color-research repo into a delivery-capable UI
system.

## Bottom line

`docs/gnome-gtk4-guide.md` is the repo's GTK/libadwaita translation layer. It
shows how the accessibility-aware token system becomes an application-scoped
desktop theme with redundant cues and deliberate CVD variants, while also
revealing that the current GTK integration still centers the production palette
lane.
