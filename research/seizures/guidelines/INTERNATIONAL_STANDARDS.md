# International Standards for Photosensitive Epilepsy Prevention

**Last Updated:** 2025-12-27
**Purpose:** Reference guide to international PSE guidelines and standards

---

## Overview

Five major international guidelines govern photosensitive epilepsy (PSE) risk across different technology domains. While they address similar risk factors, they are not fully harmonized, which can create confusion for content creators working across multiple platforms.

---

## Comparison Matrix

| Feature | WCAG 2.x | ISO 9241-391 | ITU-R BT.1702 | Ofcom (UK) | NAB-J (Japan) |
|---------|----------|--------------|---------------|------------|---------------|
| **Domain** | Web | HCI/Displays | Television | UK TV | Japanese Media |
| **Latest Version** | 2.2 (2023) | 2016 | 3 (2023) | Current | Post-1997 |
| **Flash Rate Limit** | 3/sec | 3/sec | 3/sec | 3/sec | 3/sec |
| **Area Threshold** | 25% of 10-deg | 25% screen | 25% screen | 25% screen | 25% screen |
| **Red Flash Defined** | Yes | Yes | Mentioned | Mentioned | Yes |
| **Pattern Guidelines** | Basic | Yes | Yes | Yes | Yes |
| **HDR Support** | No | No | Yes | No | Yes |
| **Cumulative Risk** | No | Yes | Yes | Yes | Implicit |
| **Free to Access** | Yes | Paid | Free PDF | Free | Varies |

---

## WCAG (Web Content Accessibility Guidelines)

### Authority
- **Organization:** World Wide Web Consortium (W3C)
- **Scope:** Web content globally
- **Legal Status:** Referenced in accessibility laws worldwide

### Success Criteria

#### SC 2.3.1 Three Flashes or Below Threshold (Level A)

**Official Definition:**
> "Web pages do not contain anything that flashes more than three times in any one second period, or the flash is below the general flash and red flash thresholds."

**Technical Thresholds:**

| Threshold Type | Criterion |
|----------------|-----------|
| General Flash | Relative luminance change >= 10% of max, darker state < 0.80 |
| Red Flash | Saturated red (R >= 80%, R-(G+B) >= 80% of max) |
| Area | < 25% of 10-degree visual field (341 x 256 px at 1024 x 768) |
| Frequency | <= 3 flashes per second |

#### SC 2.3.2 Three Flashes (Level AAA)

**Official Definition:**
> "Web pages do not contain anything that flashes more than three times in any one-second period."

**Key Difference:** No exceptions for size, brightness, or color. Even a single flashing pixel violates this criterion.

#### SC 2.3.3 Animation from Interactions (Level AAA)

**Official Definition:**
> "Motion animation triggered by interaction can be disabled, unless the animation is essential to the functionality or the information being conveyed."

### 2023 Updates
- Red flash thresholds harmonized with ISO 9241-391
- WCAG 2.2 published as W3C Recommendation
- All three WCAG 2.x versions remain active standards

### Resources
- Understanding 2.3.1: https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold.html
- Understanding 2.3.2: https://www.w3.org/WAI/WCAG21/Understanding/three-flashes.html
- Understanding 2.3.3: https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html

---

## ISO 9241-391:2016

### Authority
- **Organization:** International Organization for Standardization
- **Full Title:** "Ergonomics of human-system interaction - Part 391: Requirements, analysis and compliance test methods for the reduction of photosensitive seizures"
- **Scope:** Electronic displays globally

### Key Features

**Covered Stimuli:**
- Flashing/flickering images
- Regular patterns (stripes, grids, etc.)
- Rapidly changing images
- Spatial patterns

**Unique Aspects:**
- Most comprehensive pattern sensitivity coverage
- Clinical aspects documented in Annex C
- Provides sample conformance testing procedures
- Considers viewing environment factors

### Technical Requirements

| Parameter | Requirement |
|-----------|-------------|
| Flash Rate | <= 3 per second |
| Area | < 25% of screen |
| Luminance | Defined relative changes |
| Red | Specific saturation formula |
| Patterns | Spatial frequency limits |

### Revision Status
- ISO/AWI 9241-391 currently in development
- Expected to address modern display technologies

### Access
- Purchase required: https://www.iso.org/standard/56350.html
- Related standards: ISO/IEC 40500:2012 (WCAG 2.0)

---

## ITU-R BT.1702

### Authority
- **Organization:** International Telecommunication Union (UN agency)
- **Full Title:** "Guidance for the reduction of photosensitive epileptic seizures caused by television"
- **Current Version:** ITU-R BT.1702-3 (November 2023)
- **Scope:** Television broadcast worldwide

### Key Technical Guidelines

**Flash Definition:**
> "A potentially harmful flash occurs when there is a pair of opposing changes in luminance."

**Permitted Flashes:**
- Isolated single, double, or triple flashes: Acceptable
- Sequences of flashes: Not permitted
- Rapid image sequences (fast cuts): Evaluated as potential flashes

### HDR Content Provisions

| Content Type | Max Luminance |
|--------------|---------------|
| SDR | 200 cd/m2 |
| HLG (Hybrid Log-Gamma) | 1,000 cd/m2 |
| PQ (Perceptual Quantization) | 10,000 cd/m2 |

**Darker Range Handling:**
- When darker state < 160 cd/m2
- Up to 20 cd/m2 difference permitted

### Cumulative Effects Warning
> "A sequence of flashes over a time period of 5 seconds might be problematic even if under the thresholds."

### Access
- Free PDF: https://www.itu.int/rec/R-REC-BT.1702

