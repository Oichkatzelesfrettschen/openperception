# Visual Accessibility Evidence Matrix

**Version:** 1.0.0
**Date:** 2025-12-27
**Sources:** 7 markdown compendiums, 400+ cataloged papers (PDFs not distributed due to copyright)

---

## Matrix Format

Each claim follows this structure:
- **ID**: Unique identifier (CLM-XXXX)
- **Statement**: Testable claim
- **Axis**: [chromatic|luminance|spatial|temporal|depth|cognitive]
- **UI Primitive**: Affected meaning primitives
- **Constraint**: [hard_safety|soft_comfort|performance_tradeoff]
- **Threshold**: Quantitative value if available
- **Evidence**: [standard|guideline|clinical|controlled_study|observational|model]
- **Source**: Citation with DOI/URL

---

## 1. TEMPORAL AXIS: Seizure Safety

### INV-001: Flash Frequency Limit
| Field | Value |
|-------|-------|
| ID | CLM-0001 |
| Statement | Flash frequency above 3Hz triggers seizures in susceptible individuals |
| Axis | temporal |
| UI Primitive | hazard, feedback |
| Constraint | hard_safety |
| Threshold | <= 3 flashes/second |
| Evidence | standard |
| Source | WCAG 2.3.1 - https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold |
| Notes | Danger zone 15-25Hz (peak at ~16Hz), risk range 3-60Hz. U.S. Section 508 prohibits flicker 2-55Hz |

### INV-002: Red Flash Saturation
| Field | Value |
|-------|-------|
| ID | CLM-0002 |
| Statement | Red flashes with R>=80% AND (R-G-B)>=80% are extra dangerous |
| Axis | temporal, chromatic |
| UI Primitive | hazard, feedback |
| Constraint | hard_safety |
| Threshold | R < 80% OR (R-G-B) < 80% of max |
| Evidence | standard |
| Source | ISO 9241-391:2016, WCAG 2.2 |
| Notes | Pokemon incident (1997): 685 hospitalizations from 12Hz red-blue flashing. Red excited L-cones alone without inhibition |

### INV-003: Flash Area Threshold
| Field | Value |
|-------|-------|
| ID | CLM-0003 |
| Statement | Flash area exceeding 25% of 10-degree visual field increases seizure risk |
| Axis | temporal, spatial |
| UI Primitive | hazard |
| Constraint | hard_safety |
| Threshold | < 25% of 341x256 px @ 1024x768 |
| Evidence | standard |
| Source | WCAG 2.3.1 |
| Notes | Based on 10-degree central visual field at typical viewing distance |

### INV-004: Pattern Oscillation Limit
| Field | Value |
|-------|-------|
| ID | CLM-0004 |
| Statement | Oscillating patterns with more than 5 light-dark pairs can trigger seizures |
| Axis | temporal, spatial |
| UI Primitive | hazard |
| Constraint | hard_safety |
| Threshold | < 5 light-dark pairs oscillating |
| Evidence | standard |
| Source | ITU-R BT.1702-3 |
| Notes | Pattern sensitivity often underdiagnosed (58.3% had EEGs without pattern testing) |

### CLM-0005: Cumulative Exposure Risk
| Field | Value |
|-------|-------|
| ID | CLM-0005 |
| Statement | Sequences of flashing lasting >5 seconds pose risk even below individual thresholds |
| Axis | temporal |
| UI Primitive | hazard |
| Constraint | hard_safety |
| Threshold | < 5 seconds cumulative |
| Evidence | guideline |
| Source | Ofcom Broadcasting Code |
| Notes | Cumulative effects acknowledged in ITU-R BT.1702 |

---

## 2. LUMINANCE AXIS: Contrast

### INV-005: Text Contrast Floor
| Field | Value |
|-------|-------|
| ID | CLM-0010 |
| Statement | 4.5:1 contrast compensates for 20/40 vision loss |
| Axis | luminance |
| UI Primitive | state, focus, navigation |
| Constraint | hard_safety |
| Threshold | >= 4.5:1 (normal text), >= 3:1 (large text 18pt+) |
| Evidence | standard |
| Source | WCAG 1.4.3 - https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum |
| Notes | Based on 3 x 1.5 = 4.5 to compensate for contrast sensitivity loss |

### CLM-0011: Enhanced Contrast for Severe Vision Loss
| Field | Value |
|-------|-------|
| ID | CLM-0011 |
| Statement | 7:1 contrast compensates for 20/80 vision loss |
| Axis | luminance |
| UI Primitive | state, focus, navigation |
| Constraint | soft_comfort |
| Threshold | >= 7:1 |
| Evidence | standard |
| Source | WCAG 1.4.6 |
| Notes | AAA level, recommended for critical text |

### INV-006: UI Component Contrast
| Field | Value |
|-------|-------|
| ID | CLM-0012 |
| Statement | UI components require 3:1 contrast against adjacent colors |
| Axis | luminance |
| UI Primitive | focus, state, affordance |
| Constraint | hard_safety |
| Threshold | >= 3:1 |
| Evidence | standard |
| Source | WCAG 1.4.11 |

### CLM-0013: High Contrast Discomfort
| Field | Value |
|-------|-------|
| ID | CLM-0013 |
| Statement | 21:1 black-on-white causes discomfort for photophobia and migraines |
| Axis | luminance |
| UI Primitive | all |
| Constraint | soft_comfort |
| Threshold | < 21:1 for low-glare mode |
| Evidence | observational |
| Source | Neurodiversity Design System - https://neurodiversity.design/principles/colour/ |
| Notes | Conflict with low vision needs - requires dial with floor/ceiling |

### CLM-0014: High Contrast Mode Effectiveness
| Field | Value |
|-------|-------|
| ID | CLM-0014 |
| Statement | High contrast mode improves reading performance by 25% for low vision |
| Axis | luminance |
| UI Primitive | navigation, state |
| Constraint | soft_comfort |
| Threshold | +25% reading performance |
| Evidence | controlled_study |
| Source | Journal of Visual Impairment & Blindness |
| Notes | 30.6% of WebAIM survey respondents use high contrast |

