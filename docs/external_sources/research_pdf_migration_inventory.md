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
