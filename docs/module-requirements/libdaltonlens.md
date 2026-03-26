# libDaltonLens Requirements

This file documents the local C build and test expectations for the
`algorithms/libDaltonLens/` submodule as used from the root repo.

## Required

- CMake 3.16+
- a working C compiler

## Build

```bash
cd algorithms/libDaltonLens
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release
```

## Test

```bash
cd algorithms/libDaltonLens/build
./tests/test_simulation
```

## Notes

- the root `Makefile` exposes this lane with `make build-c` and `make test-c`
- if your host lacks a compiler toolchain, the rest of the repo can still be
  used without this optional native build lane
