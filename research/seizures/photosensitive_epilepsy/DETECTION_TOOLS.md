# Photosensitive Epilepsy Detection Tools and Algorithms

**Last Updated:** 2026-03-19
**Purpose:** Comprehensive guide to PSE detection software and methodologies

---

## Overview

This document catalogs available tools for detecting seizure-triggering content in digital media, including their capabilities, limitations, licensing, and download locations.

---

## Tool Comparison Matrix

| Tool | Developer | Cost | Open Source | Domain | Status |
|------|-----------|------|-------------|--------|--------|
| PEAT | Trace Center/UMD | Free | Partial | Web | Retired |
| PEAT 2.0 | Community | Free | Yes | Web | Active |
| Harding FPA | Cambridge Research | Commercial | No | Broadcast | Active |
| Apple VFR | Apple Inc. | Free | Yes | Video | Active |
| EA IRIS | Electronic Arts | Free | Yes (BSD) | Games | Active |
| Flikcer | Independent | Free | Partial | Web | Active |

---

## PEAT (Photosensitive Epilepsy Analysis Tool)

### Overview
The original free tool developed by the Trace R&D Center at the University of Wisconsin-Madison (now University of Maryland).

### Technical Details
- **Analysis Engine:** Based on HardingFPA, licensed from Cambridge Research
- **Target Standard:** WCAG 2.0 Success Criterion 2.3.1
- **Input:** Screen capture or video files

### Download
- **URL:** https://trace.umd.edu/peat/
- **File:** PEAT_2017-02-15.zip
- **Installation:** Extract to directory, run PEAT.exe

### Features
- Screen capture functionality
- Video file analysis
- Pass/fail determination
- Frame-by-frame analysis

### Limitations
- **Status:** Retired, no longer actively supported
- **Video Formats:** Limited support for modern codecs
- **Capture Function:** May not work with modern browsers
- **Workarounds:**
  - Capture video with external tool
  - Convert videos to AVI format

### License Restrictions
> "Use of PEAT to assess material commercially produced for television broadcast, film, home entertainment, or gaming industries is prohibited."

**Permitted Uses:**
- Web content
- Software interfaces
- Educational materials
- Non-commercial applications

### Browser Configuration
Disable hardware GPU acceleration for capture:
- Chrome: Settings > Advanced > System > "Use hardware acceleration"
- Firefox: Options > Performance > "Use recommended performance settings"

### Contact
- Email: trace-info@umd.edu

---

## PEAT 2.0 (Community Version)

### Overview
Community-developed alternative using modern technologies.

### Technical Details
- **Framework:** Qt
- **Vision Library:** OpenCV
- **License:** Open source

### Repository
- **URL:** https://github.com/rakeeb-hossain/PEAT_V2

### Features
- Modern codebase
- Better video format support
- Cross-platform potential

### Status
- Community maintained
- May have different analysis algorithms than original PEAT
- Verify against known test cases before production use

---

## Harding Flash and Pattern Analyser (FPA)

### Overview
The industry-standard commercial tool developed by Cambridge Research Systems Ltd., based on research by Professor Graham Harding at Aston University.

### History
- **1990s:** Manual protocols developed for UK broadcast
- **2000:** First automated Harding FPA software launched
- **2018:** DPP technical requirements updated (UK)
- **Ongoing:** Continuous updates for new standards

### Technical Details
- **Analysis:** Frame-by-frame luminance, color, and pattern analysis
- **Standards Supported:** Ofcom, ITU-R BT.1702, NAB-J, ISO 9241-391
- **Output:** Pass/fail certificates for broadcast compliance

### Features
- Luminance flash detection
- Red flash detection
- Spatial pattern detection
- Multiple guideline support
- Automated certificate generation
- Broadcast workflow integration

### Website
- **URL:** https://hardingtest.com/
- **Commercial Info:** https://www.hardingfpa.com/hardingfpa-for-broadcast/broadcast-industry/

### Licensing
- Commercial license required
- Industry standard for broadcast, film, gaming
- Used by all UK television stations
- Integrated into major post-production workflows

### Testing Options
- **Manual Test:** Available on website
- **Japanese/NAB 2006 spec:** Optional for stricter testing
- **HDR Support:** Available in recent versions

### Workflow Integration
When content fails:
1. Identify offending sequences
2. Reduce flash count and/or color intensity
3. Re-edit problem areas
4. Re-test entire program
5. Generate new certificate

---

## Apple Video Flashing Reduction