### CLM-0015: APCA Perceptual Contrast
| Field | Value |
|-------|-------|
| ID | CLM-0015 |
| Statement | APCA provides more accurate contrast assessment than WCAG 2.x ratios |
| Axis | luminance |
| UI Primitive | all text |
| Constraint | performance_tradeoff |
| Threshold | Lc 75+ for body text, Lc 45+ for UI |
| Evidence | model |
| Source | https://github.com/Myndex/SAPC-APCA |
| Notes | Candidate for WCAG 3.0, handles dark mode better |

---

## 3. CHROMATIC AXIS: Color Vision Deficiency

### CLM-0020: Brettel Algorithm Gold Standard
| Field | Value |
|-------|-------|
| ID | CLM-0020 |
| Statement | Brettel 1997 half-plane projection is gold standard for dichromat simulation |
| Axis | chromatic |
| UI Primitive | identity, state, hazard |
| Constraint | model |
| Threshold | N/A |
| Evidence | model |
| Source | Brettel, Vienot, Mollon (1997) JOSA-A |
| Notes | Uses 475nm/575nm for protan/deutan, 485nm/660nm for tritan |

### CLM-0021: Gamma Linearization Required
| Field | Value |
|-------|-------|
| ID | CLM-0021 |
| Statement | CVD simulation requires sRGB gamma linearization before LMS conversion |
| Axis | chromatic |
| UI Primitive | all |
| Constraint | hard_safety |
| Threshold | gamma decode before, encode after |
| Evidence | model |
| Source | DaltonLens - https://daltonlens.org |
| Notes | Missing gamma is most common implementation bug |

### CLM-0022: Machado Severity Parameter
| Field | Value |
|-------|-------|
| ID | CLM-0022 |
| Statement | Machado 2009 model supports severity 0.0-1.0 for anomalous trichromacy |
| Axis | chromatic |
| UI Primitive | identity, state |
| Constraint | model |
| Threshold | severity 0.0 (normal) to 1.0 (dichromat) |
| Evidence | model |
| Source | Machado et al. (2009) IEEE TVCG |
| Notes | Precomputed matrices in 0.1 steps available |

### INV-007: Non-Color Encoding
| Field | Value |
|-------|-------|
| ID | CLM-0023 |
| Statement | Information conveyed by color must also be available through non-color means |
| Axis | chromatic |
| UI Primitive | all semantic roles |
| Constraint | hard_safety |
| Threshold | Every role has shape/pattern/label backup |
| Evidence | standard |
| Source | WCAG 1.4.1 |
| Notes | Essential for 8% of males with CVD |

### CLM-0024: CVD Population Statistics
| Field | Value |
|-------|-------|
| ID | CLM-0024 |
| Statement | ~8% of males and ~0.5% of females have some form of CVD |
| Axis | chromatic |
| Constraint | observational |
| Threshold | 8% male, 0.5% female |
| Evidence | clinical |
| Source | Multiple epidemiological studies |
| Notes | Protan/deutan most common (red-green), tritan rare |

---

## 4. SPATIAL AXIS: Acuity, Field Loss, Typography

### INV-008: Touch Target Minimum
| Field | Value |
|-------|-------|
| ID | CLM-0030 |
| Statement | Interactive elements must be at least 44x44 CSS pixels |
| Axis | spatial |
| UI Primitive | affordance, focus |
| Constraint | hard_safety |
| Threshold | >= 44x44 CSS px |
| Evidence | standard |
| Source | WCAG 2.5.5 |
| Notes | WCAG 2.5.8 (AAA) requires 44px with no overlapping targets |

### CLM-0031: Text Size Minimum
| Field | Value |
|-------|-------|
| ID | CLM-0031 |
| Statement | Increasing print from 10pt to 16pt increases fluent reading from 88% to 94.4% |
| Axis | spatial |
| UI Primitive | navigation, state |
| Constraint | soft_comfort |
| Threshold | >= 16px (12pt) minimum, 18pt+ preferred |
| Evidence | controlled_study |
| Source | Legge et al. (2007), J Vis 7(2):8 - https://doi.org/10.1167/7.2.8 (PubMed 17040418) |
| Notes | RNIB and industry recommend 18pt+ for large print |

### CLM-0032: Line Height Requirements
| Field | Value |
|-------|-------|
| ID | CLM-0032 |
| Statement | Line height >= 1.5x font size improves readability for low vision and dyslexia |
| Axis | spatial |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | >= 1.5x font size |
| Evidence | standard |
| Source | WCAG 1.4.12 |
| Notes | Reduces crowding effect between lines |

### CLM-0033: Text Spacing Requirements
| Field | Value |
|-------|-------|
| ID | CLM-0033 |
| Statement | Letter spacing >= 0.12em, word spacing >= 0.16em improves readability |
| Axis | spatial |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | letter: >= 0.12em, word: >= 0.16em, paragraph: >= 2x font |
| Evidence | standard |
| Source | WCAG 1.4.12 |

### CLM-0034: Line Length Optimal
| Field | Value |
|-------|-------|
| ID | CLM-0034 |
| Statement | 50-65 characters per line is optimal for reading |
| Axis | spatial |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | 50-65 characters |
| Evidence | observational |
| Source | Typography research consensus |

### CLM-0035: Sans-Serif Preference
| Field | Value |
|-------|-------|
| ID | CLM-0035 |
| Statement | Sans-serif fonts preferred for low vision and digital displays |
| Axis | spatial |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Evidence | clinical |
| Source | Low Vision Research Report |
| Notes | Serifs significantly degrade legibility for low vision |

---

## 5. DEPTH AXIS: Stereo Independence

### CLM-0050: Stereoblindness Prevalence
| Field | Value |
|-------|-------|
| ID | CLM-0050 |
| Statement | Best-evidence synthesis converges on about 7% stereoblindness prevalence in adults under 60 |
| Axis | depth |
| Constraint | observational |
| Threshold | ~7% median prevalence |
| Evidence | clinical |
| Source | Chopin, Bavelier, Levi (2019), Ophthalmic Physiol Opt |

