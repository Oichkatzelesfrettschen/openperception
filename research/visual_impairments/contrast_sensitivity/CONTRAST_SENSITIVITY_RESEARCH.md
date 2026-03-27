# Contrast Sensitivity: Accessibility Research Report

**Research Date:** December 2024
**Focus:** WCAG contrast guidelines, APCA algorithm, research foundations

Primary source lane:

- [Vision clinical source cache](/home/eirikr/Github/openperception/docs/external_sources/vision_clinical_source_cache.md)

---

## Understanding Contrast Sensitivity

### Definition
Contrast sensitivity is the ability to distinguish between an object and its background. Unlike visual acuity (sharpness), contrast sensitivity measures the minimum difference in light levels needed to perceive patterns.

### Impact on Low Vision
> "Some people with low vision experience low contrast, meaning there aren't very many bright or dark areas. Everything tends to appear about the same brightness, making it hard to distinguish outlines, borders, edges, and details."

## WCAG 2.x Contrast Requirements

### Current Standards

| Level | Normal Text | Large Text | UI Components |
|-------|-------------|------------|---------------|
| **AA** | 4.5:1 | 3:1 | 3:1 (WCAG 2.1) |
| **AAA** | 7:1 | 4.5:1 | N/A |

### Large Text Definition
- 18pt (24 CSS pixels) regular weight
- 14pt (19 CSS pixels) bold weight

### Scientific Basis

The contrast ratios are based on vision loss research:

| Vision Level | Equivalent Ratio |
|--------------|------------------|
| 20/40 acuity | 4.5:1 (compensates for 1.5x contrast loss) |
| 20/80 acuity | 7:1 (compensates for ~2.3x contrast loss) |

> "The 4.5:1 ratio accounts for the loss in contrast that results from moderately low visual acuity, congenital or acquired color deficiencies."

**Source:** [W3C Understanding Contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

## Limitations of WCAG 2.x Contrast

### Dark Mode Problems
> "WCAG 2.x overstates contrast for dark colors to the point that 4.5:1 can be functionally unreadable when one of the colors in a pair is near black."

### Not Ceiling, Just Floor
> "When text contrast is increased to something like 4.52:1, yes this passes, but that doesn't make it 'accessible'--some folks will genuinely still struggle to read that comfortably. WCAG is the floor, not the ceiling."

### Excessive Contrast Issues
> "It's not recommended to use pure black on white (21:1 contrast) as some people have disabilities that make that too difficult to read or cause migraines."

## APCA: Advanced Perceptual Contrast Algorithm

### Overview
APCA is the candidate contrast method for WCAG 3.0, developed to address limitations of current standards.

> "APCA is a new method for predicting contrast for use in emerging web standards (WCAG 3) for determining readability contrast."

### Key Improvements Over WCAG 2.x

1. **Considers font weight and size** together
2. **Handles dark mode** accurately
3. **Accounts for spatial frequency** (text detail)
4. **Perceptually linear** measurements

### How APCA Works

- Reports contrast as Lc (lightness contrast) values
- Range: Lc 0 to Lc 105+
- Lc 15: Point of invisibility for many users
- Lc 90: Preferred for body text

### APCA vs WCAG 2.x

| Scenario | WCAG 2.x | APCA |
|----------|----------|------|
| Dark mode text | Often fails unnecessarily | Accurate assessment |
| Light text on dark | May pass incorrectly | Correct polarity handling |
| Large bold text | Same as small text | Appropriate reduction |

### Research Validation

> "Independent studies were conducted, including a couple of studies using groups of 500 random colors. A PhD at Cambridge in the U.K. did an independent study using approximately 5,000 colors."

### Resources

- [GitHub - SAPC-APCA](https://github.com/Myndex/SAPC-APCA)
- [APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)
- [The Easy Intro to APCA](https://git.apcacontrast.com/documentation/APCAeasyIntro.html)

## Practical Guidelines

### Recommended Contrast Zones

| Use Case | Minimum Ratio | Preferred |
|----------|---------------|-----------|
| Body text | 4.5:1 | 7:1+ |
| Large headings | 3:1 | 4.5:1+ |
| UI components | 3:1 | 4.5:1+ |
| Decorative | N/A | N/A |

### The "Goldilocks Zone"
Level AAA requirements (7:1 for regular text, 4.5:1 for large text) serve as a good target for comfortable reading without being excessive.

### Conditions Requiring Higher Contrast

- Cataracts (clouding reduces contrast)
- Macular degeneration
- Diabetic retinopathy
- Age-related vision changes
- Glaucoma

### Conditions Requiring Lower Contrast

- Photophobia (light sensitivity)
- Some types of migraines
- Certain autism spectrum conditions
- Irlen syndrome

## Testing Tools

### Online Checkers
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Colour Contrast Analyser (TPGi)](https://www.tpgi.com/color-contrast-checker/)

### Browser Extensions
- WAVE Evaluation Tool
- axe DevTools
- Lighthouse (Chrome DevTools)

### APCA Tools
- [APCA Contrast Calculator](https://www.myndex.com/APCA/)

## Design Recommendations

1. **Test both light and dark modes** with appropriate algorithms
2. **Provide user customization** for contrast preferences
3. **Consider ambient lighting** conditions
4. **Use patterns or borders** in addition to color contrast
5. **Test with real users** who have contrast sensitivity issues

## Key Research

1. **WebAIM Contrast and Color Accessibility**
   - [WebAIM Guide](https://webaim.org/articles/contrast/)

2. **W3C Understanding Contrast (Minimum)**
   - [W3C](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

3. **APCA Documentation**
   - [APCA GitHub](https://github.com/Myndex/SAPC-APCA)

4. **Make Things Accessible - WCAG 2.2 Contrast**
   - [Guide](https://www.makethingsaccessible.com/guides/contrast-requirements-for-wcag-2-2-level-aa/)

---

*See also: [LOW_VISION_ACCESSIBILITY_RESEARCH.md](../low_vision/LOW_VISION_ACCESSIBILITY_RESEARCH.md)*
