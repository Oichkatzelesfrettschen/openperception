# Unified Color Scheme Scope

Date: 2026-03-22

## Why this note exists

This is a scoping pass across four threads that were getting conflated:

1. human-visible palette design for `openperception`,
2. current color-vision-deficiency research,
3. QCD "color" language around quarks, gluons, and SU(3),
4. Cayley-Dickson and surreal algebra references in `~/Github/open_gororoba` and `~/Documents`.

The main conclusion is simple:

- There is no purely visual color scheme that "each and every human can see" if we include achromatopsia and non-perceptual blindness.
- There is, however, a defensible unified scheme for almost all sighted users if we optimize for luminance, contrast, redundant encodings, and common color-vision deficiencies.
- QCD color charge and Cayley-Dickson structure can be productive metaphors for palette organization, but they are not the physical basis of human color perception.

## Executive answer

The best near-term move is not "replace magenta/red with something mathematically cosmic." It is:

- keep the project's perceptually validated indigo backbone,
- rotate the accent family from hot magenta into mauve,
- reserve burgundy as a tertiary or "surreal" emphasis family,
- require shape, line-style, label, and texture redundancy anywhere meaning would otherwise depend on hue alone.

That yields a palette that is measurably better than the current indigo/magenta pair for protan and deutan simulation while staying visually adjacent to the existing design language.

## What the current repo already has

`openperception` already contains a solid accessibility baseline:

- `tokens/color-tokens.json`
- `tokens/color-tokens-oklch.css`
- `docs/colorblind-friendly-design-guide.md`
- `tools/contrast_check.py`
- `tools/separation_check.py`
- `algorithms/DaltonLens-Python/daltonlens/simulate.py`

The current default pair is:

- Indigo strong: `#3730A3`
- Magenta strong: `#86198F`

Using the repo's Oklab logic plus DaltonLens simulation, the current indigo/magenta pair has these approximate strong-token distances:

| Pair | Normal | Protan | Deutan | Tritan |
|---|---:|---:|---:|---:|
| current indigo vs magenta | 0.158 | 0.035 | 0.095 | 0.166 |

That `0.035` under protan is the warning sign: the pair nearly collapses.

## What the latest research changes

### 1. How many "types of blindness" are there actually?

There are two different questions here.

For color vision deficiency, the 2025 Ophthalmology meta-analysis explicitly stratified by:

- type: deutan, protan, tritan,
- severity: anomalous trichromacy, dichromacy, monochromacy.

That is already at least 6 clinically meaningful buckets before acquired causes and mixed etiologies are added.

For vision loss more broadly, WHO still distinguishes levels such as moderate visual impairment, severe visual impairment, and blindness. So if the target is "all humans," a color-only solution is ruled out immediately.

Design implication:

- "Universal color scheme" is only coherent if "universal" means "works for most sighted users and degrades safely through non-color cues."

### 2. What is established in human color perception?

Human-visible color is not derived from quarks or gluons. It is driven by cone responses to spectra:

`L = integral S(lambda) l_bar(lambda) d lambda`

`M = integral S(lambda) m_bar(lambda) d lambda`

`S = integral S(lambda) s_bar(lambda) d lambda`

Then perception is organized through opponent channels and luminance-like combinations. For interface work, the practical version is:

- optimize luminance contrast,
- optimize perceptual distance in Oklab/OKLCH,
- simulate protan, deutan, and tritan confusion.

### 3. What is QCD "color" really?

QCD color is an internal gauge degree of freedom, not visible hue. Mathematically, quarks live in the fundamental representation `3` of SU(3), antiquarks in `3-bar`, and gluons in the adjoint `8`, often summarized as:

`3 x 3-bar = 8 + 1`

That is a symmetry statement about strong interactions, not a prescription for UI palettes. It is valid as metaphor, not as psychophysics.

### 4. What does Cayley-Dickson add?

From the harmonized surreal Cayley-Dickson draft in `~/Documents`, the rigorous part is the standard doubling:

