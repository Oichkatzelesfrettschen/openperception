"""
Validate live governance files for task tracking and known-issues discipline.
"""
from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TASK_LEDGER_PATH = Path("docs/task-ledger.md")
KNOWN_ISSUES_PATH = Path("docs/KNOWN_ISSUES.md")
BANNED_TODO_DOCS = (Path("CHANGELOG.md"), Path("CLAUDE.md"))
TASK_LINE_RE = re.compile(r"^- \[(?P<status>[ x])\] (?P<task_id>T\d{3}) (?P<text>.+)$", re.M)
ISSUE_HEADING_RE = re.compile(r"^## (?P<issue_id>KI-\d{3})\b", re.M)
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
ROOT_FILES = {
    "README.md",
    "REQUIREMENTS.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "MASTER_INDEX.md",
    "Makefile",
    "pyproject.toml",
    "requirements-dev.txt",
}
PATH_PREFIXES = (
    "algorithms/",
    "artifacts/",
    "datasets/",
    "docs/",
    "examples/",
    "gtk4/",
    "papers/",
    "python-packages/",
    "research/",
    "specs/",
    "templates/",
    "tex/",
    "tokens/",
    "tools/",
)


def _looks_like_repo_path(token: str) -> bool:
    if token in ROOT_FILES:
        return True
    return token.startswith(PATH_PREFIXES)


def _iter_backticked_repo_paths(text: str) -> list[str]:
    return [token for token in BACKTICK_RE.findall(text) if _looks_like_repo_path(token)]


def validate_task_governance(repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []

    task_ledger = repo_root / TASK_LEDGER_PATH
    if not task_ledger.exists():
        return [f"missing task ledger: {TASK_LEDGER_PATH.as_posix()}"]

    known_issues = repo_root / KNOWN_ISSUES_PATH
    if not known_issues.exists():
        errors.append(f"missing known issues file: {KNOWN_ISSUES_PATH.as_posix()}")

    task_text = task_ledger.read_text(encoding="utf-8")
    task_matches = list(TASK_LINE_RE.finditer(task_text))
    task_ids = [match.group("task_id") for match in task_matches]
    expected_ids = [f"T{index:03d}" for index in range(1, len(task_ids) + 1)]
    if len(task_ids) < 100 or task_ids != expected_ids:
        errors.append(
            "task ledger must contain at least 100 ordered task IDs starting at T001 without gaps: "
            f"{TASK_LEDGER_PATH.as_posix()}"
        )

    for token in _iter_backticked_repo_paths(task_text):
        if not (repo_root / token).exists():
            errors.append(
                "task ledger references missing repo path: "
                f"{token} in {TASK_LEDGER_PATH.as_posix()}"
            )

    if known_issues.exists():
        issues_text = known_issues.read_text(encoding="utf-8")
        issue_ids = ISSUE_HEADING_RE.findall(issues_text)
        if len(issue_ids) < 3:
            errors.append(
                "known issues file must contain at least 3 issue headings: "
                f"{KNOWN_ISSUES_PATH.as_posix()}"
            )
        if len(issue_ids) != len(set(issue_ids)):
            errors.append(
                "known issues file contains duplicate issue IDs: "
                f"{KNOWN_ISSUES_PATH.as_posix()}"
            )
        for token in _iter_backticked_repo_paths(issues_text):
            if not (repo_root / token).exists():
                errors.append(
                    "known issues references missing repo path: "
                    f"{token} in {KNOWN_ISSUES_PATH.as_posix()}"
                )

    for rel_path in BANNED_TODO_DOCS:
        doc_path = repo_root / rel_path
        if not doc_path.exists():
            continue
        text = doc_path.read_text(encoding="utf-8")
        if "TODO" in text:
            errors.append(
                f"loose TODO wording must be replaced with tracked issue language: {rel_path}"
            )

    return sorted(errors)