### INV-009: Monocular Cue Sufficiency
| Field | Value |
|-------|-------|
| ID | CLM-0051 |
| Statement | Essential depth info must be available through static monocular cues; stereo may enrich but not gate completion |
| Axis | depth |
| UI Primitive | depth, navigation |
| Constraint | hard_safety |
| Threshold | Occlusion or order cue + size or perspective cue + edge or lighting cue |
| Evidence | standard |
| Source | Frontiers XR inclusivity perspective (2022); Microsoft XAG 103 |
| Notes | Pladere et al. explicitly recommend increasing monocular cue saliency or offering a 2D mode; if stereo-off or motion-reduced paths break the mechanic, the design is not merged yet |

### CLM-0052: Monocular Depth Cues
| Field | Value |
|-------|-------|
| ID | CLM-0052 |
| Statement | Texture, occlusion, relative size, perspective, shading, and motion parallax provide usable depth information for users without stereopsis |
| Axis | depth |
| UI Primitive | depth |
| Constraint | soft_comfort |
| Evidence | controlled_study |
| Source | Wang and Saunders (2022); Nadler et al. (2016) |
| Notes | Wang and Saunders found comparable texture-based slant performance under monocular conditions; motion parallax is helpful, but it must reinforce rather than replace static cues |

### CLM-0053: Reduced-Motion Depth Preservation
| Field | Value |
|-------|-------|
| ID | CLM-0053 |
| Statement | Motion-based depth cues should reinforce, not replace, static cues because reduced-motion paths must preserve the same scene meaning |
| Axis | depth |
| UI Primitive | depth, feedback |
| Constraint | soft_comfort |
| Evidence | review_plus_standard |
| Source | Nadler et al. (2016); Microsoft XAG 117 |
| Notes | Nadler et al. treat motion parallax as a powerful and sufficient cue, but it is movement-dependent; if depth only "works" while the camera moves, the scene is underspecified |

---

## 6. COGNITIVE AXIS: Load, Attention, Memory

### CLM-0060: Miller's Law
| Field | Value |
|-------|-------|
| ID | CLM-0060 |
| Statement | Working memory holds 7 +/- 2 items simultaneously |
| Axis | cognitive |
| UI Primitive | navigation, priority |
| Constraint | soft_comfort |
| Threshold | 5-9 items max |
| Evidence | controlled_study |
| Source | Miller (1956) |
| Notes | Navigation menus should limit to 5-9 options |

### CLM-0061: Cognitive Disability Prevalence
| Field | Value |
|-------|-------|
| ID | CLM-0061 |
| Statement | 19% of global population has cognitive disability |
| Axis | cognitive |
| Constraint | observational |
| Threshold | 19% |
| Evidence | clinical |
| Source | Cognitive Load Research Report |
| Notes | Most prevalent form of disability need |

### CLM-0062: Neurodivergence Prevalence
| Field | Value |
|-------|-------|
| ID | CLM-0062 |
| Statement | 15-20% of global population is neurodivergent |
| Axis | cognitive |
| Constraint | observational |
| Threshold | 15-20% |
| Evidence | observational |
| Source | Neurodivergence Research Report |

### CLM-0063: Age-Specific UI Reduces Load
| Field | Value |
|-------|-------|
| ID | CLM-0063 |
| Statement | Age-specific UI design reduced cognitive load by 42% per NASA-TLX |
| Axis | cognitive |
| UI Primitive | navigation, progress |
| Constraint | soft_comfort |
| Threshold | 42% reduction possible |
| Evidence | controlled_study |
| Source | 2024 Cognitive Architecture Research |

### CLM-0064: Progressive Disclosure for ADHD
| Field | Value |
|-------|-------|
| ID | CLM-0064 |
| Statement | Progressive disclosure reduces cognitive load for ADHD users |
| Axis | cognitive |
| UI Primitive | navigation, progress |
| Constraint | soft_comfort |
| Evidence | controlled_study |
| Source | Weyerhauser & Piccolo, INTERACT 2025 |
| Notes | Both ADHD and neurotypical groups benefited |

### INV-010: Cognitive Authentication Bypass
| Field | Value |
|-------|-------|
| ID | CLM-0065 |
| Statement | Cognitive function tests cannot be required for authentication |
| Axis | cognitive |
| UI Primitive | affordance |
| Constraint | hard_safety |
| Threshold | Alternative method must exist |
| Evidence | standard |
| Source | WCAG 3.3.8 |

### CLM-0066: Reading Level Target
| Field | Value |
|-------|-------|
| ID | CLM-0066 |
| Statement | Text should not require reading ability above lower secondary education (grade 9) |
| Axis | cognitive |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | Grade 9 / age 14 reading level |
| Evidence | standard |
| Source | WCAG 3.1.5 (AAA) |

### CLM-0067: ADHD-Friendly Design Principles
| Field | Value |
|-------|-------|
| ID | CLM-0067 |
| Statement | ADHD users need: simplified interfaces, progressive disclosure, minimal distractions, user-controlled animations |
| Axis | cognitive |
| UI Primitive | navigation, focus |
| Constraint | soft_comfort |
| Evidence | controlled_study |
| Source | Multiple ADHD UX studies 2024-2025 |

### CLM-0068: Autism Sensory-Friendly Design
| Field | Value |
|-------|-------|
| ID | CLM-0068 |
| Statement | Autistic users prefer: clean layouts, limited color palette, no auto-play, consistent patterns |
| Axis | cognitive |
| UI Primitive | navigation, focus |
| Constraint | soft_comfort |
| Evidence | controlled_study |
| Source | ASPECTSS Framework, AASPIRE Guidelines |
| Notes | CDC: 1 in 36 children diagnosed with autism |

---

## 7. MOTION/ANIMATION

