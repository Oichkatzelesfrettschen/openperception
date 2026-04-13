#!/usr/bin/env python3
"""Run a warning-clean OctaneBlender headless startup probe."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess

from octane_bootstrap import (
    build_headless_probe_command,
    build_octane_env,
    collect_octane_warnings,
    ensure_octane_server,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--blender-executable",
        default="OctaneBlender",
        help="Octane Blender executable to probe (default: OctaneBlender).",
    )
    parser.add_argument(
        "--python-expr",
        default='print("probe")',
        help="Python expression to execute during the probe.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=60,
        help="Maximum time to wait for the probe subprocess.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a machine-readable JSON report.",
    )
    return parser.parse_args()


def run_probe(
    blender_executable: str,
    python_expr: str,
    timeout_seconds: int,
) -> dict[str, object]:
    resolved_executable = shutil.which(blender_executable) or blender_executable
    server_info = ensure_octane_server(
        pathlib.Path("/tmp/openperception_octaneserver_probe.log")
    )
    command = build_headless_probe_command(resolved_executable, python_expr)
    env = build_octane_env()
    proc = subprocess.run(
        command,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    combined_output = (proc.stdout or "") + (proc.stderr or "")
    warnings = collect_octane_warnings(combined_output)
    report = {
        "blender_executable": resolved_executable,
        "command": command,
        "returncode": proc.returncode,
        "server": server_info,
        "warnings": warnings,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "ok": proc.returncode == 0
        and server_info.get("running", False)
        and not warnings,
    }
    return report


def main() -> int:
    args = parse_args()
    report = run_probe(args.blender_executable, args.python_expr, args.timeout_seconds)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Blender executable: {report['blender_executable']}")
        print(f"Server status: {report['server']['output']}")
        if report["warnings"]:
            print("Warnings:")
            for warning in report["warnings"]:
                print(f"- {warning}")
        else:
            print("Warnings: none")
        print(f"Return code: {report['returncode']}")
        print(f"Probe status: {'ok' if report['ok'] else 'failed'}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