### Overview
Reference implementation released by Apple for detecting and reducing flashing in video content.

### Release
- **Date:** March 2023
- **License:** Open source

### Repository
- **URL:** https://github.com/apple/VideoFlashingReduction

### Implementations Available
| Language | Directory |
|----------|-----------|
| Swift | VideoFlashingReduction_Xcode |
| MATLAB | VideoFlashingReduction_MATLAB |
| Mathematica | VideoFlashingReduction_Mathematica |

### Purpose
- Calculate risk of flashing lights in video
- Reduce flashing in detected sequences
- Reference for developers implementing their own tools

### Documentation
- Technical summary available in repository
- Algorithm details documented

### Use Cases
- Pre-publication video analysis
- Content warning generation
- Automated remediation
- Integration into video pipelines

---

## EA IRIS

### Overview
Electronic Arts' photosensitivity analysis tool, open-sourced as part of their accessibility initiative.

### Release
- **Date:** December 2023
- **License:** BSD (permissive open source)
- **Announcement:** Part of expanded accessibility patent pledge

### Technical Details
- Analyzes captured video footage
- Identifies potentially harmful flashing/patterns
- Provides immediate feedback during development

### Games Using IRIS
- EA SPORTS Madden NFL 24
- EA SPORTS FC 24
- EA SPORTS WRC

### Features
- Free to use
- Easy integration into development pipelines
- Early detection during production
- Clear feedback on problematic sequences

### Industry Impact
> "Before IRIS, there weren't any free and easy-to-use tools for photosensitivity analysis that were available."

### Related EA Initiatives
- Accessibility Patent Pledge (2021, expanded 2023-2024)
- 23+ accessibility patents pledged royalty-free
- Open source accessibility technology releases

### Access
- GitHub (search: EA IRIS photosensitivity)
- EA Accessibility Portal: https://www.ea.com/accessibility

---

## Flikcer

### Overview
Web application and Chrome extension for photosensitivity detection, based on ITU-R and Ofcom guidelines.

### Features
- Frame-by-frame video analysis
- Brightness comparison between consecutive frames
- Pixel grouping based on change direction
- 25% screen area threshold detection
- Problematic frame removal capability
- Safer video download option

### Technology
- Machine learning techniques
- Web-based interface
- Chrome browser extension

### Algorithm Overview
1. Compare brightness of each pixel to corresponding pixel in next frame
2. Group pixels by positive/negative change
3. Accumulate values for both groups
4. Check against 25% screen area threshold
5. Flag or remove problematic frames

### Access
- Web application available
- Chrome extension available
- Devpost: https://devpost.com/software/flikcer-web-app-for-photosensitive-epilepsy-resolution

---

## Platform Built-in Analysis

### YouTube
- Runs Harding FPA during video upload
- May warn or block videos that fail
- Automatic analysis

### Vimeo
- Similar automated analysis during upload
- Warning system for problematic content

### Limitations
- Results not always visible to uploaders
- May not catch all issues
- Not a substitute for pre-upload testing

---

## Professional QC Systems

### BATON (Interra Systems)
- File-based QC for broadcast
- Implements Ofcom, NAB-J, ITU-R BT.1702 algorithms
- Enterprise-level solution

### Other QC Tools
- Various broadcast QC vendors include PSE checking
- Often bundled with loudness, color, and other compliance checks
- Consult vendor documentation for PSE capabilities

---

## Algorithm Principles

### General Approach

All PSE detection algorithms share common principles:

1. **Frame Extraction**
   - Video decoded to individual frames
   - Consistent frame rate handling
   - Color space normalization

2. **Luminance Calculation**
   - Convert RGB to relative luminance
   - Standard formula: L = 0.2126R + 0.7152G + 0.0722B
   - Per-pixel or region-based

3. **Temporal Analysis**
   - Compare consecutive frames
   - Track luminance transitions
   - Count flash occurrences per second

4. **Spatial Analysis**
   - Calculate affected area
   - Apply 25% threshold rule
   - Consider viewing distance assumptions

5. **Color Analysis**
   - Identify saturated red pixels
   - Check RGB ratios against thresholds
   - Track red flash transitions

6. **Pattern Detection** (advanced)
   - Identify regular geometric patterns
   - Calculate spatial frequency
   - Check contrast levels

### Detection Formula (Simplified)

```
hazardous = (flash_count > 3/sec) AND
            (affected_area > 0.25) AND
            ((luminance_change > 0.1) OR is_saturated_red)
```

