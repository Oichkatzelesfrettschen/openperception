# Red Theme From Foundations

Date: 2026-03-22

## Goal

This note re-derives the red-theme triage from repo-local foundations instead
of from aesthetic preference alone.

Primary source files in this repo:

- `docs/colorblind-friendly-design-guide.md`
- `docs/contrast-guide.md`
- `docs/oklch-guide.md`
- `tokens/color-tokens.json`
- `tools/contrast_check.py`
- `tools/separation_check.py`
- `algorithms/DaltonLens-Python/daltonlens/simulate.py`
- `docs/red-theme-triage.md`

## Step 1. Start from the repo's first principle

The repo already commits to an accessibility-first rule:

- color must not carry meaning alone,
- text and controls must meet contrast targets,
- CVD variants must remain distinguishable,
- monochrome fallback must still work.

That means any red-theme proposal must be judged as a semantic system, not only
as a wallpaper or mood board.

## Step 2. Separate two different problems

There are two different design problems:

1. atmosphere or skin:
   - wallpaper
   - panel chrome
   - document surfaces
   - brand mood
2. semantic interaction system:
   - primary CTA
   - links
   - warnings
   - state encoding
   - chart series

An earlier raw scratch-note stage mixed these together. The first real
derivation step is to split them.

## Step 3. Use the repo's validation machinery

This repo already provides two key validators:

- contrast ratio checks via `tools/contrast_check.py`
- perceptual separation checks via `tools/separation_check.py`

On top of that, we have full CVD simulation through the vendored
`DaltonLens-Python` package.

Therefore a red theme is acceptable only if:

- its text/surface pairings pass WCAG,
- its strong tokens stay separated enough for the intended use,
- it does not collapse warning/brand/interactive semantics into one hue family.

## Step 4. Test the red family as semantics

Pure red is a bad foundation for the whole semantic stack because it tries to
do too many jobs at once:

- urgency,
- danger,
- prestige,
- warmth,
- identity,
- selection.

That creates a semantic collision even before CVD enters the picture.

A system where red is both "the brand" and "the warning" is structurally weak.

## Step 5. Test the red family as atmosphere

The local red-theme corpus becomes much stronger once the target changes from
"all semantics" to "theme skin."

Mahogany, burgundy, oxblood, maroon, brass, cream, and slate work well for:

- depth,
- warmth,
- authority,
- classic desktop mood,
- institutional or BSD-adjacent identity.

In that role, the red family does not have to carry every interactive meaning.

## Step 6. Derive the correct role for red in this repo

Given Steps 1-5, the correct placement is:

- primary interaction should remain on a more stable non-red family,
- red should enter as tertiary emphasis or atmosphere,
- warning red should stay explicit and narrow,
- charts and states still need shape, label, dash, and hatch redundancy.

This is exactly why the accessible experimental pack ended up as:

- indigo for structure,
- mauve for accent,
- burgundy for tertiary/high-gravity emphasis.

That structure lets the project keep the emotional register of red without
making the whole system brittle.

## Step 7. Re-derive the red-theme outcome

From the repo's own premises, the triage follows:

### Greenlight

- red/mahogany document skins
- wallpaper-driven classical desktop themes
- burgundy tertiary emphasis
- brass-and-cream accent systems paired with dark wood tones

### Yellowlight

- maroon-heavy surfaces for dashboards or docs
- red-forward chart palettes, but only with strong non-color redundancy

### Redlight

- pure red as the only primary CTA family
- red as both brand and warning lane
- red/black-only default UI semantics

## Step 8. What the experimental red pack means

The repo now includes a separate red/mahogany pack:

- `tokens/experimental-red-mahogany.json`
- `tokens/experimental-red-mahogany.css`

This is the correct implementation form for the red theme:

- separate pack,
- atmosphere-first,
- not a silent replacement for the default semantic stack.

Its structure is:

- mahogany = primary shell/chrome family
- brass = accent family
- burgundy = tertiary emphasis family
- cream = reading surface
- slate/brown-gray = text and neutral structure

## Step 9. The final derivation in one sentence

From repo-local accessibility and validation foundations, the red theme is
valid as a separate skin or tertiary-emphasis lane, but not as the default
meaning-first interaction system.
