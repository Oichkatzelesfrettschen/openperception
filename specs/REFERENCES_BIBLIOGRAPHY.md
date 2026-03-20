# UVAS+ References and Bibliography

**Version:** 1.0.0
**Last Updated:** 2026-03-19
**Purpose:** Consolidated bibliography of all sources cited in UVAS+ specification documents

---

## 1. Web Content Accessibility Guidelines (WCAG)

### 1.1 Primary WCAG References

| Citation | URL | Used In |
|----------|-----|---------|
| WCAG 2.2 Specification | https://www.w3.org/TR/WCAG22/ | All specs |
| WCAG 2.1 Specification | https://www.w3.org/TR/WCAG21/ | Legacy references |
| WCAG 3.0 (Working Draft) | https://www.w3.org/TR/wcag-3.0/ | APCA integration (not yet in published draft as of Aug 2025) |
| APCA (SAPC-APCA) | https://github.com/Myndex/SAPC-APCA | Contrast algorithm for WCAG 3.0 (LC scores replace ratios) |

### 1.2 Understanding Documents

| Success Criterion | Understanding Document | Topic |
|-------------------|------------------------|-------|
| SC 1.4.1 | https://www.w3.org/WAI/WCAG21/Understanding/use-of-color | Color not sole conveyor |
| SC 1.4.3 | https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum | 4.5:1 contrast minimum |
| SC 1.4.4 | https://www.w3.org/WAI/WCAG21/Understanding/resize-text | 200% text resize |
| SC 1.4.6 | https://www.w3.org/WAI/WCAG21/Understanding/contrast-enhanced | 7:1 enhanced contrast |
| SC 1.4.10 | https://www.w3.org/WAI/WCAG21/Understanding/reflow | 320px reflow |
| SC 1.4.11 | https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast | 3:1 UI contrast |
| SC 1.4.12 | https://www.w3.org/WAI/WCAG21/Understanding/text-spacing | Text spacing overrides |
| SC 2.2.2 | https://www.w3.org/WAI/WCAG21/Understanding/pause-stop-hide | Pause moving content |
| SC 2.3.1 | https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold | Flash threshold |
| SC 2.3.3 | https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions | Motion from interactions |
| SC 2.4.7 | https://www.w3.org/WAI/WCAG21/Understanding/focus-visible | Focus visibility |
| SC 2.4.11 | https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum | Focus not obscured |
| SC 2.5.5 | https://www.w3.org/WAI/WCAG21/Understanding/target-size | 44x44px touch targets |
| SC 2.5.8 | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum | 24x24px minimum |
| SC 3.1.5 | https://www.w3.org/WAI/WCAG21/Understanding/reading-level | Reading level (AAA) |
| SC 3.3.8 | https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication | Accessible authentication |

---

## 2. ISO Standards

| Standard | Title | Topic |
|----------|-------|-------|
| ISO 9241-112:2017 | Ergonomics of human-system interaction - Dialogue principles | Temporal consistency |
| ISO 9241-303:2011 | Requirements for electronic visual displays | Display quality |
| ISO 9241-391:2016 | Requirements for the reduction of photosensitive seizures | Flash/seizure safety |
| ISO 12640-3:2007 | Input scanner target (IT8.7/1) | Color measurement |
| ISO 3664:2009 | Viewing conditions - Graphic technology | Viewing conditions |

---

## 3. Color Vision and CVD Research

### 3.1 CVD Simulation Algorithms

| Author(s) | Year | Title | Publication | DOI/URL |
|-----------|------|-------|-------------|---------|
| Brettel, Vienot & Mollon | 1997 | Computerized simulation of color appearance for dichromats | Journal of the Optical Society of America A | doi:10.1364/JOSAA.14.002647 |
| Vienot, Brettel & Mollon | 1999 | Digital video colourmaps for checking the legibility of displays by dichromats | Color Research & Application | doi:10.1002/(SICI)1520-6378(199908)24:4<243::AID-COL5>3.0.CO;2-3 |
| Machado, Oliveira & Fernandes | 2009 | A Physiologically-based Model for Simulation of Color Vision Deficiency | IEEE Transactions on Visualization and Computer Graphics | doi:10.1109/TVCG.2009.113 |

### 3.2 CVD Tools and Libraries

| Tool | License | URL | Purpose |
|------|---------|-----|---------|
| DaltonLens | MIT | https://daltonlens.org | CVD simulation library |
| colour-science | BSD-3 | https://colour-science.org | Color science library |
| Color Oracle | Free | https://colororacle.org | Desktop CVD simulator |

