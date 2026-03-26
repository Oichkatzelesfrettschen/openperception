# Repo Claims Audit Sources

This source index supports the March 26, 2026 repo-audit tranche recorded in
`docs/repo-audit-2026-03-26.md`.

## Primary Sources

### Python Language Support

- Python 3.10 "What's New" page documenting PEP 604, the union type operator:
  https://docs.python.org/3/whatsnew/3.10.html

### Web Accessibility Standards

- WCAG 2.1 Understanding SC 1.4.3 Contrast (Minimum):
  https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- WCAG 2.2 Understanding SC 2.4.13 Focus Appearance:
  https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html

### Depth And Stereoblindness

- Chopin, Bavelier, and Levi 2019 PubMed record for stereoblindness prevalence:
  https://pubmed.ncbi.nlm.nih.gov/30776852/

## Local Runtime Evidence

- `python3 tools/validate.py`
- `python3 tools/check_claims_registry.py`
- `python3 -m pytest tools/tests/test_validate.py tools/tests/test_check_claims_registry.py -q`
