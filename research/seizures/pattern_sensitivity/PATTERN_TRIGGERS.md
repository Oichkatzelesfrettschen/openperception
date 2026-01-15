# Pattern Sensitivity and Seizure Triggers

**Last Updated:** 2025-12-27
**Purpose:** Research documentation on pattern-induced seizures

---

## Overview

Pattern sensitivity is a condition related to photosensitive epilepsy where seizures can be triggered by viewing certain geometric patterns, even without flashing. It affects a subset of photosensitive individuals and is often underdiagnosed because it is not routinely tested during EEG recordings.

---

## Epidemiology

### Prevalence
- Pattern sensitivity occurs in various epileptic syndromes
- Pattern-sensitive epilepsy is a distinct subtype of visually provoked reflex epilepsies
- Some patients have pattern sensitivity WITHOUT photosensitivity (16.6% in one study)
- Often co-occurs with photosensitive epilepsy

### Diagnostic Challenges
- 58.3% of patients had previous EEGs without pattern sensitivity testing
- Requires specific stimuli during EEG to diagnose
- Often missed in clinical settings

---

## Characteristics of Problematic Patterns

### Spatial Properties

| Property | High Risk | Lower Risk |
|----------|-----------|------------|
| Contrast | High contrast (black/white, bright colors) | Low contrast, muted tones |
| Geometry | Regular, repeating patterns | Irregular, organic shapes |
| Lines | Bold, parallel stripes | Varied line widths |
| Coverage | Large area of visual field | Small, peripheral |

### Pattern Types at Risk

1. **Stripes and Bars**
   - Horizontal, vertical, or diagonal
   - High contrast light/dark alternation
   - Specific spatial frequencies

2. **Grids and Checkerboards**
   - Regular repeating squares
   - High contrast intersections
   - Large area coverage

3. **Radiating Patterns**
   - Lines emanating from center
   - Sunburst designs
   - Spiral patterns

4. **Oscillating/Moving Patterns**
   - Direction-changing stripes
   - Vibrating geometric shapes
   - Rotating patterns

### Movement Factors

| Movement Type | Risk Level |
|---------------|------------|
| Static pattern | Moderate (for very sensitive individuals) |
| Slow, steady movement | Lower |
| Oscillating/vibrating | Higher |
| Direction changes | Higher |
| Flashing patterns | Highest |

---

## Environmental Triggers

Research has documented real-world pattern triggers:

### Indoor Environments
- Window screens and venetian blinds
- Striped wallpaper and textiles
- Ceiling tiles (especially acoustic panels)
- Escalator steps (moving lines)
- Fluorescent light grilles
- Patterned floor tiles

### Clothing and Textiles
- Bold striped clothing
- Geometric print fabrics
- Houndstooth patterns
- Checkered materials

### Technology
- CRT monitor scan lines (historical)
- Poorly rendered graphics
- Moiré patterns from screen capture
- Interlaced video artifacts

### Outdoor/Natural
- Sun through trees (flickering pattern)
- Water reflections
- Fence posts while driving
- Stadium seating patterns

---

## Research Findings (2020-2025)

### Self-Induced Seizures Study (2021)

**Citation:** Published in Epilepsy & Behavior (2021)

**Methodology:**
- Analyzed 73 images from 14 pattern-sensitive patients
- Semi-structured interviews about trigger experiences

**Image Categories:**
| Category | Percentage |
|----------|------------|
| Objects with patterns | 43% |
| Pure patterns | 28% |
| External scenes | 22% |
| TV/computer screens | 6% |

**Key Finding:**
> "All patients described the visual triggers as 'uncomfortable'; the appearance of enjoyable visual epileptic symptoms (especially multi-colored hallucinations) transformed uncomfortable images into pleasant stimuli."

**Behavioral Insight:**
Some patients self-induced seizures as a coping mechanism for stress.

### Chromatic Pattern Research

**Finding:** Flickering patterns that shift in chromaticity cause discomfort and may trigger seizures.

**Key Variables:**
1. **Chromatic contrast** - Higher leads to more discomfort
2. **Brightness contrast** - Independent additive effect
3. **Red saturation** - Highly saturated red more problematic
4. **Flicker frequency** - Dangerous range 3-60 Hz

---

## Clinical Presentation

### Typical Seizure Types Evoked by Patterns
- Absences (brief loss of awareness)
- Myoclonic jerks (sudden muscle jerks, especially upper extremities)
- Associated eye blinking
- Facial contractions

