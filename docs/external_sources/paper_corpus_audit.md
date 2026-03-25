# Paper Corpus Audit

Audit date: 2026-03-25

This note captures the paper-corpus state after the duplicate-collapse tranche.

## Current Shape

- `papers/downloads/` is now versioned intentionally.
- PDF papers in `papers/` and `research/` are configured for Git LFS.
- The paper corpus no longer has any live `research/*.pdf` debt.
- Bibliographies, provenance manifests, HTML captures, and text extracts remain
  in normal Git for reviewability.

## Repaired Gaps

### 1. Legacy placeholders were replaced or retired

The six tracked zero-byte placeholder PDFs have been removed from `research/`
and replaced with canonical cache entries in `papers/downloads/`.

- Four placeholders now resolve to real PDF plus text sidecars.
- Two placeholders now resolve to PMC HTML full-text captures plus trace
  artifacts documenting blocked direct PDF fetches.

See:

- `papers/downloads/CANONICAL_REGISTRY.json`
- `papers/downloads/paper_corpus_tracking.bib`
- [Paper corpus registry](/home/eirikr/Github/openperception/docs/external_sources/paper_corpus_registry.md)

### 2. Duplicate mirrors across canonical lanes were collapsed

The last byte-identical cross-lane mirror groups were removed from `research/`
so the repo now has one canonical on-disk copy per tracked paper artifact:

- `papers/downloads/algorithms/Brettel_1997_Dichromat_Simulation.pdf`
- retired mirrors:
  `research/colorblindness/algorithms/Brettel_1997_Dichromat_Simulation.pdf`,
  `research/colorblindness/algorithms/Brettel_Vienot_Mollon_1997_Dichromat_Simulation.pdf`

- `papers/downloads/algorithms/Machado_2009_CVD_Simulation.pdf`
- retired mirrors:
  `research/colorblindness/algorithms/Machado_2009_CVD_Simulation.pdf`,
  `research/colorblindness/algorithms/Machado_Oliveira_Fernandes_2009_CVD_Simulation.pdf`

- `papers/downloads/algorithms/Vienot_1999_Digital_Colourmaps.pdf`
- retired mirror:
  `research/colorblindness/algorithms/Vienot_1999_Digital_Colourmaps.pdf`

- `papers/downloads/cognitive_load/Virtual_Multitasking_Cognitive_Load.pdf`
- retired mirror:
  `research/cognitive_load/2025_Predicting_Cognitive_Load_VR_Multitasking.pdf`

The registry now records those paths as removed legacy aliases, and the paper
corpus verifier will fail if equivalent cross-lane PDF duplicates reappear.

### 3. Root-level paper outliers were retired into topic lanes

The last tracked paper PDFs living directly under `papers/` were migrated into
topic lanes under `papers/downloads/`:

- `papers/downloads/color_vision/Zhu_2024_Computational_Trichromacy_Reconstruction_AR.pdf`
- retired outlier:
  `papers/arXiv_2408.01895_Trichromacy_Reconstruction_AR.pdf`

- `papers/downloads/color_vision/Kotani_2025_Color_Vision_Emergence_Framework.pdf`
- retired outlier:
  `papers/arXiv_2408.16916_Color_Vision_Emergence_Framework.pdf`

## Quality Gate

The paper corpus now has a dedicated verifier:

```bash
python3 tools/check_paper_corpus.py
```

It fails on zero-byte PDFs, bad registry hashes, lingering legacy aliases,
stray `papers/*.pdf` outliers, and any duplicate PDF groups that reappear
across the canonical cache and research lanes. It also blocks stale Markdown
references to retired alias paths outside the provenance docs that are meant to
record them.

## Remaining Follow-Up

1. Keep future paper additions in `papers/downloads/` first, with provenance or
   trace artifacts added in the same change.
2. Treat any new `research/*.pdf` file as a verifier failure, not as acceptable
   migration debt.
3. Keep non-paper reference assets in dataset-specific lanes such as
   `datasets/source_assets/`, with a provenance note beside the asset.
