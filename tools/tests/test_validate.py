"""Tests for unified validator and runtime gap reporting."""
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime_gap_report import build_json_report, build_markdown_report
from validate import compute_overall_status, exit_code_for_results, run_validators


def write_tokens(path: Path, primary: str, accent: str) -> None:
    payload = {
        "default": {
            "brand": {
                "text": "#111111",
                "surface": "#FFFFFF",
                "primaryStrong": primary,
                "accentStrong": accent,
            },
            "gray": {
                "700": "#374151",
                "500": "#6B7280",
            },
        }
    }
    path.write_text(json.dumps(payload))


def test_run_validators_returns_implemented_and_missing(tmp_path: Path) -> None:
    tokens_path = tmp_path / "tokens.json"
    write_tokens(tokens_path, "#1F4ACC", "#C026D3")

    results, missing, skipped = run_validators(tokens_path=tokens_path)

    assert [result.gate_id for result in results] == [
        "GATE-002",
        "GATE-003",
        "GATE-004",
        "GATE-005",
        "GATE-006",
    ]
    assert [spec.gate_id for spec in skipped] == ["GATE-001"]
    assert [spec.gate_id for spec in missing] == []


def test_blocking_fail_controls_exit_code(tmp_path: Path) -> None:
    tokens_path = tmp_path / "tokens.json"
    write_tokens(tokens_path, "#777777", "#888888")

    results, _, _ = run_validators(tokens_path=tokens_path)

    assert compute_overall_status(results) == "FAIL"
    assert exit_code_for_results(results, strict_warnings=False) == 1


def test_warning_gate_can_warn_without_failing_process(tmp_path: Path) -> None:
    tokens_path = tmp_path / "tokens.json"
    write_tokens(tokens_path, "#777777", "#888888")

    results, _, _ = run_validators(tokens_path=tokens_path, only_gate_ids={"GATE-003"})

    assert compute_overall_status(results) == "WARN"
    assert exit_code_for_results(results, strict_warnings=False) == 0
    assert exit_code_for_results(results, strict_warnings=True) == 1


def test_runtime_gap_report_contains_expected_sections() -> None:
    report = build_markdown_report()

    assert "## Validator Gates" in report
    assert "GATE-002 CONTRAST" in report
    assert "## Claims Coverage Snapshot" in report
    assert "Unified validator entrypoint" in report


def test_runtime_gap_report_json_has_gates_and_areas() -> None:
    report = build_json_report()

    assert "gates" in report
    assert "areas" in report
    assert "claims_summary" in report
    assert any(gate["gate_id"] == "GATE-003" for gate in report["gates"])
    assert any(
        gate["gate_id"] == "GATE-001" and gate["required_input"] == "seizure_manifest"
        for gate in report["gates"]
    )
    assert any(area["name"] == "Typography" for area in report["areas"])
    assert any(
        area["name"] == "Evidence and claims"
        and area["status"] == "partial"
        and "tools/check_claims_registry.py" in area["runtime_artifacts"]
        for area in report["areas"]
    )
    assert any(
        area["name"] == "Typography"
        and area["status"] == "partial"
        and "tools/validators/typography.py" in area["runtime_artifacts"]
        for area in report["areas"]
    )
    assert any(
        area["name"] == "Axis conflict resolution"
        and area["status"] == "partial"
        and "tools/profile_resolver.py" in area["runtime_artifacts"]
        for area in report["areas"]
    )
    assert any(
        area["name"] == "Scaling and display adaptation"
        and area["status"] == "partial"
        and "tools/scaling.py" in area["runtime_artifacts"]
        for area in report["areas"]
    )


def test_validate_json_includes_auxiliary_runtime_surfaces(tmp_path: Path) -> None:
    tokens_path = tmp_path / "tokens.json"
    write_tokens(tokens_path, "#1F4ACC", "#C026D3")

    results, missing, _ = run_validators(tokens_path=tokens_path)
    from validate import build_auxiliary_runtime_summary, results_to_json

    payload = results_to_json(results, missing, build_auxiliary_runtime_summary())

    assert "auxiliary_runtime" in payload
    assert any(item["name"] == "TYPE-001 TYPOGRAPHY" for item in payload["auxiliary_runtime"])


def test_rendered_auxiliary_runtime_can_be_added(monkeypatch) -> None:
    from rendered_cognitive_check import RENDERED_GATE_ID as cognitive_gate_id
    from rendered_cognitive_check import RENDERED_GATE_NAME as cognitive_gate_name
    from rendered_spatial_check import RENDERED_GATE_ID as spatial_gate_id
    from rendered_spatial_check import RENDERED_GATE_NAME as spatial_gate_name
    from validate import build_auxiliary_runtime_summary_with_rendered
    from validators.base import GateResult, Severity

    monkeypatch.setattr(
        "rendered_spatial_check.run_rendered_spatial_audit",
        lambda: GateResult(
            gate_id=spatial_gate_id,
            gate_name=spatial_gate_name,
            severity=Severity.WARNING,
        ),
    )
    monkeypatch.setattr(
        "rendered_cognitive_check.run_rendered_cognitive_audit",
        lambda: GateResult(
            gate_id=cognitive_gate_id,
            gate_name=cognitive_gate_name,
            severity=Severity.WARNING,
        ),
    )

    payload = build_auxiliary_runtime_summary_with_rendered(include_rendered=True)

    assert any(item["name"] == "RENDER-004 SPATIAL_RENDERED" for item in payload)
    assert any(item["name"] == "RENDER-006 COGNITIVE_RENDERED" for item in payload)