### CLM-0070: Reduced Motion Preference
| Field | Value |
|-------|-------|
| ID | CLM-0070 |
| Statement | Users with vestibular disorders experience nausea from parallax, zooming, swooping animations |
| Axis | temporal |
| UI Primitive | feedback, navigation |
| Constraint | soft_comfort |
| Evidence | standard |
| Source | WCAG 2.3.3 |
| Notes | Must respect prefers-reduced-motion |

### CLM-0071: Safe Animation Duration
| Field | Value |
|-------|-------|
| ID | CLM-0071 |
| Statement | Animations under 0.5 seconds are generally safe for vestibular disorders |
| Axis | temporal |
| UI Primitive | feedback |
| Constraint | soft_comfort |
| Threshold | < 0.5 seconds |
| Evidence | observational |
| Source | MDN Vestibular Guidelines |

### CLM-0072: Auto-Play Control Required
| Field | Value |
|-------|-------|
| ID | CLM-0072 |
| Statement | Auto-playing content must be pausable, stoppable, or hideable |
| Axis | temporal |
| UI Primitive | feedback |
| Constraint | soft_comfort |
| Evidence | standard |
| Source | WCAG 2.2.2 |

---

## Evidence Summary Statistics

| Axis | Hard Safety | Soft Comfort | Model/Tradeoff | Total |
|------|-------------|--------------|----------------|-------|
| Temporal | 5 | 3 | 0 | 8 |
| Luminance | 2 | 4 | 1 | 7 |
| Chromatic | 2 | 0 | 3 | 5 |
| Spatial | 1 | 5 | 0 | 6 |
| Depth | 1 | 2 | 0 | 3 |
| Cognitive | 1 | 7 | 0 | 8 |
| **Total** | **12** | **21** | **4** | **37** |

### Evidence Weight Distribution

| Weight | Count |
|--------|-------|
| Standard (WCAG, ISO, etc.) | 15 |
| Guideline (XAG, industry) | 3 |
| Clinical (medical studies) | 5 |
| Controlled Study | 9 |
| Observational | 3 |
| Model (algorithm papers) | 4 |

---

## 8. TYPOGRAPHY AXIS (Legibility)

### CLM-0080: X-Height Ratio Readability
| Field | Value |
|-------|-------|
| ID | CLM-0080 |
| Statement | Fonts with x-height ratio >= 0.50 are significantly more readable at small sizes |
| Axis | spatial (legibility) |
| UI Primitive | navigation, state |
| Constraint | soft_comfort |
| Threshold | x-height/cap-height >= 0.50 |
| Evidence | controlled_study |
| Source | Legge & Bigelow (2011), Tinker (1963) |
| Notes | Higher x-height increases apparent size without changing point size |

### CLM-0081: Character Disambiguation
| Field | Value |
|-------|-------|
| ID | CLM-0081 |
| Statement | Fonts failing Il1/0Oo/rnm disambiguation cause 3-5x more reading errors |
| Axis | spatial (legibility), cognitive |
| UI Primitive | navigation, identity |
| Constraint | soft_comfort |
| Threshold | All disambiguation pairs visually distinct |
| Evidence | controlled_study |
| Source | Arditi & Cho (2005), Bernard et al. (2001) |
| Notes | Critical for code, data, and technical content |

### CLM-0082: Dyslexia Font Spacing
| Field | Value |
|-------|-------|
| ID | CLM-0082 |
| Statement | Increased letter/word spacing improves reading speed by 20% for dyslexic readers |
| Axis | spatial (legibility), cognitive |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | letter-spacing >= 0.05em, word-spacing >= 0.12em |
| Evidence | controlled_study |
| Source | British Dyslexia Association, Zorzi et al. (2012) |

### CLM-0083: All-Caps Readability Degradation
| Field | Value |
|-------|-------|
| ID | CLM-0083 |
| Statement | Extended all-caps text reduces reading speed by 13-20% |
| Axis | spatial (legibility), cognitive |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | All-caps limited to < 50 characters |
| Evidence | controlled_study |
| Source | Tinker (1963), Poulton (1967) |
| Notes | All-caps eliminates word-shape recognition |

### CLM-0084: Line Length Reading Efficiency
| Field | Value |
|-------|-------|
| ID | CLM-0084 |
| Statement | Lines exceeding 80 characters increase reading time and eye-tracking errors |
| Axis | spatial (legibility), cognitive |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | <= 80 characters, optimal 45-75 |
| Evidence | controlled_study |
| Source | Dyson & Haselgrove (2001), Rayner & Pollatsek (1989) |

### CLM-0085: Font Weight for Low Vision
| Field | Value |
|-------|-------|
| ID | CLM-0085 |
| Statement | Medium weight (500) improves legibility over regular (400) for low vision users |
| Axis | spatial (legibility), luminance |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | Weight 500+ for accessibility modes |
| Evidence | clinical |
| Source | APHont development research, RNIB |

---

## 9. LAYOUT AXIS (Structure)

### INV-L01: Touch Target Size (repeated from spatial, emphasized)
| Field | Value |
|-------|-------|
| ID | CLM-0090 |
| Statement | Interactive elements < 44px cause 2.5x more mis-taps for motor-impaired users |
| Axis | spatial (structure) |
| UI Primitive | affordance, focus |
| Constraint | hard_safety |
| Threshold | >= 44x44 CSS px |
| Evidence | standard |
| Source | WCAG 2.5.5, Fitts's Law research |

### CLM-0091: Touch Target Spacing
| Field | Value |
|-------|-------|
| ID | CLM-0091 |
| Statement | Spacing < 8px between touch targets increases accidental activation by 40% |
| Axis | spatial (structure) |
| UI Primitive | affordance |
| Constraint | soft_comfort |
| Threshold | >= 8px between targets |
| Evidence | controlled_study |
| Source | WCAG 2.5.8 draft, mobile usability studies |

### CLM-0092: Reflow at 200% Zoom
| Field | Value |
|-------|-------|
| ID | CLM-0092 |
| Statement | Content must reflow to avoid horizontal scrolling at 320px CSS equivalent |
| Axis | spatial (structure) |
| UI Primitive | navigation |
| Constraint | hard_safety |
| Threshold | No horizontal scroll at 200% zoom |
| Evidence | standard |
| Source | WCAG 1.4.10 |

