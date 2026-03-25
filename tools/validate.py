#!/usr/bin/env python3
"""
Unified validator entrypoint for implemented OpenPerception gates.

WHY: specs/VALIDATORS_FRAMEWORK.md declares a unified CLI, but the repository
previously only exposed standalone scripts and direct module execution. This
script executes the implemented subset and makes spec-only gaps explicit.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from profile_resolver import compose_profiles
from scaling import build_report as build_scaling_report
from validator_registry import (
    DEFAULT_TOKENS_JSON,
    implemented_gate_specs,
    spec_only_gate_specs,
)
from validators.base import Severity, Status
from validators.typography import TypographyGate


def run_validators(
    tokens_path: Path | None = None,
    only_gate_ids: set[str] | None = None,
    seizure_manifest_path: Path | None = None,
) -> tuple[list[Any], list[Any], list[Any]]:
    executed = []
    skipped = []
    for spec in implemented_gate_specs():
        if only_gate_ids and spec.gate_id not in only_gate_ids:
            continue
        if spec.required_input == "seizure_manifest":
            if seizure_manifest_path is None:
                skipped.append(spec)
                continue
            gate = spec.factory(seizure_manifest_path) if spec.factory else None
        else:
            gate = spec.factory(tokens_path) if spec.factory else None
        if gate is None:
            continue
        executed.append(gate.validate())

    missing = []
    for spec in spec_only_gate_specs():
        if only_gate_ids and spec.gate_id not in only_gate_ids:
            continue
        missing.append(spec)

    return executed, missing, skipped


def compute_overall_status(results: list[Any]) -> str:
    blocking_fail = False
    any_warn = False
    any_fail = False
    for result in results:
        if result.status == Status.WARN:
            any_warn = True
        if result.status == Status.FAIL:
            any_fail = True
            if result.severity == Severity.BLOCKING:
                blocking_fail = True
            else:
                any_warn = True
    if blocking_fail:
        return "FAIL"
    if any_warn or any_fail:
        return "WARN"
    return "PASS"


def exit_code_for_results(results: list[Any], strict_warnings: bool) -> int:
    overall = compute_overall_status(results)
    if overall == "FAIL":
        return 1
    if strict_warnings and overall == "WARN":
        return 1
    return 0


def build_auxiliary_runtime_summary() -> list[dict[str, Any]]:
    return build_auxiliary_runtime_summary_with_rendered(include_rendered=False)


def build_auxiliary_runtime_summary_with_rendered(
    *, include_rendered: bool
) -> list[dict[str, Any]]:
    typography_result = TypographyGate().validate()
    profile_payload = compose_profiles(["standard"])
    scaling_payload = build_scaling_report(44, 76, 1.0, "touch-target")
    scaling_ok = scaling_payload["quantized_px"] >= 44.0

    summary = [
        {
            "name": "TYPE-001 TYPOGRAPHY",
            "status": typography_result.status.value,
            "details": {
                "checks": len(typography_result.checks),
            },
        },
        {
            "name": "PROFILE-001 AXIS_PROFILE_RESOLUTION",
            "status": "PASS" if not profile_payload["conflicts"] else "WARN",
            "details": {
                "selected_profiles": profile_payload["selected_profiles"],
                "conflict_count": len(profile_payload["conflicts"]),
            },
        },
        {
            "name": "SCALE-001 QUANTIZATION",
            "status": "PASS" if scaling_ok else "FAIL",
            "details": {
                "touch_target_quantized_px": scaling_payload["quantized_px"],
                "effective_scale": scaling_payload["effective_scale"],
            },
        },
    ]
    if include_rendered:
        from rendered_cognitive_check import run_rendered_cognitive_audit
        from rendered_spatial_check import run_rendered_spatial_audit

        rendered_spatial = run_rendered_spatial_audit()
        rendered_cognitive = run_rendered_cognitive_audit()
        summary.extend(
            [
                {
                    "name": "RENDER-004 SPATIAL_RENDERED",
                    "status": rendered_spatial.status.value,
                    "details": {
                        "checks": len(rendered_spatial.checks),
                    },
                },
                {
                    "name": "RENDER-006 COGNITIVE_RENDERED",
                    "status": rendered_cognitive.status.value,
                    "details": {
                        "checks": len(rendered_cognitive.checks),
                    },
                },
            ]
        )
    return summary


def results_to_json(
    results: list[Any], missing: list[Any], auxiliary_runtime: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "overall_status": compute_overall_status(results),
        "executed_gates": [
            {
                "gate_id": result.gate_id,
                "gate_name": result.gate_name,
                "severity": result.severity.value,
                "status": result.status.value,
                "checks": [
                    {
                        "name": check.name,
                        "status": check.status.value,
                        "message": check.message,
                        "value": check.value,
                        "threshold": check.threshold,
                    }
                    for check in result.checks
                ],
            }
            for result in results
        ],
        "spec_only_gates": [
            {
                "gate_id": spec.gate_id,
                "gate_name": spec.gate_name,
                "severity": spec.severity,
                "status": spec.status,
                "description": spec.description,
            }
            for spec in missing
        ],
        "auxiliary_runtime": auxiliary_runtime,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run implemented validator gates and report spec-only gaps.",
    )
    parser.add_argument(
        "--tokens",
        default=str(DEFAULT_TOKENS_JSON),
        help="Path to token JSON file (default: tokens/color-tokens.json)",
    )
    parser.add_argument(
        "--only",
        help="Comma-separated list of gate IDs to run or report, e.g. GATE-002,GATE-003",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of text output.",
    )
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Return non-zero if any warning gate warns or fails.",
    )
    parser.add_argument(
        "--seizure-manifest",
        help="Path to seizure frame manifest JSON for executing GATE-001.",
    )
    parser.add_argument(
        "--rendered-audits",
        action="store_true",
        help="Also run the optional browser-backed rendered spatial and cognitive audits.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    tokens_path = Path(args.tokens)
    only_gate_ids = {part.strip() for part in args.only.split(",")} if args.only else None
    seizure_manifest_path = Path(args.seizure_manifest) if args.seizure_manifest else None
    results, missing, skipped = run_validators(
        tokens_path=tokens_path,
        only_gate_ids=only_gate_ids,
        seizure_manifest_path=seizure_manifest_path,
    )
    auxiliary_runtime = build_auxiliary_runtime_summary_with_rendered(
        include_rendered=args.rendered_audits
    )

    if args.json:
        payload = results_to_json(results, missing, auxiliary_runtime)
        payload["skipped_gates"] = [
            {
                "gate_id": spec.gate_id,
                "gate_name": spec.gate_name,
                "severity": spec.severity,
                "status": spec.status,
                "description": spec.description,
                "required_input": spec.required_input,
            }
            for spec in skipped
        ]
        print(json.dumps(payload, indent=2))
    else:
        print("OpenPerception Unified Validator")
        print(f"Tokens: {tokens_path}")
        print("")
        for result in results:
            print(result)
        print("")
        print(f"Overall runtime status: {compute_overall_status(results)}")
        print("Auxiliary runtime surfaces:")
        for item in auxiliary_runtime:
            print(f"  - {item['name']}: {item['status']}")
        if skipped:
            print("Available but skipped (input required):")
            for spec in skipped:
                print(
                    f"  - {spec.gate_id} {spec.gate_name} requires --{spec.required_input.replace('_', '-')}"
                )
        if missing:
            print("Spec-only gates not executed:")
            for spec in missing:
                print(
                    f"  - {spec.gate_id} {spec.gate_name} ({spec.severity}): "
                    f"{spec.description}"
                )

    return exit_code_for_results(results, args.strict_warnings)


if __name__ == "__main__":
    raise SystemExit(main())
