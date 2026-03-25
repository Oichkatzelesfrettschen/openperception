# Red Theme Axiomatic Derivation

Date: 2026-03-25

This note decomposes the red-theme lane and re-derives it from repo axioms
instead of from "make it feel red" intuition.

## Repo Axioms

The relevant local axioms are stable now:

- color must not carry meaning alone
- semantic roles should not collapse into one hue family
- simulation validates loss, but is not itself the accommodation
- static recoloring is different from recognition support
- warm atmosphere is allowed, but not at the cost of semantic clarity

Those constraints come from the repo's accessibility-first token work, the
contrast and CVD gates, and the newer color-support taxonomy.

## Decomposition

The old red lane was doing too many jobs at once. The useful decomposition is:

1. structure
2. interpretive accent
3. high-gravity emphasis
4. warning/error
5. atmosphere and surface

Treating those as separate jobs is the key move. Once they are separated, the
lane stops fighting itself.

## Re-Derived Role Map

From those axioms, the warm lane resolves to:

- structure: grounded mahogany/umber neutrals, not bright red
- interpretive accent: brass, because it stays warm without colliding with
  warning semantics
- high-gravity emphasis: burgundy, used deliberately as tertiary emphasis
- warning/error: explicit narrow warning red, still text-labeled and redundant
- atmosphere: cream, parchment, wood, and warm neutral surfaces

This keeps the lane recognizably red-adjacent without making "red" do every
semantic job.

## Why This Is Better

It aligns with three newer repo findings.

First, the color-support taxonomy now distinguishes simulation, static
recoloring, recognition aid, and reconstructive work. That means a theme lane
should not pretend hue alone will recover meaning.

Second, the refined CVD gate makes the semantic constraint concrete: primary
and accent need perceptual distance headroom. A single red-family stack tends
to compress that space.

Third, the repo's newer depth and redundancy work keeps converging on the same
rule: atmosphere can enrich a system, but essential meaning needs a more stable
backbone.

## Token Consequences

The updated `experimental-red-mahogany.json` now follows this map:

- `mahogany` is a grounded structure family
- `brass` is the accent family
- `burgundy` is the tertiary family
- `cream` is the reading surface
- `gray` holds text and neutral structure

The authored variants also now include:

- `default`
- `protan`
- `deutan`
- `tritan`
- `mono`

That makes the lane consistent with the repo's other authored accessibility
packs instead of leaving it as a one-off mood board.

## One-Sentence Distillation

The refined red lane is not "red as primary semantics." It is a warm,
structure-first lane where mahogany carries weight, brass carries
interpretation, and burgundy carries gravity.
