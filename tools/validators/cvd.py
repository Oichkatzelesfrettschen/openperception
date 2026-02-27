"""
CVD gate (GATE-003) - Color Vision Deficiency separation check.

WHY: VALIDATORS_FRAMEWORK.md specifies GATE-003 checks whether semantic colors
     remain distinguishable after CVD simulation. This refactors separation_check.py
     into the gate pattern so it integrates with the validation pipeline.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Optional

# Allow running this module directly from the tools/ directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from okcolor import hex_to_srgb, srgb_to_oklab
from validators.base import (
    CheckResult,
    GateResult,
    Severity,
    Status,
    ValidatorGate,
)


# ---------------------------------------------------------------------------
# Oklab distance utility
# ---------------------------------------------------------------------------

def oklab_distance(hex1: str, hex2: str) -> float:
    r1, g1, b1 = hex_to_srgb(hex1)
    L1, a1, b1_ = srgb_to_oklab(r1, g1, b1)
    r2, g2, b2 = hex_to_srgb(hex2)
    L2, a2, b2_ = srgb_to_oklab(r2, g2, b2)
    return math.sqrt((L1 - L2) ** 2 + (a1 - a2) ** 2 + (b1_ - b2_) ** 2)


# ---------------------------------------------------------------------------
# CVD gate
# ---------------------------------------------------------------------------

# Minimum Oklab distance threshold for adequate CVD separation.
# Below this threshold, two semantic colors are likely confused under CVD.
CVD_DISTANCE_THRESHOLD = 0.15
CVD_DISTANCE_WARN = 0.20


class CVDGate(ValidatorGate):
    """GATE-003: CVD - color vision deficiency separation check.

    Validates that primary and accent colors have sufficient Oklab distance
    to remain distinguishable under color vision deficiency conditions.

    Usage
    -----
    gate = CVDGate(tokens_json_path)
    result = gate.validate()
    print(result)
    """

    gate_id = "GATE-003"
    gate_name = "CVD"
    severity = Severity.WARNING

    def __init__(self, tokens_json_path: Optional[Path] = None):
        if tokens_json_path is None:
            tokens_json_path = (
                Path(__file__).resolve().parents[2] / "tokens" / "color-tokens.json"
            )
        self.tokens_path = tokens_json_path

    def validate(self, **kwargs) -> GateResult:
        result = self._make_result()
        tokens = json.loads(self.tokens_path.read_text())

        for variant_name, data in tokens.items():
            brand = data.get("brand", {})
            primary = brand.get("primaryStrong") or brand.get("primary")
            accent = brand.get("accentStrong") or brand.get("accent")

            if not primary or not accent:
                result.checks.append(
                    CheckResult(
                        name=f"{variant_name}/primary-vs-accent",
                        status=Status.WARN,
                        message="Missing primaryStrong or accentStrong token",
                    )
                )
                continue

            try:
                dist = oklab_distance(primary, accent)
            except (ValueError, Exception) as exc:
                result.checks.append(
                    CheckResult(
                        name=f"{variant_name}/primary-vs-accent",
                        status=Status.FAIL,
                        message=f"Error computing distance: {exc}",
                    )
                )
                continue

            if dist >= CVD_DISTANCE_WARN:
                status = Status.PASS
                msg = f"Oklab distance {dist:.3f} >= {CVD_DISTANCE_WARN:.2f} (adequate)"
            elif dist >= CVD_DISTANCE_THRESHOLD:
                status = Status.WARN
                msg = f"Oklab distance {dist:.3f} in borderline range [{CVD_DISTANCE_THRESHOLD:.2f}, {CVD_DISTANCE_WARN:.2f})"
            else:
                status = Status.FAIL
                msg = f"Oklab distance {dist:.3f} < {CVD_DISTANCE_THRESHOLD:.2f} (insufficient separation)"

            result.checks.append(
                CheckResult(
                    name=f"{variant_name}/primary-vs-accent",
                    status=status,
                    message=msg,
                    value=dist,
                    threshold=CVD_DISTANCE_THRESHOLD,
                )
            )

        return result


if __name__ == "__main__":
    gate = CVDGate()
    result = gate.validate()
    print(result)
    raise SystemExit(0 if result.status != Status.FAIL else 1)
