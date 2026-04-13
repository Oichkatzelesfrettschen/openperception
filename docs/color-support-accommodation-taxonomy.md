# Color Support Accommodation Taxonomy

This note separates several color-support modes that are often collapsed into a
single bucket. In this repo, that separation matters because simulation,
daltonization, interactive recognition aids, and reconstructive color models do
different jobs, answer different user needs, and carry different evidence
expectations.

## Why Separate The Modes

Color support work gets muddier than it needs to when every color transform is
described as "helping colorblind users" in the same way. That phrase can mean:

- previewing what information collapses under a simulated deficiency
- altering an image so some differences survive more reliably
- helping a user learn or recover color names in a task
- exploring how color dimensionality might be restored or extended in future
  systems

Those are related, but they are not interchangeable. This repo treats them as
distinct accommodation modes so that evaluation claims stay honest and design
guidance stays actionable.

## Mode 1: Simulation And Preview

Simulation estimates how a scene, image, or interface may look under a specific
color-vision deficiency model. In this repo, simulation is primarily a
validation tool, not itself an accommodation.

Use simulation when you need to:

- check whether categories collapse under protan, deutan, or tritan models
- verify that contrast, labels, icons, and patterns still carry the meaning
- compare palette candidates before shipping a design

Do not treat simulation as proof that an interface is accessible on its own.
Simulation helps us find where information disappears. It does not supply the
missing cues by itself.

Canonical local sources:

- `papers/downloads/algorithms/Brettel_1997_Dichromat_Simulation.pdf`
- `papers/downloads/algorithms/Vienot_1999_Digital_Colourmaps.pdf`
- `papers/downloads/algorithms/Machado_2009_CVD_Simulation.pdf`
- `papers/downloads/algorithms/Stockman_2019_Cone_Fundamentals_CIE_Standards.pdf`
- `papers/downloads/algorithms/Vienot_2015_Cone_Fundamentals_Past_Present_Future.pdf`

Related repo docs:

- [CVD simulator guide](/home/eirikr/Github/openperception/docs/simulator-guide.md)
- [Algorithm source cache](/home/eirikr/Github/openperception/docs/external_sources/algorithm_source_cache.md)
- [Algorithm comparison guide](/home/eirikr/Github/openperception/research/colorblindness/algorithms/ALGORITHM_COMPARISON.md)

## Mode 2: Static Recoloring And Daltonization

Daltonization modifies an image or interface so that differences that would
collapse for some CVD viewers are redistributed into distinctions they may
perceive more reliably. In this repo, daltonization is an intervention mode
with tradeoffs, not a universal fix.

Use daltonization when you need to:

- remediate a static artifact that cannot be fully redesigned
- preserve more distinction for a targeted viewing condition
- explore whether a post hoc transform helps a concrete task

Be careful about overclaiming. Daltonization can improve distinguishability
without preserving natural appearance, semantic meaning, or exact color naming
equally well across tasks.

Compendium sources (not locally cached as PDFs):

- Section 2 of `papers/colorblindness_algorithms_compendium.md` (Fidaner, Lin,
  Ozguven 2005; Kuhn, Oliveira, Fernandes 2008; image recoloring surveys 2021)

Related repo docs:

- [Daltonization guide](/home/eirikr/Github/openperception/docs/daltonization-guide.md)
- [Colorblind-friendly design guide](/home/eirikr/Github/openperception/docs/colorblind-friendly-design-guide.md)
- [CVD research report](/home/eirikr/Github/openperception/research/colorblindness/CVD_RESEARCH_REPORT.md)

## Mode 3: Interactive Recognition Aids

Recognition aids help a user recover task-relevant color identity, not just
tell two patches apart in isolation. In this repo, that is a distinct support
mode because many real tasks require color naming, not only color separation.

Use recognition aids when you need to:

- help users identify or name colors in context
- support workflows like sorting, labeling, interpretation, or object lookup
- add a learnable cue through interaction, motion, or temporal variation

Zhu et al. (2024) is the strongest local example in this repo. Its AR system
uses temporal color shifts as an extra cue that users can learn, which is a
different goal from simply recoloring the whole scene.

Canonical local source:

- `papers/downloads/color_vision/Zhu_2024_Computational_Trichromacy_Reconstruction_AR.pdf`

Related repo docs:

- [Color vision source cache](/home/eirikr/Github/openperception/docs/external_sources/color_vision_source_cache.md)
- [Color vision primary source notes](/home/eirikr/Github/openperception/research/colorblindness/primary_source_notes.md)
- [CVD research report](/home/eirikr/Github/openperception/research/colorblindness/CVD_RESEARCH_REPORT.md)

## Mode 4: Restorative And Speculative Reconstruction

Some work is better understood as reconstructive, restorative, or conceptual
modeling rather than as a ready-to-ship accessibility accommodation. These
systems can still matter to the repo, but they should be described with the
right confidence level.

Use this category when you need to:

- discuss future-facing restoration or enhancement scenarios
- describe modeling work about how color dimensionality may emerge or change
- distinguish exploratory research from production accessibility guidance

Kotani and Ng (2025) belongs here. It broadens the conceptual frame around
color dimensionality and emergence, but it is not a direct UI accommodation
recipe for present-day product work.

Canonical local source:

- `papers/downloads/color_vision/Kotani_2025_Color_Vision_Emergence_Framework.pdf`

Related repo docs:

- [Color vision source cache](/home/eirikr/Github/openperception/docs/external_sources/color_vision_source_cache.md)
- [Color vision primary source notes](/home/eirikr/Github/openperception/research/colorblindness/primary_source_notes.md)
- [CVD research report](/home/eirikr/Github/openperception/research/colorblindness/CVD_RESEARCH_REPORT.md)

## Choosing The Right Mode

Pick the mode by the user goal, not by habit.

| If you need to... | Default mode |
|-------------------|--------------|
| validate whether encoded meaning survives CVD | simulation and preview |
| repair a static artifact that already exists | static recoloring or daltonization |
| help users name or identify colors in context | interactive recognition aid |
| discuss future restoration or dimensionality changes | reconstructive or speculative modeling |

Repo default:

- start with redundant cues, contrast, labels, icons, and patterns
- use simulation to validate those cues
- use daltonization only when a concrete intervention is actually needed
- use recognition aids when the task depends on color naming or contextual
  identification
- describe reconstructive work as exploratory unless the evidence is clearly
  product-ready

## Limits And Preference

No single color-support mode should be treated as a universal CVD solution.
Diagnosis category alone does not determine one correct accommodation, and
different tasks can favor different strategies for the same user.

That means repo claims should stay narrow:

- simulation claims are about predicted appearance under a model
- daltonization claims are about post hoc distinguishability tradeoffs
- recognition-aid claims are about task-level identification or naming support
- reconstructive-model claims are about conceptual or future-facing capability

## Local Source Trails

Use these local entry points when extending the lane:

- [Algorithm source cache](/home/eirikr/Github/openperception/docs/external_sources/algorithm_source_cache.md)
- [Color vision source cache](/home/eirikr/Github/openperception/docs/external_sources/color_vision_source_cache.md)
- [Algorithm comparison guide](/home/eirikr/Github/openperception/research/colorblindness/algorithms/ALGORITHM_COMPARISON.md)
- [Color vision primary source notes](/home/eirikr/Github/openperception/research/colorblindness/primary_source_notes.md)
- [CVD research report](/home/eirikr/Github/openperception/research/colorblindness/CVD_RESEARCH_REPORT.md)