### CLM-0093: Navigation Depth Cognitive Load
| Field | Value |
|-------|-------|
| ID | CLM-0093 |
| Statement | Menu depth > 4 levels increases task failure rate by 35% |
| Axis | cognitive (structure) |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | <= 4 levels nesting |
| Evidence | controlled_study |
| Source | Kiger (1984), Miller (1981) |

### CLM-0094: Heading Hierarchy Screen Readers
| Field | Value |
|-------|-------|
| ID | CLM-0094 |
| Statement | Skipped heading levels cause screen reader users to miss 28% of content |
| Axis | cognitive (structure) |
| UI Primitive | navigation |
| Constraint | hard_safety |
| Threshold | No skipped heading levels |
| Evidence | controlled_study |
| Source | WebAIM Screen Reader Survey |

### CLM-0095: Focus Indicator Area
| Field | Value |
|-------|-------|
| ID | CLM-0095 |
| Statement | Focus indicators with area >= 2px perimeter are 40% more discoverable |
| Axis | luminance, spatial (structure) |
| UI Primitive | focus |
| Constraint | hard_safety |
| Threshold | >= 2px outline width, >= 3:1 contrast |
| Evidence | standard |
| Source | WCAG 2.4.11, 2.4.12 |

---

## 10. VISUALIZATION AXIS

### CLM-0100: Color-Only Encoding Error Rate
| Field | Value |
|-------|-------|
| ID | CLM-0100 |
| Statement | Charts using color-only encoding have 45% interpretation error rate for CVD users |
| Axis | chromatic, cognitive |
| UI Primitive | identity, state |
| Constraint | hard_safety |
| Threshold | Every category encoded with color + second channel |
| Evidence | controlled_study |
| Source | Geissbuehler & Coch (2022), Color Universal Design |

### CLM-0101: Chart Legend Item Limit
| Field | Value |
|-------|-------|
| ID | CLM-0101 |
| Statement | Charts with > 8 legend items have 60% lower comprehension accuracy |
| Axis | cognitive |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | <= 8 categories per chart |
| Evidence | controlled_study |
| Source | Cleveland & McGill (1984), Heer & Bostock (2010) |

### CLM-0102: Annotation Density
| Field | Value |
|-------|-------|
| ID | CLM-0102 |
| Statement | > 5 annotations per chart panel reduces comprehension by 25% |
| Axis | cognitive |
| UI Primitive | navigation, identity |
| Constraint | soft_comfort |
| Threshold | <= 5 annotations per panel |
| Evidence | controlled_study |
| Source | Tufte (1983), Cairo (2012) |

### CLM-0103: Line Stroke Width Visibility
| Field | Value |
|-------|-------|
| ID | CLM-0103 |
| Statement | Line strokes < 1pt are invisible for users with low vision or at scaled export |
| Axis | spatial, luminance |
| UI Primitive | identity |
| Constraint | soft_comfort |
| Threshold | >= 1.0pt stroke width |
| Evidence | clinical |
| Source | RNIB Chart Accessibility Guidelines |

### CLM-0104: Chart Text Minimum Size
| Field | Value |
|-------|-------|
| ID | CLM-0104 |
| Statement | Chart text < 8pt at export resolution fails legibility for 20/40 vision |
| Axis | spatial |
| UI Primitive | navigation |
| Constraint | soft_comfort |
| Threshold | >= 8pt at final export size |
| Evidence | clinical |
| Source | Print accessibility research, RNIB |

### CLM-0105: Sequential Palette Lightness Range
| Field | Value |
|-------|-------|
| ID | CLM-0105 |
| Statement | Sequential palettes need lightness range of 50+ for discriminability |
| Axis | chromatic, luminance |
| UI Primitive | identity |
| Constraint | soft_comfort |
| Threshold | L* range >= 50 |
| Evidence | controlled_study |
| Source | ColorBrewer research, Harrower & Brewer (2003) |

### CLM-0106: Perceptual Uniformity in Color Scales
| Field | Value |
|-------|-------|
| ID | CLM-0106 |
| Statement | Non-perceptually-uniform color scales cause 30% data misinterpretation |
| Axis | chromatic |
| UI Primitive | identity |
| Constraint | soft_comfort |
| Threshold | Use perceptually uniform scales (viridis, cividis) |
| Evidence | controlled_study |
| Source | Borland & Taylor (2007), Crameri et al. (2020) |

---

## Updated Evidence Summary Statistics

| Axis | Hard Safety | Soft Comfort | Model/Tradeoff | Total |
|------|-------------|--------------|----------------|-------|
| Temporal | 5 | 3 | 0 | 8 |
| Luminance | 2 | 4 | 1 | 7 |
| Chromatic | 2 | 1 | 3 | 6 |
| Spatial | 1 | 5 | 0 | 6 |
| Depth | 1 | 2 | 0 | 3 |
| Cognitive | 1 | 7 | 0 | 8 |
| Typography (Legibility) | 0 | 6 | 0 | 6 |
| Layout (Structure) | 3 | 3 | 0 | 6 |
| Visualization | 1 | 6 | 0 | 7 |
| **Total** | **16** | **37** | **4** | **57** |

### Evidence Weight Distribution (Updated)

| Weight | Count |
|--------|-------|
| Standard (WCAG, ISO, etc.) | 19 |
| Guideline (XAG, industry) | 3 |
| Clinical (medical studies) | 8 |
| Controlled Study | 21 |
| Observational | 3 |
| Model (algorithm papers) | 4 |

---

---

## 11. DISPLAY ADAPTATION AXIS (Display Physics)

### CLM-0110: Device-Independent Pixel Reference
| Field | Value |
|-------|-------|
| ID | CLM-0110 |
| Statement | 1 DIP (Device-Independent Pixel) = 1/96 inch at reference density |
| Axis | display |
| UI Primitive | all |
| Constraint | standard |
| Threshold | DPI_ref = 96 |
| Evidence | standard |
| Source | Microsoft Learn: DPI and Device-Independent Pixels |
| Notes | CSS reference pixel also tied to 96 DPI conceptual model |