### 3.3 CVD Statistics

| Source | URL | Data |
|--------|-----|------|
| Color Blind Awareness | https://www.colourblindawareness.org/colour-blindness/types-of-colour-blindness/ | CVD prevalence rates |
| NIH/NEI | https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness | Clinical definitions |

---

## 4. Contrast and Perception

### 4.1 APCA (Accessible Perceptual Contrast Algorithm)

| Resource | URL | Notes |
|----------|-----|-------|
| APCA Repository | https://github.com/Myndex/SAPC-APCA | Reference implementation |
| APCA Calculator | https://www.myndex.com/APCA/ | Online tool |
| APCA-W3 | https://github.com/nicetoad/APCA-W3 | W3C integration |

### 4.2 Traditional Contrast Tools

| Tool | URL | Use |
|------|-----|-----|
| WebAIM Contrast Checker | https://webaim.org/resources/contrastchecker/ | WCAG 2.x contrast |
| axe-core | https://www.deque.com/axe/ | Automated testing |
| Deque University | https://dequeuniversity.com/ | Training resources |

---

## 5. Seizure and Photosensitivity Safety

### 5.1 Standards and Guidelines

| Source | URL/Reference | Topic |
|--------|---------------|-------|
| Epilepsy Action | https://www.epilepsy.org.uk/info/seizure-triggers/photosensitive-epilepsy | Photosensitive triggers |
| Epilepsy Foundation | https://www.epilepsy.com/what-is-epilepsy/seizure-triggers/photosensitivity | Trigger guidance |
| Harding Test | https://hardingtest.com/ | Commercial flash testing |
| ITU-R BT.1702-3 | ITU Recommendation | Broadcast flash guidance |

### 5.2 Analysis Tools

| Tool | URL | License |
|------|-----|---------|
| PEAT (Photosensitive Epilepsy Analysis Tool) | https://trace.umd.edu/peat/ | Free |
| EA IRIS | https://github.com/electronicarts | BSD |
| Apple VideoFlashingReduction | https://github.com/apple/VideoFlashingReduction | Apache 2.0 |

### 5.3 Research

| Authors | Year | Title | Publication |
|---------|------|-------|-------------|
| Harding & Harding | 2010 | Photosensitive epilepsy and image safety | Applied Ergonomics |
| Wilkins et al. | 2004 | A neuropsychological theory of positive visual phenomena in migraine | Cephalalgia |

---

## 6. Display Technology

### 6.1 DPI and Scaling

| Platform | URL | Topic |
|----------|-----|-------|
| Microsoft High DPI | https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows | Windows DPI awareness |
| Microsoft DIP Model | https://learn.microsoft.com/en-us/windows/win32/learnwin32/dpi-and-device-independent-pixels | Device-independent pixels |
| Apple backingScaleFactor | https://developer.apple.com/documentation/appkit/nswindow/1419459-backingscalefactor | macOS scaling |
| GTK 4 HiDPI | https://docs.gtk.org/gtk4/property.Widget.scale-factor.html | GTK scaling |
| Qt 6 High DPI | https://doc.qt.io/qt-6/highdpi.html | Qt scaling |
| Wayland Fractional Scale | https://wayland.app/protocols/fractional-scale-v1 | Wayland protocol |
| Arch Wiki HiDPI | https://wiki.archlinux.org/title/HiDPI | Linux reference |

### 6.2 Variable Refresh Rate (VRR)

| Source | URL/Reference | Topic |
|--------|---------------|-------|
| VESA Adaptive-Sync | https://www.vesa.org/ | VRR specification |
| Digital Foundry | https://www.digitalfoundry.net/ | Frame pacing analysis |
| AMD FreeSync | https://www.amd.com/en/technologies/freesync | FreeSync specification |
| NVIDIA G-SYNC | https://www.nvidia.com/en-us/geforce/technologies/g-sync/ | G-SYNC specification |

### 6.3 E-Ink and Reflective Displays

| Source | URL | Topic |
|--------|-----|-------|
| IEEE Spectrum E-Paper | https://spectrum.ieee.org/e-paper-display-modos | E-ink technology |
| E Ink Corporation | https://www.eink.com/ | E-ink specifications |

---

## 7. Typography and Reading

### 7.1 Readability Research

| Authors | Year | Title | Publication |
|---------|------|-------|-------------|
| Legge & Bigelow | 2011 | Does print size matter for reading? | Journal of Vision |
| Pelli et al. | 2007 | Crowding and eccentricity determine reading rate | Journal of Vision |
| Arditi & Cho | 2005 | Serifs and font legibility | Vision Research |

