# Comprehensive Compendium of Colorblindness Simulation and Correction Algorithms

## Table of Contents
1. [Color Vision Simulation Algorithms](#1-color-vision-simulation-algorithms)
2. [Daltonization and Color Correction Algorithms](#2-daltonization-and-color-correction-algorithms)
3. [LMS Colorspace and Cone Fundamentals Research](#3-lms-colorspace-and-cone-fundamentals-research)
4. [Color Universal Design Papers](#4-color-universal-design-papers)
5. [Accessibility Tools and Methods](#5-accessibility-tools-and-methods)
6. [Open Source Implementations](#6-open-source-implementations)
7. [Color Vision Testing Research](#7-color-vision-testing-research)

---

## 1. Color Vision Simulation Algorithms

### 1.1 Brettel, Vienot, Mollon (1997) - The Foundational Algorithm

**Title:** Computerized simulation of color appearance for dichromats

**Authors:** Hans Brettel, Francoise Vienot, John D. Mollon

**Year:** 1997

**Publication:** Journal of the Optical Society of America A, Vol. 14, No. 10, pp. 2647-2655

**DOI:** 10.1364/JOSAA.14.002647

**Direct PDF:** https://vision.psychol.cam.ac.uk/jdmollon/papers/Dichromat_simulation.pdf

**Description:** This seminal paper proposes an algorithm that transforms digitized color images to simulate the appearance for dichromatic observers. The algorithm represents color stimuli as vectors in a three-dimensional LMS space and replaces each stimulus by its projection onto a reduced stimulus surface. This surface is defined by a neutral axis and the LMS locations of monochromatic stimuli perceived as the same hue by normal trichromats and dichromats. For protan/deutan simulations, wavelengths of 475nm (blue) and 575nm (yellow) are used; for tritan, 485nm (blue-green) and 660nm (red).

**PubMed:** https://pubmed.ncbi.nlm.nih.gov/9316278/

**Optica:** https://opg.optica.org/josaa/abstract.cfm?uri=josaa-14-10-2647

---

### 1.2 Vienot, Brettel, Mollon (1999) - Simplified Matrix Method

**Title:** Digital Video Colourmaps for Checking the Legibility of Displays by Dichromats

**Authors:** Francoise Vienot, Hans Brettel, John D. Mollon

**Year:** 1999

**Publication:** Color Research and Application, Vol. 24, No. 4, pp. 243-252

**Direct PDF:** https://vision.psychol.cam.ac.uk/jdmollon/papers/colourmaps.pdf

**Description:** This follow-up paper simplifies the 1997 algorithm by using a single diagonal plane (black-white-blue-yellow) for protanopia and deuteranopia cases. This allows the projection to be expressed as a single 3x3 matrix, reducing the full simulation pipeline to a single matrix multiplication. The method is computationally faster while maintaining similar accuracy for protan and deutan simulations.

---

### 1.3 Machado, Oliveira, Fernandes (2009) - Physiologically-Based Model

**Title:** A Physiologically-based Model for Simulation of Color Vision Deficiency

**Authors:** Gustavo M. Machado, Manuel M. Oliveira, Leandro A. F. Fernandes

**Year:** 2009

**Publication:** IEEE Transactions on Visualization and Computer Graphics, Vol. 15, No. 6, pp. 1291-1298

**DOI:** 10.1109/TVCG.2009.113

**Direct PDF:** https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/Machado_Oliveira_Fernandes_CVD_Vis2009_final.pdf

**Companion Website:** https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html

**Description:** This model is based on the stage theory of human color vision and derived from electrophysiological studies. It is the first model to consistently handle normal color vision, anomalous trichromacy, and dichromacy in a unified way. The simulation uses a single matrix multiplication, with pre-computed matrices available for severity levels from 0 (normal) to 1 (complete dichromacy) in 0.1 increments. The model was validated through experimental evaluation with color vision deficient individuals.

---

### 1.4 Meyer & Greenberg (1988) - First Computer Graphics Algorithm

**Title:** Color-defective vision and computer graphics displays

**Authors:** Gary W. Meyer, Donald P. Greenberg

**Year:** 1988

**Publication:** IEEE Computer Graphics and Applications, Vol. 8, No. 5, pp. 28-40

**Description:** This was the first paper to propose an actual algorithm to simulate color vision deficiency, working in the CIE XYZ color space. While foundational, later work by Vienot et al. noted that working in XYZ is suboptimal as it does not account for altered luminosity perception in dichromats. This work inspired the Vischeck implementation.

---

### 1.5 Recent Validation Studies

**Title:** Evaluating the accuracy of color vision deficiency simulation: Methodologies and a comparative analysis of current models

**Year:** 2025

**Publication:** Optics Communications (ScienceDirect)

**URL:** https://www.sciencedirect.com/science/article/abs/pii/S0030401825004894

**Description:** Proposes an accuracy evaluation method for CVD simulation models validated through experiments comparing color deficient observers performing original color vision tests and color normal observers performing simulated ones.

---

## 2. Daltonization and Color Correction Algorithms

### 2.1 Fidaner, Lin, Ozguven (2005) - Original Daltonization

**Title:** Analysis of Color Blindness

**Authors:** Onur Fidaner, Poliang Lin, Nevran Ozguven

**Year:** 2005

**Website:** http://www.daltonize.org/2010/05/lms-daltonization-algorithm.html

**Description:** The foundational daltonization algorithm that adjusts colors to improve perception for colorblind individuals. The process involves: (1) RGB to LMS conversion, (2) simulation of color blindness, (3) calculation of error/difference, (4) application of error modification matrix to shift colors toward visible spectrum, (5) LMS to RGB conversion. This algorithm has become the basis for most daltonization implementations.

---

### 2.2 Kuhn, Oliveira, Fernandes (2008) - Naturalness-Preserving Recoloring

**Title:** An Efficient Naturalness-Preserving Image-Recoloring Method for Dichromats

**Authors:** Giovane R. Kuhn, Manuel M. Oliveira, Leandro A. F. Fernandes

**Year:** 2008

**Publication:** IEEE Transactions on Visualization and Computer Graphics, Vol. 14, No. 6, pp. 1747-1754

**URL:** https://www.researchgate.net/publication/23456246_An_Efficient_Naturalness-Preserving_Image-Recoloring_Method_for_Dichromats

**Description:** Presents an efficient and automatic image-recoloring technique for dichromats that preserves image naturalness while highlighting important visual details. Uses a mass-spring system to optimize color distances in CIE L*a*b* color space. The approach is about three orders of magnitude faster than previous methods.

---

### 2.3 Image Recoloring Survey (2021)

**Title:** Image recoloring for color vision deficiency compensation: a survey

**Authors:** Various

**Year:** 2021

**Publication:** The Visual Computer

**URL:** https://link.springer.com/article/10.1007/s00371-021-02240-0

**Description:** Comprehensive survey reviewing representative existing recoloring methods, categorizing them according to methodological characteristics, and summarizing evaluation metrics. Key requirements identified: preservation of color naturalness and preservation/enhancement of color contrast.

---

### 2.4 Novel Image Recoloring Approach (2021)

**Title:** A Novel Approach to Image Recoloring for Color Vision Deficiency

**Year:** 2021

**Publication:** MDPI Sensors

**DOI/URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8069325/

**Description:** Proposes a novel method to modify color images for protanopia and deuteranopia with criteria including preserving image naturalness and color contrast enhancement. Uses four algorithmic modules.

---

### 2.5 Swin Transformer for CVD Compensation (2024)

**Title:** Image recoloring for color vision deficiency compensation using Swin transformer

**Year:** 2024

**Publication:** Neural Computing and Applications

**URL:** https://link.springer.com/article/10.1007/s00521-023-09367-2

**Description:** Uses deep neural network with a loss function considering naturalness and contrast. Introduces unsupervised training approach and a new dataset for training DNN models for CVD compensation.

---

## 3. LMS Colorspace and Cone Fundamentals Research

### 3.1 Smith & Pokorny (1975) - Classic Cone Fundamentals

**Title:** Spectral sensitivity of the foveal cone photopigments between 400 and 500 nm

**Authors:** Vivianne C. Smith, Joel Pokorny

**Year:** 1975

**Publication:** Vision Research, Vol. 15, pp. 161-171

**CVRL Database:** http://www.cvrl.org/database/text/cones/sp.htm

**Description:** Established the Smith & Pokorny 2-deg cone fundamentals based on the CIE Judd-Vos 2-deg CMFs. These fundamentals are derived from the Judd CMFs published in 1951. Note: L(lambda)+M(lambda) = V(lambda), meaning the sum of L and M cone fundamentals equals the luminosity function.

---

### 3.2 Stockman & Sharpe (2000) - CIE Standard Cone Fundamentals

**Title:** Spectral sensitivities of the middle- and long-wavelength sensitive cones derived from measurements in observers of known genotype

**Authors:** Andrew Stockman, Lindsay T. Sharpe

**Year:** 2000

**Publication:** Vision Research, Vol. 40, pp. 1711-1737

**CIE Standard:** CIE 170-1:2006 "Fundamental Chromaticity Diagram with Physiological Axes"

**CVRL Website:** http://www.cvrl.org/

**Description:** These physiologically-based LMS functions were adopted by CIE in 2006 as the standard cone fundamentals. The functions are derived from Stiles and Burch RGB CMF data combined with newer measurements about cone contributions. Both LMS and XYZ versions are defined for 2-deg and 10-deg vision.

---

### 3.3 Stockman (2023) - Formulae for Cone Sensitivities

**Title:** Formulae for generating standard and individual human cone spectral sensitivities

**Authors:** Andrew Stockman

**Year:** 2023

**Publication:** Color Research & Application (Wiley)

**URL:** https://onlinelibrary.wiley.com/doi/full/10.1002/col.22879

**Description:** Presents practical formulae for generating cone fundamentals for standard observers for 2-deg and 10-deg vision that accurately reproduce the CIE 2006 observer. Extends from 390nm to 360nm at short wavelengths and 830nm to 850nm at long wavelengths. Allows modeling of individual differences in macular, lens, and photopigment optical densities.

---

### 3.4 Hunt-Pointer-Estevez Matrix

**Description:** The Hunt-Pointer-Estevez (HPE) transformation matrix is used for conversion from CIE XYZ to LMS in the Hunt and RLAB color appearance models. Also called the von Kries transformation matrix.

**HPE Matrix (normalized to D65):**
```
M_HPE = [  0.4002   0.7076  -0.0808 ]
        [ -0.2263   1.1653   0.0457 ]
        [  0        0        0.9182 ]
```

**Reference:** https://en.wikipedia.org/wiki/LMS_color_space

---

### 3.5 Cone Response Transformation Research

**Title:** A new transformation of cone responses to opponent color responses

**Year:** 2021

**Publication:** PubMed/PMC

**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8084791/

**Description:** Discusses the transformation from LMS cone responses to r-g, y-b opponent color chromatic responses. Traditional coding: L-M gives r-g, while (L+M)-S gives y-b.

---

## 4. Color Universal Design Papers

### 4.1 Okabe & Ito - Color Universal Design Guidelines

**Title:** Color Universal Design (CUD): How to Make Figures and Presentations that are Friendly to Colorblind People

**Authors:** Masataka Okabe, Kei Ito

**Year:** 2008

**Source:** J*Fly Data Depository for Drosophila researchers

**Description:** One of the most cited resources for creating colorblind-accessible figures. Offers "3(+1) Principles of Color Universal Design," with the first principle being to choose color schemes that can be easily identified by people with all types of color vision.

---

### 4.2 Viridis Color Maps

**Title:** Introduction to the viridis color maps

**Authors:** Stefan van der Walt, Nathaniel Smith (original), Jamie R. Nunez et al. (cividis)

**R Package:** https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html

**Description:** Provides perceptually-uniform, colorblind-friendly color maps including viridis, magma, plasma, inferno, cividis, mako, rocket, and turbo. The viridis scale makes maximum use of available color space while maintaining uniformity. Works well for deuteranopia and protanopia; less optimal for tritanopia (rare).

---

### 4.3 ColorBrewer

**Authors:** Cynthia Brewer

**Website:** https://colorbrewer2.org/

**Description:** Interactive tool for selecting colorblind-friendly palettes. Includes diverging palettes (BrBG, PiYG, PRGn, PuOr, RdBu, RdYlBu), qualitative palettes (Dark2, Paired, Set2), and numerous sequential palettes. All palettes are included in matplotlib and seaborn.

---

### 4.4 CHI 2022 - Large Scale Accessibility Study

**Title:** Accessibility for Color Vision Deficiencies: Challenges and Findings of a Large Scale Study on Paper Figures

**Year:** 2022

**Publication:** CHI Conference on Human Factors in Computing Systems

**URL:** https://dl.acm.org/doi/abs/10.1145/3491102.3502133

**Description:** Based on 1,710 images sampled from VIS30K visualization dataset over five years. Simulated four CVD types on each image. Found approximately 60% of images were rated accessible. Indicates accessibility issues are subjective and hard to detect.

---

### 4.5 WCAG Guidelines

**Title:** WCAG 2.1 Success Criterion 1.4.1: Use of Color

**URL:** https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html

**Description:** Level A requirement stating color must not be the only visual means of conveying information. Contrast requirements: 4.5:1 for normal text, 3:1 for large text (Level AA); 7:1 and 4.5:1 for Level AAA.

---

## 5. Accessibility Tools and Methods

### 5.1 Web Accessibility Research

**Title:** Investigating Color-Blind User-Interface Accessibility via Simulated Interfaces

**Year:** 2024

**Publication:** MDPI Computers

**arXiv:** https://arxiv.org/abs/2401.10357

**Description:** Examines how WCAG guidelines impact perceived user functionality and aesthetic look for CVD users. Results indicate UIs relying on color to distinguish icons or indicate errors are harder to use for CVD users.

---

### 5.2 Quantitative Web Accessibility Assessment

**Title:** A novel heuristic method for quantitative assessment of web accessibility for colorblind

**Year:** 2023

**Publication:** Universal Access in the Information Society

**URL:** https://link.springer.com/article/10.1007/s10209-023-01006-w

**Description:** Proposes a novel heuristic method to evaluate compliance with WCAG guidelines through a web accessibility score. Evaluated websites from four categories with respect to color blindness disability.

---

### 5.3 Color Vision Devices Meta-Analysis

**Title:** Color vision devices for color vision deficiency patients: A systematic review and meta-analysis

**Year:** 2022

**Publication:** PMC

**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9498227/

**Description:** Compares and analyzes different color vision devices (electronic and optical) for CVD patients. Included 16 research reports. Found insufficient evidence to support that current devices improve color perception.

---

### 5.4 Design Resources Scoping Review

**Title:** Designing for Colour Vision Deficiency: A Scoping Review of Resources That Support Designers in Choosing Accessible Colours

**Year:** 2024

**Publication:** ResearchGate

**URL:** https://www.researchgate.net/publication/394501320

**Description:** Scoping review of 113 academic papers on CVD-accessibility design methods. Found lack of variety in methods; most tools simulate CVD but rarely help explore alternatives or generate accessible palettes.

---

## 6. Open Source Implementations

### 6.1 DaltonLens Project

**libDaltonLens (C):**
- URL: https://github.com/DaltonLens/libDaltonLens
- Description: Single-file, public domain, zero-dependency C library implementing CVD simulation algorithms. Unit tested against reference implementations.

**DaltonLens-Python:**
- URL: https://github.com/DaltonLens/DaltonLens-Python
- Description: R&D companion package supporting Vienot 1999, Brettel 1997, and Machado 2009 models.

**Online Simulator:** https://daltonlens.org/colorblindness-simulator

**Technical Documentation:**
- Understanding LMS-based CVD Simulations: https://daltonlens.org/understanding-cvd-simulation/
- Review of Open Source Simulations: https://daltonlens.org/opensource-cvd-simulation/
- SVG Filters for CVD Simulation: https://daltonlens.org/cvd-simulation-svg-filters/

---

### 6.2 JavaScript Implementations

**jsColorblindSimulator:**
- URL: https://github.com/MaPePeR/jsColorblindSimulator
- Demo: https://mapeper.github.io/jsColorblindSimulator/
- Description: Browser-based implementation of Brettel et al. (1997), adapted for modern sRGB monitors.

**@bjornlu/colorblind:**
- URL: https://github.com/bluwy/colorblind
- Description: Zero-dependencies color blindness simulation library for JavaScript.

**RGBlind:**
- URL: https://github.com/interaktivarum/rgblind
- Description: Open-source real-time color blindness simulation tool for the web.

---

### 6.3 Python Libraries

**daltonize:**
- PyPI: https://pypi.org/project/daltonize/
- GitHub: https://github.com/joergdietrich/daltonize
- Description: Simulates and corrects images for dichromatic color blindness. Works with matplotlib figures.

**colorspacious:**
- PyPI: https://pypi.org/project/colorspacious/
- Description: Colorspace conversion library including CVD simulation using Machado et al. (2009). Includes CIECAM02 implementation.

**colour-science:**
- GitHub: https://github.com/colour-science/colour
- Description: Comprehensive color science library for Python.

---

### 6.4 R Packages

**colorspace:**
- URL: http://colorspace.r-forge.r-project.org/articles/color_vision_deficiency.html
- Description: Implements Machado et al. (2009) transformation matrices. Functions: deutan(), protan(), tritan() with severity parameter.

**dichromat:**
- CRAN: https://cran.r-project.org/web/packages/dichromat/dichromat.pdf
- Description: Color schemes for dichromats.

---

### 6.5 Other Implementations

**Peacock (C++/Python):**
- URL: https://github.com/jkulesza/peacock
- Description: Command-line application to convert images for colorblind simulation.

**ColorBlindness (Processing):**
- URL: https://github.com/hx2A/ColorBlindness
- Description: Processing library for simulating color blindness.

**jupyterlab_colorblind:**
- URL: https://github.com/mattwigway/jupyterlab_colorblind
- Description: JupyterLab extension using Machado et al. (2009) matrices.

---

### 6.6 Web Tools

**Coblis:**
- URL: https://www.color-blindness.com/coblis-color-blindness-simulator/
- Description: Online CVD simulator. V2 uses HCIRN function based on jsColorblindSimulator.

**Vischeck:**
- URL: https://www.vischeck.com/
- Description: Classic online simulator inspired by Meyer & Greenberg (1988).

**Myndex CVD Simulator:**
- URL: https://www.myndex.com/CVD/
- Description: Brettel/Vienot CVD simulator.

**Toptal Color Filter:**
- URL: https://www.toptal.com/designers/colorfilter
- Description: Web page color blindness testing tool.

---

### 6.7 Browser Developer Tools

**Chrome DevTools:**
- URL: https://developer.chrome.com/docs/chromium/cvd
- Description: Built-in CVD simulation in Chrome DevTools using SVG filters.

**SVG Filter Collections:**
- hail2u/color-blindness-emulation: https://github.com/hail2u/color-blindness-emulation
- Description: SVG file containing filters for 8 types of color blindness.

**AcceCSS:**
- URL: https://lukyvj.github.io/accecss/
- Description: SCSS mixin for adding colorblindness filters.

---

## 7. Color Vision Testing Research

### 7.1 Anomaloscope and Rayleigh Match

**Nagel Anomaloscope (1907):**
- Description: Gold standard for color vision assessment. Uses Rayleigh match: observers match mixture of red (670nm) and green (546nm) to spectral yellow (589nm).

**Title:** The Nagel anomaloscope: its calibration and recommendations for diagnosis and research
- URL: https://pubmed.ncbi.nlm.nih.gov/15290149/

**Title:** Variability of Rayleigh and Moreland test results using anomaloscope in young adults
- Year: 2021
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC8139452/

---

### 7.2 Ishihara Pseudoisochromatic Plates

**Original Work:**
- Author: Shinobu Ishihara
- Year: 1917
- Description: Color vision test using pseudoisochromatic plates with randomized colored dots forming numbers visible to normal trichromats but not to those with red-green CVD.

**Accuracy Study:**
- Title: Limitation of standard pseudoisochromatic plates in identifying colour vision deficiencies when compared with genetic testing
- Year: 2022
- URL: https://onlinelibrary.wiley.com/doi/10.1111/aos.15103

---

### 7.3 Confusion Lines and Copunctal Points

**CVRL Gallery:** http://cvrl.ucl.ac.uk/gallery/Dichromat_confusions.htm

**Description:** Confusion lines are lines in color space where colors cannot be discriminated by a specific type of dichromat. Copunctal points are where confusion lines intersect, corresponding to the missing cone primary.

**Protan/Deutan:** Confuse spectral yellow-greens, yellows, oranges, and reds (540-700nm spectrum locus)

**Tritan:** Isochromatic lines converge on "blue" corner of CIE diagram

---

## Additional Resources

### CVRL (Colour & Vision Research Laboratory)
- Website: http://www.cvrl.org/
- Description: Primary source for cone fundamentals, color matching functions, and transformation matrices.

### CIE Technical Reports
- CIE 170-1:2006: Fundamental Chromaticity Diagram with Physiological Axes - Part 1
- CIE 170-2:2015: Part 2

### Google Colab Notebook
- DaltonLens Implementation Comparison: https://colab.research.google.com/github/DaltonLens/daltonlens.org/blob/master/_notebooks/2021-10-19-OpenSource-ColorBlindness-Simulations.ipynb

---

## Citation Notes

When citing colorblindness simulation algorithms:

1. **For dichromacy simulation:** Cite Brettel, Vienot, & Mollon (1997) as the foundational work
2. **For simplified matrix method:** Cite Vienot, Brettel, & Mollon (1999)
3. **For anomalous trichromacy:** Cite Machado, Oliveira, & Fernandes (2009)
4. **For daltonization:** Cite Fidaner, Lin, & Ozguven (2005) and Kuhn, Oliveira, & Fernandes (2008)
5. **For cone fundamentals:** Cite Smith & Pokorny (1975) or Stockman & Sharpe (2000) depending on application

---

## See Also

Related compendiums in this repository:

- `papers/COLORBLINDNESS_ACADEMIC_PAPERS.md` -- Epidemiology, genetics, clinical research, and gene therapy for CVD
- `papers/achromatopsia_bcm_research_compendium.md` -- Achromatopsia and blue cone monochromacy (total/rod monochromacy)
- `papers/cognitive_load_visual_processing_papers.md` -- Cognitive load in visual interfaces; working memory capacity
- `specs/EVIDENCE_MATRIX.md` -- Claims matrix citing Brettel, Vienot, and Machado algorithms (CLM-0020 through CLM-0023)

---

*Compiled: 2025-12-27*
*For: Colorblindness Research Compendium*
