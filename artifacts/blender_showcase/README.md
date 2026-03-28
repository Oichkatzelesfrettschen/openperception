# Blender Showcase Artifacts

This directory holds first-class Blender showcase artifacts for the repo's
living accessibility concept lane.

Why this is tracked:

- the showcase is a distilled visual artifact of repo findings, not disposable
  scratch output
- the renders make the repo's operational accessibility model legible to humans
- the `.blend` file captures layout, lighting, and scene composition choices
  that belong with the repo's design-system research
- the concept is documented in `CONCEPT.md` so the artifact does not drift into
  slogans or detached mood-board language
- the current concept uses real science inputs from sibling repos instead of toy
  placeholder geometry

Current source-of-truth files:

- `CONCEPT.md`
- `../../docs/generated/repo_stats.json`
- `../../docs/generated/repo_stats.md`
- `animated/README.md`
- `generated/physics_views_manifest.json`
- `animated/animated_views_manifest.json`
- `animated/gw_chirp_accessible.gif`
- `animated/neutrino_cooling_guided.gif`
- `animated/blackhole_lensing_depth_safe.gif`
- `openperception_palette_showcase_spec.json`
- `openperception_palette_showcase_render.png`
- `openperception_palette_showcase_scene.blend`

Historical files:

- `openperception_palette_showcase_render_v1.png`
- `openperception_palette_showcase_render_v2.png`
- `openperception_palette_showcase_scene_v1.blend`
- `openperception_palette_showcase_spec_v1.json`

The current spec and current `.png` / `.blend` outputs reflect the latest token
findings, generated repo stats, real source views from `compact-common` and
`Blackhole`, and the repo's stereoblindness-informed depth guidance:

- static monocular cues first
- stereo as enrichment, not requirement
- motion as reinforcement, not sole recovery path

The scene is also expected to stay legible with low caption dependence:

- the back rail should stay quiet and non-competitive
- the left foreground view should read as a color-safe GW chirp
- the center foreground view should read as a symbol-guided neutrino explainer
- the right foreground view should read as a depth-safe black-hole lensing view

The animated lane is expected to stay just as concrete:

- `animated/gw_chirp_accessible.gif` should read as real detector strain turned
  into a clearer chirp-focused accessible view
- `animated/neutrino_cooling_guided.gif` should read as real captured neutrino
  explainer frames turned into a more guided process view
- `animated/blackhole_lensing_depth_safe.gif` should read as real `Blackhole`
  desktop orbit frames turned into a depth-safe lensing view with contour and
  anchor reinforcement

For the current black-hole still, the honest source basis is the sibling
`Blackhole` desktop/OpenGL compare capture at
`/home/eirikr/Github/Blackhole/logs/compare/compare_8_compute.png`. That
source is currently a better visual basis for the depth-safe lane than the
repaired Blender/CUDA bridge stills.

The current harsher readability pass removes the bottom plaque and header so
the three panels have to teach themselves without explanatory copy.

Generated repo stats are allowed to drive the cadence of those forms so the
artifact remains a living concept instead of a frozen illustration.

The current canonical render path prefers Octane inside Octane Blender, with
Eevee Next or Cycles used only as honest fallbacks when the live session does
not expose Octane.

The Octane path uses Octane-native area lights and materials so the canonical
render stays truthful instead of slipping into black or washed-out passes.

Regeneration path:

1. `make octane-probe`
2. `make showcase-render`

`make showcase-render` is the preferred path because it refreshes the generated
physics-view panels from sibling-repo renders, rebuilds repo stats, emits the
canonical spec, regenerates the tracked animated GIFs, and then renders the
tracked `.png` and `.blend` through the clean Octane-first automation path.

The `Blackhole` bridge is still part of the upstream repair lane, but its role
here is currently diagnostic rather than canonical-beauty. We only promote a
bridge artifact into this showcase once it is both technically sound and
visually honest as the strongest sibling-repo source.

This lane is tracked with Git LFS for `.png` and `.blend` files.

Blender backup files such as `.blend1` are not tracked as artifacts.
