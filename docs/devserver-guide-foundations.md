# Devserver Guide From Foundations

Date: 2026-03-22

## What `devserver-guide.md` really is

`docs/devserver-guide.md` is the repo's iteration-speed note.

It exists because many of the repo's examples and publishing artifacts are only
meaningful when served through HTTP rather than opened directly from disk.

So this guide is part of the repo's developer-experience infrastructure, not
its accessibility theory layer.

## Step 1. Identify the problem it solves

The dev server solves a very practical problem:

- browser examples need a real HTTP origin,
- token CSS and example scripts need predictable relative paths,
- people need a fast feedback loop while editing docs and demos.

Without this, even good examples become annoying to validate and easy to
misread.

## Step 2. What the implementation actually is

The guide points at `tools/devserver.py`, which is intentionally simple:

- Python stdlib HTTP serving,
- file watching,
- live-reload notifications,
- configurable port and root directory.

This minimalism matters. It keeps the repo easy to run without requiring a
heavy JS toolchain.

## Step 3. Why this matters in OpenPerception

OpenPerception has several artifact types that benefit from fast local serving:

- browser simulator examples,
- contrast examples,
- palette comparison pages,
- generated docs and static outputs.

That means the dev server is not just a convenience. It is part of how the repo
keeps theory and visible output tightly coupled during iteration.

## Step 4. Where the guide is slightly inaccurate

One small implementation detail is worth noting:

- the guide's troubleshooting note mentions WebSocket errors,
- but `tools/devserver.py` uses Server-Sent Events for live reload.

That does not change how people use it, but it is the kind of detail that
matters in a foundations note because it clarifies what the tool actually is.

## Step 5. What this guide reveals about the repo

The dev server guide shows that OpenPerception values:

- local reproducibility,
- low-friction previewing,
- and quick validation of accessibility-facing examples.

That may sound mundane, but it is important. A repo with many visual claims
needs a clean way to inspect those claims in practice.

## Bottom line

`docs/devserver-guide.md` is the repo's local-iteration guide. It turns the
project's static examples and token-driven outputs into something easy to serve,
inspect, and reload, which helps keep accessibility work visible while it is
being developed.