### CLM-0111: Effective Scale Equation
| Field | Value |
|-------|-------|
| ID | CLM-0111 |
| Statement | S_eff = (DPI_physical / 96) x Scale_user produces correct logical-to-physical mapping |
| Axis | display |
| UI Primitive | all |
| Constraint | model |
| Threshold | N/A |
| Evidence | model |
| Source | Windows Effective Pixels, CSS Values and Units Level 3 |
| Notes | Unified equation works across Windows, macOS, Linux windowing systems |

### CLM-0112: Base-4 Grid Scaling Cleanliness
| Field | Value |
|-------|-------|
| ID | CLM-0112 |
| Statement | Base-4 pixel grid produces whole-number results at common scaling factors (1.25, 1.5, 2.0) |
| Axis | display |
| UI Primitive | all layout |
| Constraint | soft_comfort |
| Threshold | Sizes in multiples of 4lp |
| Evidence | guideline |
| Source | Microsoft Fluent Design, Material Design spacing |
| Notes | 4 x 1.25 = 5, 4 x 1.5 = 6, 4 x 2.0 = 8 (all integers) |

### CLM-0113: Wayland Fractional Scaling Mechanism
| Field | Value |
|-------|-------|
| ID | CLM-0113 |
| Statement | Wayland fractional-scale-v1 protocol uses overscale + compositor downsampling |
| Axis | display |
| UI Primitive | all |
| Constraint | model |
| Threshold | N/A |
| Evidence | standard |
| Source | wayland.app/protocols/fractional-scale-v1 |
| Notes | XWayland apps often blurry under fractional scaling without explicit support |

### CLM-0114: E-ink Display Refresh Rate
| Field | Value |
|-------|-------|
| ID | CLM-0114 |
| Statement | Modern fast e-ink displays achieve ~10 Hz refresh for simple content |
| Axis | display, temporal |
| UI Primitive | all |
| Constraint | observational |
| Threshold | 1-10 Hz typical |
| Evidence | observational |
| Source | IEEE Spectrum: E-Paper Display Refresh Rate |
| Notes | Full refresh slower, partial refresh faster but with ghosting |

### CLM-0115: OLED PWM Dimming Frequency
| Field | Value |
|-------|-------|
| ID | CLM-0115 |
| Statement | Many OLED displays use 240-360 Hz PWM dimming at low brightness |
| Axis | display, temporal |
| UI Primitive | all |
| Constraint | observational |
| Threshold | 240-360 Hz typical |
| Evidence | observational |
| Source | OLED-Info: PWM in OLED Displays |
| Notes | Can cause discomfort for flicker-sensitive users; higher refresh reduces perception |

### CLM-0116: VRR Brightness Flicker in Low Range
| Field | Value |
|-------|-------|
| ID | CLM-0116 |
| Statement | VRR displays may exhibit brightness flicker at lower refresh range (40-60 Hz) |
| Axis | display, temporal |
| UI Primitive | all |
| Constraint | observational |
| Threshold | VRR low range (varies by panel) |
| Evidence | observational |
| Source | VESA Adaptive-Sync Whitepaper, user reports |
| Notes | Content patterns can aggravate or mitigate; hardware-dependent |

### CLM-0117: Photosensitive Epilepsy Peak Risk Band
| Field | Value |
|-------|-------|
| ID | CLM-0117 |
| Statement | Photosensitive epilepsy seizure risk peaks in 10-25 Hz frequency band |
| Axis | temporal |
| UI Primitive | hazard |
| Constraint | hard_safety |
| Threshold | Avoid sustained luminance oscillation in 10-25 Hz |
| Evidence | clinical |
| Source | Epilepsy Action, PMC International Guidelines (2024) |
| Notes | Risk exists outside this band but peaks here; higher refresh displays don't change content frequency |

### CLM-0118: WCAG Reflow 320px Equivalence
| Field | Value |
|-------|-------|
| ID | CLM-0118 |
| Statement | Content must reflow without horizontal scroll at 320 CSS px width at 400% zoom |
| Axis | spatial, display |
| UI Primitive | navigation |
| Constraint | hard_safety |
| Threshold | No horizontal scroll at 320 CSS px equivalent |
| Evidence | standard |
| Source | WCAG 1.4.10, Understanding Reflow |
| Notes | 1280px at 400% = 320px; ensures content works on small/zoomed viewports |

### CLM-0119: CRT Manufacturing Capability
| Field | Value |
|-------|-------|
| ID | CLM-0119 |
| Statement | CRT manufacturing/repair capability still exists for industrial and specialty applications |
| Axis | display |
| UI Primitive | all |
| Constraint | observational |
| Threshold | N/A |
| Evidence | observational |
| Source | Thomas Electronics, specialty CRT vendors |
| Notes | Legacy support still relevant for some industrial/medical/retro-gaming contexts |

### CLM-0120: Modular Scale Typography Perception
| Field | Value |
|-------|-------|
| ID | CLM-0120 |
| Statement | Human perception of size steps is multiplicative; modular scales (ratio 1.125-1.25) feel uniform |
| Axis | spatial, cognitive |
| UI Primitive | navigation, identity |
| Constraint | soft_comfort |
| Threshold | Scale ratio 1.125-1.25 typical |
| Evidence | controlled_study |
| Source | Bringhurst, Elements of Typographic Style; Major Second/Minor Third scales |
| Notes | Geometric progression more natural than arithmetic for size hierarchies |

### CLM-0121: Quantization Required for Crispness
| Field | Value |
|-------|-------|
| ID | CLM-0121 |
| Statement | Fractional pixel sizes cause blur; rounding to integer pixels required for crisp rendering |
| Axis | display |
| UI Primitive | all |
| Constraint | soft_comfort |
| Threshold | Round final px to nearest integer |
| Evidence | model |
| Source | Font rendering research, GNOME fractional scaling discourse |
| Notes | Particularly important for text; anti-aliasing helps but doesn't eliminate |

