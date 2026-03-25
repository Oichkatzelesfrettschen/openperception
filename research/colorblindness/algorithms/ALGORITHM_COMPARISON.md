# Color Vision Deficiency Simulation Algorithms - Comparison Guide

## Quick Reference

| Algorithm | Year | Best For | Performance | Accuracy |
|-----------|------|----------|-------------|----------|
| Brettel et al. | 1997 | Tritanopia, Reference standard | 2 matrix ops/pixel | Gold standard |
| Viénot et al. | 1999 | Protanopia, Deuteranopia | 1 matrix op/pixel | Excellent |
| Machado et al. | 2009 | Anomalous trichromacy | 1 matrix op/pixel | Excellent |
| Coblis V1 | - | AVOID | Fast | Poor |

## Recommended Selection

### Tritanopia (Blue-Yellow Deficiency)
**Use: Brettel 1997** - Only validated algorithm for this condition.

### Protanopia (Red-Blind) / Deuteranopia (Green-Blind)
**Use: Viénot 1999** - Faster than Brettel, handles extreme values better.
**Alternative: Brettel 1997** - Equally accurate, slightly slower.

### Protanomaly / Deuteranomaly (Partial Red/Green Deficiency)
**Use: Machado 2009** - Principled severity interpolation with precomputed matrices.

## Implementation Pipeline

All valid methods follow:
1. **sRGB → Linear RGB** (gamma decode - CRITICAL, often omitted!)
2. **Linear RGB → LMS** (cone response space)
3. **Apply CVD transformation** (reduce/eliminate cone contribution)
4. **LMS → Linear RGB**
5. **Linear RGB → sRGB** (gamma encode)

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

## Available Implementations

### Reference Libraries
- **libDaltonLens**: C, public domain, zero dependencies
- **DaltonLens-Python**: Unit-tested, three main methods
- **colour-science**: Comprehensive Python toolkit

### Browser/Software
- **Color Oracle**: Java/Objective-C, Brettel 1997
- **Chromium/Firefox DevTools**: Machado 2009
- **GIMP**: Brettel 1997 display filter

## Key Papers (Canonical Local Cache)

1. `papers/downloads/algorithms/Brettel_1997_Dichromat_Simulation.pdf` - Foundational dichromat simulation
2. `papers/downloads/algorithms/Machado_2009_CVD_Simulation.pdf` - Physiologically-based model
3. `papers/downloads/algorithms/Vienot_1999_Digital_Colourmaps.pdf` - Simplified digital display approach

Legacy research-local copies still exist for some of these papers, but the
canonical cache lane for new citations is `papers/downloads/algorithms/`.

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
