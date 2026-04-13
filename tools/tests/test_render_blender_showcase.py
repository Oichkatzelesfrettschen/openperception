"""Tests for the repo-owned Blender showcase render driver."""

from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from render_blender_showcase import run_showcase_regeneration


def test_render_driver_stops_on_failed_probe(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        "render_blender_showcase._run_repo_stats",
        lambda: type("Proc", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
    )
    monkeypatch.setattr(
        "render_blender_showcase._run_spec_generation",
        lambda *_args, **_kwargs: type(
            "Proc", (), {"returncode": 0, "stdout": "", "stderr": ""}
        )(),
    )
    monkeypatch.setattr(
        "render_blender_showcase.run_probe",
        lambda *_args, **_kwargs: {
            "ok": False,
            "warnings": ["can't connect to octane server"],
        },
    )

    report = run_showcase_regeneration(
        "OctaneBlender",
        "octane",
        tmp_path / "spec.json",
        tmp_path / "render.png",
        tmp_path / "scene.blend",
        skip_probe=False,
    )

    assert report["ok"] is False
    assert report["probe"]["ok"] is False
    assert report["render"] == {}


def test_render_driver_reports_warning_matches(monkeypatch, tmp_path) -> None:
    class _Proc:
        returncode = 0
        stdout = "Octane: can't connect to Octane server.\n"
        stderr = ""

    spec_path = tmp_path / "spec.json"
    render_path = tmp_path / "render.png"
    blend_path = tmp_path / "scene.blend"
    spec_path.write_text("{}", encoding="utf-8")
    render_path.write_text("png", encoding="utf-8")
    blend_path.write_text("blend", encoding="utf-8")

    monkeypatch.setattr(
        "render_blender_showcase._run_repo_stats",
        lambda: type("Proc", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
    )
    monkeypatch.setattr(
        "render_blender_showcase._run_spec_generation",
        lambda *_args, **_kwargs: type(
            "Proc", (), {"returncode": 0, "stdout": "", "stderr": ""}
        )(),
    )
    monkeypatch.setattr(
        "render_blender_showcase._render_showcase",
        lambda *_args, **_kwargs: _Proc(),
    )

    report = run_showcase_regeneration(
        "OctaneBlender",
        "octane",
        spec_path,
        render_path,
        blend_path,
        skip_probe=True,
    )

    assert report["ok"] is False
    assert report["render"]["warnings"] == ["can't connect to octane server"]


def test_render_driver_succeeds_when_outputs_exist_and_no_warnings(
    monkeypatch, tmp_path
) -> None:
    class _Proc:
        returncode = 0
        stdout = "render ok\n"
        stderr = ""

    spec_path = tmp_path / "spec.json"
    render_path = tmp_path / "render.png"
    blend_path = tmp_path / "scene.blend"
    spec_path.write_text("{}", encoding="utf-8")
    render_path.write_text("png", encoding="utf-8")
    blend_path.write_text("blend", encoding="utf-8")

    monkeypatch.setattr(
        "render_blender_showcase._run_repo_stats",
        lambda: type("Proc", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
    )
    monkeypatch.setattr(
        "render_blender_showcase._run_spec_generation",
        lambda *_args, **_kwargs: type(
            "Proc", (), {"returncode": 0, "stdout": "", "stderr": ""}
        )(),
    )
    monkeypatch.setattr(
        "render_blender_showcase.run_probe",
        lambda *_args, **_kwargs: {"ok": True, "warnings": []},
    )
    monkeypatch.setattr(
        "render_blender_showcase._render_showcase",
        lambda *_args, **_kwargs: _Proc(),
    )

    report = run_showcase_regeneration(
        "OctaneBlender",
        "auto",
        spec_path,
        render_path,
        blend_path,
        skip_probe=False,
    )

    assert report["ok"] is True
    assert report["render"]["warnings"] == []