### Warning Signs
- Visual discomfort viewing patterns
- Headache onset
- Dizziness
- Nausea
- Desire to look away

---

## Testing and Diagnosis

### Pattern Sensitivity Testing During EEG

**Standard Stimuli:**
- Alternating black and white stripes
- Various spatial frequencies
- Different viewing distances
- Static and oscillating presentations

**Diagnostic Criteria:**
- Abnormal EEG response to pattern stimuli
- Reproducible across presentations
- Clinical correlation with reported triggers

### Self-Assessment Questions

Individuals may be pattern-sensitive if they experience discomfort viewing:
- [ ] Striped clothing or textiles
- [ ] Escalator steps
- [ ] Venetian blinds
- [ ] Patterned floor tiles
- [ ] Busy geometric wallpaper
- [ ] Ceiling tiles
- [ ] Certain architectural features

---

## Design Guidelines for Pattern Safety

### General Principles

| Do | Don't |
|----|-------|
| Use low contrast patterns | High contrast black/white stripes |
| Vary line widths | Uniform repeating lines |
| Keep patterns small | Large area pattern coverage |
| Use irregular patterns | Regular geometric grids |
| Static or slow movement | Oscillating/vibrating patterns |

### Specific Recommendations

**Stripe Patterns:**
- Avoid more than 5 light/dark pairs
- Keep contrast below 50%
- Add variation to line spacing
- Limit to small decorative areas

**Grid Patterns:**
- Use subtle color differences
- Avoid high contrast intersections
- Consider rounded corners
- Limit overall coverage

**Background Patterns:**
- Low contrast (< 20%)
- Irregular or organic shapes
- No regular geometric repetition
- Allow user override/removal

### Web and Digital Content

```css
/* Example: Safe decorative pattern */
.safe-pattern {
  background: repeating-linear-gradient(
    45deg,
    #f0f0f0,
    #f0f0f0 10px,
    #e8e8e8 10px,
    #e8e8e8 20px
  );
  /* Low contrast, angled, not horizontal/vertical */
}

/* Avoid: High contrast regular stripes */
.unsafe-pattern {
  background: repeating-linear-gradient(
    0deg,
    #000000,
    #000000 5px,
    #ffffff 5px,
    #ffffff 10px
  );
  /* High contrast, horizontal, regular spacing */
}
```

### Video and Animation

**Safe Practices:**
- Avoid full-screen geometric transitions
- Don't use strobe-like pattern reveals
- Limit oscillating background patterns
- Test all patterned content

**Testing:**
- PEAT can detect some pattern issues
- Harding FPA includes pattern analysis
- Manual review for complex patterns

---

## Relationship to Other Conditions

### Photosensitive Epilepsy
- Pattern sensitivity often co-occurs
- Some individuals have only one or the other
- Testing should include both stimuli

### Visual Stress / Meares-Irlen Syndrome
- Related to pattern sensitivity
- Involves reading difficulties
- May benefit from colored overlays
- Not necessarily seizure-related

### Migraine
- Patterns can trigger migraines
- Overlap with photosensitivity
- Similar avoidance strategies help

### Vestibular Disorders
- Complex patterns can cause dizziness
- Motion sickness symptoms
- Affected by pattern + movement combination

---

## Resources

### Research Papers
- Pattern-sensitive patients self-induction study: https://pubmed.ncbi.nlm.nih.gov/34252828/
- Pattern sensitivity diagnosis: https://pmc.ncbi.nlm.nih.gov/articles/PMC3404594/
- Pattern-sensitive epilepsy delineation: https://pubmed.ncbi.nlm.nih.gov/15660768/

### Clinical Resources
- Epilepsy Foundation: https://www.epilepsy.com/what-is-epilepsy/seizure-triggers/photosensitivity
- Epilepsy Society UK: https://epilepsysociety.org.uk/about-epilepsy/epileptic-seizures/seizure-triggers/photosensitive-epilepsy

### Standards
- ISO 9241-391:2016 (includes pattern guidelines)
- ITU-R BT.1702 (broadcast patterns)
- Ofcom guidance (pattern provisions)

---

## Document Information

**Related Documents:**
- `/research/seizures/photosensitive_epilepsy/COMPREHENSIVE_RESEARCH.md`
- `/research/seizures/guidelines/INTERNATIONAL_STANDARDS.md`
