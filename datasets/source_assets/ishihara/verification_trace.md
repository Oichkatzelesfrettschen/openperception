# Ishihara Verification Trace

Updated: 2026-03-25

## Local Asset

- Path: `datasets/source_assets/ishihara/Ishihara_38_Plates_Test.pdf`
- SHA-256: `549b389d9bf921006a0d4d52941728b1b15f77df3cf766a79e0f21a1d3b31786`
- Size: `2816420` bytes

## What Was Re-Verified

The local PDF clearly contains the 38-plate Ishihara set plus answer-key pages.
Local text extraction shows:

- `ISHIHARA COLOUR PLATES`
- `ISHIHARA COLOUR PLATES - 38 SET`
- plate-by-plate normal / red-green-deficiency answers

Official or bibliographic references for the 38-plate edition were also
re-verified:

- Isshinkai reference page: confirms the Ishihara test was created by Dr.
  Shinobu Ishihara and describes the 38-plate edition as the standard
  publication.
- Oculus product page: lists "Ishihara Colour Chart (38 Plates Edition)" as a
  commercial diagnostic product.
- University of Edinburgh support-library catalogue: lists "Ishihara's tests
  for colour deficiency (38 plates)" with Kanehara Trading / Isshinkai
  bibliographic attribution.

## Exact-File Provenance Gap

Two public PDF mirrors were fetched and compared by hash:

- `https://www.iisgaribaldi.edu.it/wp-content/uploads/2024/12/tavolediishihara.pdf`
- `https://picassciences.com/wp-content/uploads/2015/01/ishihara38.pdf`

Those two mirrors matched each other:

- SHA-256: `c7a2e710c132d37098fb048e4766e74a68a8baee0799422deb9e3d19e0d77d21`
- Size: `1494387` bytes

They do not match the local cached asset, which means the exact acquisition
path for the local PDF is still unresolved. The current repo asset therefore
has stronger bibliographic verification than byte-level source-url verification.

## Current Interpretation

The local file is kept because its content is useful to the Ishihara learning
tool and clearly corresponds to the 38-plate reference set, but it should be
treated as a legacy local cache artifact until an exact upstream source can be
re-identified.
