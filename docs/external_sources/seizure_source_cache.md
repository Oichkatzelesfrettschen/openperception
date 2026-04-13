# Seizure Source Cache

This index documents the repaired primary-source cache used for seizure-safety
research in OpenPerception.

## Scope

These artifacts back the repo's photosensitive epilepsy and seizure-trigger
documentation.

Machine-readable registry:

- [CANONICAL_REGISTRY.json](/home/eirikr/Github/openperception/papers/downloads/CANONICAL_REGISTRY.json)

## Cached Sources

| ID | Citation | Local Artifacts | Access Mode | Notes |
|----|----------|-----------------|-------------|-------|
| `fisher_2022` | Fisher et al. *Epilepsia* (2022). | `papers/downloads/seizures/Fisher_2022_Visually_Sensitive_Seizures.pdf`, `papers/downloads/seizures/Fisher_2022_Visually_Sensitive_Seizures.txt` | PDF and text | Open repository PDF cached from the University of Essex record. |

## External Standards References (Not Locally Cached)

These normative sources are repeatedly cited in `specs/` but cannot be cached
locally due to paywalls or terms of use.  They are indexed here so that
contributors know where to find them and when to check for updates.

| ID | Source | URL | Notes |
|----|--------|-----|-------|
| `itu_r_bt1702_3` | ITU-R BT.1702-3 Guidance for the reduction of photosensitive epileptic seizures caused by television (2023 rev.) | https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.1702-3-202311-I!!PDF-E.pdf | Primary normative source for flash-rate and pattern limits used in GATE-001 SEIZURE validator. Free download from ITU website. Cited in `specs/EVIDENCE_MATRIX.md` and `specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md`. |
| `harding_test` | Harding Flash and Pattern Analyser (commercial compliance tool) | https://hardingtest.com/ | Reference implementation for broadcast photosensitivity compliance testing. Cited in `specs/VALIDATORS_FRAMEWORK.md` as the reference tool for GATE-001. Not open-source; check site for licensing. |

## Related Docs

- [Seizure primary source notes](/home/eirikr/Github/openperception/research/seizures/photosensitive_epilepsy/primary_source_notes.md)
- [Comprehensive seizure research report](/home/eirikr/Github/openperception/research/seizures/photosensitive_epilepsy/COMPREHENSIVE_RESEARCH.md)
- [Paper corpus registry](/home/eirikr/Github/openperception/docs/external_sources/paper_corpus_registry.md)
