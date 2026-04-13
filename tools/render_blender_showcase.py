#!/usr/bin/env python3
"""Regenerate the living Blender showcase through the repo-owned clean path."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from octane_bootstrap import build_octane_env, collect_octane_warnings
from octane_headless_probe import run_probe


REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_STATS_JSON = REPO_ROOT / "docs" / "generated" / "repo_stats.json"
REPO_STATS_MD = REPO_ROOT / "docs" / "generated" / "repo_stats.md"
SPEC_OUTPUT = (
    REPO_ROOT
    / "artifacts"
    / "blender_showcase"
    / "openperception_palette_showcase_spec.json"
)
RENDER_OUTPUT = (
    REPO_ROOT
    / "artifacts"
    / "blender_showcase"
    / "openperception_palette_showcase_render.png"
)
BLEND_OUTPUT = (
    REPO_ROOT
    / "artifacts"
    / "blender_showcase"
    / "openperception_palette_showcase_scene.blend"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blender-executable", default="OctaneBlender")
    parser.add_argument(
        "--engine", choices=("auto", "octane", "eevee", "cycles"), default="auto"
    )
    parser.add_argument("--spec-output", default=str(SPEC_OUTPUT))
    parser.add_argument("--render-output", default=str(RENDER_OUTPUT))
    parser.add_argument("--blend-output", default=str(BLEND_OUTPUT))
    parser.add_argument("--skip-probe", action="store_true")
    parser.add_argument(
        "--json", action="store_true", help="Emit a machine-readable report."
    )
    return parser.parse_args()


def _run_command(
    command: list[str], *, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, capture_output=True, text=True, env=env)


def _run_repo_stats() -> subprocess.CompletedProcess[str]:
    return _run_command(
        [
            shutil.which("python3") or "python3",
            str(REPO_ROOT / "tools" / "repo_stats.py"),
            "--output-json",
            str(REPO_STATS_JSON),
            "--output-md",
            str(REPO_STATS_MD),
        ]
    )


def _run_spec_generation(spec_output: Path) -> subprocess.CompletedProcess[str]:
    return _run_command(
        [
            shutil.which("python3") or "python3",
            str(REPO_ROOT / "tools" / "palette_showcase_spec.py"),
            "--output",
            str(spec_output),
        ]
    )


def _render_showcase(
    blender_executable: str,
    engine: str,
    spec_output: Path,
    render_output: Path,
    blend_output: Path,
) -> subprocess.CompletedProcess[str]:
    env = build_octane_env()
    return _run_command(
        [
            shutil.which(blender_executable) or blender_executable,
            "--background",
            "--factory-startup",
            "--python",
            str(REPO_ROOT / "tools" / "blender_palette_showcase_scene.py"),
            "--",
            "--spec",
            str(spec_output),
            "--output",
            str(render_output),
            "--engine",
            engine,
            "--blend-output",
            str(blend_output),
        ],
        env=env,
    )


def run_showcase_regeneration(
    blender_executable: str,
    engine: str,
    spec_output: Path,
    render_output: Path,
    blend_output: Path,
    *,
    skip_probe: bool,
) -> dict[str, object]:
    report: dict[str, object] = {
        "blender_executable": shutil.which(blender_executable) or blender_executable,
        "engine": engine,
        "repo_stats": {},
        "spec_generation": {},
        "probe": None,
        "render": {},
    }

    repo_stats_proc = _run_repo_stats()
    report["repo_stats"] = {
        "returncode": repo_stats_proc.returncode,
        "stdout": repo_stats_proc.stdout,
        "stderr": repo_stats_proc.stderr,
    }
    if repo_stats_proc.returncode != 0:
        report["ok"] = False
        return report

    spec_proc = _run_spec_generation(spec_output)
    report["spec_generation"] = {
        "returncode": spec_proc.returncode,
        "stdout": spec_proc.stdout,
        "stderr": spec_proc.stderr,
    }
    if spec_proc.returncode != 0:
        report["ok"] = False
        return report

    if not skip_probe and engine in {"auto", "octane"}:
        probe = run_probe(blender_executable, 'print("probe")', 60)
        report["probe"] = probe
        if not probe["ok"]:
            report["ok"] = False
            return report

    render_proc = _render_showcase(
        blender_executable, engine, spec_output, render_output, blend_output
    )
    combined_output = (render_proc.stdout or "") + (render_proc.stderr or "")
    warnings = collect_octane_warnings(combined_output)
    report["render"] = {
        "returncode": render_proc.returncode,
        "stdout": render_proc.stdout,
        "stderr": render_proc.stderr,
        "warnings": warnings,
        "render_output": str(render_output),
        "blend_output": str(blend_output),
        "render_exists": render_output.exists(),
        "blend_exists": blend_output.exists(),
    }
    report["ok"] = (
        render_proc.returncode == 0
        and not warnings
        and render_output.exists()
        and blend_output.exists()
    )
    return report


def main() -> int:
    args = parse_args()
    report = run_showcase_regeneration(
        args.blender_executable,
        args.engine,
        Path(args.spec_output),
        Path(args.render_output),
        Path(args.blend_output),
        skip_probe=args.skip_probe,
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"Repo stats: {'ok' if report['repo_stats'].get('returncode') == 0 else 'failed'}"
        )
        print(
            f"Spec generation: {'ok' if report['spec_generation'].get('returncode') == 0 else 'failed'}"
        )
        if report["probe"] is not None:
            print(f"Probe: {'ok' if report['probe']['ok'] else 'failed'}")
        print(
            f"Render: {'ok' if report['render'].get('returncode') == 0 else 'failed'}"
        )
        warnings = report["render"].get("warnings", [])
        print(f"Render warnings: {', '.join(warnings) if warnings else 'none'}")
        print(f"Showcase regeneration: {'ok' if report.get('ok') else 'failed'}")
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
