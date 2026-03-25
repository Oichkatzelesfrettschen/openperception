# Research PDF Migration Inventory

Updated: 2026-03-25

This note tracks the remaining PDFs that still live under `research/` instead of
the canonical `papers/downloads/` cache.

Direct `research/...pdf` references are now treated as provenance-only
references. Outside this inventory and the paper-corpus provenance docs, tracked
Markdown and BibTeX should point to canonical cache artifacts or cite the
source by title/DOI until the artifact is migrated.

## Current Totals

- Remaining research-local PDFs: 5
- Topic buckets:
  `cognitive_load` 2, `colorblindness` 2, `neurodivergence` 1

## Decision Buckets

| Path | Bucket | Rationale |
|------|--------|-----------|
| `research/colorblindness/Ishihara_38_Plates_Test.pdf` | Keep local | Test asset rather than a canonical literature-cache paper. |
| `research/cognitive_load/2024_Cognitive_Load_Measurement_Methods.pdf` | Provenance needed before migration | Useful topic paper, but no canonical cache entry or source note yet. |
| `research/cognitive_load/2024_Minimalism_vs_Complexity_UX_Cognitive_Load.pdf` | Provenance needed before migration | Useful topic paper, but no canonical cache entry or source note yet. |
| `research/colorblindness/blue_cone_monochromacy/Cideciyan_2024_BCM_Retinal_Structure_Clinical_Endpoints.pdf` | Provenance needed before migration | Topic-relevant BCM paper without canonical cache metadata yet. |
| `research/neurodivergence/autism/2024_Visual_Mental_Imagery_Autism.pdf` | Provenance needed before migration | Topic-relevant autism paper without canonical cache metadata yet. |

## Topic Counts

| Topic | Count | Paths |
|-------|-------|-------|
| `cognitive_load` | 2 | `research/cognitive_load/2024_Cognitive_Load_Measurement_Methods.pdf`, `research/cognitive_load/2024_Minimalism_vs_Complexity_UX_Cognitive_Load.pdf` |
| `colorblindness` | 2 | `research/colorblindness/Ishihara_38_Plates_Test.pdf`, `research/colorblindness/blue_cone_monochromacy/Cideciyan_2024_BCM_Retinal_Structure_Clinical_Endpoints.pdf` |
| `neurodivergence` | 1 | `research/neurodivergence/autism/2024_Visual_Mental_Imagery_Autism.pdf` |

## Next Migration Order

1. Add provenance and source-note lanes for the remaining four literature PDFs.
2. Leave the Ishihara test asset local unless we later define a non-paper asset
   cache lane.
