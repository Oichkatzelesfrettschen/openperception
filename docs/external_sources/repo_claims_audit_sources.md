# Repo Claims Audit Sources

This source index supports the March 26, 2026 repo-audit tranche recorded in
`docs/repo-audit-2026-03-26.md`.

Machine-readable bibliography support now lives in:

- [repo_claims_audit_sources.bib](/home/eirikr/Github/openperception/docs/external_sources/repo_claims_audit_sources.bib)
- [paper_corpus_tracking.bib](/home/eirikr/Github/openperception/papers/downloads/paper_corpus_tracking.bib)

## Primary Sources

### Python Language Support

- Python 3.10 "What's New" page documenting PEP 604, the union type operator:
  https://docs.python.org/3/whatsnew/3.10.html

### Web Accessibility Standards

- WCAG 2.1 Understanding SC 1.4.3 Contrast (Minimum) -- 4.5:1 normal text / 3:1 large text:
  https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- WCAG 2.1 Understanding SC 1.4.11 Non-text Contrast -- 3:1 UI components and graphics:
  https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html
- WCAG 2.2 Understanding SC 2.4.13 Focus Appearance:
  https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
- WCAG 2.2 Understanding SC 2.3.1 Three Flashes Or Below Threshold:
  https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html

### Ergonomics And ISO Standards

- ISO 9241-171:2008 Ergonomics of human-system interaction -- Part 171:
  Guidance on software accessibility.  Cited as a foundational standard
  in the ROADMAP priority matrix.  Abstract and scope at:
  https://www.iso.org/standard/39080.html

### Depth And Stereoblindness

- Chopin, Bavelier, and Levi 2019 PubMed record for stereoblindness prevalence:
  https://pubmed.ncbi.nlm.nih.gov/30776852/
- Kim, Angelaki, and DeAngelis 2016 PMC full text for motion-parallax depth:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4901450/

## Local Runtime Evidence

- `python3 tools/validate.py`
- `python3 tools/check_claims_registry.py`
- `python3 -m pytest tools/tests/test_validate.py tools/tests/test_check_claims_registry.py -q`
- `make check`