`A_(n+1)(F) = CD(A_n(F); -1) = A_n(F) + A_n(F)`

with the usual multiplication law over a real-closed field or surreal subfield.

That is useful as a way to organize families, tiers, and recursive derivations. It is not evidence that human-accessible color ought to follow Cayley-Dickson or surreal-number structure. The right role here is architectural:

- primary family,
- accent family,
- tertiary family,
- neutral ladder,
- per-deficiency projections.

## Mathematical derivation of an equivalent mauve/indigo/burgundy scheme

### Step 1. Preserve what is already validated

The current palette already satisfies the repo's contrast checks for the strong tokens. So the safest move is to preserve:

- the lightness ladder,
- most of the chroma budget,
- the neutral ramp.

In OKLCH terms, the current validated anchors are approximately:

- Indigo 700: `L=0.39843 C=0.17734 h=277.37`
- Magenta 700: `L=0.45191 C=0.19218 h=324.59`

### Step 2. Rotate hue, not structure

To get an "equivalent" palette, define new target hue families:

- indigo target hue: about `280`
- mauve target hue: about `334`
- burgundy target hue: about `16`

Then preserve lightness and most chroma:

- `new_token = OKLCH(L_old, C_adjusted, h_target)`

with a modest chroma taper on mauve so it reads as mauve rather than electric magenta.

### Step 3. Enforce contrast

For text and solid controls, require:

- body text contrast >= `4.5:1`
- UI component contrast >= `3:1`
- preferred strong token contrast with white >= `7:1` where feasible

### Step 4. Enforce perceptual separation under simulation

For semantic peers, compare Oklab distances after CVD simulation. A practical design goal is not an abstract perfect threshold, but "avoid collapse."

The proposed strong-pair result is:

| Pair | Normal | Protan | Deutan | Tritan |
|---|---:|---:|---:|---:|
| proposed indigo vs mauve | 0.163 | 0.099 | 0.144 | 0.166 |

This is materially better than the current pair for protan and deutan, while staying in the same visual neighborhood.

## Proposed unified reference palette

Neutrals can stay as-is from the current repo.

### Primary: Indigo

| Token | OKLCH | Hex |
|---|---|---|
| indigo-700 | `0.40 0.18 281` | `#3E2DA4` |
| indigo-600 | `0.51 0.23 280` | `#5743E3` |
| indigo-500 | `0.59 0.20 279` | `#6967F0` |
| indigo-300 | `0.79 0.10 278` | `#ABB4FA` |
| indigo-100 | `0.93 0.03 276` | `#E2E7FD` |

### Accent: Mauve

| Token | OKLCH | Hex |
|---|---|---|
| mauve-700 | `0.46 0.14 336` | `#853275` |
| mauve-600 | `0.60 0.18 334` | `#BD4EAC` |
| mauve-400 | `0.75 0.13 332` | `#DE8ED2` |
| mauve-200 | `0.90 0.07 330` | `#FACEF4` |

### Tertiary / Surreal: Burgundy

| Token | OKLCH | Hex |
|---|---|---|
| burgundy-800 | `0.33 0.13 18` | `#68021A` |
| burgundy-700 | `0.43 0.15 16` | `#901C32` |
| burgundy-600 | `0.52 0.17 14` | `#B52F4A` |
| burgundy-300 | `0.78 0.10 18` | `#F19D9F` |
| burgundy-100 | `0.93 0.03 20` | `#FCE0E0` |

### Recommended semantic mapping

- Indigo: navigation, links, stable primary actions, trusted system state
- Mauve: annotation, highlights, secondary emphasis, "interpretive" content
- Burgundy: warnings, surreal/research emphasis, tertiary callouts, high-gravity moments
- Gray ramp: structure, text, surfaces, borders

## The actual universal rule

If the target includes:

- protanopia and deuteranopia,
- tritanopia,
- monochromacy,
- low vision,
- non-perceptual blindness,

then the real unified scheme is not color-only. It is:

