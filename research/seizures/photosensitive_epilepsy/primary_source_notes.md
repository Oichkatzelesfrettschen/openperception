# Photosensitive Epilepsy Primary Source Notes

This file captures the paper-by-paper extraction behind the repaired
photosensitive epilepsy source cache.

## Source Set

- [Seizure source cache](/home/eirikr/Github/openperception/docs/external_sources/seizure_source_cache.md)
- [Paper corpus registry](/home/eirikr/Github/openperception/docs/external_sources/paper_corpus_registry.md)
- [Comprehensive seizure research report](/home/eirikr/Github/openperception/research/seizures/photosensitive_epilepsy/COMPREHENSIVE_RESEARCH.md)

## 1. Fisher Et Al. (2022)

Citation:
`Visually sensitive seizures: An updated review by the Epilepsy Foundation.`

Local artifacts:

- `papers/downloads/seizures/Fisher_2022_Visually_Sensitive_Seizures.pdf`
- `papers/downloads/seizures/Fisher_2022_Visually_Sensitive_Seizures.txt`

Granular findings:

- The review states that light flashes, patterns, or color changes can provoke
  seizures in up to 1 in 4000 persons.
- It distinguishes the photoparoxysmal response (PPR) on EEG from clinically
  photosensitive seizures.
- The paper highlights risk for flashes in the 3-60 Hz range, especially
  15-20 Hz, when bright enough and large enough in the visual field.
- It flags red flashes and oscillating stripes as especially concerning visual
  content.
- The review notes that virtual reality and three-dimensional imagery are not
  inherently dangerous, but become risky when they include provocative flash or
  pattern content.
- Prevention guidance includes avoiding provocative stimuli, covering one eye,
  reducing contrast, wearing dark glasses, and sitting at least two meters from
  screens.

Project distillation:

- The repo's seizure gate should continue treating flash frequency, saturated
  red, and patterned oscillation as separate but interacting hazard channels.
- We should not assume immersive or stereoscopic media are safe just because the
  format is novel; the content characteristics still govern risk.
- User guidance should include practical mitigation advice when provocative
  content cannot be fully avoided.
