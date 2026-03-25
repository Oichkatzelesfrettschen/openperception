# Research PDF Migration Inventory

Updated: 2026-03-25

This note tracks the remaining PDFs that still live under `research/` instead of
the canonical `papers/downloads/` cache.

Direct `research/...pdf` references are now treated as provenance-only
references. Outside this inventory and the paper-corpus provenance docs, tracked
Markdown and BibTeX should point to canonical cache artifacts or cite the
source by title/DOI until the artifact is migrated.

## Current Totals

- Remaining research-local PDFs: 1
- Topic buckets: `colorblindness` 1

## Decision Buckets

| Path | Bucket | Rationale |
|------|--------|-----------|
| `research/colorblindness/Ishihara_38_Plates_Test.pdf` | Keep local | Test asset rather than a canonical literature-cache paper. |

## Topic Counts

| Topic | Count | Paths |
|-------|-------|-------|
| `colorblindness` | 1 | `research/colorblindness/Ishihara_38_Plates_Test.pdf` |

## Next Migration Order

1. Decide whether the Ishihara test asset deserves a separate non-paper cache
   lane or should remain a deliberate research-local exception.