---

## Ofcom Broadcasting Code (UK)

### Authority
- **Organization:** Office of Communications (UK regulator)
- **Scope:** All UK television broadcasts
- **Enforcement:** Legal requirement with penalties

### Rule 2.12

**Official Text:**
> "Television broadcasters must take precautions to maintain a low level of risk to viewers who have photosensitive epilepsy. Where it is not reasonably practicable to follow the Ofcom guidance, and where broadcasters can demonstrate that the broadcasting of flashing lights and/or patterns is editorially justified, viewers should be given an adequate verbal and also, if appropriate, text warning at the start of the programme or programme item."

### Technical Guidance

| Parameter | Threshold |
|-----------|-----------|
| Flash Rate | > 3/sec is potentially harmful |
| Duration | > 5 seconds cumulative may be problematic |
| Area | 25% screen maximum |
| Intensity | Specific thresholds per Harding FPA |

### Compliance Requirements

1. **Testing:** All content must be tested with approved tools
2. **Failed Content:** Must be re-edited
3. **Re-testing:** Entire program after fixes
4. **Certification:** PSE test certificate required
5. **Warnings:** Required if content cannot be modified

### Enforcement Examples
- The Voice UK: Found in breach for flashing lights > 5 seconds
- Various advertisers: ASA/CAP enforcement for non-compliant ads

### Resources
- Broadcasting Code Section 2: https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-two-harm-offence
- Technical Guidance: https://www.ofcom.org.uk/siteassets/resources/documents/tv-radio-and-on-demand/broadcast-guidance/gn_flash.pdf

---

## Japan Broadcasting Guidelines (NAB-J)

### Background

**Origin:** Developed following the 1997 Pokemon incident
- 685 viewers hospitalized
- 208 admitted to hospitals
- Led to immediate regulatory action

### Key Rules

| Rule | Specification |
|------|---------------|
| Red Flash Rate | Maximum 3 per second |
| Red Flash Duration | Maximum 2 seconds total |
| Testing | Mandatory for broadcast content |
| Warnings | Required for children's programming |

### Scope
- Television broadcast
- Anime production
- Online streaming platforms (adapted)

### HDR Support
- Max luminance: 1,000 cd/m2 (HLG) / 10,000 cd/m2 (PQ)
- Aligned with ITU-R BT.1702

### Testing
- Compatible with Harding FPA "Japanese/NAB 2006 spec" option
- Used by anime production studios
- Automated QC systems (BATON) support NAB-J

### Cultural Impact
- Standard "well-lit room" warnings on children's programming
- Anime industry self-regulation
- Production pipeline integration

---

## U.S. Section 508

### Authority
- **Law:** Section 508 of the Rehabilitation Act
- **Scope:** U.S. Federal agency websites and IT

### Technical Requirement
> "Pages shall be designed to avoid causing the screen to flicker with a frequency greater than 2 Hz and less than 55 Hz."

### Relationship to WCAG
- Section 508 refresh (2017) incorporated WCAG 2.0 Level A and AA
- WCAG 2.3.1 (Three Flashes) is included

### Enforcement
- Applies to federal agencies
- Private sector bound by other laws (ADA, state laws)

---

## Guidelines Gap Analysis

### Key Findings from Jordan & Vanderheiden (2024)

**Harmonization Issues:**
1. Different definitions of "saturated red"
2. Varying area calculation methods
3. Inconsistent pattern guidelines
4. Different approaches to HDR content
5. Cumulative exposure handled differently

**Technology Gaps:**
- VR/AR content not specifically addressed
- Mobile device viewing distances
- High refresh rate displays (120Hz+)
- Variable refresh rate (VRR) technologies

**Recommendations:**
1. Harmonize red flash thresholds (ISO and WCAG led in 2023)
2. Develop unified pattern sensitivity guidelines
3. Address emerging display technologies
4. Create single reference implementation

### Reference
- Full paper: https://dl.acm.org/doi/10.1145/3694790
- PMC version: https://pmc.ncbi.nlm.nih.gov/articles/PMC11872230/

---

## Compliance Decision Tree

```
Content Contains Flashing?
|
+-- No --> PASS
|
+-- Yes --> Count flashes per second
           |
           +-- <= 3/sec --> Check area
           |                |
           |                +-- < 25% screen --> PASS
           |                |
           |                +-- >= 25% screen --> Check luminance
           |                                     |
           |                                     +-- < 10% change --> PASS
           |                                     |
           |                                     +-- >= 10% change --> Check red
           |                                                          |
           |                                                          +-- Not saturated red --> PASS (2.3.1)
           |                                                          |
           |                                                          +-- Saturated red --> FAIL
           |
           +-- > 3/sec --> FAIL (both 2.3.1 and 2.3.2)
```

---

## Testing Tools by Standard

| Standard | Recommended Tool | Notes |
|----------|------------------|-------|
| WCAG | PEAT, Apple VFR | Web content only |
| ISO 9241-391 | Harding FPA | Commercial |
| ITU-R BT.1702 | Harding FPA, BATON | Broadcast |
| Ofcom | Harding FPA | Required for UK |
| NAB-J | Harding FPA (Japan spec), BATON | Anime industry |
| Games | EA IRIS, Harding FPA | Multi-platform |

---

## Document Information

**Purpose:** Quick reference for accessibility practitioners
**Related Documents:**
- `/research/seizures/photosensitive_epilepsy/COMPREHENSIVE_RESEARCH.md`
- `/research/seizures/pattern_sensitivity/PATTERN_TRIGGERS.md`
