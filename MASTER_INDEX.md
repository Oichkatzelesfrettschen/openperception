# Visual Accessibility Research Compendium - Master Index

**Repository:** OpenPerception (see repository root)
**Compiled:** March 25, 2026
**Total PDFs:** 36 (in `papers/downloads/` -- for research use only; see DOI/URL links for official access)
**Total Compendiums:** 35 markdown files

---

## Table of Contents

1. [Research Categories](#research-categories)
2. [PDF Collections](#pdf-collections)
3. [Compendium Files](#compendium-files)
4. [Directory Structure](#directory-structure)
5. [Key References by Topic](#key-references-by-topic)

---

## Research Categories

### 1. Color Vision Deficiency (CVD)
- **Protanopia** (red-blind) - L-cone dysfunction
- **Deuteranopia** (green-blind) - M-cone dysfunction
- **Tritanopia** (blue-blind) - S-cone dysfunction
- **Achromatopsia** (complete colorblindness) - CNGA3/CNGB3 mutations
- **Blue Cone Monochromacy** - OPN1LW/OPN1MW mutations

### 2. CVD Simulation Algorithms
- **Brettel 1997** - Gold standard dichromat simulation
- **Vienot 1999** - Simplified matrix method
- **Machado 2009** - Severity parameter model
- **Daltonization** - Color correction methods

### 3. Visual Impairments
- **Stereoblindness** - Depth perception disorders
- **Low Vision** - Visual acuity deficits
- **Visual Field Loss** - Hemianopia, scotomas
- **Contrast Sensitivity** - Detection thresholds
- **Nystagmus** - Eye movement disorders

### 4. Neurodivergence
- **ADHD** - Visual attention processing
- **Autism Spectrum** - Enhanced/altered perception
- **Dyslexia** - Visual processing components
- **Dyscalculia** - Number/spatial processing

### 5. Photosensitive Seizures
- **Photosensitive Epilepsy** - Flash triggers
- **Pattern Sensitivity** - Geometric patterns
- **WCAG Guidelines** - Web accessibility standards
- **Broadcast Standards** - Ofcom, ITU, ISO

### 6. Cognitive Load
- **Visual Working Memory** - Capacity limits
- **Attention Resources** - Allocation theory
- **Interface Design** - Dashboard optimization
- **Measurement Methods** - Eye tracking, fNIRS, EEG

---

## PDF Collections

### Downloaded Papers by Category

#### Algorithms (3 papers)
| File | Description |
|------|-------------|
| `Brettel_1997_Dichromat_Simulation.pdf` | Foundational dichromat simulation |
| `Vienot_1999_Digital_Colourmaps.pdf` | Simplified matrix method |
| `Machado_2009_CVD_Simulation.pdf` | Physiologically-based model |

#### Colorblindness (5 papers)
| File | Description |
|------|-------------|
| `Color_Universal_Design_DNN_2025.pdf` | Deep learning CUD |
| `Dyschromatopsia_Mechanisms_2024.pdf` | CVD mechanisms review |
| `MedlinePlus_Color_Vision_Deficiency.pdf` | Clinical overview |
| `OPN1LW_Exon_Deletion_RG_CVD.pdf` | Genetic case study |
| `OPN1LW_OPN1MW_Mutations_CVD.pdf` | Opsin gene mutations |

#### ADHD (5 papers)
| File | Description |
|------|-------------|
| `2024_Eye_Tracking_ADHD_Screening.pdf` | Eye tracking screening |
| `ADHD_Pediatrics_Review_2024.pdf` | Neuroimaging review |
| `ADHD_Perceptual_Oscillations_2025.pdf` | 91.8% ML classification |
| `ADHD_Peripheral_Vision_2023.pdf` | Neuro-glasses intervention |
| `Gestalt_Processing_CVI_ADHD_2024.pdf` | Visual selective attention |

#### Autism (7 papers)
| File | Description |
|------|-------------|
| `AASPIRE_Autism_Web_Accessibility_Guidelines_2019.pdf` | Participatory web accessibility guidelines |
| `2min_Eye_Tracking_ASD_2024.pdf` | Brief screening protocol |
| `Eye_Tracking_ASD_2024.pdf` | Novel metrics system |
| `Eye_Tracking_ASD_DL_2025.pdf` | Deep learning diagnosis |
| `Manning_2024_Visual_Processing_Autism_Dyslexia.pdf` | Cross-syndrome study |
| `Visual_Complexity_Autism_2025.pdf` | Sensory preferences |
| `Visual_Perception_Autism_Review.pdf` | Comprehensive review |

#### Dyslexia (1 paper)
| File | Description |
|------|-------------|
| `Mueller-Axt_2024_Magnocellular_LGN_Dyslexia.pdf` | Visual thalamus neuroimaging evidence |

#### Cognitive Load (10 papers)
| File | Description |
|------|-------------|
| `Adaptive_Learning_Cognitive_Load.pdf` | ALT analysis |
| `CLT_Emerging_Trends_2025.pdf` | Theory evolution |
| `Cognition_Computation_Attention.pdf` | Human-AI comparison |
| `Dashboard_Visualization_Literacy_2024.pdf` | Teacher study |
| `Eye_Tracking_MR_Cognitive_Load_2025.pdf` | Mixed reality |
| `Rethinking_PreTraining_Cognitive_Load.pdf` | CLT implications |
| `Self_Explanation_Programming_2024.pdf` | Programming education |
| `Virtual_Multitasking_Cognitive_Load.pdf` | UCSB study |
| `Visual_Temporal_Attention_2024.pdf` | Attention review |
| `VWM_Meaningfulness_2024.pdf` | Working memory |

#### Seizures (3 papers)
| File | Description |
|------|-------------|
| `Fisher_2022_Visually_Sensitive_Seizures.pdf` | Epilepsy Foundation review |
| `ITU-R_BT1702-3_PSE_Guidelines.pdf` | International standard |
| `Multisensory_Flicker_Epilepsy_2024.pdf` | 40Hz stimulation |

#### Stereoblindness And Depth Source Cache
| File | Description |
|------|-------------|
| `Stereoblindness_VR_Training.pdf` | VR depth training |
| `Pladere_et_al_2022_Inclusivity_in_Stereoscopic_XR.pdf` | XR inclusivity and adaptive depth presentation |
| `Wang_Saunders_2022_Texture_Slant_Stereoblindness.txt` | Full-text extraction from PMC HTML article |
| `Nadler_et_al_2016_Motion_Parallax_Depth_Review.txt` | Full-text extraction from PMC HTML article |
| `Chopin_Bavelier_Levi_2019_Stereoblindness_Best_Evidence_Synthesis.pubmed.txt` | PubMed abstract trace for prevalence synthesis |

Applied documentation:
- `docs/harmonized-depth-accommodation-guide.md` - Stereo-independent depth guidance for shared scene meaning
- `docs/external_sources/stereoblindness_depth_sources.md` - Source cache and provenance index
- `research/visual_impairments/stereoblindness/primary_source_notes.md` - Paper-by-paper granular extraction

#### Canonical Corpus Registry
| File | Description |
|------|-------------|
| `CANONICAL_REGISTRY.json` | Canonical paper paths, legacy aliases, and file hashes |
| `paper_corpus_tracking.bib` | BibTeX tracking for repaired legacy placeholders |
| `docs/external_sources/paper_corpus_registry.md` | Human-readable canonical cache policy and duplicate map |

### Existing Research PDFs

Located in `/research/` subdirectories:
- `Brettel_Vienot_Mollon_1997_Dichromat_Simulation.pdf`
- `Machado_Oliveira_Fernandes_2009_CVD_Simulation.pdf`
- `Stockman_2019_Cone_Fundamentals_CIE_Standards.pdf`
- `Vienot_2015_Cone_Fundamentals_Past_Present_Future.pdf`
- Canonical source-cache paths now live under `papers/downloads/`; see `docs/external_sources/paper_corpus_registry.md`
- And 18+ more across research subdirectories

---

## Compendium Files

### Primary Research Compendiums

| File | Topic | Papers Cataloged |
|------|-------|------------------|
| `papers/colorblindness_algorithms_compendium.md` | CVD simulation algorithms | 50+ |
| `papers/COLORBLINDNESS_ACADEMIC_PAPERS.md` | Protanopia/Deuteranopia/Tritanopia | 47 |
| `papers/achromatopsia_bcm_research_compendium.md` | Achromatopsia & BCM | 30+ |
| `papers/ADHD_Visual_Processing_Papers_2023-2025.md` | ADHD visual processing | 30+ |
| `papers/autism_visual_processing_bibliography.md` | Autism visual processing | 50+ |
| `papers/photosensitive_epilepsy_research_compendium.md` | Seizure safety | 40+ |
| `papers/cognitive_load_visual_processing_papers.md` | Cognitive load | 75+ |
| `docs/harmonized-depth-accommodation-guide.md` | Applied depth accommodation synthesis | Curated primary sources |

### Research Domain Files

| Directory | Files |
|-----------|-------|
| `research/colorblindness/` | CVD types, algorithms, simulations |
| `research/visual_impairments/` | Stereoblindness, low vision, nystagmus |
| `research/neurodivergence/` | ADHD, autism, dyslexia |
| `research/seizures/` | Photosensitive epilepsy, guidelines |
| `research/cognitive_load/` | CLT, visual processing |

---

## Directory Structure

```
openperception/
├── algorithms/
│   ├── libDaltonLens/          # C implementation
│   └── DaltonLens-Python/      # Python R&D package
├── docs/
│   ├── colorblind-friendly-design-guide.md
│   ├── oklch-guide.md
│   └── simulator-guide.md
├── papers/
│   ├── downloads/              # Downloaded PDFs by category
│   │   ├── adhd/
│   │   ├── algorithms/
│   │   ├── autism/
│   │   ├── cognitive_load/
│   │   ├── colorblindness/
│   │   ├── dyslexia/
│   │   ├── seizures/
│   │   └── stereoblindness/
│   ├── colorblindness_algorithms_compendium.md
│   ├── COLORBLINDNESS_ACADEMIC_PAPERS.md
│   ├── achromatopsia_bcm_research_compendium.md
│   ├── ADHD_Visual_Processing_Papers_2023-2025.md
│   ├── autism_visual_processing_bibliography.md
│   ├── photosensitive_epilepsy_research_compendium.md
│   └── cognitive_load_visual_processing_papers.md
├── research/
│   ├── colorblindness/
│   │   ├── protanopia/
│   │   ├── deuteranopia/
│   │   ├── tritanopia/
│   │   ├── achromatopsia/
│   │   ├── blue_cone_monochromacy/
│   │   ├── algorithms/
│   │   └── simulations/
│   ├── visual_impairments/
│   │   ├── stereoblindness/
│   │   ├── low_vision/
│   │   ├── visual_field_loss/
│   │   ├── contrast_sensitivity/
│   │   └── nystagmus/
│   ├── neurodivergence/
│   │   ├── adhd/
│   │   ├── autism/
│   │   ├── dyslexia/
│   │   └── dyscalculia/
│   ├── seizures/
│   │   ├── photosensitive_epilepsy/
│   │   ├── pattern_sensitivity/
│   │   └── guidelines/
│   └── cognitive_load/
└── datasets/
    └── ishihara-plate-learning/
```

---

## Key References by Topic

### CVD Simulation (Essential Papers)
1. Brettel, Vienot, Mollon (1997) - JOSA-A - Dichromat simulation foundation
2. Vienot, Brettel, Mollon (1999) - Color Res Appl - Single matrix method
3. Machado, Oliveira, Fernandes (2009) - IEEE TVCG - Severity parameter model

### Cone Fundamentals
1. Smith & Pokorny (1975) - Vision Research - Classic cone fundamentals
2. Stockman & Sharpe (2000) - Vision Research - CIE 2006 standard basis

### Gene Therapy
1. CNGA3 trials: NCT02610582 (German), NCT03758404 (AGTC)
2. CNGB3 trials: NCT03001310 (MeiraGTx), NCT02935517 (AGTC)
3. BCM: CIRM $4.7M award to Blue Gen Therapeutics (2024)

### Photosensitive Seizures
1. Fisher et al. (2022) - Epilepsy Foundation updated review
2. ITU-R BT.1702-3 (2023) - International broadcast standard
3. WCAG 2.3.1 - Three flashes or below threshold (Level A)

### Eye Tracking Biomarkers
1. ADHD: Retinal fundus 95.5-96.9% AUROC
2. ADHD: Perceptual oscillations 91.8% ML accuracy
3. Autism: Eye tracking metrics 88-100% sensitivity

### Accessibility Standards
- WCAG 2.1: Color contrast 4.5:1 (AA), 7:1 (AAA)
- Flash limits: Max 3/second, danger zone 15-20 Hz
- Pattern limits: Max 5 light-dark pairs if oscillating

---

## Statistics Summary

| Metric | Count |
|--------|-------|
| Total PDFs | 36 (in papers/downloads/) |
| Compendium Markdown Files | 7 |
| Research Domain Markdowns | 29 |
| Papers Cataloged (estimated) | 420+ |
| Research Categories | 6 major |
| Subcategories | 20+ |
| Last Research Update | 2026-03-19 |

---

## Usage Notes

### Finding Papers
1. Check `papers/downloads/` for canonical downloaded PDFs
2. Check compendium files for paper lists with DOIs/URLs
3. Use `docs/external_sources/paper_corpus_registry.md` for canonical-path and legacy-alias tracking

### Key Compendiums
- **For CVD algorithms**: `colorblindness_algorithms_compendium.md`
- **For seizure safety**: `photosensitive_epilepsy_research_compendium.md`
- **For neurodivergence**: ADHD/autism markdown files
- **For cognitive load**: `cognitive_load_visual_processing_papers.md`

### Open Access Sources
- arXiv preprints: Freely available
- Frontiers journals: Open access (CC BY)
- PMC: PubMed Central free full text
- MDPI journals: Open access

---

*Index generated: March 25, 2026*
*Updated: March 25, 2026 (repaired placeholder sources, added canonical corpus registry, refreshed cache counts)*
*For: Visual Accessibility Research Compendium*