### CLM-0122: Hysteresis Quantization Prevents Jitter
| Field | Value |
|-------|-------|
| ID | CLM-0122 |
| Statement | Values oscillating near rounding boundaries cause visible jitter; hysteresis dead zone prevents this |
| Axis | display, temporal |
| UI Primitive | all |
| Constraint | soft_comfort |
| Threshold | Hysteresis band 0.2 px, max 0.4 px |
| Evidence | model |
| Source | Digital Foundry frame pacing analysis, GNOME/KDE scaling discussions |
| Notes | Per-key state tracking required; reset on major scale changes |

### CLM-0123: Touch Targets Use Ceiling Quantization
| Field | Value |
|-------|-------|
| ID | CLM-0123 |
| Statement | Touch targets must use ceiling (never floor/round) to maintain 44lp minimum |
| Axis | spatial, display |
| UI Primitive | action |
| Constraint | hard_safety |
| Threshold | Always ceil() for touch targets, no hysteresis |
| Evidence | standard |
| Source | WCAG 2.5.5, Fitts's Law research |
| Notes | Safety-critical; rounding down could create non-compliant targets |

### CLM-0124: DPI Transition Is First-Class Event
| Field | Value |
|-------|-------|
| ID | CLM-0124 |
| Statement | When S_eff changes (monitor hop, user zoom), applications must handle as first-class event with state preservation |
| Axis | display |
| UI Primitive | all |
| Constraint | soft_comfort |
| Threshold | < 20ms total transition budget |
| Evidence | guideline |
| Source | Windows Per-Monitor v2, macOS backingScaleFactor, GTK scale-factor signal |
| Notes | Focus, scroll position, selection must be preserved across transitions |

### CLM-0125: Single Scaling Authority Required
| Field | Value |
|-------|-------|
| ID | CLM-0125 |
| Statement | Only one component may own scaling per platform to prevent double-scaling artifacts |
| Axis | display |
| UI Primitive | all |
| Constraint | soft_comfort |
| Threshold | Exactly one authority in scaling chain |
| Evidence | guideline |
| Source | GTK, Qt, Windows, macOS platform documentation |
| Notes | Platform owns scaling (apply user scale, ask platform for final DPI) |

### CLM-0126: 2D Content Exempt from Single-Axis Reflow
| Field | Value |
|-------|-------|
| ID | CLM-0126 |
| Statement | Content requiring 2D layout for meaning (games, maps, tables) is exempt from reflow requirements |
| Axis | spatial, display |
| UI Primitive | navigation, canvas |
| Constraint | standard |
| Threshold | Exemption scoped to specific 2D region only |
| Evidence | standard |
| Source | WCAG 1.4.10 exception clause, Deque University |
| Notes | Surrounding UI (menus, controls) must still reflow; exempt content needs pan/zoom |

### CLM-0127: Frame Pacing Jitter Maximum 10%
| Field | Value |
|-------|-------|
| ID | CLM-0127 |
| Statement | Frame timing deviation beyond 10% of intended period creates visible stuttering |
| Axis | temporal, display |
| UI Primitive | all |
| Constraint | soft_comfort |
| Threshold | frame_time_deviation <= 10% of intended_period |
| Evidence | controlled_study |
| Source | Digital Foundry frame pacing analysis, game performance research |
| Notes | Even at high frame rates, inconsistent timing degrades perceived smoothness |

### CLM-0128: Vestibular Sensitivity Motion Limits
| Field | Value |
|-------|-------|
| ID | CLM-0128 |
| Statement | Aggressive parallax, zoom, and rotation can trigger vestibular discomfort |
| Axis | temporal, spatial |
| UI Primitive | decoration |
| Constraint | soft_comfort |
| Threshold | Parallax <= 0.5, zoom <= 2 stops/sec, rotation <= 45 deg/sec |
| Evidence | clinical |
| Source | Vestibular Disorders Association, WCAG 2.3.3 |
| Notes | prefers-reduced-motion should disable or minimize these effects |

### CLM-0129: E-Ink Requires State-Change Semantics
| Field | Value |
|-------|-------|
| ID | CLM-0129 |
| Statement | E-ink displays should receive discrete state changes, not continuous updates |
| Axis | display, temporal |
| UI Primitive | all |
| Constraint | soft_comfort |
| Threshold | Min 500ms dwell time, no oscillation, batch updates |
| Evidence | observational |
| Source | IEEE Spectrum E-Paper, E Ink Corporation specifications |
| Notes | Continuous updates cause ghosting and battery drain; prefer step functions |

### CLM-0130: OKLCH Perceptual Uniformity
| Field | Value |
|-------|-------|
| ID | CLM-0130 |
| Statement | OKLCH provides perceptually uniform lightness enabling predictable contrast calculations |
| Axis | luminance, chromatic |
| UI Primitive | all |
| Constraint | model |
| Threshold | L values correlate with contrast (not exact) |
| Evidence | model |
| Source | Bjorn Ottosson Oklab paper (2020), CSS Color Level 4 |
| Notes | Lightness alone does not determine contrast; APCA still required for validation |

### CLM-0131: CVD-Safe Axis Is Blue-Orange
| Field | Value |
|-------|-------|
| ID | CLM-0131 |
| Statement | Blue-orange color axis is distinguishable by all common CVD types; red-green is not |
| Axis | chromatic |
| UI Primitive | identity, hazard |
| Constraint | hard_safety |
| Threshold | Avoid red-green as sole distinguisher; prefer blue-orange |
| Evidence | clinical |
| Source | Color Blind Awareness, Colorblind Association guidelines |
| Notes | 8% of males have red-green CVD; blue-orange unaffected |

---

## Updated Evidence Summary Statistics (with Display Physics)

*Version 1.3.0 - Updated 2025-12-27 with Quantization, DPI Transition, Reflow Exceptions, Temporal Stability, and Color Theory claims*

