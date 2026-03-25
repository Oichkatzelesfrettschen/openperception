# Ishihara Source Asset

This directory holds the repo's cached Ishihara 38-plate reference PDF as a
dataset-support asset rather than as a literature paper.

## Why This Lives Here

- The file supports the Ishihara learning-tool lane under
  `datasets/ishihara-plate-learning/`.
- It is not treated as a canonical academic paper for the paper corpus.
- Keeping it outside `research/` prevents the paper-corpus verifier from having
  to tolerate special-case PDF debt.

## Provenance Status

The current local artifact now has an exact re-verified upstream source URL.
Its local hash, former path, and current role are recorded in `PROVENANCE.json`.

The current verification trace lives in `verification_trace.md`, which records:

- re-verified bibliographic and product references for the 38-plate edition,
- hash comparison against public mirror PDFs,
- the remaining gap between content verification and exact acquisition-path
  verification.
