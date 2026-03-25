# DaltonLens-Python In This Repo

Date: 2026-03-22

## What it is

`algorithms/DaltonLens-Python` is a vendored Python package for color-vision
deficiency simulation and daltonization.

Repo-local evidence:

- `algorithms/DaltonLens-Python/README.md`
- `algorithms/DaltonLens-Python/daltonlens/main.py`
- `algorithms/DaltonLens-Python/daltonlens/simulate.py`
- `algorithms/DaltonLens-Python/daltonlens/convert.py`
- `algorithms/DaltonLens-Python/tests/test_simulate.py`

Its role inside `openperception` is not just "reference material." It is the
actual engine we are already using to reason about palette collapse under
protan, deutan, and tritan simulation.

## Step 1. Entry points

The package has a simple CLI entry:

- `daltonlens/__main__.py` imports and runs `main()`
- `daltonlens/main.py` implements the command-line tool

The CLI supports:

- `simulate`
- `daltonize`

with model selection:

- `auto`
- `vienot`
- `brettel`
- `machado`
- `vischeck`
- `coblisV1`
- `coblisV2`

## Step 2. Core job of the package

At the highest level, DaltonLens-Python does three things:

1. convert image data between color spaces,
2. simulate how colors/images appear under different CVD regimes,
3. optionally transform colors to improve distinguishability.

That means it is an algorithmic engine, not just an image viewer.

## Step 3. The data path

The path through the code is:

1. load image as sRGB `uint8`
2. convert to normalized float
3. linearize sRGB into linear RGB
4. convert linear RGB into LMS-like cone space
5. apply a simulation transform for the chosen deficiency/model
6. convert back to linear RGB
7. encode back to sRGB `uint8`

You can see those pieces directly in:

- `daltonlens/main.py`
- `daltonlens/convert.py`
- `daltonlens/simulate.py`

## Step 4. Why LMS matters here

The package is built around LMS-style cone models because CVD simulation is
most naturally expressed in terms of altered cone responses and confusion
directions.

The conversion layer in `convert.py` provides:

- sRGB <-> linear RGB
- linear RGB <-> XYZ
- XYZ <-> LMS

and a set of `LMSModel` implementations, including the repo-preferred:

- `LMSModel_sRGB_SmithPokorny75`

This is the important bridge between display color and perceptual simulation.

## Step 5. How simulation is organized

`simulate.py` contains:

- `Deficiency.PROTAN`
- `Deficiency.DEUTAN`
- `Deficiency.TRITAN`

and several simulator classes.

The most important ones for this repo are:

- `Simulator_Vienot1999`
- `Simulator_Brettel1997`
- `Simulator_Machado2009`
- `Simulator_AutoSelect`

The selection logic is especially important:

- tritan -> Brettel 1997
- full-severity protan/deutan -> Vienot 1999
- lower-severity anomalous cases -> Machado 2009

That is exactly why our palette checks have been meaningful instead of arbitrary.

## Step 6. Why this matters to OpenPerception

For this repo, DaltonLens-Python is the foundation for saying things like:

- the current indigo/magenta pair collapses under protan,
- the proposed indigo/mauve pair improves deutan separation,
- a red theme can be atmospheric without being a safe semantic default.

Without a simulation engine, those would be aesthetic claims.
With DaltonLens-Python, they become testable claims.

## Step 7. Test structure

The vendored package includes a healthy test corpus:

- CLI tests
- conversion tests
- daltonization tests
- simulation tests
- regression images in `tests/images`

`tests/test_simulate.py` compares generated outputs against stored golden
images for:

- Vienot 1999
- Brettel 1997
- Vischeck
- Machado 2009
- Coblis variants
- AutoSelect routing

That makes it more than a loose dependency: it is a reproducible subsystem.

## Step 8. Research and notebook layer

The vendored subtree also includes:

- `research/`
- notebooks for precomputed matrices
- notebooks for simulation analysis

So the package spans three layers:

1. theory/research notebooks,
2. library code,
3. tested CLI/runtime behavior.

## Step 9. What it is not

DaltonLens-Python is not:

- the whole of `openperception`,
- the only accessibility check in the repo,
- a design-token system by itself.

Instead, it is one of the repo's foundational engines, paired with:

- token files,
- contrast checks,
- Oklab/OKLCH reasoning,
- docs and examples.

## Step 10. Why it showed up as a dirty subtree

`git status` showed `algorithms/DaltonLens-Python` as a pre-existing worktree
item. That likely means:

- it is vendored from upstream,
- or it is a git submodule / nested git checkout,
- or it has local edits not made in this pass.

I did not modify it in this round.

## Bottom line

Inside this repo, DaltonLens-Python is the simulation backbone that lets the
palette work move from taste to evidence.
