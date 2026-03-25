# Color Vision Deficiency Simulation Algorithms - Comparison Guide

Primary support-mode docs:

- [Color support accommodation taxonomy](/home/eirikr/Github/openperception/docs/color-support-accommodation-taxonomy.md)
- [Algorithm source cache](/home/eirikr/Github/openperception/docs/external_sources/algorithm_source_cache.md)
- [Color vision source cache](/home/eirikr/Github/openperception/docs/external_sources/color_vision_source_cache.md)

## Quick Reference

| Mode | Representative Work | Best For | Runtime Shape | Evidence Posture |
|------|----------------------|----------|---------------|------------------|
| Simulation and preview | Brettel 1997, Vienot 1999, Machado 2009 | Validation, QA, palette comparison | Matrix-based pixel transforms | Strong, established |
| Static recoloring and daltonization | Fidaner-style daltonization, later recoloring work | Remediating a static artifact | Transform plus optimization or heuristic shifts | Useful, task-dependent |
| Interactive recognition aid | Zhu 2024 AR reconstruction | Color naming and contextual identification | User interaction plus temporal cueing | Promising, task-specific |
| Restorative or speculative modeling | Kotani and Ng 2025 | Conceptual and future-facing restoration questions | Computational learning framework | Exploratory, not a shipping default |
| Legacy simulation | Coblis V1 | Avoid for serious evaluation | Fast | Poor |

## Recommended Selection

Choose by user goal first:

- If you need to verify whether meaning survives CVD, use simulation.
- If you need to improve a static artifact people will actually consume, use
  daltonization or redesign, then validate with simulation.
- If the task requires accurate color naming or contextual color
  identification, consider an interactive recognition aid.
- If you are discussing restoration or the emergence of richer color
  dimensionality, keep that in the reconstructive or speculative lane rather
  than treating it as a default accessibility intervention.

### Simulation and preview

#### Tritanopia (Blue-Yellow Deficiency)
**Use: Brettel 1997** - The strongest local reference for tritanopia preview.

#### Protanopia (Red-Blind) / Deuteranopia (Green-Blind)
**Use: Viénot 1999** - Faster than Brettel, good for protan/deutan preview.
**Alternative: Brettel 1997** - Strong reference baseline when consistency is
more important than speed.

#### Protanomaly / Deuteranomaly (Partial Red/Green Deficiency)
**Use: Machado 2009** - Best local option when severity interpolation matters.

## Implementation Pipeline

Simulation algorithms in this section follow the same core pipeline:
1. **sRGB → Linear RGB** (gamma decode - CRITICAL, often omitted!)
2. **Linear RGB → LMS** (cone response space)
3. **Apply CVD transformation** (reduce/eliminate cone contribution)
4. **LMS → Linear RGB**
5. **Linear RGB → sRGB** (gamma encode)

That pipeline does not automatically describe daltonization, interactive
recognition systems, or speculative reconstruction models. Those modes may use
simulation internally, but their user-facing purpose is different.

## Critical Implementation Notes

### Common Bug: Missing Gamma Correction
Many implementations skip sRGB linearization, causing:
- Colors appear too dark across brightness range
- Incorrect simulation results

### Matrix Selection
RGB-to-LMS conversion matrix choice significantly impacts results:
- Hunt-Pointer-Estevez (HPE)
- CIECAM02
- Smith-Pokorny fundamentals

## Support Modes Beyond Simulation

### Static recoloring and daltonization

Daltonization is not the same thing as simulation. Simulation predicts a view;
daltonization alters the viewed artifact. That distinction matters because a
system can be excellent for preview and still be a poor intervention.

Use this mode when:

- a static artifact already exists and cannot be fully redesigned
- some color differences need to survive more reliably for a target task
- the tradeoff between naturalness and distinguishability is acceptable

Do not overclaim:

- better color separation is not the same as better color naming
- a transformed artifact can help one task while hurting another
- post hoc correction is not a substitute for redundant cues

See also:

