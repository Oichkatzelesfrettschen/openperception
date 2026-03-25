# Paper Downloads

This directory is the repo's curated local paper cache.

## Storage Policy

- PDF papers in this tree are stored with Git LFS.
- Bibliographies, provenance files, HTML captures, and text extracts stay in
  normal Git for reviewability and grepability.
- This directory is intentionally versioned even though the repo has a broad
  `downloads/` ignore rule elsewhere.

## Purpose

Use this tree for cached primary sources that back claims, guides, and specs in
the repo. Keep filenames stable and ASCII-only.

Non-paper reference assets belong in `datasets/source_assets/` instead of this
literature cache.

## Layout

- `adhd/`
- `algorithms/`
- `autism/`
- `blue_cone_monochromacy/`
- `cognitive_load/`
- `contrast_sensitivity/`
- `colorblindness/`
- `color_vision/`
- `dyslexia/`
- `low_vision/`
- `nystagmus/`
- `seizures/`
- `stereoblindness/`
- `visual_field_loss/`

Tracking files:

- `CANONICAL_REGISTRY.json`
- `paper_corpus_tracking.bib`

## Expectations

- Add provenance for newly fetched sources when practical.
- Prefer one deterministic filename per source.
- Retire research-local PDF mirrors once a canonical cache path exists.
- In tracked Markdown and BibTeX, prefer canonical `papers/downloads/` paths
  over direct `research/...pdf` references.
- Keep distilled summaries in markdown outside this cache, and use this tree as
  the backing artifact store.

Related audit:

- [Paper corpus audit](/home/eirikr/Github/openperception/docs/external_sources/paper_corpus_audit.md)
- [Paper corpus registry](/home/eirikr/Github/openperception/docs/external_sources/paper_corpus_registry.md)
