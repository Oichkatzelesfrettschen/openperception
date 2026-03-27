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

Current source-of-truth files:

- `openperception_palette_showcase_spec.json`
- `openperception_palette_showcase_render.png`
- `openperception_palette_showcase_scene.blend`

Historical files:

- `openperception_palette_showcase_render_v1.png`
- `openperception_palette_showcase_render_v2.png`
- `openperception_palette_showcase_scene_v1.blend`
- `openperception_palette_showcase_spec_v1.json`

The current spec and current `.png` / `.blend` outputs reflect the latest token
findings, generated repo stats, and the repo's stereoblindness-informed depth
guidance:

- static monocular cues first
- stereo as enrichment, not requirement
- motion as reinforcement, not sole recovery path

The current canonical render path prefers Octane inside Octane Blender, with
Eevee Next or Cycles used only as honest fallbacks when the live session does
not expose Octane.

The Octane path uses Octane-native area lights and materials so the canonical
render stays truthful instead of slipping into black or washed-out passes.

Regeneration path:

1. `python3 tools/palette_showcase_spec.py --output artifacts/blender_showcase/openperception_palette_showcase_spec.json`
2. run `tools/blender_palette_showcase_scene.py` inside Blender with the same
   spec path and output paths in this directory

This lane is tracked with Git LFS for `.png` and `.blend` files.

Blender backup files such as `.blend1` are not tracked as artifacts.
