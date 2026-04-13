# Research PDF Migration Inventory

Updated: 2026-03-25

This note tracks the retirement of PDFs that previously lived under `research/`
instead of the canonical `papers/downloads/` cache.

Direct `research/...pdf` references are now treated as provenance-only
references. Outside this inventory and the paper-corpus provenance docs, tracked
Markdown and BibTeX should point to canonical cache artifacts or cite the
source by title/DOI until the artifact is migrated.

## Current Totals

- Remaining research-local PDFs: 0
- Topic buckets: none

## Retirement Result

All literature PDFs that used to live under `research/` have been migrated into
the canonical paper cache under `papers/downloads/`.

The last non-paper exception was also retired from `research/`:

| Former Path | Resolution | Current Location |
|-------------|------------|------------------|
| `research/colorblindness/Ishihara_38_Plates_Test.pdf` | Reclassified as a dataset-support source asset rather than a literature paper. | `datasets/source_assets/ishihara/Ishihara_38_Plates_Test.pdf` |

## Follow-Up

1. Re-verify an upstream acquisition URL for the Ishihara source asset when a
   trustworthy source is identified.
2. Keep future non-paper reference artifacts in `datasets/source_assets/`
   instead of `research/`.

## HTML Trace Upgrade Review (2026-04-12)

Four PMC articles are cached as full-text HTML with PDF-blocked traces.
These are upgrade candidates if direct PDF access becomes available.

| Artifact | Topic Lane | Status |
|----------|-----------|--------|
| `Sechrest_2023_BCM_Gene_Therapy_Review.html` | `blue_cone_monochromacy` | PMC full-text HTML; PDF was blocked at cache time. Upgrade when PDF is accessible. |
| `2024_INS_Gene_Therapy_Clinical_Trials.html` | `nystagmus` | PMC full-text HTML; PDF was blocked at cache time. Upgrade when PDF is accessible. |
| `Nadler_et_al_2016_Motion_Parallax_Depth_Review.html` | `stereoblindness` | PMC full-text HTML; PDF was blocked at cache time. Upgrade when PDF is accessible. |
| `Wang_Saunders_2022_Texture_Slant_Stereoblindness.html` | `stereoblindness` | PMC full-text HTML; PDF was blocked at cache time. Upgrade when PDF is accessible. |

Resolution path: re-fetch each PDF via its DOI or PMC ID in a session where
PMC direct-download is available. Replace the `.html` primary artifact with
the PDF and retain the `.pdf.trace.html` as a provenance record. Update the
corresponding source-cache doc to reflect the new access mode.
