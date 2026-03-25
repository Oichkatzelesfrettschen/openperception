# Neurodivergence Primary Source Notes

This file captures the paper-by-paper extraction behind the repaired
neurodivergence source cache.

## Source Set

- [Neurodivergence source cache](/home/eirikr/Github/openperception/docs/external_sources/neurodivergence_source_cache.md)
- [Paper corpus registry](/home/eirikr/Github/openperception/docs/external_sources/paper_corpus_registry.md)
- [Neurodivergence accessibility research report](/home/eirikr/Github/openperception/research/neurodivergence/NEURODIVERGENCE_COGNITIVE_ACCESSIBILITY_RESEARCH.md)

## 1. Yoo Et Al. (2024)

Citation:
`Development of an innovative approach using portable eye tracking to assist ADHD screening: a machine learning study.`

Local artifacts:

- `papers/downloads/adhd/2024_Eye_Tracking_ADHD_Screening.pdf`
- `papers/downloads/adhd/2024_Eye_Tracking_ADHD_Screening.txt`

Granular findings:

- The study compares 56 children with ADHD and 79 typically developing
  children.
- It derives 33 eye-tracking features across five tasks covering selective
  attention, working memory, and response inhibition.
- Participants with ADHD showed increased saccade latency and degree, along
  with shorter fixation time in the eye-tracking tasks.
- The best eye-tracking-only ensemble reached 76.3% classification accuracy.
- The paper reports no significant AUC difference between the eye-tracking
  model and conventional ATA or Stroop-based screening comparisons.
- The authors still frame the method as a promising screening aid rather than a
  standalone diagnostic replacement.

Project distillation:

- ADHD-relevant interface burden is not only verbal or subjective; gaze
  stability, forced reorientation, and inhibitory control are measurable visual
  burdens.
- Repo guidance should treat rapid gaze-shift demands and unstable fixation
  anchors as cognitive-accessibility concerns, not merely aesthetics.
- We should avoid overclaiming any single behavioral or eye-tracking measure as
  diagnostic proof.

## 2. Raymaker Et Al. (2019)

Citation:
`Development of the AASPIRE Web Accessibility Guidelines for Autistic Web Users.`

Local artifacts:

- `papers/downloads/autism/AASPIRE_Autism_Web_Accessibility_Guidelines_2019.pdf`
- `papers/downloads/autism/AASPIRE_Autism_Web_Accessibility_Guidelines_2019.txt`

Granular findings:

- The guidelines were developed through a community-based participatory
  research process with autistic partners involved throughout.
- The paper organizes web accessibility into three dimensions: physical,
  intellectual, and social accessibility.
- The evaluation involved 170 autistic end users.
- Reported outcomes were strong: 97% easy to use, 95% easy to understand, 97%
  important, 96% useful, and 92% willing to recommend it to a friend.
- The paper explicitly warns that accessibility needs can conflict across
  populations; for example, high-contrast palettes helpful for low vision may
  be painful or unreadable for some autistic users with hypersensitive vision.
- The authors describe multiple selectable themes as a practical resolution to
  those conflicting needs.

Project distillation:

- Autism guidance in the repo should keep the three-axis framing: physical,
  intellectual, and social accessibility.
- Configurability matters as much as any single default palette or layout
  decision.
- Social-context clarity and plain-language structure belong in accessibility
  guidance alongside sensory controls.

## 3. Muller-Axt Et Al. (2024)

Citation:
`Dysfunction of the magnocellular subdivision of the visual thalamus in developmental dyslexia.`

Local artifacts:

- `papers/downloads/dyslexia/Mueller-Axt_2024_Magnocellular_LGN_Dyslexia.pdf`
- `papers/downloads/dyslexia/Mueller-Axt_2024_Magnocellular_LGN_Dyslexia.txt`

Granular findings:

- The study uses 7 Tesla MRI to examine 26 young adults with dyslexia and 28
  matched controls.
- It reports altered function and microstructure in the magnocellular LGN
  rather than the parvocellular LGN.
- The paper links those magnocellular alterations with rapid automatized naming
  of letters and numbers (RANln), especially in male participants with
  dyslexia.
- The authors describe the result as the first in-vivo evidence that
  magnocellular LGN alterations are a hallmark of developmental dyslexia.
- The paper treats dyslexia as involving broader visual-sensory timing and
  thalamic processing, not only orthographic preference or font choice.

Project distillation:

- Dyslexia accommodations in the repo should not collapse into "use a dyslexia
  font" as if that fully addresses the condition.
- Time pressure, rapid symbol naming, and visual sequencing load are part of
  the relevant burden surface.
- Typography guidance should remain important, but repo claims should not imply
  that typography alone explains dyslexia accessibility.