- [Daltonization guide](/home/eirikr/Github/openperception/docs/daltonization-guide.md)
- [Color support accommodation taxonomy](/home/eirikr/Github/openperception/docs/color-support-accommodation-taxonomy.md)

### Interactive recognition support

Some systems help users identify colors in context rather than only distinguish
abstract patches. Zhu et al. (2024) is the key local reference here: it uses
temporal color shifts in AR to create an extra learnable cue for color
recognition tasks.

Use this mode when:

- exact color naming matters
- users are working in a live interactive task
- a learnable temporal or motion-based cue is acceptable

### Restorative or speculative reconstruction

Some papers belong in the repo because they sharpen our conceptual language
around color vision, not because they are ready-made UI accommodations. Kotani
and Ng (2025) fits that role by modeling how color dimensionality may emerge in
the brain.

Use this lane when:

- discussing restoration, enhancement, or future sensory models
- separating conceptual modeling from present-day product guidance
- avoiding the assumption that trichromacy is the only meaningful endpoint

## Choose The Right Mode For The Job

| If you need to... | Prefer... | Why |
|-------------------|-----------|-----|
| check whether UI meaning collapses under CVD | simulation and preview | best validation lane |
| repair a static image, chart, or screenshot | daltonization plus redesign where possible | direct intervention lane |
| help users identify or name colors in a task | interactive recognition support | recognition is not just discrimination |
| talk about restoration or future color dimensionality | reconstructive or speculative modeling | conceptual lane, not shipping default |

Repo default:

- Start with redundant cues, not color alone.
- Use simulation to validate.
- Use daltonization only when there is a concrete artifact to remediate.
- Use recognition aids when the task truly depends on color identity.
- Describe reconstructive models as exploratory unless the evidence supports a
  stronger claim.

## Available Implementations

### Reference Libraries
- **libDaltonLens**: C, public domain, zero dependencies
- **DaltonLens-Python**: Unit-tested, three main methods
- **colour-science**: Comprehensive Python toolkit

These tools primarily occupy the simulation and preview lane. Some also support
daltonization, but that should be documented as intervention behavior rather
than conflated with simulation accuracy.

### Browser/Software
- **Color Oracle**: Java/Objective-C, Brettel 1997
- **Chromium/Firefox DevTools**: Machado 2009
- **GIMP**: Brettel 1997 display filter

## Canonical Source Trails

Simulation:

1. `papers/downloads/algorithms/Brettel_1997_Dichromat_Simulation.pdf`
2. `papers/downloads/algorithms/Machado_2009_CVD_Simulation.pdf`
3. `papers/downloads/algorithms/Vienot_1999_Digital_Colourmaps.pdf`
4. `papers/downloads/algorithms/Stockman_2019_Cone_Fundamentals_CIE_Standards.pdf`
5. `papers/downloads/algorithms/Vienot_2015_Cone_Fundamentals_Past_Present_Future.pdf`

Interactive recognition and reconstruction:

1. `papers/downloads/color_vision/Zhu_2024_Computational_Trichromacy_Reconstruction_AR.pdf`
2. `papers/downloads/color_vision/Kotani_2025_Color_Vision_Emergence_Framework.pdf`

Canonical cache and note surfaces:

- [Algorithm source cache](/home/eirikr/Github/openperception/docs/external_sources/algorithm_source_cache.md)
- [Color vision source cache](/home/eirikr/Github/openperception/docs/external_sources/color_vision_source_cache.md)
- [Color support accommodation taxonomy](/home/eirikr/Github/openperception/docs/color-support-accommodation-taxonomy.md)

## Technical Details

### Brettel 1997
- Transforms stimuli to LMS space
- Projects onto reduced stimulus surface
- Uses neutral axis + monochromatic anchors (575nm yellow, 475nm blue for protan/deutan)

### Viénot 1999
- Simplified for digital displays (sRGB monitors)
- Single 3x3 matrix per deficiency type
- Not designed for tritanopia

### Machado 2009
- Based on stage theory of color vision
- Precomputed matrices for severity 0.0-1.0 in 0.1 steps
- Note: Equations 17-18 have typo in original paper, matrices are correct
