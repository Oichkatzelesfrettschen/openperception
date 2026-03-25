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

## Exact-File Comparison History

The exact upstream source for the local file was recovered:

- `https://www.challengetb.org/publications/tools/country/Ishihara_Tests.pdf`

That file is a byte-for-byte match for the local cached asset:

- SHA-256: `549b389d9bf921006a0d4d52941728b1b15f77df3cf766a79e0f21a1d3b31786`
- Size: `2816420` bytes

Other public PDF mirrors were also fetched and compared by hash:

- `https://www.iisgaribaldi.edu.it/wp-content/uploads/2024/12/tavolediishihara.pdf`
- `https://picassciences.com/wp-content/uploads/2015/01/ishihara38.pdf`

Those two mirrors did not match the local Challenge TB copy. The first two
mirrors matched each other:

- SHA-256: `c7a2e710c132d37098fb048e4766e74a68a8baee0799422deb9e3d19e0d77d21`
- Size: `1494387` bytes

The University of Mustansiriyah copy was also a different file:

- `https://uomustansiriyah.edu.iq/media/lectures/3/3_2025_09_22%2112_51_13_AM.pdf`
- SHA-256: `3a3d90171492e3d2cb87ea7b148fca53f439fc5fb1455592a0b1f0793f20e1d6`
- Size: `2687974` bytes

## Current Interpretation

The local file is now tied to an exact upstream acquisition URL, while the
mirror comparisons remain useful evidence that multiple public Ishihara 38-set
PDF layouts circulate online.
