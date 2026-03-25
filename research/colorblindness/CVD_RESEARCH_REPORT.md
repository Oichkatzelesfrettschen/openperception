# Color Vision Deficiency Research Report

**Generated:** 2025-12-27
**Last Updated:** 2026-03-25
**Purpose:** Comprehensive accessibility research repository for color vision deficiency (CVD)

---

## Table of Contents

1. [Overview and Statistics](#overview-and-statistics)
2. [Protanopia (L-cone Deficiency)](#protanopia-l-cone-deficiency)
3. [Deuteranopia (M-cone Deficiency)](#deuteranopia-m-cone-deficiency)
4. [Tritanopia (S-cone Deficiency)](#tritanopia-s-cone-deficiency)
5. [Achromatopsia (Complete Color Blindness)](#achromatopsia-complete-color-blindness)
6. [Blue Cone Monochromacy](#blue-cone-monochromacy)
7. [Simulation Algorithms](#simulation-algorithms)
8. [Daltonization and Recoloring Algorithms](#daltonization-and-recoloring-algorithms)
9. [Accessibility Design Guidelines](#accessibility-design-guidelines)
10. [Open Datasets and Resources](#open-datasets-and-resources)
11. [Color Vision Testing](#color-vision-testing)
12. [Open Source Tools and Libraries](#open-source-tools-and-libraries)

---

## Overview and Statistics

Color vision deficiency (CVD), commonly called "color blindness," affects approximately:

- **300+ million people globally**
- **8% of males** (1 in 12 men)
- **0.5% of females** (1 in 200 women)

CVD is primarily inherited through X-linked recessive genes for red-green deficiencies, while blue-yellow deficiencies follow autosomal dominant inheritance.

---

## Protanopia (L-cone Deficiency)

### Definition

Protanopia is a type of red-green color blindness where the L-cones (long-wavelength sensitive, responsible for red perception) are absent or non-functional. Protanomalous individuals have L-cones with shifted spectral sensitivity.

### Genetics

- X-linked recessive inheritance
- Caused by mutations in the OPN1LW gene on the X chromosome
- Affects approximately 1% of males

### Key Research (2023-2025)

#### 2024 Papers

1. **"Fast image recoloring for red-green anomalous trichromacy with contrast enhancement and naturalness preservation"**
   - Authors: Zhou, Huang, Zhu, Chen, Go, Mao
   - Journal: The Visual Computer (July 2024)
   - Focus: Real-time recoloring algorithms for protanopia/protanomaly

2. **"Investigating Color-Blind User-Interface Accessibility via Simulated Interfaces"**
   - Journal: MDPI Computers (February 2024)
   - URL: https://www.mdpi.com/2073-431X/13/2/53
   - Summary: Builds on physiologically based CVD models; proposes novel simulation-based experimental protocol

3. **"Image recoloring for color vision deficiency compensation using Swin transformer"**
   - Journal: Neural Computing and Applications (April 2024)
   - URL: https://link.springer.com/article/10.1007/s00521-023-09367-2
   - Summary: Deep learning approach using Swin transformer for CVD compensation

#### Clinical Characteristics

- Reduced sensitivity to red light
- Confusion between red-green, red-brown, green-brown color pairs
- Darkened perception of red wavelengths
- Protanomalous individuals show shifted Rayleigh match (require more red in mixture)

### Diagnosis via Anomaloscope

- Protanopes accept any mixture of red and green as matching yellow
- Protanomalous observers require more red light in the Rayleigh match
- Matching luminance of 589 nm light is below normal for protanomalous

---

## Deuteranopia (M-cone Deficiency)

### Definition

Deuteranopia is the most common form of red-green color blindness where M-cones (medium-wavelength sensitive, responsible for green perception) are absent. Deuteranomalous individuals have M-cones with shifted spectral sensitivity.

### Genetics

- X-linked recessive inheritance
- Caused by mutations in the OPN1MW gene on the X chromosome
- Affects approximately 5% of males (most common CVD type)

### Key Research (2023-2025)

#### Foundational Algorithm Papers

1. **"Information Preserving Color Transformation for Protanopia and Deuteranopia"**
   - Authors: Huang et al.
   - Journal: IEEE Transactions
   - URL: https://ieeexplore.ieee.org/document/4303068/
   - Summary: Presents color transformation preserving information while maintaining naturalness

2. **"Image recoloring for color vision deficiency compensation: a survey"**
   - Journal: The Visual Computer (2021, still highly relevant)
   - URL: https://link.springer.com/article/10.1007/s00371-021-02240-0
   - Summary: Comprehensive survey of recoloring methods; methods increase blue component to compensate for red-green confusion

#### 2024 Research

3. **"Filters and recoloring algorithms to improve mobile accessibility for users with color blindness"**
   - Conference: ICECCT 2024
   - URL: https://dl.acm.org/doi/10.1145/3705754.3705954
   - Summary: Mobile-focused accessibility solutions

### Clinical Characteristics

- Similar to protanopia but without luminosity loss in red
- Confusion between green-red, green-brown, blue-purple pairs
- Deuteranomalous observers require more green in Rayleigh match
- Matching luminance remains normal (unlike protanopia)

---

## Tritanopia (S-cone Deficiency)

### Definition

Tritanopia is a rare form of blue-yellow color blindness where S-cones (short-wavelength sensitive, responsible for blue perception) are absent or non-functional.

### Genetics

- **Autosomal dominant inheritance** (not X-linked)
- Caused by mutations in the OPN1SW gene on Chromosome 7
- Affects approximately **1 in 10,000 individuals**
- Affects males and females equally

### Key Research (2023-2025)

#### 2024 Comprehensive Review

1. **"Dyschromatopsia: a comprehensive analysis of mechanisms and cutting-edge treatments for color vision deficiency"**
   - Authors: Researchers at Wuhan University of Science and Technology
   - Journal: Frontiers in Neuroscience (January 2024)
   - URL: https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2024.1265630/full
   - DOI: Included in Frontiers
   - Summary: Comprehensive analysis of genetic basis, mechanisms, and treatment approaches including gene therapy and pharmacological interventions

### Causes

- **Congenital:** Rare inherited form
- **Acquired:** More common; caused by:
  - Aging of the eye
  - Glaucoma
  - Diabetes (retinal damage)
  - Alcoholism (toxic to inner retinal layers)
  - Traumatic brain injury

### Clinical Characteristics

- Difficulty distinguishing: green-blue, yellow-pink, purple-red
- S-cones constitute only ~1% of retinal cone cells
- No effective treatment for inherited form
- EnChroma glasses are NOT effective for tritanopia

---

## Achromatopsia (Complete Color Blindness)

### Definition

Achromatopsia (ACHM), also known as rod monochromatism or total color blindness, is a rare autosomal recessive disorder affecting all three cone cell types, resulting in complete cone dysfunction.

### Prevalence

- Affects approximately **1 in 30,000 people**

### Genetics

Up to **90% of patients** carry mutations in one of these genes:

| Gene | Function | Prevalence |
|------|----------|------------|
| CNGA3 | Alpha subunit of cone CNG channel | ~40% |
| CNGB3 | Beta subunit of cone CNG channel | ~50% |
| GNAT2 | Cone transducin | Rare |
| PDE6C | Cone PDE6 | Rare |
| PDE6H | Cone PDE6 | Rare |
| ATF6 | Unfolded protein response regulator | ~1% |

### Key Research (2023-2025)

#### Gene Therapy Research

1. **"Achromatopsia: Genetics and Gene Therapy"** (2022, foundational)
   - URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC8766373/
   - Summary: Comprehensive overview of genetic causes and gene therapy prospects

2. **Gene Therapy Clinical Trial Results (2023)**
   - Source: Medical Xpress
   - URL: https://medicalxpress.com/news/2023-07-gene-therapy-vision-achromatopsia-patients.html
   - Summary: Following CNGA3 gene augmentation therapy, patients reported perceiving "red" distinctly from previous vision

3. **"Dyschromatopsia: comprehensive analysis"** (2024)
   - URL: https://pubmed.ncbi.nlm.nih.gov/38298913/
   - Summary: Reviews gene therapy clinical trials (began 2016); pediatric participants showed improved cone function

#### Treatment Status

- **No pharmaceutical treatments currently available**
- Management includes:
  - Genetic counseling
  - Dark/red-tinted glasses for photophobia
  - Low vision aids
- Gene therapy shows promise but faces challenges:
  - Visual cortex may not develop normally without cone input
  - Earlier treatment (childhood) likely more effective
  - Multiple Phase I/II trials ongoing (clinicaltrials.gov)

### Clinical Characteristics

- Complete loss of color discrimination (see only light/dark)
- Poor visual acuity (typically 20/200)
- Severe photophobia
- Nystagmus
- Foveal cone dystrophy

---

## Blue Cone Monochromacy

Primary source lane:

- [Vision clinical source cache](/home/eirikr/Github/openperception/docs/external_sources/vision_clinical_source_cache.md)
- [BCM primary source notes](/home/eirikr/Github/openperception/research/colorblindness/blue_cone_monochromacy/primary_source_notes.md)

### Definition

Blue cone monochromacy (BCM) is a rare X-linked congenital disorder characterized by complete loss or severe reduction of L- and M-cone function, leaving only S-cones functional.

### Genetics

- X-linked recessive inheritance
- Caused by mutations in the OPN1LW/OPN1MW gene cluster on X chromosome
- Two most common genetic causes:
  1. Deletion mutations
  2. C203R missense mutation (most common)

### Key Research (2023-2025)

#### 2023 Publications

1. **"Blue cone monochromacy and gene therapy"** (March 2023)
   - Authors: West Virginia University researchers
   - Journal: Vision Research
   - URL: https://www.sciencedirect.com/science/article/pii/S0042698923000457
   - PubMed: https://pubmed.ncbi.nlm.nih.gov/37001420/
   - PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC10182257/
   - Local cache: `papers/downloads/blue_cone_monochromacy/Sechrest_2023_BCM_Gene_Therapy_Review.html`
   - Summary: Comprehensive review covering genetic causes, clinical features, animal models, and AAV gene therapy progress

2. **"Preclinical Evaluation of ADVM-062"** (July 2023)
   - Journal: Molecular Therapy
   - Summary: Novel intravitreal gene therapy vector for BCM treatment

#### 2024 Publications

3. **"Evaluation of Retinal Structure and Visual Function in Blue Cone Monochromacy to Develop Clinical Endpoints for L-opsin Gene Therapy"** (October 2024)
   - Authors: University of Pennsylvania, University of Tubingen
   - PubMed: https://pubmed.ncbi.nlm.nih.gov/39408969/
   - Summary: Developing clinical endpoints for L-opsin gene therapy trials

4. **"Structural and Functional Rescue of Cones with C203R Mutation"** (2024)
   - Journal: JCI Insight
   - Summary: Demonstrated rescue of cones carrying the common C203R missense mutation

#### 2025 Research

5. **"Molecular mechanisms limiting the AAV gene therapy treatment window in mouse models of BCM"**
   - Journal: Communications Biology
   - URL: https://www.nature.com/articles/s42003-025-09045-0
   - Summary: Reveals limited therapeutic windows; identifies upregulated cone-specific promoters for aged BCM cones

### Clinical Trial Progress

- **BCM Families Foundation** funding:
  - $130,888 to West Virginia University (2023-2024)
  - $400,000 to University of Tubingen (2010-2024)
- Goal: IND application to FDA/EMA for Phase I/II gene therapy trial
- Positive findings: Sufficient cone cells present in BCM patients for gene therapy

### Clinical Characteristics

- Poor visual acuity
- Severely impaired color discrimination
- Myopia
- Nystagmus
- Photophobia

---

## Simulation Algorithms

### Overview

Three primary algorithms dominate CVD simulation research:

1. **Brettel, Vienot & Mollon (1997)**
2. **Vienot, Brettel & Mollon (1999)**
3. **Machado, Oliveira & Fernandes (2009)**

### Algorithm Comparison

| Algorithm | Protanopia | Deuteranopia | Tritanopia | Anomalous Trichromacy | Computation |
|-----------|------------|--------------|------------|----------------------|-------------|
| Brettel 1997 | Excellent | Excellent | **Best choice** | No | 2x 3x3 matrices |
| Vienot 1999 | Excellent | Excellent | Poor | No | 1x 3x3 matrix |
| Machado 2009 | Good | Good | Good | **Yes** | 1x 3x3 matrix |

### Key Papers

1. **"Computerized simulation of color appearance for dichromats"** (Brettel et al., 1997)
   - Journal: JOSA A
   - URL: https://opg.optica.org/josaa/abstract.cfm?uri=josaa-14-10-2647
   - Method: Projects stimuli onto reduced stimulus surface in LMS space
   - Best for: All dichromacy types, especially tritanopia
   - Canonical local cache: `papers/downloads/algorithms/Brettel_1997_Dichromat_Simulation.pdf`

2. **"Digital video colourmaps for checking the legibility of displays by dichromats"** (Vienot et al., 1999)
   - Simpler algorithm for protanopia/deuteranopia
   - Better handling of extreme values
   - Canonical local cache: `papers/downloads/algorithms/Vienot_1999_Digital_Colourmaps.pdf`

3. **"A Physiologically-based Model for Simulation of Color Vision Deficiency"** (Machado et al., 2009)
   - Canonical local cache: `papers/downloads/algorithms/Machado_2009_CVD_Simulation.pdf`
   - Journal: IEEE TVCG
   - URL: https://ieeexplore.ieee.org/document/5290741/
   - PDF: https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/Machado_Oliveira_Fernandes_CVD_Vis2009_final.pdf
   - Method: Incorporates opponent-color theory (stage theory)
   - Unique capability: Simulates anomalous trichromacy (not just dichromacy)
   - Local copy: Not distributed (copyright); obtain via DOI or institutional access

### Recent Research (2025)

4. **"Evaluating the accuracy of color vision deficiency simulation: Methodologies and a comparative analysis of current models"**
   - Journal: Optics Communications (May 2025)
   - URL: https://www.sciencedirect.com/science/article/abs/pii/S0030401825004894
   - Finding: Machado and Yaguchi models significantly outperform Yang model; stage theory dominates simulation accuracy

### Implementation Resources

- **DaltonLens Guide:** https://daltonlens.org/understanding-cvd-simulation/
- **Myndex CVD Simulator:** https://www.myndex.com/CVD/

### Color Space Transformation

Proper CVD simulation requires:

1. **sRGB to Linear RGB:** Remove gamma correction
2. **Linear RGB to XYZ:** Standard sRGB matrix
3. **XYZ to LMS:** Smith-Pokorny, Bradford, or Hunt-Pointer-Estevez matrix

**Important:** Many implementations incorrectly apply LMS transformations directly to gamma-corrected sRGB values, producing inaccurate results.

### Cone Fundamentals

Standard cone spectral sensitivities:

- **Stockman & Sharpe (2000):** CIE-sanctioned "physiologically-relevant" standards
- **Smith & Pokorny:** Historical reference (flawed at short wavelengths)
- **CVRL Database:** http://www.cvrl.org/cones.htm

Recent publication:
- **"Formulae for generating standard and individual human cone spectral sensitivities"** (Stockman et al., 2024)
  - URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10946592/

---

## Daltonization and Recoloring Algorithms

### Definition

Daltonization is the process of modifying images to improve color discrimination for CVD observers while maintaining naturalness for normal vision observers.

### Key Design Principles

1. **Color Contrast:** Enhanced distinguishability
2. **Color Consistency:** Preserve relative relationships
3. **Color Naturalness:** Minimize unnatural appearance

### Recent Research (2023-2025)

#### NVIDIA Research (2023)

1. **"Luminance-Preserving and Temporally Stable Daltonization"**
   - Authors: Ebelin, Crassin, Denes, Oskarsson, Astrom, Akenine-Moller
   - Conference: Eurographics 2023
   - URL: https://research.nvidia.com/publication/2023-05_daltonization
   - URL: https://diglib.eg.org/items/fc9b3da1-606d-40f4-808f-aa2e319f39d9
   - Performance: **0.2 ms per frame on GPU**
   - Features: Real-time, luminance-preserving, temporally stable

#### Deep Learning Approaches (2023-2024)

2. **"Image recoloring for color vision deficiency compensation using Swin transformer"** (2024)
   - URL: https://link.springer.com/article/10.1007/s00521-023-09367-2
   - Approach: Swin Transformer architecture
   - Goals: Contrast enhancement + naturalness preservation

3. **"Personalized Image Generation for Color Vision Deficiency Population"** (ICCV 2023)
   - URL: https://openaccess.thecvf.com/content/ICCV2023/papers/Jiang_Personalized_Image_Generation_for_Color_Vision_Deficiency_Population_ICCV_2023_paper.pdf
   - Focus: Personalized generation based on individual CVD characteristics

4. **"ColorAssist"** (2024)
   - Features: FZU-CVDSet dataset (first large-scale CVD-individual-labeled dataset)
   - Modules: Perception-guided feature extraction + diffusion transformer

#### Interactive Recognition And Reconstruction (2024-2025)

5. **"Computational Trichromacy Reconstruction: Empowering the Color-Vision Deficient to Recognize Colors Using Augmented Reality"** (2024)
   - Conference: UIST 2024
   - DOI: 10.1145/3654777.3676415
   - Canonical local cache: `papers/downloads/color_vision/Zhu_2024_Computational_Trichromacy_Reconstruction_AR.pdf`
   - Key contribution: distinguishes color recognition from mere discrimination and uses interactive temporal color shifts to create a learnable extra cue for dichromats
   - Study structure: psychophysics on 16 CVD participants and a 9-day longitudinal study on 8 participants

6. **"A Computational Framework for Modeling Emergence of Color Vision in the Human Brain"** (2025)
   - Venue: ICLR 2025 (oral)
   - URL: https://openreview.net/forum?id=g3xuCtrG6H
   - Canonical local cache: `papers/downloads/color_vision/Kotani_2025_Color_Vision_Emergence_Framework.pdf`
   - Key contribution: models color vision as an emergent N-dimensional cortical representation inferred from optic nerve signals rather than a fixed trichromatic assumption
   - Practical relevance: informs restoration and enhancement framing, but is not itself a direct accessibility intervention paper

#### Machine Learning for Ishihara Enhancement (2025)

5. **"Enhancing Ishihara and educational images using machine learning"**
   - Journal: Frontiers in Artificial Intelligence
   - URL: https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1676644/full
   - Results: One-vs-All strategy achieved 99.7% accuracy; recognition improved from <20% to full visibility

### Algorithm Categories

| Category | Description | Impact |
|----------|-------------|--------|
| LMS Daltonization | Works in LMS color space | Moderate effect |
| Color Contrast Enhancement | Maximizes contrast | Highest CVD benefit, most change |
| LAB Color Adjustment | Works in CIELAB space | Smallest effect |

### Content-Dependent vs Content-Independent

- **Content-Independent:** Global pixel processing; may not ensure contrast for confused colors
- **Content-Dependent:** Considers image content and spatial location; better results

---

## Accessibility Design Guidelines

### WCAG 2.2 Requirements

#### Contrast Ratios

| Level | Normal Text | Large Text | Non-text Elements |
|-------|-------------|------------|-------------------|
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | N/A |

**Large text definition:** 18pt regular or 14pt bold (approximately 24px or 18.5px)

#### Contrast Ratio Formula

```
Contrast Ratio = (L1 + 0.05) / (L2 + 0.05)
```

Where L1, L2 are relative luminances (lighter/darker):

```
L = 0.2126 * R + 0.7152 * G + 0.0722 * B

For each channel:
  if (sRGB <= 0.03928):
    value = sRGB / 12.92
  else:
    value = ((sRGB + 0.055) / 1.055) ^ 2.4
```

**Important:** Values should NOT be rounded (e.g., 4.499:1 does not meet 4.5:1)

### Key Guidelines

1. **Never rely on color alone** (WCAG 1.4.1)
   - Add text labels, patterns, shapes, or icons
   - Use asterisks for required fields, not just red color

2. **Avoid problematic color combinations:**
   - Green + Black
   - Blue + Gray
   - Green + Blue
   - Green + Brown
   - Green + Gray
   - Blue + Purple
   - Light Green + Yellow
   - Green + Red

3. **Safe color combinations:**
   - Blue + Orange
   - Blue + Red
   - Any two colors with different lightness values

4. **Use patterns and textures** in charts and graphs

5. **Offer colorblind modes** with customization options

### Resources

- **Smashing Magazine Guide:** https://www.smashingmagazine.com/2024/02/designing-for-colorblindness/
- **WCAG 2025 Contrast Guide:** https://www.allaccessible.org/blog/color-contrast-accessibility-wcag-guide-2025
- **WebAIM Contrast Checker:** https://webaim.org/resources/contrastchecker/

### Legal Context (2024-2025)

- **83.6% of websites** fail color contrast requirements (WebAIM 2024)
- **4,605 ADA lawsuits** filed in 2024
- **European Accessibility Act** in force since June 28, 2025

### Industry Examples

- **Trello:** Colorblind Friendly mode with textured label overlays (2014)
- **Microsoft:** Colorblind-friendly designs across platforms
- **UpWork/Royal Bank of Canada:** Worked with accessibility experts

---

## Open Datasets and Resources

### CVD Simulation and Recoloring Datasets

1. **CVD GAN Dataset**
   - Training: 2,313 image pairs
   - Testing: 771 image pairs
   - Total: 3,084 image pairs
   - Method: Improved Octree Quantization Method (IOQM)
   - GitHub: https://github.com/doubletry/pix2pix
   - GitHub: https://github.com/doubletry/CycleGAN
   - GitHub: https://github.com/doubletry/BicycleGAN
   - Paper: "Color vision deficiency datasets & recoloring evaluation using GANs"
   - URL: https://link.springer.com/article/10.1007/s11042-020-09299-2

2. **FZU-CVDSet** (mentioned in ColorAssist research)
   - First large-scale CVD-individual-labeled dataset
   - Labeled by actual CVD individuals

3. **ColorBlindnessEval Benchmark**
   - 500 Ishihara-like images (numbers 0-99)
   - Generated via Monte Carlo method
   - Purpose: Evaluate VLM robustness
   - GitHub: https://github.com/icfaust/IshiharaMC

### Color Vision Test Resources

1. **Ishihara Test**
   - Original: 38 plates edition (1917)
   - Online version: https://www.color-blindness.com/ishihara-38-plates-cvd-test/

2. **Farnsworth-Munsell Tests**
   - D-15: 15 color hues (screening)
   - FM 100: 100 color hues (detailed assessment)
   - D-15 desaturated (Lanthony, 1974)
   - Digital versions available but require calibrated displays

3. **Cambridge Colour Test**
   - Computer-based pseudoisochromatic test
   - Images generated randomly (cannot be memorized)

4. **DIVE Color Test** (2024)
   - New digital automated test
   - Measures protan, deutan, tritan axes
   - Validated against Ishihara and FM-100
   - Paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC10888327/

5. **FInD (Foraging Interactive D-prime)** (2024)
   - Novel computer-based, rapid, self-administered tool
   - Quantifies CVD type and severity
   - Paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC10592291/

### Cone Fundamental Data

- **CVRL Database:** http://www.cvrl.org/cones.htm
- **Stockman & Sharpe (2000):** CIE standard cone fundamentals
- Formats: ASCII CSV, XML, HTML tables, graphical plots

---

## Color Vision Testing

### Anomaloscope (Gold Standard)

The Rayleigh match test definitively diagnoses inherited red-green CVD:

- **Principle:** Match mixture of 545nm + 670nm to 589nm yellow
- **Normal range:** 34-46 units (Oculus HMC)
- **Protanomalous:** Require more red (670nm) in mixture; reduced luminance match
- **Deuteranomalous:** Require more green; normal luminance match
- **Dichromats:** Accept any mixture ratio

### Severity Assessment

- Matching range width indicates severity
- Larger range = more severe defect
- Extreme anomaly may be difficult to distinguish from dichromacy

### Aviation Standards (EASA)

| Condition | CAD Test Threshold |
|-----------|-------------------|
| Deuteranomaly | < 6 SN |
| Protanomaly | < 12 SN |
| Tritanomaly | > 2 SN |

### Recent Research on Digital Testing (2024)

- **"The D15 color arrangement test retains its diagnostic value"** (November 2024)
  - URL: https://www.medrxiv.org/content/10.1101/2024.11.15.24314633v1.full
  - Finding: D15 test remains valid even without perfectly calibrated displays
  - Evaluated 627,431 arrangements across various screen types

---

## Open Source Tools and Libraries

### CVD Simulation Libraries

1. **DaltonLens / libDaltonLens**
   - Language: C (single-file, public domain)
   - GitHub: https://github.com/DaltonLens/libDaltonLens
   - Algorithms: Brettel 1997, Vienot 1999
   - Documentation: https://daltonlens.org/opensource-cvd-simulation/

2. **colorspace (R package)**
   - URL: http://colorspace.r-forge.r-project.org/reference/simulate_cvd.html
   - Implements: CVD simulation with proper sRGB handling

3. **cmweather (Python)**
   - GitHub: https://github.com/openradar/cmweather
   - Purpose: CVD-friendly colormaps for weather/climate visualization
   - Install: `pip install cmweather` or `mamba install cmweather`
   - Paper: Sherman et al. (2024), Bull. Amer. Meteor. Soc.

4. **colorBlindness (R package)**
   - CRAN: https://cran.r-project.org/web/packages/colorBlindness/
   - Purpose: Safe color palettes for plots

5. **Color_Blindness_Toolkit**
   - GitHub: https://github.com/bhav09/Color_Blindness_Toolkit

### Online Simulators

1. **Coblis (Color Blindness Simulator)**
   - URL: https://www.color-blindness.com/coblis-color-blindness-simulator/

2. **DaltonLens Online Simulator**
   - URL: https://daltonlens.org/colorblindness-simulator

3. **Myndex Brettel/Vienot CVD Simulator**
   - URL: https://www.myndex.com/CVD/

### Contrast Checking Tools

1. **WebAIM Contrast Checker**
   - URL: https://webaim.org/resources/contrastchecker/

2. **Siege Media Contrast Ratio**
   - URL: https://www.siegemedia.com/contrast-ratio

3. **ColorContrast.app**
   - URL: https://colorcontrast.app/

### Browser Extensions

- **Colorblindly:** Chrome extension for CVD simulation

### Design Tool Plugins

- **Stark:** Plugin for Sketch, Adobe XD, Figma
- **Accessible Color Palette Builder**

---

## References

### Foundational Papers (Algorithms)

1. Brettel, H., Vienot, F., & Mollon, J. D. (1997). Computerized simulation of color appearance for dichromats. *Journal of the Optical Society of America A*, 14(10), 2647-2655.

2. Vienot, F., Brettel, H., & Mollon, J. D. (1999). Digital video colourmaps for checking the legibility of displays by dichromats. *Color Research & Application*, 24(4), 243-252.

3. Machado, G. M., Oliveira, M. M., & Fernandes, L. A. (2009). A physiologically-based model for simulation of color vision deficiency. *IEEE Transactions on Visualization and Computer Graphics*, 15(6), 1291-1298.

### 2024-2025 Key Publications

4. Frontiers in Neuroscience. (2024). Dyschromatopsia: a comprehensive analysis of mechanisms and cutting-edge treatments for color vision deficiency. https://doi.org/10.3389/fnins.2024.1265630

5. Vision Research. (2023). Blue cone monochromacy and gene therapy. https://doi.org/10.1016/j.visres.2023.108196

6. Optics Communications. (2025). Evaluating the accuracy of color vision deficiency simulation: Methodologies and a comparative analysis of current models.

7. NVIDIA Research. (2023). Luminance-Preserving and Temporally Stable Daltonization. Eurographics 2023.

8. Stockman, A., et al. (2024). Formulae for generating standard and individual human cone spectral sensitivities. *Color Research & Application*.

9. Zhu, Y., Chen, E., Hascup, C., Yan, Y., & Sharma, G. (2024). Computational trichromacy reconstruction: Empowering the color-vision deficient to recognize colors using augmented reality. *UIST 2024*. DOI: 10.1145/3654777.3676415

10. Kotani, A., & Ng, R. (2025). A computational framework for modeling emergence of color vision in the human brain. *ICLR 2025*. https://openreview.net/forum?id=g3xuCtrG6H

### Accessibility Standards

11. W3C. (2023). Web Content Accessibility Guidelines (WCAG) 2.2. https://www.w3.org/TR/WCAG22/

---

## 2025-2026 Research Updates

### CVD Simulation Model Accuracy (2025)

A 2025 study evaluated the accuracy of existing CVD simulation models using a novel
methodology based on quantified color vision tests administered to both color-deficient
observers (CDOs) and color-normal observers (CNOs) viewing simulated images:
- **Machado (2009)** and **Yaguchi** models significantly outperform the Yang model
- Evaluation method compares CDO test results on original colors vs. CNO results on simulated colors
- Confirms Machado as the strongest general-purpose simulator for anomalous trichromacy

**Source**: "Evaluating the accuracy of color vision deficiency simulation:
Methodologies and a comparative analysis of current models." *Optics Communications*, 2025.

### Gene Therapy Clinical Trials

#### Achromatopsia (CNGA3/CNGB3)

Five registered gene therapy clinical trials for achromatopsia as of mid-2025:

| Trial | Gene | Phase | Sponsor | Status |
|-------|------|-------|---------|--------|
| NCT02610582 | CNGA3 | I/II | STZ/RD-CURE | Completed |
| NCT03758404 | CNGA3 | I/II | AGTC | Results reported |
| NCT03001310 | CNGB3 | I/II | MeiraGTx | Phase I/II complete |
| NCT02935517 | CNGB3 | I/II | AGTC | Results reported |
| Lonfat et al. 2025 | Review | -- | Multiple | Survey paper |

**Key findings (AGTC, 2025)**:
- CNGB3 therapy: 2 adults + 2 pediatric patients showed improved retinal sensitivity
  at second-highest dose; improvements in light discomfort also observed
- CNGA3 therapy: No consistent evidence of biologic activity
- Hypothesis: CNGA3 patients have defective protein that may interfere with therapeutic
  protein function, while CNGB3 patients have no protein expressed

**Key findings (MeiraGTx)**:
- AAV8-hCARp.hCNGB3 delivered subretinally was safe and well tolerated
- No consistent efficacy at 24 weeks, though some participants showed trends
  in color vision and photo-aversion improvement

#### Blue Cone Monochromacy (BCM)

- **CIRM grant**: $4.7M awarded to Blue Gen Therapeutics / Children's Hospital LA (2024)
- **BGTF-027**: Intravitreal gene therapy encoding functional L-opsin; Phase 1
  clinical trial protocol being developed (announced July 2025)
- **ADVM-062**: Adverum Biotechnologies' intravitreal AAV.7m8 vector for sustained
  L-opsin expression (preclinical)
- **Treatment window study (2025)**: Communications Biology published research on
  molecular mechanisms limiting the AAV gene therapy treatment window in BCM mouse
  models, informing optimal patient age for intervention

**Source**: Lonfat, N., Moreno-Leon, L., Punzo, C., & Khanna, H. (2025).
"Update on Gene Therapy Clinical Trials for Eye Diseases." *Human Gene Therapy*.
DOI: 10.1177/10430342251379824

### Daltonization Advances

#### NVIDIA Luminance-Preserving Daltonization (2023)

Ebelin et al. proposed a real-time daltonization algorithm that:
- Preserves luminance (unlike Fidaner method which can shift brightness)
- Provides temporal stability (no flickering during camera movement)
- Runs in 0.2 ms/frame on GPU
- Outperforms Machado-Oliveira and Huang et al. methods for temporal consistency

**Citation**: Ebelin, P., Crassin, C., Denes, G., Oskarsson, M., Astrom, K., &
Akenine-Moller, T. (2023). "Luminance-Preserving and Temporally Stable
Daltonization." *Eurographics 2023 Short Papers*.

#### Deep Learning Daltonization (2025)

- Pix2Pix GAN-based recoloring achieving naturalistic output
- Swin Transformer approach for CVD compensation (Springer, 2023)
- ResNet-50/EfficientNet/DenseNet feature embeddings with PCA fusion achieving
  99.7% accuracy (OvA) and 100% (MLP) for Ishihara enhancement
- Optimal daltonization parameters: alpha=0.54 (deuteranopia), 0.64 (protanopia)
- Survey with 15 diagnosed students: recognition of previously unreadable digits
  increased from <20% to full visibility

**Source**: "Enhancing Ishihara and educational images using machine learning."
*Frontiers in Artificial Intelligence*, 2025. DOI: 10.3389/frai.2025.1676644

### Interactive Color Recognition And AR Assistance

Zhu et al. (UIST 2024) add an important distinction that static recoloring
papers often blur: helping users discriminate colors is not the same as helping
them recognize and name those colors in real tasks.

Key repo-relevant takeaways:

- The system augments a dichromat's native 2D percept with a third, learned cue
  via swipe-controlled temporal color shifts.
- The paper reports both psychophysical discrimination gains and task-level
  color-recognition benefits in Lego-building and art-interpretation scenarios.
- For OpenPerception, some accommodations should be evaluated against naming and
  task completion, not only against pairwise color separability.

**Canonical local cache**:
`papers/downloads/color_vision/Zhu_2024_Computational_Trichromacy_Reconstruction_AR.pdf`

### Computational Models Of Color-Vision Emergence

Kotani and Ng (ICLR 2025) broaden the conceptual frame for the repo by treating
color vision as an emergent cortical representation whose dimensionality must be
inferred from optic nerve signals.

Key repo-relevant takeaways:

- The framework naturally recovers 1D, 2D, 3D, and 4D color representations
  depending on the number of photoreceptor classes in the simulated retina.
- It helps separate today's accessibility questions from longer-horizon
  restoration or enhancement questions, including gene-therapy-linked shifts in
  color dimensionality.
- For repo writing, it supports avoiding language that treats trichromacy as
  the only natural endpoint of color perception while still keeping current UI
  accommodations grounded in today's users.

**Canonical local cache**:
`papers/downloads/color_vision/Kotani_2025_Color_Vision_Emergence_Framework.pdf`

### ChromATA: Real-Time CVD Processing (2025)

ChromATA (Chromatic Accessibility Through Adaptation) is a real-time image processing
system for CVD simulation and accommodation, extending Machado 2009 with GPU shader
support for real-time rendering applications.

**Source**: IJSRC, 2025.

### WCAG 3.0 and APCA Status (2025-2026)

- WCAG 3.0 remains in Working Draft as of August 2025
- APCA (Accessible Perceptual Contrast Algorithm) is NOT yet in the published draft
- APCA produces Lightness Contrast (LC) scores 0-100+ instead of ratios
- LC thresholds are context-dependent (body text ~60, headlines ~45)
- WCAG WG charter targets Q2/2026 for completion (considered optimistic)
- WCAG 2.2 remains the current recommendation

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-27 | 1.0 | Initial comprehensive report |
| 2026-03-19 | 1.1 | Added 2025-2026 research updates: simulation accuracy study, gene therapy trials, NVIDIA daltonization, deep learning approaches, WCAG 3.0/APCA status |
| 2026-03-25 | 1.2 | Added canonical color-vision source synthesis for AR color recognition and computational color-vision emergence modeling |

---

*This report is part of the Colorblindness Accessibility Research Repository.*
