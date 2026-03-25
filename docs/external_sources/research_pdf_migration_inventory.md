# Research PDF Migration Inventory

Updated: 2026-03-25

This note tracks the remaining PDFs that still live under `research/` instead of
the canonical `papers/downloads/` cache.

Direct `research/...pdf` references are now treated as provenance-only
references. Outside this inventory and the paper-corpus provenance docs, tracked
Markdown and BibTeX should point to canonical cache artifacts or cite the
source by title/DOI until the artifact is migrated.

## Current Totals

- Remaining research-local PDFs: 11
- Topic buckets:
  `cognitive_load` 2, `colorblindness` 4, `neurodivergence` 2,
  `visual_impairments` 3

## Decision Buckets

| Path | Bucket | Rationale |
|------|--------|-----------|
| `research/colorblindness/Ishihara_38_Plates_Test.pdf` | Keep local | Test asset rather than a canonical literature-cache paper. |
| `research/colorblindness/algorithms/Stockman_2019_Cone_Fundamentals_CIE_Standards.pdf` | Migrate with provenance | Algorithm-support reference already surfaced in discovery docs. |
| `research/colorblindness/algorithms/Vienot_2015_Cone_Fundamentals_Past_Present_Future.pdf` | Migrate with provenance | Algorithm-support reference already surfaced in discovery docs. |
| `research/neurodivergence/autism/Manning_2024_Visual_Processing_Autism_Dyslexia.pdf` | Migrate with provenance | Cross-syndrome paper already surfaced in discovery docs. |
| `research/cognitive_load/2024_Cognitive_Load_Measurement_Methods.pdf` | Provenance needed before migration | Useful topic paper, but no canonical cache entry or source note yet. |
| `research/cognitive_load/2024_Minimalism_vs_Complexity_UX_Cognitive_Load.pdf` | Provenance needed before migration | Useful topic paper, but no canonical cache entry or source note yet. |
| `research/colorblindness/blue_cone_monochromacy/Cideciyan_2024_BCM_Retinal_Structure_Clinical_Endpoints.pdf` | Provenance needed before migration | Topic-relevant BCM paper without canonical cache metadata yet. |
| `research/neurodivergence/autism/2024_Visual_Mental_Imagery_Autism.pdf` | Provenance needed before migration | Topic-relevant autism paper without canonical cache metadata yet. |
| `research/visual_impairments/contrast_sensitivity/2024_Contrast_Sensitivity_Glaucoma_Suspect.pdf` | Provenance needed before migration | Topic-relevant clinical paper without canonical cache metadata yet. |
| `research/visual_impairments/low_vision/2024_Systematic_Review_Mobile_Interface_Visually_Impaired.pdf` | Provenance needed before migration | Topic-relevant review without canonical cache metadata yet. |
| `research/visual_impairments/visual_field_loss/2024_Telerehabilitation_Hemianopia_Children.pdf` | Provenance needed before migration | Topic-relevant rehab paper without canonical cache metadata yet. |

## Topic Counts

| Topic | Count | Paths |
|-------|-------|-------|
| `cognitive_load` | 2 | `research/cognitive_load/2024_Cognitive_Load_Measurement_Methods.pdf`, `research/cognitive_load/2024_Minimalism_vs_Complexity_UX_Cognitive_Load.pdf` |
| `colorblindness` | 4 | `research/colorblindness/Ishihara_38_Plates_Test.pdf`, `research/colorblindness/algorithms/Stockman_2019_Cone_Fundamentals_CIE_Standards.pdf`, `research/colorblindness/algorithms/Vienot_2015_Cone_Fundamentals_Past_Present_Future.pdf`, `research/colorblindness/blue_cone_monochromacy/Cideciyan_2024_BCM_Retinal_Structure_Clinical_Endpoints.pdf` |
| `neurodivergence` | 2 | `research/neurodivergence/autism/2024_Visual_Mental_Imagery_Autism.pdf`, `research/neurodivergence/autism/Manning_2024_Visual_Processing_Autism_Dyslexia.pdf` |
| `visual_impairments` | 3 | `research/visual_impairments/contrast_sensitivity/2024_Contrast_Sensitivity_Glaucoma_Suspect.pdf`, `research/visual_impairments/low_vision/2024_Systematic_Review_Mobile_Interface_Visually_Impaired.pdf`, `research/visual_impairments/visual_field_loss/2024_Telerehabilitation_Hemianopia_Children.pdf` |

## Next Migration Order

1. Move the three already surfaced papers into `papers/downloads/` with
   provenance: Stockman 2019, Vienot 2015, Manning 2024.
2. Add provenance and source-note lanes for the remaining eight literature PDFs.
3. Leave the Ishihara test asset local unless we later define a non-paper asset
   cache lane.
