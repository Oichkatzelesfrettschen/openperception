#!/usr/bin/env python3
"""Helpers for warning-clean OctaneBlender automation."""
from __future__ import annotations

import os
import pathlib
import shutil
import socket
import subprocess
import time


WARNING_PATTERNS = (
    "error of initialization or activation on render-server",
    "can't connect to octane server",
    "connecttoserver",
    "socket connect error",
    "error binding socket on tcp port",
)


def build_octane_env() -> dict[str, str]:
    """Return an environment compatible with OctaneServer launches."""
    env = os.environ.copy()
    env.pop("OCIO", None)
    return env


def is_local_port_open(port: int, host: str = "127.0.0.1", timeout: float = 0.5) -> bool:
    """Return whether a local TCP port is actively accepting connections."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def _pgrep_matches(pattern: str) -> list[int]:
    proc = subprocess.run(
        ["pgrep", "-f", pattern],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return []
    matches: list[int] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.isdigit():
            matches.append(int(line))
    return matches


def ensure_octane_server(
    log_path: str | pathlib.Path | None = None,
    wait_seconds: float = 10.0,
) -> dict[str, object]:
    """Ensure OctaneServer is listening on localhost:5130."""
    server_binary = shutil.which("OctaneServer")
    if server_binary is None:
        return {
            "binary": "",
            "launched": False,
            "running": False,
            "pids": [],
            "output": "OctaneServer not found on PATH",
            "log_path": str(log_path) if log_path is not None else "",
        }

    existing_pids = _pgrep_matches(r"^/usr/local/OctaneServer/OctaneServer")
    if existing_pids and is_local_port_open(5130):
        return {
            "binary": server_binary,
            "launched": False,
            "running": True,
            "pids": existing_pids,
            "output": "OctaneServer already running",
            "log_path": str(log_path) if log_path is not None else "",
        }

    env = build_octane_env()
    resolved_log = pathlib.Path(log_path).resolve() if log_path is not None else None
    log_handle = None
    try:
        if resolved_log is not None:
            resolved_log.parent.mkdir(parents=True, exist_ok=True)
            log_handle = resolved_log.open("a", encoding="utf-8")
        else:
            log_handle = pathlib.Path(os.devnull).open("w", encoding="utf-8")

        subprocess.Popen(
            [server_binary],
            stdin=subprocess.DEVNULL,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=env,
        )
    except Exception as exc:
        if log_handle is not None:
            log_handle.close()
        return {
            "binary": server_binary,
            "launched": False,
            "running": False,
            "pids": [],
            "output": f"OctaneServer launch failed: {exc}",
            "log_path": str(resolved_log) if resolved_log is not None else "",
        }
    finally:
        if log_handle is not None:
            log_handle.close()

    deadline = time.time() + wait_seconds
    while time.time() < deadline:
        pids = _pgrep_matches(r"^/usr/local/OctaneServer/OctaneServer")
        if pids and is_local_port_open(5130):
            return {
                "binary": server_binary,
                "launched": True,
                "running": True,
                "pids": pids,
                "output": "OctaneServer auto-launched",
                "log_path": str(resolved_log) if resolved_log is not None else "",
            }
        time.sleep(0.25)

    return {
        "binary": server_binary,
        "launched": True,
        "running": False,
        "pids": _pgrep_matches(r"^/usr/local/OctaneServer/OctaneServer"),
        "output": (
            "OctaneServer auto-launch attempted, but no live listening server "
            "was detected on 127.0.0.1:5130"
        ),
        "log_path": str(resolved_log) if resolved_log is not None else "",
    }


def collect_octane_warnings(output: str) -> list[str]:
    """Return matched warning patterns from Octane stdout/stderr."""
    lowered = output.lower()
    matches: list[str] = []
    for pattern in WARNING_PATTERNS:
        if pattern in lowered:
            matches.append(pattern)
    return matches


def build_headless_probe_command(blender_executable: str, python_expr: str) -> list[str]:
    """Build the canonical warning-clean OctaneBlender probe command."""
    return [
        blender_executable,
        "--background",
        "--factory-startup",
        "--python-expr",
        python_expr,
    ]
