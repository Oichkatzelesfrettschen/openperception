"""
Base classes for the OpenPerception validator gate framework.

WHY: VALIDATORS_FRAMEWORK.md defines 6 gate types (SEIZURE, CONTRAST, CVD,
     SPATIAL, DEPTH, COGNITIVE). This module provides the shared ABC so all
     gates implement a consistent interface and results can be aggregated.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    BLOCKING = "BLOCKING"  # CI must fail on this
    WARNING = "WARNING"    # Advisory; log but do not block


class Status(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class CheckResult:
    """Result of a single named check within a gate."""
    name: str
    status: Status
    message: str
    value: float | None = None
    threshold: float | None = None


@dataclass
class GateResult:
    """Aggregated result of all checks within one validator gate."""
    gate_id: str
    gate_name: str
    severity: Severity
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def status(self) -> Status:
        """Overall gate status: FAIL if any check failed; WARN if any warned."""
        statuses = {c.status for c in self.checks}
        if Status.FAIL in statuses:
            return Status.FAIL
        if Status.WARN in statuses:
            return Status.WARN
        return Status.PASS

    @property
    def passed(self) -> bool:
        return self.status == Status.PASS

    def __str__(self) -> str:
        lines = [f"[{self.gate_id}] {self.gate_name}: {self.status.value}"]
        for check in self.checks:
            icon = "OK" if check.status == Status.PASS else check.status.value
            lines.append(f"  [{icon}] {check.name}: {check.message}")
        return "\n".join(lines)


class ValidatorGate(ABC):
    """Abstract base class for all validator gates.

    Subclasses must implement validate() and expose gate_id, gate_name,
    and severity as class attributes.
    """

    gate_id: str
    gate_name: str
    severity: Severity

    @abstractmethod
    def validate(self, **kwargs) -> GateResult:
        """Run all checks for this gate and return a GateResult."""
        ...

    def _make_result(self) -> GateResult:
        return GateResult(
            gate_id=self.gate_id,
            gate_name=self.gate_name,
            severity=self.severity,
        )
