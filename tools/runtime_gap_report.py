#!/usr/bin/env python3
"""
Emit a concise spec-vs-runtime gap report for OpenPerception.

WHY: The repository has broad declared architecture far ahead of its current
runtime. This tool makes the lacunae explicit and actionable.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

from claims_registry import summarize_claims_registry
from validator_registry import get_gate_specs, get_runtime_areas


def build_markdown_report() -> str:
    claims_summary = summarize_claims_registry()
    lines = [
        "# OpenPerception Runtime Gap Report",
        "",
        "## Validator Gates",
        "",
        "| Gate | Status | Severity | Notes |",
        "|------|--------|----------|-------|",
    ]
    for spec in get_gate_specs():
        lines.append(
            f"| {spec.gate_id} {spec.gate_name} | {spec.status} | {spec.severity} | "
            f"{spec.description} |"
        )

    lines.extend(
        [
            "",
            "## System Areas",
            "",
            "| Area | Status | Lacuna | Next Step |",
            "|------|--------|--------|-----------|",
        ]
    )
    for area in get_runtime_areas():
        lines.append(
            f"| {area.name} | {area.status} | {area.lacuna} | {area.next_step} |"
        )

    lines.extend(
        [
            "",
            "## Claims Coverage Snapshot",
            "",
            f"- Claims tracked: {claims_summary['claim_count']}",
            f"- Implemented claims: {claims_summary['status_counts'].get('implemented', 0)}",
            f"- Partial claims: {claims_summary['status_counts'].get('partial', 0)}",
            f"- Claim-linked gates: {', '.join(sorted(claims_summary['claims_by_gate'])) or '--'}",
        ]
    )

    return "\n".join(lines) + "\n"


def build_text_report() -> str:
    claims_summary = summarize_claims_registry()
    lines = ["OpenPerception Runtime Gap Report", ""]
    lines.append("Validator gates:")
    for spec in get_gate_specs():
        lines.append(
            f"- {spec.gate_id} {spec.gate_name}: {spec.status} "
            f"({spec.severity}) - {spec.description}"
        )
    lines.append("")
    lines.append("System areas:")
    for area in get_runtime_areas():
        lines.append(f"- {area.name}: {area.status}")
        lines.append(f"  Lacuna: {area.lacuna}")
        lines.append(f"  Next: {area.next_step}")
    lines.append("")
    lines.append("Claims coverage snapshot:")
    lines.append(f"- Claims tracked: {claims_summary['claim_count']}")
    for status, count in sorted(claims_summary["status_counts"].items()):
        lines.append(f"- {status}: {count}")
    return "\n".join(lines) + "\n"


def build_json_report() -> dict[str, Any]:
    return {
        "gates": [
            {
                "gate_id": spec.gate_id,
                "gate_name": spec.gate_name,
                "status": spec.status,
                "severity": spec.severity,
                "description": spec.description,
                "module_path": spec.module_path,
                "required_input": spec.required_input,
            }
            for spec in get_gate_specs()
        ],
        "areas": [
            {
                "name": area.name,
                "status": area.status,
                "declared_sources": list(area.declared_sources),
                "runtime_artifacts": list(area.runtime_artifacts),
                "lacuna": area.lacuna,
                "next_step": area.next_step,
            }
            for area in get_runtime_areas()
        ],
        "claims_summary": summarize_claims_registry(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report declared-vs-runtime gaps across validator and system areas.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "markdown", "json"),
        default="text",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.format == "json":
        print(json.dumps(build_json_report(), indent=2))
    elif args.format == "markdown":
        print(build_markdown_report(), end="")
    else:
        print(build_text_report(), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
