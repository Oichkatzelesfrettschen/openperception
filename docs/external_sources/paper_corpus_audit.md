# Paper Corpus Audit

Audit date: 2026-03-25

This note captures the first post-LFS audit state of the paper corpus.

## Current Shape

- `papers/downloads/` is now versioned intentionally.
- PDF papers in `papers/` and `research/` are configured for Git LFS.
- Bibliographies, provenance manifests, HTML captures, and text extracts remain
  in normal Git for reviewability.

## Observed Gaps

### 1. Zero-byte legacy PDF placeholders

The following tracked files currently exist as zero-byte placeholders:

- `research/colorblindness/blue_cone_monochromacy/Sechrest_2023_BCM_Gene_Therapy_Review.pdf`
- `research/neurodivergence/adhd/2024_Eye_Tracking_ADHD_Screening.pdf`
- `research/neurodivergence/autism/AASPIRE_Autism_Web_Accessibility_Guidelines_2019.pdf`
- `research/neurodivergence/dyslexia/Mueller-Axt_2024_Magnocellular_LGN_Dyslexia.pdf`
- `research/seizures/photosensitive_epilepsy/Fisher_2022_Visually_Sensitive_Seizures.pdf`
- `research/visual_impairments/nystagmus/2024_INS_Gene_Therapy_Clinical_Trials.pdf`

These should be treated as missing-source stubs, not as valid cached papers.

### 2. Duplicate PDFs across canonical lanes

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

## Recommended Next Steps

1. Choose one canonical storage lane for each paper: either `papers/downloads/`
   as the source cache or `research/` as the topic-local archive.
2. Replace zero-byte placeholders with real artifacts plus provenance, or
   explicitly convert them into README-style trace notes.
3. Update docs that cite duplicate filenames so claims point to one stable
   artifact path per source.
4. Add a lightweight verifier that flags zero-byte PDFs and duplicate filenames
   with differing paths.
