# Non-Paper Source Assets

This index tracks repo-owned reference artifacts that support datasets or tools
but do not belong in the canonical academic paper corpus.

## Scope

Use this lane for non-paper assets that would be misleading inside
`papers/downloads/`, such as test-sheet PDFs, reference stimuli, or teaching
materials used by a dataset or interactive tool.

## Tracked Assets

| ID | Asset | Local Path | Provenance | Notes |
|----|-------|------------|------------|-------|
| `ishihara_38_plate_reference` | Ishihara Colour Plates - 38 Set | `datasets/source_assets/ishihara/Ishihara_38_Plates_Test.pdf` | `datasets/source_assets/ishihara/PROVENANCE.json` | Migrated out of `research/` because it is a dataset-support reference asset, not a literature paper. Bibliographic provenance for the 38-plate edition is re-verified, while exact byte-level acquisition lineage for the local PDF remains unresolved and is documented in the verification trace. |

## Related Docs

- [Dataset source assets README](/home/eirikr/Github/openperception/datasets/source_assets/README.md)
- [Ishihara source asset README](/home/eirikr/Github/openperception/datasets/source_assets/ishihara/README.md)
- [Ishihara verification trace](/home/eirikr/Github/openperception/datasets/source_assets/ishihara/verification_trace.md)
- [Research PDF migration inventory](/home/eirikr/Github/openperception/docs/external_sources/research_pdf_migration_inventory.md)

## Verification

Run:

```bash
python3 tools/check_source_assets.py
```

The verifier checks:

- every file under `datasets/source_assets/` is indexed in a nearby
  `PROVENANCE.json`,
- recorded hashes and sizes match the local artifacts,
- PDF assets have valid `%PDF` headers,
- each asset entry provides either an exact upstream URL or bibliographic
  reference URLs,
- any declared verification trace exists.
