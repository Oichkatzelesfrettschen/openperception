# Paper Corpus Audit

Audit date: 2026-03-25

This note captures the paper-corpus state after the first repair tranche.

## Current Shape

- `papers/downloads/` is now versioned intentionally.
- PDF papers in `papers/` and `research/` are configured for Git LFS.
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

### 2. Duplicate PDFs across canonical lanes are documented

The following files are byte-identical duplicates:

- `papers/downloads/algorithms/Brettel_1997_Dichromat_Simulation.pdf`
- `research/colorblindness/algorithms/Brettel_1997_Dichromat_Simulation.pdf`
- `research/colorblindness/algorithms/Brettel_Vienot_Mollon_1997_Dichromat_Simulation.pdf`

- `papers/downloads/algorithms/Machado_2009_CVD_Simulation.pdf`
- `research/colorblindness/algorithms/Machado_2009_CVD_Simulation.pdf`
- `research/colorblindness/algorithms/Machado_Oliveira_Fernandes_2009_CVD_Simulation.pdf`

- `papers/downloads/algorithms/Vienot_1999_Digital_Colourmaps.pdf`
- `research/colorblindness/algorithms/Vienot_1999_Digital_Colourmaps.pdf`

- `papers/downloads/cognitive_load/Virtual_Multitasking_Cognitive_Load.pdf`
- `research/cognitive_load/2025_Predicting_Cognitive_Load_VR_Multitasking.pdf`

These are not urgent because LFS de-duplicates object storage by content, but
they do create naming drift and citation ambiguity.

## Quality Gate

The paper corpus now has a dedicated verifier:

```bash
python3 tools/check_paper_corpus.py
```

It fails on zero-byte PDFs, bad registry hashes, lingering legacy placeholder
paths, and duplicate groups that drift away from the documented canonical map.

## Remaining Follow-Up

1. Collapse the documented cross-lane duplicate groups once downstream docs stop
   depending on research-local mirror PDFs.
2. Keep future paper additions in `papers/downloads/` first, with provenance or
   trace artifacts added in the same change.
