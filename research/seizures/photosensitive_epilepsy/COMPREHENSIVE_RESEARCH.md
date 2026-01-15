# Photosensitive Epilepsy and Seizure-Triggering Content: Comprehensive Research Report

**Last Updated:** 2025-12-27
**Research Period:** 2020-2025
**Purpose:** Accessibility research for seizure prevention in digital content

---

## Table of Contents

1. [Overview of Photosensitive Epilepsy](#overview-of-photosensitive-epilepsy)
2. [Flash Frequency Thresholds](#flash-frequency-thresholds)
3. [Red Flash Saturation Thresholds](#red-flash-saturation-thresholds)
4. [Pattern-Induced Seizures](#pattern-induced-seizures)
5. [International Guidelines and Standards](#international-guidelines-and-standards)
6. [Detection Tools and Algorithms](#detection-tools-and-algorithms)
7. [Case Studies](#case-studies)
8. [Guidelines for Video, Animation, and Games](#guidelines-for-video-animation-and-games)
9. [Web Development Best Practices](#web-development-best-practices)
10. [Resources and Downloads](#resources-and-downloads)
11. [References and Citations](#references-and-citations)

---

## Overview of Photosensitive Epilepsy

### Definition

Photosensitive epilepsy (PSE) is a form of epilepsy in which seizures are triggered by visual stimuli that form patterns in time or space, such as flashing lights, bold regular patterns, or regular moving patterns.

### Epidemiology

- **General prevalence:** PSE affects approximately 1 in 4,000 people (0.025% of the population)
- **Among epilepsy patients:** Approximately 3-5% of people with epilepsy have photosensitivity
- **Age distribution:** Most commonly develops between ages 7-19 years
- **Gender:** More common in females than males
- **Photosensitivity decreases with age:** Many individuals "outgrow" the condition by their mid-20s

### Common Symptoms

Exposure to triggering stimuli can cause:
- Seizures (including tonic-clonic, absence, and myoclonic)
- Blurred vision
- Headaches
- Dizziness
- Nausea
- Loss of consciousness

### Primary Triggers

1. **Flashing lights** at specific frequencies (3-60 Hz, most dangerous at 15-25 Hz)
2. **Rapid color transitions** (especially involving saturated red)
3. **High-contrast geometric patterns** (stripes, grids, checkerboards)
4. **Moving or oscillating patterns**
5. **Rapid scene cuts** in video content

---

## Flash Frequency Thresholds

### The "Three Flashes Per Second" Rule

The fundamental principle across all major guidelines is that content should not flash more than **three times in any one-second period**, unless the flash falls below specific thresholds for intensity, color, and area.

### Scientific Basis

- **Most dangerous frequency range:** 15-25 flashes per second (Hz)
- **Broader risk range:** 3-60 Hz
- **U.S. Section 508:** Prohibits flicker between 2 Hz and 55 Hz
- **Sensitivity under 3 Hz:** Uncommon but possible

### Flash Definition

A flash is defined as a pair of opposing changes:
- An increase in luminance followed by a decrease, OR
- A decrease in luminance followed by an increase

### Threshold Conditions

For a flash to be considered potentially hazardous, THREE conditions must be met simultaneously:

1. **Magnitude threshold:** Relative luminance change of 10% or more of maximum relative luminance, where the darker image is below 0.80 relative luminance
2. **Flash count threshold:** More than 3 flashes per second
3. **Area threshold:** Combined flash area exceeds 25% of any 10-degree visual field (approximately 341 x 256 pixels on a 1024 x 768 display at typical viewing distance)

### Two WCAG Compliance Levels

| Criterion | Level | Requirement |
|-----------|-------|-------------|
| WCAG 2.3.1 | A (minimum) | No more than 3 flashes per second, OR flashes below general/red thresholds |
| WCAG 2.3.2 | AAA (enhanced) | No flashing greater than 3 per second regardless of brightness or size |

---

## Red Flash Saturation Thresholds

### Why Red is Particularly Dangerous

People are significantly more sensitive to red flashing than other colors. The 1997 Pokemon incident specifically involved red-blue alternating flashes at 12 Hz, with the red being a pure red that excited red cones alone without inhibitory responses from blue and green cones.

### WCAG Red Flash Definition

A **red flash** is defined as any pair of opposing transitions involving **saturated red**, where:

```
Saturated Red Criteria:
- R >= 80% of maximum possible R value
- AND (R - (G + B)) >= 80% of maximum possible (R - (G + B)) value
```

Where R, G, B are the red, green, and blue color values.

### Technical Interpretation

For an 8-bit color system (0-255 range):
- R must be >= 204 (80% of 255)
- (R - G - B) must be >= 204

### Current Guidelines Coverage

| Standard | Red Flash Threshold Defined? |
|----------|------------------------------|
| WCAG 2.x | Yes - specific formula |
| ISO 9241-391 | Yes - specific formula |
| ITU-R BT.1702 | Mentions risk, no specific threshold |
| Ofcom | Mentions risk, follows Harding FPA |
| Japan/NAB-J | Mentions risk, follows specific guidelines |

**Note:** In 2023, WCAG 2.2 and the updated WCAG 2.1 harmonized their red flash thresholds with ISO 9241-391.

---

## Pattern-Induced Seizures

### Pattern Sensitivity Overview

Pattern sensitivity is a related but distinct condition from flash sensitivity. Some individuals can experience seizures from viewing static or slowly moving geometric patterns.

### Characteristics of Problematic Patterns

1. **High contrast:** Bold differences between light and dark
2. **Regular geometry:** Stripes, grids, checkerboards, radiating lines
3. **Spatial frequency:** Certain stripe widths per degree of visual angle
4. **Movement:** Oscillating or direction-changing patterns
5. **Large area:** Patterns covering significant portion of visual field

### Environmental Triggers

Research has identified environmental patterns that can trigger seizures:
- Window screens and blinds
- Striped clothing and textiles
- Escalator steps
- Ceiling tiles
- Striped wallpaper
- Tablecloths with geometric patterns

### Research Findings (2020-2025)

A 2021 study in *Epilepsy & Behavior* analyzed visual triggers from pattern-sensitive patients:
- 43% Objects with patterns
- 28% Pure patterns (stripes, grids)
- 22% External scenes
- 6% TV or computer screens

### Diagnostic Challenges

Pattern sensitivity is often underdiagnosed because:
- It is not routinely tested during EEG recordings
- 58.3% of patients in one study had previous EEGs without pattern sensitivity testing
- 16.6% had pattern sensitivity WITHOUT photosensitivity

### Chromatic Patterns

Recent research indicates:
- Flickering patterns that shift in chromaticity cause discomfort
- Higher chromatic contrast leads to increased discomfort
- Flickers containing highly saturated red cause greater discomfort than those without

---

## International Guidelines and Standards

### Overview of Major Guidelines

Five major international guidelines govern photosensitive epilepsy risk in media:

| Organization | Standard | Domain | Latest Version |
|--------------|----------|--------|----------------|
| W3C | WCAG 2.x | Web content | 2023 (2.2) |
| ISO | ISO 9241-391 | Human-system interaction | 2016 (revision underway) |
| ITU | ITU-R BT.1702 | Television broadcast | 2023 (v3) |
| Ofcom (UK) | Broadcasting Code Rule 2.12 | UK television | Current |
| NAB-J (Japan) | Japanese Broadcasting Guidelines | Japanese media | Post-1997 |

### WCAG (Web Content Accessibility Guidelines)

**Applicable Success Criteria:**

#### SC 2.3.1 Three Flashes or Below Threshold (Level A)

> "Web pages do not contain anything that flashes more than three times in any one second period, or the flash is below the general flash and red flash thresholds."

**Key Requirements:**
- Maximum 3 flashes per second, OR
- Flash area < 25% of 10-degree visual field (341 x 256 px at 1024 x 768), OR
- Luminance change < 10% AND darker state >= 0.80 relative luminance

#### SC 2.3.2 Three Flashes (Level AAA)

> "Web pages do not contain anything that flashes more than three times in any one-second period."

**Key Difference:** This is absolute - no flashing over 3 per second regardless of size or brightness.

#### SC 2.3.3 Animation from Interactions (Level AAA)

> "Motion animation triggered by interaction can be disabled, unless the animation is essential."

### ISO 9241-391:2016

**Full Title:** "Ergonomics of human-system interaction - Part 391: Requirements, analysis and compliance test methods for the reduction of photosensitive seizures"

**Scope:**
- Requirements and recommendations for electronic displays
- Addresses flashing AND regular patterns
- Considers visual content, viewing environment, and viewer characteristics

**Key Thresholds:**
- Defines "saturated red" specifically
- Provides minimum color difference between states of red flash
- Addresses both temporal (flashing) and spatial (patterns) triggers

### ITU-R BT.1702

**Full Title:** "Guidance for the reduction of photosensitive epileptic seizures caused by television"

**Current Version:** ITU-R BT.1702-3 (November 2023)

**Key Features:**
- Addresses HDR content (up to 10,000 cd/m2 for PQ, 1,000 cd/m2 for HLG)
- Defines critical luminance differences in cd/m2 units
- Acknowledges cumulative effects of extended flashing below thresholds

**Technical Guidelines:**
- Isolated single, double, or triple flashes are acceptable
- Sequences of flashes are not permitted
- Rapid image sequences (fast cuts) are evaluated as potential flashes

### Ofcom Broadcasting Code (UK)

**Rule 2.12:**
> "Television broadcasters must take precautions to maintain a low level of risk to viewers who have photosensitive epilepsy."

**Requirements:**
- Maximum 3 flashes per second
- Area restrictions on flashing content
- Verbal and text warnings if compliance is not reasonably practicable

**Enforcement:**
- All UK broadcasters must test content
- Failed content requires re-editing
- Violations can result in regulatory action

**Cumulative Risk Warning:**
> "A sequence of flashing images lasting more than 5 seconds might constitute a risk even when it falls below individual thresholds."

### Japan Broadcasting Guidelines (Post-Pokemon)

**Background:** Developed after the 1997 Pokemon incident (685 hospitalizations)

**Key Rules:**
- Red flashing limited to maximum 3 times per second
- Red flashing limited to 2 seconds total duration
- Expanded use of warnings for children's programming

---

## Detection Tools and Algorithms

### Harding Flash and Pattern Analyser (FPA)

**Developer:** Cambridge Research Systems Ltd., based on research by Professor Graham Harding (Aston University)

**Purpose:** Commercial tool for broadcast and entertainment industry

**Features:**
- Analyzes video frame-by-frame
- Detects luminance flashes, red flashes, and spatial patterns
- Generates pass/fail certificates
- Implements Ofcom, ITU-R BT.1702, and NAB-J guidelines

**Availability:**
- Commercial license required for broadcast/entertainment
- Website: https://hardingtest.com/
- Industry standard for television and film

**Testing Process:**
1. Video is analyzed for potentially provocative sequences
2. Violations of amplitude, frequency, and area limits are logged
3. Failed content requires re-editing
4. After fixes, entire program must be re-tested

### PEAT (Photosensitive Epilepsy Analysis Tool)

**Developer:** Trace R&D Center, University of Maryland

**Purpose:** Free tool for web content analysis

**Download:** https://trace.umd.edu/peat/

**Features:**
- Free for web content analysis
- Based on adapted HardingFPA engine for WCAG 2.0
- Screen capture functionality
- Video file analysis

**Limitations:**
- Retired/no longer actively supported
- Limited video format support
- CAPTURE function may not work with modern browsers
- NOT licensed for broadcast, film, gaming, or home entertainment

**Installation Notes:**
- Unzip PEAT_2017-02-15.zip to installation directory
- Disable hardware GPU acceleration in browser for capture
- Convert videos to AVI format if needed

### PEAT 2.0 (Community Version)

**Repository:** https://github.com/rakeeb-hossain/PEAT_V2

**Technology:** Qt and OpenCV

**Status:** Community-maintained alternative

### Apple Video Flashing Reduction

**Release Date:** March 2023

**Repository:** https://github.com/apple/VideoFlashingReduction

**Available Implementations:**
- Swift (Xcode project)
- MATLAB
- Mathematica

**Purpose:**
- Calculate risk of flashing lights in video content
- Reduce flashing in detected sequences
- Reference implementation for developers

### EA IRIS

**Developer:** Electronic Arts

**Release Date:** December 2023

**License:** BSD (open source)

**Repository:** Available on GitHub

**Features:**
- Automatic frame-by-frame analysis
- Identifies potentially harmful flashing/patterns
- Early pipeline integration for game development
- Successfully used in EA SPORTS titles (Madden NFL 24, FC 24, WRC)

**Industry Impact:**
> "Before IRIS, there weren't any free and easy-to-use tools for photosensitivity analysis that were available."

### Other Tools and Resources

| Tool | Type | Availability |
|------|------|--------------|
| Flikcer | Web app/Chrome extension | Web-based |
| YouTube/Vimeo | Automated upload analysis | Built-in |
| BATON | Professional QC system | Commercial |
| Photosensitivity Pal | Chrome extension | Free |

### Algorithm Principles

Modern detection algorithms evaluate:

1. **Frame-to-frame luminance changes**
   - Compare brightness values of corresponding pixels
   - Track magnitude and direction of changes
   - Accumulate areas exceeding thresholds

2. **Color analysis**
   - Identify saturated red states
   - Track red flash transitions
   - Measure color saturation levels

3. **Temporal analysis**
   - Count flash occurrences per second
   - Detect flash patterns and frequencies
   - Identify cumulative exposure risks

4. **Spatial analysis**
   - Calculate affected screen area
   - Apply 25% threshold rule
   - Consider viewing distance factors

---

## Case Studies

### The Pokemon Shock Incident (1997)

**Date:** December 16, 1997

**Episode:** "Denno Senshi Porygon" (Computer Warrior Porygon), Episode 38 of Pokemon

**What Happened:**
- A 4-second sequence showed an explosion with red-blue alternating flashes at 12 Hz
- The flashes occupied a significant portion of the screen
- The red was a pure, saturated red exciting only red cones

**Casualties:**
- 685 viewers taken to hospitals by ambulance
- 208 admitted to hospitals
- 3 admitted while unconscious
- Highest incidence in 11-15 year age group
- Oldest affected: 58 years old

**Symptoms Reported:**
- Seizures and convulsions
- Blurred vision
- Headaches, dizziness, nausea
- Loss of consciousness

**Mass Hysteria Component:**
- Many symptoms (headaches, dizziness, nausea) are atypical of PSE seizures
- Classical PSE symptoms (drooling, stiffness, tongue biting) were less common
- 12,000 additional children reported mild symptoms after news coverage
- Some viewers watched replays the next day and reported symptoms

**Long-term Outcomes:**
- 70% (68/103) of patients who had seizures had no seizures in 3-year follow-up
- Only 3 of 78 children with no prior history developed recurrent seizures
- The event itself did not precipitate chronic epilepsy

**Industry Response:**
- Episode never re-broadcast or commercially released worldwide
- Pokemon went on hiatus for 4 months
- Nintendo shares fell 3.2% the following day
- Led to Japanese and UK broadcast guidelines
- Porygon never had a significant role in the anime again

**Cultural Legacy:**
- Guinness World Record: "Most Photosensitive Epileptic Seizures Caused by a Television Show"
- Parodied in The Simpsons ("Thirty Minutes over Tokyo", 1999)
- Established precedent for global media safety standards

### The Golden Wonder Pot Noodle Incident (1993, UK)

**What Happened:**
- Television advertisement screened in the UK
- Caused seizures in three individuals
- Led to development of first UK television guidelines

**Significance:**
- First major incident to prompt regulatory action
- Led Professor Graham Harding to develop testing methodology

### The Voice UK Ofcom Ruling

**What Happened:**
- Flashing lights shown for over 5 seconds total
- Exceeded maximum limits set by PSE Guidelines

**Ruling:**
- Ofcom found breach of Rule 2.12
- Cited significant risk to viewers with PSE susceptibility

**Significance:**
- Demonstrates ongoing enforcement of guidelines
- Cumulative exposure (5+ seconds) is a risk factor

### Cyberpunk 2077 Controversy (2020)

**What Happened:**
- Game contained a "braindance" sequence with rapid red and white flashing
- Resembled patterns used in real neurological testing for epilepsy
- Journalist Liana Ruppert experienced a seizure during review

**Response:**
- CD Projekt Red added epilepsy warning to game
- Added option to disable braindance effect
- Sparked broader industry discussion about game accessibility

---

## Guidelines for Video, Animation, and Games

### Video Content Guidelines

**Pre-Production:**
- Plan sequences to avoid rapid light/dark transitions
- Limit strobe effects and flash photography scenes
- Choose color palettes that avoid saturated red contrasts

**Production:**
- Monitor flash frequency during editing
- Keep flashing sequences under 2 seconds
- Ensure flashing areas are small (<25% of frame)

**Post-Production:**
- Test all content with approved tools (Harding FPA, PEAT, IRIS)
- Reduce flash intensity if needed
- Add warnings if content cannot be modified

**Distribution:**
- YouTube and Vimeo run Harding FPA during upload
- Include content warnings for any borderline material
- Provide alternative versions where possible

### Animation Guidelines

**Web Animations (CSS/JavaScript):**

```css
/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.001ms !important;
    transition-duration: 0.001ms !important;
  }
}
```

**Safe Animation Practices:**
- Use fade transitions instead of hard cuts
- Limit animation speed to avoid perceived flashing
- Avoid oscillating or vibrating effects
- Test with PEAT for complex animations

**Animated GIFs:**
- Cannot be paused by browser auto-play settings
- Consider using video formats with controls instead
- Provide static alternatives
- Install GIF blockers for affected users

### Video Game Guidelines

**Xbox Accessibility Guidelines (XAGs):**

| Do | Don't |
|----|-------|
| Test with industry-standard tools | Use term "epilepsy safe mode" |
| Provide flashing reduction options | Allow flashing >3 per second |
| Warn about photosensitive content | Create strobe effects in cutscenes |
| Allow disabling of screen shake | Use rapid red color transitions |

**Game-Specific Considerations:**
- Victory screens and power-up effects
- Explosions and combat effects
- Menu transitions and loading screens
- Damage indicators and screen flashes
- Spell/ability visual effects

**Testing Recommendations:**
1. Record gameplay video of all sequences
2. Run through IRIS, PEAT, or Harding FPA
3. Flag any sequences exceeding thresholds
4. Modify effects or provide toggle options
5. Never claim "epilepsy safe" - use "photosensitivity options"

**Platform Guidance:**

| Platform | Recommendation |
|----------|----------------|
| Nintendo | Uses "seizure robot" for testing; comprehensive warnings |
| PlayStation | Standard health warnings; recommends well-lit play |
| Xbox | Published accessibility guidelines; industry leadership |
| PC | Developer responsibility; use available tools |

### Warning Requirements

**Effective Warnings Include:**
- Specific mention of photosensitive epilepsy risk
- Advice to sit far from screen
- Advice to play in well-lit room
- Recommendation for breaks (10-15 minutes per hour)
- Note about consulting physician if history of seizures

---

## Web Development Best Practices

### CSS prefers-reduced-motion

**Purpose:** Detect user's OS-level preference for reduced animation

**Implementation:**

```css
/* Standard animation */
.animated-element {
  animation: bounce 0.5s infinite;
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .animated-element {
    animation: none;
  }
}
```

**User Settings by OS:**

| OS | Location |
|----|----------|
| Windows 10/11 | Settings > Ease of Access > Display > Show animations |
| macOS | System Preferences > Accessibility > Display > Reduce motion |
| iOS | Settings > Accessibility > Motion > Reduce Motion |
| Android | Settings > Accessibility > Remove Animations |

### Content Guidelines

**WCAG 2.3.1 Compliance Checklist:**

- [ ] No content flashes more than 3 times per second
- [ ] Flash area is less than 341 x 256 pixels (at 1024 x 768)
- [ ] No saturated red flashing (R >= 80%, R-G-B >= 80%)
- [ ] Luminance changes are below 10% of maximum
- [ ] prefers-reduced-motion is honored
- [ ] Auto-playing content can be paused/stopped
- [ ] Warnings provided for borderline content

### Implementation Strategies

**Pause/Stop Controls:**
```html
<video autoplay muted loop id="hero-video">
  <source src="hero.mp4" type="video/mp4">
</video>
<button onclick="document.getElementById('hero-video').pause()">
  Pause Video
</button>
```

**Auto-play Consideration:**
```javascript
// Check for reduced motion preference
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (prefersReducedMotion) {
  // Show static content instead
  document.getElementById('hero-video').style.display = 'none';
  document.getElementById('hero-image').style.display = 'block';
}
```

**Safe Animation Types:**
- Color fades
- Opacity transitions
- Small scale changes
- Smooth position transitions

**Risky Animation Types:**
- Rapid zooming
- Spinning effects
- Parallax with high contrast
- Strobe or blink effects
- Rapid color cycling

### Browser Extensions for Users

| Extension | Purpose | Platform |
|-----------|---------|----------|
| Photosensitivity Pal | Blocks seizure-risk content | Chrome |
| GIF blockers | Stops animated GIFs | Various |
| Dark mode extensions | Reduces contrast | Various |

---

## Resources and Downloads

### Official Tools

| Tool | URL | Cost |
|------|-----|------|
| PEAT | https://trace.umd.edu/peat/ | Free (web use only) |
| Apple Video Flashing Reduction | https://github.com/apple/VideoFlashingReduction | Free (open source) |
| EA IRIS | https://github.com/electronicarts/iris (search EA GitHub) | Free (BSD license) |
| Harding FPA | https://hardingtest.com/ | Commercial |

### Standards Documents

| Standard | URL |
|----------|-----|
| WCAG 2.1 SC 2.3.1 | https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold.html |
| WCAG 2.1 SC 2.3.2 | https://www.w3.org/WAI/WCAG21/Understanding/three-flashes.html |
| ISO 9241-391:2016 | https://www.iso.org/standard/56350.html |
| ITU-R BT.1702-3 | https://www.itu.int/rec/R-REC-BT.1702 |
| Ofcom Guidance Note | https://www.ofcom.org.uk/siteassets/resources/documents/tv-radio-and-on-demand/broadcast-guidance/gn_flash.pdf |

### Research and Educational Resources

| Resource | URL |
|----------|-----|
| Epilepsy Foundation - Photosensitivity | https://www.epilepsy.com/what-is-epilepsy/seizure-triggers/photosensitivity |
| Epilepsy Society UK | https://epilepsysociety.org.uk/about-epilepsy/epileptic-seizures/seizure-triggers/photosensitive-epilepsy |
| MDN Web Docs - Seizure Disorders | https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Seizure_disorders |
| Game Accessibility Guidelines | https://gameaccessibilityguidelines.com/avoid-flickering-images-and-repetitive-patterns/ |

### Academic Papers

| Paper | Citation | Access |
|-------|----------|--------|
| International Guidelines Gap Analysis | Jordan & Vanderheiden (2024), ACM TACCESS | https://dl.acm.org/doi/10.1145/3694790 |
| Pattern-sensitive PSE self-induction | Epilepsy & Behavior (2021) | https://pubmed.ncbi.nlm.nih.gov/34252828/ |
| Pokemon Incident Long-term Outcomes | Neurology (2004) | https://pubmed.ncbi.nlm.nih.gov/15037709/ |
| Pattern Sensitivity Diagnosis | PMC (2012) | https://pmc.ncbi.nlm.nih.gov/articles/PMC3404594/ |

### GitHub Repositories

| Repository | Purpose |
|------------|---------|
| https://github.com/apple/VideoFlashingReduction | Apple's reference implementation |
| https://github.com/rakeeb-hossain/PEAT_V2 | Community PEAT alternative |
| https://github.com/traceRERC/pseGuidelines | Proposed unified PSE guidelines |

---

## References and Citations

### Web Accessibility Sources

- [Understanding Success Criterion 2.3.1 | W3C](https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold.html)
- [Understanding Success Criterion 2.3.2 | W3C](https://www.w3.org/WAI/WCAG21/Understanding/three-flashes.html)
- [Web accessibility for seizures and physical reactions | MDN](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Seizure_disorders)
- [WCAG 2.3 Seizures and Physical Reactions | UAMS](https://communications.uams.edu/web/kb/wcag-2-3-seizures-and-physical-reactions/)

### Research Papers

- Jordan, J. B. & Vanderheiden, G. C. (2024). "International Guidelines for Photosensitive Epilepsy: Gap Analysis and Recommendations." ACM Transactions on Accessible Computing. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11872230/)
- Pattern-sensitive patients with epilepsy (2021). Epilepsy & Behavior. [PubMed](https://pubmed.ncbi.nlm.nih.gov/34252828/)
- Effectiveness of broadcasting guidelines (2004). Neurology. [PubMed](https://pubmed.ncbi.nlm.nih.gov/15037709/)

### Tools and Technology

- [Photosensitive Epilepsy Analysis Tool (PEAT) | Trace Center](https://trace.umd.edu/peat/)
- [Apple Video Flashing Reduction | GitHub](https://github.com/apple/VideoFlashingReduction)
- [Harding Test | Official Site](https://hardingtest.com/)
- [HardingFPA for Broadcast | Cambridge Research](https://www.hardingfpa.com/hardingfpa-for-broadcast/broadcast-industry/)

### Industry Guidelines

- [Xbox Accessibility Guideline 118 | Microsoft](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/118)
- [Game Accessibility Guidelines | Avoid flickering](https://gameaccessibilityguidelines.com/avoid-flickering-images-and-repetitive-patterns/)
- [Flashing images in advertising | ASA/CAP](https://www.asa.org.uk/news/flashing-images-in-advertising.html)

### Regulatory Bodies

- [Ofcom Broadcasting Code Section 2 | Ofcom](https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-two-harm-offence)
- [ITU-R BT.1702 | ITU](https://www.itu.int/rec/R-REC-BT.1702)
- [ISO 9241-391:2016 | ISO](https://www.iso.org/standard/56350.html)

### Case Study Sources

- [Denno Senshi Porygon | Wikipedia](https://en.wikipedia.org/wiki/Denn%C5%8D_Senshi_Porygon)
- [Revisiting the Pokemon Panic at 25 | Center for Inquiry](https://centerforinquiry.org/blog/revisiting-the-pokemon-panic-at-25/)
- [Attack of the Pocket Monsters: No Lasting Effects | PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC1176371/)

### Epilepsy Organizations

- [Photosensitive Epilepsy | Epilepsy Society UK](https://epilepsysociety.org.uk/about-epilepsy/epileptic-seizures/seizure-triggers/photosensitive-epilepsy)
- [Photosensitivity and Seizures | Epilepsy Foundation](https://www.epilepsy.com/what-is-epilepsy/seizure-triggers/photosensitivity)
- [Photosensitive epilepsy and online content | Epilepsy Action](https://www.epilepsy.org.uk/press/photosensitive-epilepsy-and-online-content)

### CSS and Development

- [prefers-reduced-motion | MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)
- [Animation and motion | web.dev](https://web.dev/learn/accessibility/motion)
- [Revisiting prefers-reduced-motion | CSS-Tricks](https://css-tricks.com/revisiting-prefers-reduced-motion/)

---

## Document Information

**Author:** Automated research compilation
**Research Date:** December 2025
**Sources:** Web search results from academic databases, W3C, regulatory bodies, and industry sources
**License:** For accessibility research purposes

**Disclaimer:** This document is for educational and research purposes. Medical advice should be sought from qualified healthcare professionals. Implementation of accessibility features should be validated with current standards and appropriate testing tools.
