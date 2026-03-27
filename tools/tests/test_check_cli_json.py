"""Tests for machine-readable integrity-check CLI output."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from .test_check_paper_corpus import seed_minimal_repo
from .test_check_source_assets import seed_asset_repo
from .test_check_source_cache_links import write_source_cache
from .test_check_task_governance import seed_repo


TOOLS_DIR = Path(__file__).resolve().parents[1]


def run_check(script_name: str, *args: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(TOOLS_DIR / script_name), "--json", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_task_governance_cli_emits_json(tmp_path: Path) -> None:
    seed_repo(tmp_path)

    payload = run_check("check_task_governance.py", "--repo-root", str(tmp_path))

    assert payload["ok"] is True
    assert payload["check_id"] == "governance"
    assert "T001" in payload["task_refs"]
    assert "KI-004" in payload["issue_refs"]


def test_source_cache_links_cli_emits_json(tmp_path: Path) -> None:
    source_cache = tmp_path / "docs" / "external_sources" / "topic_source_cache.md"
    report = tmp_path / "research" / "topic" / "REPORT.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(f"# report\n\n- [Source cache]({source_cache})\n", encoding="utf-8")
    write_source_cache(
        source_cache,
        f"# Topic Source Cache\n\n- [Report]({report})\n",
    )

    payload = run_check("check_source_cache_links.py", "--repo-root", str(tmp_path))

    assert payload["ok"] is True
    assert payload["check_id"] == "source_cache_links"
    assert "T083" in payload["task_refs"]


def test_source_assets_cli_emits_json(tmp_path: Path) -> None:
    seed_asset_repo(tmp_path)

    payload = run_check("check_source_assets.py", "--repo-root", str(tmp_path))

    assert payload["ok"] is True
    assert payload["check_id"] == "source_assets"
    assert "T082" in payload["task_refs"]


def test_paper_corpus_cli_emits_json(tmp_path: Path) -> None:
    registry = seed_minimal_repo(tmp_path)

    payload = run_check(
        "check_paper_corpus.py",
        "--registry",
        str(registry),
        "--repo-root",
        str(tmp_path),
    )

    assert payload["ok"] is True
    assert payload["check_id"] == "paper_corpus"
    assert payload["metadata"]["registry_path"] == str(registry)


def test_claims_registry_cli_emits_json() -> None:
    payload = run_check("check_claims_registry.py")

    assert payload["ok"] is True
    assert payload["check_id"] == "claims_registry"
    assert "T041" in payload["task_refs"]


def test_repo_stats_cli_emits_json(tmp_path: Path) -> None:
    from .test_check_repo_stats import seed_repo

    stats_json, stats_md = seed_repo(tmp_path)

    payload = run_check(
        "check_repo_stats.py",
        "--repo-root",
        str(tmp_path),
        "--stats-json",
        str(stats_json),
        "--stats-md",
        str(stats_md),
    )

    assert payload["ok"] is True
    assert payload["check_id"] == "repo_stats"
    assert "T056" in payload["task_refs"]
