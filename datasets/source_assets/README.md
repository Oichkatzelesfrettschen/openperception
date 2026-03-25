# Dataset Source Assets

This lane holds tracked non-paper reference artifacts that support datasets,
interactive tools, or demonstrations in the repository.

## Scope

- Use `papers/downloads/` for literature papers and their provenance.
- Use `datasets/source_assets/` for non-paper reference assets such as clinical
  test sheets, sample stimuli, or tool-support files that should not be mixed
  into the paper corpus.

## Storage Policy

- PDF assets in this lane are stored with Git LFS.
- Keep filenames stable and ASCII-only.
- Add a small local provenance note for each asset so future cleanups do not
  have to reverse-engineer why the file is here.

## Verification

Run:

```bash
python3 tools/check_source_assets.py
```
