# Stereoblindness And Depth Source Cache

This index documents the primary sources cached for the stereoblindness and
depth-accommodation work in OpenPerception.

## Scope

These artifacts back the repo's depth-axis guidance and the harmonized-depth
documentation. The cache prefers full-text primary sources when available and
records fallback traces when automated PDF retrieval is blocked.

Machine-readable provenance lives at:

- [PROVENANCE.json](/home/eirikr/Github/openperception/papers/downloads/stereoblindness/PROVENANCE.json)

## Cached Sources

| ID | Citation | Local Artifacts | Access Mode | Notes |
|----|----------|-----------------|-------------|-------|
| `chopin_2019` | Chopin, Bavelier, Levi. *Ophthalmic Physiol Opt* (2019). | `papers/downloads/stereoblindness/Chopin_Bavelier_Levi_2019_Stereoblindness_Best_Evidence_Synthesis.pubmed.txt` | Abstract only | PubMed abstract cached via NCBI E-utilities. Full text was not automatically retrieved in this environment. |
| `yang_2022` | Yang, Saunders, Chen. *Journal of Vision* (2022). | `papers/downloads/stereoblindness/Wang_Saunders_2022_Texture_Slant_Stereoblindness.html`, `papers/downloads/stereoblindness/Wang_Saunders_2022_Texture_Slant_Stereoblindness.txt`, `papers/downloads/stereoblindness/Wang_Saunders_2022_Texture_Slant_Stereoblindness.pdf.trace.html` | Full-text HTML | PMC article HTML was accessible. Direct PDF download returned a proof-of-work page, which was cached as a trace artifact. Local filenames retain an older Wang-based label, but the source paper authors are Yang, Saunders, and Chen. |
| `kim_2016` | Kim, Angelaki, DeAngelis. *Philosophical Transactions B* (2016). | `papers/downloads/stereoblindness/Nadler_et_al_2016_Motion_Parallax_Depth_Review.html`, `papers/downloads/stereoblindness/Nadler_et_al_2016_Motion_Parallax_Depth_Review.txt`, `papers/downloads/stereoblindness/Nadler_et_al_2016_Motion_Parallax_Depth_Review.pdf.trace.html` | Full-text HTML | PMC article HTML was accessible. Direct PDF download returned a proof-of-work page, which was cached as a trace artifact. Local filenames retain an older Nadler-based label, but the source paper authors are Kim, Angelaki, and DeAngelis. |
| `pladere_2022` | Pladere et al. *Frontiers in Virtual Reality* (2022). | `papers/downloads/stereoblindness/Pladere_et_al_2022_Inclusivity_in_Stereoscopic_XR.pdf`, `papers/downloads/stereoblindness/Pladere_et_al_2022_Inclusivity_in_Stereoscopic_XR.html`, `papers/downloads/stereoblindness/Pladere_et_al_2022_Inclusivity_in_Stereoscopic_XR.txt` | PDF and HTML | Open access. Used for XR-specific adaptation guidance. |

## Why This Matters

- The repo now has an offline-checkable source lane for depth accessibility.
- The cache makes it easier to revisit claims without re-browsing the web.
- The blocked-PDF traces make missing artifacts explicit instead of silently
  pretending every source was equally retrievable.

## Related Docs

- [Harmonized depth accommodation guide](/home/eirikr/Github/openperception/docs/harmonized-depth-accommodation-guide.md)
- [Primary source notes](/home/eirikr/Github/openperception/research/visual_impairments/stereoblindness/primary_source_notes.md)
