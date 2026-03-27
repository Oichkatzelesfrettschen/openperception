# Blender Showcase Requirements

This file documents the regeneration requirements for the tracked Blender
showcase artifacts.

## Required For Spec Regeneration

- Python 3.10+ for repo-owned tooling

Generate the canonical spec:

```bash
python3 tools/repo_stats.py \
  --output-json docs/generated/repo_stats.json \
  --output-md docs/generated/repo_stats.md
python3 tools/palette_showcase_spec.py \
  --output artifacts/blender_showcase/openperception_palette_showcase_spec.json
```

## Required For Scene Regeneration

- Blender

Preferred current render path:

- Octane Blender with Octane available

Fallbacks:

- Eevee Next
- Cycles

## Optional For Live Agent Control

- Blender MCP configured and running against the live Blender session

## Regeneration

Preferred binary selection:

```bash
SHOWCASE_BLENDER_BIN=${SHOWCASE_BLENDER_BIN:-OctaneBlender}
```

Octane-first regeneration:

```bash
"${SHOWCASE_BLENDER_BIN}" --background --factory-startup \
  --python tools/blender_palette_showcase_scene.py -- \
  --spec artifacts/blender_showcase/openperception_palette_showcase_spec.json \
  --output artifacts/blender_showcase/openperception_palette_showcase_render.png \
  --blend-output artifacts/blender_showcase/openperception_palette_showcase_scene.blend
```

Generic Blender fallback:

```bash
blender --background --factory-startup \
  --python tools/blender_palette_showcase_scene.py -- \
  --spec artifacts/blender_showcase/openperception_palette_showcase_spec.json \
  --output artifacts/blender_showcase/openperception_palette_showcase_render.png \
  --blend-output artifacts/blender_showcase/openperception_palette_showcase_scene.blend
```

## Notes

- `.png` and `.blend` artifacts in this lane are tracked with Git LFS
- Blender backup files such as `.blend1` are intentionally not tracked
- live MCP control is optional; deterministic script-driven regeneration is the
  baseline path
- the showcase concept is documented in `artifacts/blender_showcase/CONCEPT.md`
- the generated spec now embeds repo stats, so regenerate `docs/generated/`
  before exporting the canonical spec when counts may have changed
- some hosts ship a broken `blender` binary while `OctaneBlender` works, so the
  binary name should be treated as a host-level configuration choice
