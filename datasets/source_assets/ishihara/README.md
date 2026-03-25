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

The current local artifact is a legacy cached PDF whose exact upstream source
URL has not yet been re-verified. Its local hash, former path, and current role
are recorded in `PROVENANCE.json`.
