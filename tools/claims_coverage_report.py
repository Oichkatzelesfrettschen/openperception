#!/usr/bin/env python3
"""
Emit a coverage report for the claims-to-runtime registry.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

from claims_registry import load_claims_registry, summarize_claims_registry


def build_text_report() -> str:
    summary = summarize_claims_registry()
    lines = [
        "OpenPerception Claims Coverage Report",
        "",
        f"Registry: {summary['registry_path']}",
        f"Claims tracked: {summary['claim_count']}",
        "",
        "Status counts:",
    ]
    for status, count in sorted(summary["status_counts"].items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("Claims by gate:")
    for gate_id, claim_ids in sorted(summary["claims_by_gate"].items()):
        lines.append(f"- {gate_id}: {', '.join(claim_ids)}")
    if summary["uncovered_claims"]:
        lines.append("")
        lines.append("Uncovered claims:")
        for claim_id in summary["uncovered_claims"]:
            lines.append(f"- {claim_id}")
    return "\n".join(lines) + "\n"


def build_markdown_report() -> str:
    registry = load_claims_registry()
    summary = summarize_claims_registry()
    lines = [
        "# OpenPerception Claims Coverage Report",
        "",
        f"Registry: `{summary['registry_path']}`",
        "",
        "## Status Counts",
        "",
        "| Status | Count |",
        "|--------|-------|",
    ]
    for status, count in sorted(summary["status_counts"].items()):
        lines.append(f"| {status} | {count} |")

    lines.extend(
        [
            "",
            "## Claims",
            "",
            "| Claim | Status | Gates | Runtime Artifacts | Tests |",
            "|-------|--------|-------|-------------------|-------|",
        ]
    )
    for claim in registry["claims"]:
        gates = ", ".join(claim["validator_gates"]) or "--"
        runtime_artifacts = ", ".join(claim["runtime_artifacts"]) or "--"
        tests = ", ".join(claim["tests"]) or "--"
        lines.append(
            f"| {claim['claim_id']} | {claim['status']} | {gates} | {runtime_artifacts} | {tests} |"
        )
    return "\n".join(lines) + "\n"


def build_json_report() -> dict[str, Any]:
    return {
        "summary": summarize_claims_registry(),
        "registry": load_claims_registry(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report coverage of evidence-matrix claims in runtime artifacts.",
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
