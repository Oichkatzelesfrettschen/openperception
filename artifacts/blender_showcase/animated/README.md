# Animated Showcase Artifacts

This directory holds the tracked animated accessibility views for the Blender
showcase.

Current tracked artifacts:

- `gw_chirp_accessible.gif`
- `neutrino_cooling_guided.gif`
- `animated_views_manifest.json`

What they are:

- `gw_chirp_accessible.gif`
  - basis: real `compact-common` strain data in
    `/home/eirikr/Github/compact-common/blender/data/gw170817_processed.json`
    plus the sibling-repo chirp render
  - transformation: weak detector-strain context becomes a more legible chirp
    view using stronger contrast, markers, and arrival emphasis

- `neutrino_cooling_guided.gif`
  - basis: real captured frames from the sibling-repo contact sheet at
    `/home/eirikr/Github/compact-common/dist/releases/neutrino-processes-explainer-contact-sheet-latest.png`
  - transformation: the explainer view becomes more guided through explicit
    arrows, marked process points, and a clearer progress cue

What is not tracked yet:

- there is no `blackhole_lensing` animation here yet because no real sibling-repo
  motion source is currently registered for that case
- the black-hole lane remains a still-only accessibility view until that changes

Regeneration path:

```bash
make showcase-render
```

That path regenerates these GIFs through `tools/showcase_physics_views.py` and
updates `animated_views_manifest.json` alongside the still showcase artifacts.
