# Animated Showcase Artifacts

This directory holds the tracked animated accessibility views for the Blender
showcase.

Current tracked artifacts:

- `gw_chirp_accessible.gif`
- `neutrino_cooling_guided.gif`
- `blackhole_lensing_depth_safe.gif`
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

- `blackhole_lensing_depth_safe.gif`
  - basis: real sibling `Blackhole` desktop record frames in
    `/home/eirikr/Github/Blackhole/.cache/showcase_motion_compare_orbit_near/`
    generated with the `compare-orbit-near` profile
  - transformation: the orbit view becomes more depth-safe through stronger
    contour arcs, anchor boxes, and clearer static relief cues

Regeneration path:

```bash
make showcase-render
```

That path regenerates these GIFs through `tools/showcase_physics_views.py` and
updates `animated_views_manifest.json` alongside the still showcase artifacts.