### 7.2 Font Resources

| Resource | URL | Use |
|----------|-----|-----|
| fonttools | https://github.com/fonttools/fonttools | Font analysis |
| Google Fonts | https://fonts.google.com/ | Open fonts |
| Font Squirrel | https://www.fontsquirrel.com/ | Free fonts |

---

## 8. Cognitive Accessibility

### 8.1 Plain Language

| Resource | URL | Topic |
|----------|-----|-------|
| Flesch-Kincaid | Various | Readability formulas |
| Plain Language Action Network | https://www.plainlanguage.gov/ | US plain language |
| Hemingway Editor | https://hemingwayapp.com/ | Readability tool |

### 8.2 Neurodiversity

| Resource | URL | Topic |
|----------|-----|-------|
| Neurodiversity Design System | https://neurodiversity.design/ | Design principles |

---

## 9. Toolkit and Platform Documentation

### 9.1 Desktop Toolkits

| Toolkit | Documentation URL |
|---------|-------------------|
| GTK 2/3/4 | https://docs.gtk.org/ |
| Qt 5/6 | https://doc.qt.io/ |
| FLTK | https://www.fltk.org/doc-1.3/ |
| wxWidgets | https://docs.wxwidgets.org/ |
| Tk | https://www.tcl.tk/man/ |
| EFL/Elementary | https://www.enlightenment.org/docs |

### 9.2 Embedded/Real-Time

| Toolkit | Documentation URL |
|---------|-------------------|
| LVGL | https://docs.lvgl.io/ |
| NuttX/NxWidgets | https://nuttx.apache.org/docs/ |
| Microwindows | https://github.com/ghaerr/microwindows |

### 9.3 Game/Immediate Mode

| Library | Documentation URL |
|---------|-------------------|
| SDL2 | https://wiki.libsdl.org/ |
| SDL3 | https://wiki.libsdl.org/SDL3 |
| Dear ImGui | https://github.com/ocornut/imgui |
| Nuklear | https://github.com/Immediate-Mode-UI/Nuklear |

### 9.4 Legacy

| Toolkit | Notes |
|---------|-------|
| Motif/OpenMotif | Legacy Xlib-based toolkit |
| LessTif | Motif clone |
| Metacity | GNOME 2 WM (Marco is Mate fork) |

---

## 10. Testing Tools

### 10.1 Accessibility Testing

| Tool | URL | License |
|------|-----|---------|
| axe-core | https://github.com/dequelabs/axe-core | MIT |
| Pa11y | https://pa11y.org/ | LGPL |
| WAVE | https://wave.webaim.org/ | Free (web) |
| Lighthouse | https://developers.google.com/web/tools/lighthouse | Apache 2.0 |

### 10.2 Visual Testing

| Tool | URL | Purpose |
|------|-----|---------|
| Playwright | https://playwright.dev/ | Browser automation |
| Puppeteer | https://pptr.dev/ | Chrome automation |
| Percy | https://percy.io/ | Visual regression |

---

## 11. Academic Publications

### 11.1 Color Science

```bibtex
@article{brettel1997computerized,
  title={Computerized simulation of color appearance for dichromats},
  author={Brettel, Hans and Vi{\'e}not, Fran{\c{c}}oise and Mollon, John D},
  journal={Journal of the Optical Society of America A},
  volume={14},
  number={10},
  pages={2647--2655},
  year={1997},
  publisher={Optical Society of America},
  doi={10.1364/JOSAA.14.002647}
}

@article{machado2009physiologically,
  title={A physiologically-based model for simulation of color vision deficiency},
  author={Machado, Gustavo M and Oliveira, Manuel M and Fernandes, Leandro AF},
  journal={IEEE Transactions on Visualization and Computer Graphics},
  volume={15},
  number={6},
  pages={1291--1298},
  year={2009},
  publisher={IEEE},
  doi={10.1109/TVCG.2009.113}
}

@article{vienot1999digital,
  title={Digital video colourmaps for checking the legibility of displays by dichromats},
  author={Vi{\'e}not, Fran{\c{c}}oise and Brettel, Hans and Mollon, John D},
  journal={Color Research \& Application},
  volume={24},
  number={4},
  pages={243--252},
  year={1999},
  publisher={Wiley},
  doi={10.1002/(SICI)1520-6378(199908)24:4<243::AID-COL5>3.0.CO;2-3}
}
```