1. color family,
2. lightness difference,
3. text label,
4. line style or border style,
5. marker shape or icon,
6. texture or hatch for fills,
7. optional audio/haptic equivalent in fully non-visual contexts.

That is the only rigorous answer to "a unified color scheme for everyone."

## Debt ledger

### Conceptual debt

- QCD color charge is being used interchangeably with visible color. That is scientifically false.
- Cayley-Dickson and surreal structures are useful for nomenclature and hierarchy, not for human psychophysics.
- "Latest quantum color theory" does not appear to be a standard literature term. The most defensible interpretation is QCD color charge.

### Accessibility debt

- The current indigo/magenta pair gets too close under protan simulation.
- Any meaning still carried by hue alone is technical debt.
- Monochromacy-safe semantics are impossible without shape/pattern redundancy.

### Documentation debt

- `openperception` has strong docs, but the physics metaphor layer should be explicitly labeled as metaphor.
- `open_gororoba` should avoid wording that implies QCD color is a direct perceptual-color model.

### Validation debt

- Proposed mauve/indigo/burgundy tokens should be added as a non-default experimental variant before replacing the production default.
- The same DaltonLens simulation and contrast checks should be run on charts, not just brand tokens.

## Relevant local files from `~/Documents`

The most obviously relevant unique items I found were:

1. `~/Documents/Writing/Monographs/Theme Synthesis_ Mahogany, Burgundy, Dark Red.pdf`
   - A direct aesthetic predecessor for the burgundy/mahogany line.
2. `~/Documents/Writing/Monographs/Red & Mahogany MATE Themes.pdf`
   - Likely useful for desktop-theme translation and atmosphere vocabulary.
3. `~/Documents/Projects/CayleyDickson/speculatory_surreal_cayley_dickson/surreal_cayley_dickson_harmonized.md`
   - The cleanest local statement of what is rigorous vs speculative in the surreal CD material.
4. `~/Documents/Projects/CayleyDickson/tier1_core_cd_algebra/cd_tower_structure/2505.11747v3.pdf`
   - Recent Cayley-Dickson structure reference, already mirrored in the local corpus.
5. `~/Documents/Writing/Monographs/Cayley-Dickson Ladder Taxonomy and Nomenclature from 32D to 8192D with open_gororoba Integration.pdf`
   - Relevant if the palette naming scheme is going to borrow algebraic tier language.
6. `~/Documents/Projects/CayleyDickson/tier1_core_cd_algebra/interleaved_generation_physics/tang_2023_230814768_sedenion_su5.pdf`
   - Relevant to the particle-physics analogy layer, but should be treated as analogy support, not palette evidence.

## Recommended next actions

1. Add the mauve/indigo/burgundy set as an experimental token variant rather than replacing defaults immediately.
2. Add an explicit `burgundy` family to the token source of truth.
3. Extend chart examples so every series has both color and non-color encoding.
4. Label QCD/Cayley-Dickson references as "metaphor / organizational framing" unless a claim is strictly mathematical.
5. If desired, generate a second document that turns this scope note into concrete token JSON/CSS and chart examples.

## Source anchors

External:

- W3C WCAG 2.2 Contrast Minimum: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C WCAG 2.2 Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- PubMed, `Global Prevalence of Congenital Color Vision Deficiency among Children and Adolescents, 1932-2022` (2025): https://pubmed.ncbi.nlm.nih.gov/40769301/
- CERN, color charge confinement context: https://home.cern/news/news/physics/alice-finds-charm-hadronisation-differs-lhc
- WHO classification landing page: https://www.who.int/standards/classifications/2

Local:

- `docs/colorblind-friendly-design-guide.md`
- `tokens/color-tokens.json`
- `tokens/color-tokens-oklch.css`
- `tools/contrast_check.py`
- `tools/separation_check.py`
- `algorithms/DaltonLens-Python/daltonlens/simulate.py`
- `~/Documents/Projects/CayleyDickson/speculatory_surreal_cayley_dickson/surreal_cayley_dickson_harmonized.md`
