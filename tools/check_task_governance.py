#!/usr/bin/env python3
"""
Validate repo task-tracking and known-issues governance surfaces.
"""
from __future__ import annotations

from task_governance import validate_task_governance


def main() -> int:
    errors = validate_task_governance()
    if errors:
        print("Task governance check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Task governance check passed: docs/task-ledger.md and docs/KNOWN_ISSUES.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