### Implementation Considerations

| Factor | Consideration |
|--------|---------------|
| Frame rate | Higher rates need proportional counting |
| Resolution | Scale area calculations appropriately |
| Color depth | May affect luminance precision |
| Compression | Artifacts may affect detection |
| HDR | Different luminance calculations needed |

---

## Choosing a Tool

### Decision Matrix

| Use Case | Recommended Tool |
|----------|------------------|
| Web content (free) | PEAT, PEAT 2.0, Flikcer |
| Game development | EA IRIS |
| Video production | Apple VFR |
| Broadcast compliance | Harding FPA |
| Research/education | PEAT, Apple VFR |
| Commercial entertainment | Harding FPA |

### Key Questions

1. **What is the content type?**
   - Web: PEAT, Flikcer
   - Games: IRIS
   - Video: Apple VFR, Harding FPA
   - Broadcast: Harding FPA

2. **What are the licensing requirements?**
   - Non-commercial: Most tools work
   - Commercial web: PEAT permitted
   - Commercial broadcast/games: Harding FPA required

3. **What standards must be met?**
   - WCAG only: PEAT, Apple VFR
   - Ofcom/ITU: Harding FPA
   - Multiple: Harding FPA

4. **What is the budget?**
   - Free: PEAT, PEAT 2.0, Apple VFR, IRIS, Flikcer
   - Commercial: Harding FPA

---

## Browser Extensions for End Users

### Photosensitivity Pal
- **Platform:** Chrome
- **Purpose:** Block potentially harmful content
- **URL:** Chrome Web Store

### GIF Blockers
- Various extensions available
- Block auto-playing animated GIFs
- User-controlled whitelist

### Reduced Motion Support
- OS-level setting
- Browser respects `prefers-reduced-motion`
- Sites should honor the preference

---

## Testing Workflow Best Practices

### Pre-Production
1. Design with PSE guidelines in mind
2. Brief creative teams on restrictions
3. Plan effects within safe parameters

### Production
1. Flag any potentially problematic sequences
2. Create alternative versions where possible
3. Document rationale for borderline effects

### Post-Production
1. Test all content before release
2. Use appropriate tool for domain
3. Re-test after any changes
4. Archive test results

### Release
1. Include appropriate warnings
2. Provide user controls where possible
3. Monitor for reported issues

---

## Resources

### Downloads
| Tool | URL |
|------|-----|
| PEAT | https://trace.umd.edu/peat/ |
| PEAT 2.0 | https://github.com/rakeeb-hossain/PEAT_V2 |
| Apple VFR | https://github.com/apple/VideoFlashingReduction |
| Harding FPA | https://hardingtest.com/ |

### Documentation
- PEAT User Guide: https://trace.umd.edu/photosensitive-epilepsy-analysis-tool-peat-user-guide/
- Apple VFR Technical Summary: In repository
- Harding FPA Industry Guide: https://www.hardingfpa.com/

---

## 2025-2026 Updates

### PSE Tool Validation Framework (2025)

A 2025 publication (Springer LNCS, DOI: 10.1007/978-3-031-93848-1_7) addresses
validation gaps in current PSE hazard analysis tools. Key contributions:
- Identifies gaps in testing paradigms for PEAT, Harding FPA, and similar tools
- Proposes ground-truth video sequence generation for tool validation
- Establishes conformance testing methodology for comparing PSE safety algorithms
- Relevant to OpenPerception GATE-001 SEIZURE validator development

### Platform Adoption Status (2026)

| Platform | Tool Used | Action |
|----------|-----------|--------|
| YouTube | Harding FPA | Warn/block on upload |
| Vimeo | Harding FPA | Warn/block on upload |
| Adobe Creative Suite | Custom analysis | Integration in progress |
| Browsers (CSS) | None standard | Exploratory |

### PEAT Retirement Confirmed

PEAT (Trace Center, University of Maryland) is officially retired and no longer
supported. The Harding Flash and Pattern Analyzer (FPA) is the industry successor.
PEAT 1.6 remains available in this repository (`tools/PEAT_1.6_Seizure_Analysis.zip`)
as a historical reference.

---

## Document Information

**Related Documents:**
- `/research/seizures/photosensitive_epilepsy/COMPREHENSIVE_RESEARCH.md`
- `/research/seizures/guidelines/INTERNATIONAL_STANDARDS.md`
- `/papers/photosensitive_epilepsy_research_compendium.md`