| Axis | Hard Safety | Soft Comfort | Model/Tradeoff | Total |
|------|-------------|--------------|----------------|-------|
| Temporal | 6 | 7 | 0 | 13 |
| Luminance | 2 | 4 | 2 | 8 |
| Chromatic | 3 | 1 | 4 | 8 |
| Spatial | 3 | 6 | 0 | 9 |
| Depth | 1 | 2 | 0 | 3 |
| Cognitive | 1 | 7 | 0 | 8 |
| Typography (Legibility) | 0 | 6 | 0 | 6 |
| Layout (Structure) | 3 | 3 | 0 | 6 |
| Visualization | 1 | 6 | 0 | 7 |
| Display Adaptation | 3 | 9 | 5 | 17 |
| **Total** | **23** | **51** | **11** | **85** |

### New Claims Added (CLM-0122 to CLM-0131)

| ID | Statement Summary | Axis | Constraint |
|----|-------------------|------|------------|
| CLM-0122 | Hysteresis quantization prevents jitter | display, temporal | soft_comfort |
| CLM-0123 | Touch targets use ceiling quantization | spatial, display | hard_safety |
| CLM-0124 | DPI transition is first-class event | display | soft_comfort |
| CLM-0125 | Single scaling authority required | display | soft_comfort |
| CLM-0126 | 2D content exempt from single-axis reflow | spatial, display | standard |
| CLM-0127 | Frame pacing jitter maximum 10% | temporal, display | soft_comfort |
| CLM-0128 | Vestibular sensitivity motion limits | temporal, spatial | soft_comfort |
| CLM-0129 | E-ink requires state-change semantics | display, temporal | soft_comfort |
| CLM-0130 | OKLCH perceptual uniformity | luminance, chromatic | model |
| CLM-0131 | CVD-safe axis is blue-orange | chromatic | hard_safety |

### Evidence Weight Distribution (Updated)

| Weight | Count |
|--------|-------|
| Standard (WCAG, ISO, etc.) | 25 |
| Guideline (XAG, industry) | 6 |
| Clinical (medical studies) | 11 |
| Controlled Study | 23 |
| Observational | 8 |
| Model (algorithm papers) | 9 |

---

*Matrix Version 1.3.1 - Updated 2025-12-27 with Display Physics claims (Quantization, DPI Transitions, Reflow Exceptions, Temporal Stability, Color Theory); 2026-02-26 errata: corrected PDF count, added PubMed DOI for CLM-0031, added falsifiability appendix*

---

## Appendix A: Falsifiability Criteria for Controlled-Study Claims

This appendix documents how each `controlled_study` claim could in principle be
falsified. A claim is falsifiable when an observable outcome would, if measured,
disprove it.

| CLM ID | Statement Summary | Falsification Criterion |
|--------|-------------------|------------------------|
| CLM-0014 | High contrast mode improves reading 25% | RCT shows < 5% improvement for matched low-vision cohort |
| CLM-0031 | 16pt increases fluent reading to 94.4% | Replication in digital UI context shows no threshold effect at 16pt |
| CLM-0052 | Monocular cues sufficient for most tasks | Task completion rate for stereoblind users < 80% under monocular-only conditions |
| CLM-0060 | Working memory holds 7 +/- 2 items | Robust replication shows capacity systematically > 9 or < 5 items |
| CLM-0063 | Age-specific UI reduces cognitive load 42% | NASA-TLX scores show no significant difference between age-specific and generic UI |
| CLM-0064 | Progressive disclosure reduces ADHD load | Controlled ADHD study shows error rate or task time higher with progressive disclosure |
| CLM-0067 | ADHD-friendly design principles effective | ADHD cohort shows no preference for simplified/progressive interfaces in forced choice |
| CLM-0068 | Autism sensory-friendly design preferred | Autistic cohort prefers high-stimulation interfaces over calm layouts in controlled choice |
| CLM-0080 | High x-height improves readability | Controlled reading-speed study finds x-height ratio below 0.50 outperforms high x-height fonts |
| CLM-0081 | Poor disambiguation causes 3-5x errors | Reading error study shows < 1.5x difference between ambiguous and disambiguated fonts |
| CLM-0082 | Increased spacing improves dyslexic reading 20% | Controlled dyslexic reading study shows spacing manipulation has no significant effect on speed |
| CLM-0083 | All-caps reduces reading speed 13-20% | Eye-tracking study shows all-caps and mixed-case reading speeds within 5% |
| CLM-0084 | Lines > 80ch increase reading errors | Reading comprehension study shows no significant difference at 45 vs 80 vs 120 ch line length |
| CLM-0091 | < 8px spacing increases mis-taps 40% | Touch target study shows mis-tap rate difference < 10% between 8px and 0px spacing |
| CLM-0093 | Menu depth > 4 levels increases failures 35% | Navigation study shows task failure rate difference < 10% between 2- and 5-level menus |
| CLM-0094 | Skipped headings cause users to miss 28% content | Screen-reader study shows content discovery rate difference < 10% for skipped headings |
| CLM-0100 | Color-only charts have 45% error rate for CVD | CVD participant study shows < 20% error rate difference vs dual-encoding charts |
| CLM-0101 | > 8 legend items reduce comprehension 60% | Chart study shows comprehension accuracy difference < 20% between 4 and 12 legend items |
| CLM-0102 | > 5 annotations reduce comprehension 25% | Controlled chart study shows no significant difference at 3 vs 7 annotations |
| CLM-0105 | L* range < 50 impairs palette discrimination | Controlled color discrimination study shows no impairment at L* ranges below 50 |
| CLM-0106 | Non-uniform scales cause 30% misinterpretation | Viridis vs rainbow study shows < 10% interpretation difference for controlled numeric tasks |
| CLM-0120 | Modular scales feel perceptually uniform | A/B test shows users cannot distinguish modular from arithmetic size ladders |
| CLM-0127 | > 10% frame jitter creates visible stutter | Double-blind display study shows < 50% subjects report visible stutter at 10-15% jitter |
