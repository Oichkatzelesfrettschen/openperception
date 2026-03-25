"""Tests for claims registry and coverage reporting."""
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from claims_coverage_report import build_json_report, build_markdown_report
from claims_registry import load_claims_registry, summarize_claims_registry


def test_claims_registry_loads_seeded_claims() -> None:
    registry = load_claims_registry()

    assert registry["claims"]
    assert any(claim["claim_id"] == "CLM-0010" for claim in registry["claims"])


def test_claims_registry_summary_has_status_counts_and_gate_links() -> None:
    summary = summarize_claims_registry()

    assert summary["claim_count"] >= 10
    assert summary["status_counts"]["implemented"] >= 1
    assert "GATE-002" in summary["claims_by_gate"]
    assert "GATE-003" in summary["claims_by_gate"]
    assert "GATE-006" in summary["claims_by_gate"]


def test_claims_markdown_report_contains_expected_claims() -> None:
    report = build_markdown_report()

    assert "## Claims" in report
    assert "CLM-0001" in report
    assert "GATE-001" in report


def test_claims_json_report_contains_registry_and_summary() -> None:
    report = build_json_report()

    assert "summary" in report
    assert "registry" in report
    assert any(claim["claim_id"] == "CLM-0023" for claim in report["registry"]["claims"])
    assert any(claim["claim_id"] == "CLM-0100" for claim in report["registry"]["claims"])
    assert any(claim["claim_id"] == "CLM-0092" for claim in report["registry"]["claims"])
    assert any(claim["claim_id"] == "CLM-0093" for claim in report["registry"]["claims"])
    assert any(claim["claim_id"] == "CLM-0094" for claim in report["registry"]["claims"])
    assert any(claim["claim_id"] == "CLM-0095" for claim in report["registry"]["claims"])
