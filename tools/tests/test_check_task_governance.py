"""Tests for repo task-governance validation."""
from __future__ import annotations

from pathlib import Path

from task_governance import validate_task_governance


TASK_IDS = [f"T{index:03d}" for index in range(1, 101)]


def seed_repo(repo_root: Path) -> None:
    (repo_root / "docs").mkdir(parents=True, exist_ok=True)
    (repo_root / "tools").mkdir(parents=True, exist_ok=True)
    (repo_root / "README.md").write_text("root\n", encoding="utf-8")
    (repo_root / "ROADMAP.md").write_text("roadmap\n", encoding="utf-8")
    (repo_root / "CHANGELOG.md").write_text("tracked issue language only\n", encoding="utf-8")
    (repo_root / "CLAUDE.md").write_text("tracked issue language only\n", encoding="utf-8")
    (repo_root / "tools" / "validate.py").write_text("print('ok')\n", encoding="utf-8")
    (repo_root / "docs" / "repo-audit-2026-03-26.md").write_text("audit\n", encoding="utf-8")
    task_lines = [
        f"- [{'x' if index <= 3 else ' '}] {task_id} Track `{path}`"
        for index, (task_id, path) in enumerate(
            zip(TASK_IDS, ["README.md", "ROADMAP.md", "tools/validate.py"] + ["docs/repo-audit-2026-03-26.md"] * 97),
            start=1,
        )
    ]
    (repo_root / "docs" / "task-ledger.md").write_text(
        "# Task Ledger\n\n" + "\n".join(task_lines) + "\n",
        encoding="utf-8",
    )
    (repo_root / "docs" / "KNOWN_ISSUES.md").write_text(
        "\n".join(
            [
                "# Known Issues",
                "",
                "## KI-001",
                "See `README.md`.",
                "",
                "## KI-002",
                "See `ROADMAP.md`.",
                "",
                "## KI-003",
                "See `tools/validate.py`.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_validate_task_governance_accepts_seeded_repo(tmp_path: Path) -> None:
    seed_repo(tmp_path)

    assert validate_task_governance(tmp_path) == []


def test_validate_task_governance_rejects_missing_task_path(tmp_path: Path) -> None:
    seed_repo(tmp_path)
    ledger = tmp_path / "docs" / "task-ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8").replace(
            "`tools/validate.py`", "`tools/missing.py`", 1
        ),
        encoding="utf-8",
    )

    errors = validate_task_governance(tmp_path)

    assert any("task ledger references missing repo path" in error for error in errors)


def test_validate_task_governance_rejects_short_task_ledger(tmp_path: Path) -> None:
    seed_repo(tmp_path)
    ledger = tmp_path / "docs" / "task-ledger.md"
    lines = ledger.read_text(encoding="utf-8").splitlines()
    trimmed = lines[:-1]
    ledger.write_text("\n".join(trimmed) + "\n", encoding="utf-8")

    errors = validate_task_governance(tmp_path)

    assert any("at least 100 ordered task IDs" in error for error in errors)


def test_validate_task_governance_rejects_loose_todo_wording(tmp_path: Path) -> None:
    seed_repo(tmp_path)
    (tmp_path / "CHANGELOG.md").write_text("Performance TODO still here\n", encoding="utf-8")

    errors = validate_task_governance(tmp_path)

    assert any("loose TODO wording" in error for error in errors)
