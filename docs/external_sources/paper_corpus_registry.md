# Paper Corpus Registry

Updated: 2026-03-25

This registry makes `papers/downloads/` the canonical source-cache lane for
tracked papers and trace artifacts.

## Canonical Policy

- New paper artifacts belong in `papers/downloads/`.
- `research/` should cite or discuss those artifacts, not carry placeholder PDF
  stubs or duplicate mirrors.
- When a direct PDF is blocked, cache the accessible full-text HTML plus a
  trace artifact that shows the blocked PDF path.

Machine-readable tracking:

- `papers/downloads/CANONICAL_REGISTRY.json`
- `papers/downloads/paper_corpus_tracking.bib`
- `tools/check_paper_corpus.py`

## Repaired Legacy Placeholders

| Legacy path | Canonical artifacts | Access | Notes |
|-------------|---------------------|--------|-------|
| `research/colorblindness/blue_cone_monochromacy/Sechrest_2023_BCM_Gene_Therapy_Review.pdf` | `papers/downloads/blue_cone_monochromacy/Sechrest_2023_BCM_Gene_Therapy_Review.html`, `.txt`, `.pdf.trace.html` | HTML full text | PMC HTML accessible; direct PDF blocked. |
| `research/neurodivergence/adhd/2024_Eye_Tracking_ADHD_Screening.pdf` | `papers/downloads/adhd/2024_Eye_Tracking_ADHD_Screening.pdf`, `.txt` | PDF | Frontiers publisher PDF cached. |
| `research/neurodivergence/autism/AASPIRE_Autism_Web_Accessibility_Guidelines_2019.pdf` | `papers/downloads/autism/AASPIRE_Autism_Web_Accessibility_Guidelines_2019.pdf`, `.txt` | PDF | Institutional-repository author copy cached. |
| `research/neurodivergence/dyslexia/Mueller-Axt_2024_Magnocellular_LGN_Dyslexia.pdf` | `papers/downloads/dyslexia/Mueller-Axt_2024_Magnocellular_LGN_Dyslexia.pdf`, `.txt` | PDF | Max Planck repository preproof cached. |
| `research/seizures/photosensitive_epilepsy/Fisher_2022_Visually_Sensitive_Seizures.pdf` | `papers/downloads/seizures/Fisher_2022_Visually_Sensitive_Seizures.pdf`, `.txt` | PDF | Essex repository open PDF cached. |
| `research/visual_impairments/nystagmus/2024_INS_Gene_Therapy_Clinical_Trials.pdf` | `papers/downloads/nystagmus/2024_INS_Gene_Therapy_Clinical_Trials.html`, `.txt`, `.pdf.trace.html` | HTML full text | PMC HTML accessible; direct PDF blocked. |

## Collapsed Duplicate Groups

The remaining cross-lane duplicate groups have now been retired. The canonical
path for citation and provenance remains in `papers/downloads/`, and the former
research-local mirrors are tracked below as removed aliases.

| Canonical path | Legacy duplicate paths |
|----------------|------------------------|
| `papers/downloads/algorithms/Brettel_1997_Dichromat_Simulation.pdf` | `research/colorblindness/algorithms/Brettel_1997_Dichromat_Simulation.pdf`, `research/colorblindness/algorithms/Brettel_Vienot_Mollon_1997_Dichromat_Simulation.pdf` |
| `papers/downloads/algorithms/Machado_2009_CVD_Simulation.pdf` | `research/colorblindness/algorithms/Machado_2009_CVD_Simulation.pdf`, `research/colorblindness/algorithms/Machado_Oliveira_Fernandes_2009_CVD_Simulation.pdf` |
| `papers/downloads/algorithms/Vienot_1999_Digital_Colourmaps.pdf` | `research/colorblindness/algorithms/Vienot_1999_Digital_Colourmaps.pdf` |
| `papers/downloads/cognitive_load/Virtual_Multitasking_Cognitive_Load.pdf` | `research/cognitive_load/2025_Predicting_Cognitive_Load_VR_Multitasking.pdf` |

## Quality Gate

Run the verifier with:

```bash
python3 tools/check_paper_corpus.py
```

The verifier checks:

- canonical artifacts exist and match the registry hash/size table,
- no zero-byte PDFs remain under `papers/` or `research/`,
- legacy alias paths stay removed,
- duplicate PDF groups do not reappear across `papers/` and `research/`.