### 11.2 Accessibility and Usability

```bibtex
@article{legge2011does,
  title={Does print size matter for reading? A review of findings from vision science and typography},
  author={Legge, Gordon E and Bigelow, Charles A},
  journal={Journal of Vision},
  volume={11},
  number={5},
  pages={8--8},
  year={2011},
  publisher={The Association for Research in Vision and Ophthalmology},
  doi={10.1167/11.5.8}
}

@article{pelli2007crowding,
  title={Crowding and eccentricity determine reading rate},
  author={Pelli, Denis G and Tillman, Katharine A and Freeman, Jeremy and Su, Michael and Berger, Tracey D and Majaj, Najib J},
  journal={Journal of Vision},
  volume={7},
  number={2},
  pages={20--20},
  year={2007},
  publisher={The Association for Research in Vision and Ophthalmology},
  doi={10.1167/7.2.20}
}
```

### 11.3 Photosensitivity

```bibtex
@article{harding2010photosensitive,
  title={Photosensitive epilepsy and image safety},
  author={Harding, Graham FA and Harding, Peter F},
  journal={Applied Ergonomics},
  volume={41},
  number={4},
  pages={504--508},
  year={2010},
  publisher={Elsevier},
  doi={10.1016/j.apergo.2009.08.003}
}
```

---

## 12. Quick Reference by Spec File

| Spec File | Primary References |
|-----------|-------------------|
| UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md | WCAG 2.2, ISO 9241-391, DaltonLens |
| VALIDATORS_FRAMEWORK.md | WCAG 2.x all SCs, axe-core, PEAT |
| SCALING_MATHEMATICS.md | WCAG 1.4.4, 1.4.10, Platform docs |
| SCALING_AUTHORITY_MATRIX.md | GTK, Qt, Windows, macOS docs |
| DPI_TRANSITION_CONTRACT.md | Platform DPI APIs |
| QUANTIZATION_POLICY.md | Digital Foundry, frame pacing research |
| REFLOW_EXCEPTIONS_2D.md | WCAG 1.4.10, Deque |
| DISPLAY_ADAPTATION_LAYER.md | VRR specs, E-ink specs, WCAG 2.3.1 |
| TEST_MATRIX.md | Platform docs, hardware specs |
| TYPOGRAPHY_SYSTEM.md | WCAG 1.4.4, 1.4.12, readability research |
| EVIDENCE_MATRIX.md | All primary sources |

---

## 13. Cross-References to Papers/ Compendiums

This bibliography cites sources that are further cataloged in the `papers/` compendiums:

| Bibliography Section | Compendium File | Coverage |
|---------------------|-----------------|----------|
| Sec 2 (CVD Simulation) | `papers/colorblindness_algorithms_compendium.md` | Brettel, Vienot, Machado algorithms + 2025-2026 additions |
| Sec 3 (Color Science) | `papers/COLORBLINDNESS_ACADEMIC_PAPERS.md` | Cone fundamentals, genetics, epidemiology |
| Sec 4 (Seizure Safety) | `papers/photosensitive_epilepsy_research_compendium.md` | ITU-R BT.1702, Fisher 2022, PEAT |
| Sec 6 (Neurodivergence) | `papers/ADHD_Visual_Processing_Papers_2023-2025.md` | ADHD visual processing, eye tracking |
| Sec 6 (Neurodivergence) | `papers/autism_visual_processing_bibliography.md` | Autism visual perception |
| Sec 7 (Cognitive Load) | `papers/cognitive_load_visual_processing_papers.md` | CLT, VWM, fNIRS |
| Sec 3 (Achromatopsia) | `papers/achromatopsia_bcm_research_compendium.md` | Gene therapy trials, BCM |
| (Dyslexia) | `research/neurodivergence/dyslexia/DYSLEXIA_VISUAL_PROCESSING_RESEARCH.md` | Magnocellular pathway, visual processing |

---

## 14. License Information

| Resource Type | Common Licenses |
|---------------|-----------------|
| WCAG/W3C | W3C Document License |
| ISO Standards | Commercial (purchase required) |
| Open source tools | MIT, BSD, Apache 2.0 |
| Academic papers | Various (often paywalled) |

---

## 15. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-27 | Initial compilation from all UVAS+ specs |
| 1.1.0 | 2026-03-19 | Added APCA reference, WCAG 3.0 status update, cross-references to papers/ compendiums |

---

*REFERENCES_BIBLIOGRAPHY.md Version 1.1.0 - Updated 2026-03-19*
