# Color Vision Primary Source Notes

This file captures paper-by-paper extraction for the broader color-vision
source cache that now lives in `papers/downloads/color_vision/`.

## Source Set

- [Color vision source cache](/home/eirikr/Github/openperception/docs/external_sources/color_vision_source_cache.md)
- [Paper corpus registry](/home/eirikr/Github/openperception/docs/external_sources/paper_corpus_registry.md)
- [CVD research report](/home/eirikr/Github/openperception/research/colorblindness/CVD_RESEARCH_REPORT.md)

## 1. Zhu Et Al. (2024)

Citation:
`Computational Trichromacy Reconstruction: Empowering the Color-Vision Deficient to Recognize Colors Using Augmented Reality.`

Local artifact:

- `papers/downloads/color_vision/Zhu_2024_Computational_Trichromacy_Reconstruction_AR.pdf`

Granular findings:

- The paper distinguishes color discrimination from color recognition, arguing
  that many assistive filters help users tell colors apart without helping them
  reliably name those colors in real tasks.
- Its core idea is to augment a dichromat's native 2D color percept with an
  additional learned dimension induced by temporal color shifts during user
  interaction.
- The implementation uses smartphone AR with swipe-controlled rotational color
  shifts about the gray axis in RGB space, so the interaction is practical and
  computationally cheap enough for real-time use.
- The psychophysics section reports 16 CVD participants and almost 100 total
  study hours to show that the induced shifts have discriminative power across
  CVD types.
- The longitudinal study reports eight CVD participants over nine days and
  frames the main outcome as learnable color-name recovery rather than just
  one-shot discrimination.
- Real-world evaluations use Lego sorting and interpretation of artistic works,
  both chosen because they require color naming rather than isolated patch
  discrimination.

Project distillation:

- Repo guidance should separate "can tell apart" from "can correctly name" when
  evaluating assistive color transforms.
- Interactive or temporal accommodations can be useful when they create a
  stable, learnable cue rather than merely shifting colors globally.
- AR-style assistive systems belong in the repo's accommodation landscape as a
  distinct class from static daltonization and simulation.

## 2. Kotani And Ng (2025)

Citation:
`A Computational Framework for Modeling Emergence of Color Vision in the Human Brain.`

Local artifact:

- `papers/downloads/color_vision/Kotani_2025_Color_Vision_Emergence_Framework.pdf`

Granular findings:

- The paper models color vision as something the cortex must infer from optic
  nerve signals rather than as a representation whose dimensionality is known in
  advance.
- It combines a retina/optic-nerve simulation with a self-supervised cortical
  learning hypothesis driven by natural eye-motion fluctuations.
- The framework explicitly treats neural color as an N-dimensional internal
  representation and claims that the correct dimensionality emerges naturally
  from the sensory stream.
- Its simulation reports emergence of 1D, 2D, 3D, and 4D color vision when the
  retina contains one through four photoreceptor classes.
- The paper ties dimensionality boosting to gene-therapy literature by
  simulating the shift from dichromacy to trichromacy seen in squirrel-monkey
  intervention work.
- This is a modeling paper, not an accessibility intervention paper, but it
  broadens the repo's conceptual frame for what "normal" color vision means.

Project distillation:

- Repo language should avoid treating trichromacy as the only natural endpoint
  of color perception when discussing future therapies or adaptive systems.
- Accommodation docs can stay grounded in today's user needs while still noting
  that color dimensionality itself is biologically and computationally
  modelable, not a fixed assumption.
- The paper supports a more careful distinction between simulation for current
  CVD users and speculative enhancement or restoration scenarios.
