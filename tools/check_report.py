"""
Shared output helpers for repo integrity and governance check wrappers.
"""
from __future__ import annotations

import json
from typing import Any


def emit_check_report(
    *,
    check_id: str,
    display_name: str,
    scope: str,
    errors: list[str],
    json_output: bool,
    task_refs: list[str] | None = None,
    issue_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> int:
    ok = not errors
    payload: dict[str, Any] = {
        "check_id": check_id,
        "display_name": display_name,
        "scope": scope,
        "ok": ok,
        "errors": errors,
        "task_refs": task_refs or [],
        "issue_refs": issue_refs or [],
    }
    if metadata:
        payload["metadata"] = metadata

    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if ok else 1

    if ok:
        print(f"{display_name} passed: {scope}")
        return 0

    print(f"{display_name} failed:")
    for error in errors:
        print(f"- {error}")
    return 1
