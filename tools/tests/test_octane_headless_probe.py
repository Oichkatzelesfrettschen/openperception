"""Tests for Octane headless bootstrap and probe helpers."""

from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from octane_bootstrap import build_headless_probe_command, collect_octane_warnings
from octane_headless_probe import run_probe


def test_build_headless_probe_command_uses_factory_startup() -> None:
    command = build_headless_probe_command("OctaneBlender", 'print("probe")')

    assert command == [
        "OctaneBlender",
        "--background",
        "--factory-startup",
        "--python-expr",
        'print("probe")',
    ]


def test_collect_octane_warnings_detects_connection_failures() -> None:
    output = """
Octane: ERROR of initialization or activation on render-server.
OctaneClient::connectToServer: socket connect error
Octane: can't connect to Octane server.
"""

    assert collect_octane_warnings(output) == [
        "error of initialization or activation on render-server",
        "can't connect to octane server",
        "connecttoserver",
        "socket connect error",
    ]


def test_run_probe_reports_success_without_octane_warnings(monkeypatch) -> None:
    class _Completed:
        returncode = 0
        stdout = "probe ok\n"
        stderr = ""

    monkeypatch.setattr(
        "octane_headless_probe.ensure_octane_server",
        lambda *_args, **_kwargs: {
            "running": True,
            "output": "OctaneServer already running",
        },
    )
    monkeypatch.setattr(
        "octane_headless_probe.shutil.which", lambda value: f"/usr/bin/{value}"
    )
    monkeypatch.setattr(
        "octane_headless_probe.subprocess.run", lambda *args, **kwargs: _Completed()
    )

    report = run_probe("OctaneBlender", 'print("probe")', 60)

    assert report["ok"] is True
    assert report["warnings"] == []
    assert report["command"] == [
        "/usr/bin/OctaneBlender",
        "--background",
        "--factory-startup",
        "--python-expr",
        'print("probe")',
    ]


def test_run_probe_reports_failure_when_warning_patterns_match(monkeypatch) -> None:
    class _Completed:
        returncode = 0
        stdout = "Octane: can't connect to Octane server.\n"
        stderr = ""

    monkeypatch.setattr(
        "octane_headless_probe.ensure_octane_server",
        lambda *_args, **_kwargs: {
            "running": True,
            "output": "OctaneServer already running",
        },
    )
    monkeypatch.setattr("octane_headless_probe.shutil.which", lambda value: value)
    monkeypatch.setattr(
        "octane_headless_probe.subprocess.run", lambda *args, **kwargs: _Completed()
    )

    report = run_probe("OctaneBlender", 'print("probe")', 60)

    assert report["ok"] is False
    assert report["warnings"] == ["can't connect to octane server"]
