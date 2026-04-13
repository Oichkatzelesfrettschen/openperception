#!/usr/bin/env python3
"""Validate generated-output and artifact placement for the repository."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

NESTED_REPO_ROOTS = (
    "algorithms/DaltonLens-Python/.git",
    "algorithms/libDaltonLens/.git",
    "datasets/ishihara-plate-learning/.git",
)

SOURCE_TREE_BUILD_DIRS = (
    "algorithms/DaltonLens-Python/build",
    "algorithms/libDaltonLens/build",
    "datasets/ishihara-plate-learning/build",
)


def _run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def _is_lfs_pointer(path: Path) -> bool:
    return path.read_bytes()[:80].startswith(
        b"version https://git-lfs.github.com/spec/v1"
    )


def _collect_errors() -> list[str]:
    errors: list[str] = []

    for rel_path in NESTED_REPO_ROOTS:
        if (REPO_ROOT / rel_path).exists():
            errors.append(
                f"{rel_path} exists; absorbed source trees must not keep nested Git metadata"
            )

    for rel_path in SOURCE_TREE_BUILD_DIRS:
        if (REPO_ROOT / rel_path).exists():
            errors.append(
                f"{rel_path} exists; local build products belong under build/, not source trees"
            )

    for rel_path in (
        "artifacts/generated/",
        "artifacts/blender_showcase/generated/",
    ):
        check_ignore = subprocess.run(
            ["git", "check-ignore", "-q", rel_path],
            cwd=REPO_ROOT,
            check=False,
        )
        if check_ignore.returncode != 0:
            errors.append(f"{rel_path} is not ignored")

    lfs_paths = _run_git(["lfs", "ls-files", "--name-only"]).splitlines()
    for rel_path in lfs_paths:
        if rel_path.startswith(
            ("algorithms/DaltonLens-Python/", "algorithms/libDaltonLens/")
        ):
            errors.append(f"{rel_path} is still tracked through Git LFS")

    for root in (
        REPO_ROOT / "algorithms" / "DaltonLens-Python",
        REPO_ROOT / "algorithms" / "libDaltonLens",
    ):
        if not root.exists():
            continue
        for path in root.rglob("*.png"):
            if _is_lfs_pointer(path):
                errors.append(
                    f"{path.relative_to(REPO_ROOT)} is an LFS pointer, not a PNG blob"
                )

    return errors


def main() -> int:
    errors = _collect_errors()
    if errors:
        print("Artifact layout check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Artifact layout check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
