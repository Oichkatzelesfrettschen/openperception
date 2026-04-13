"""
CONTRAST gate (GATE-002) - WCAG contrast validation.

WHY: VALIDATORS_FRAMEWORK.md specifies the CONTRAST_GATE checks WCAG AA/AAA
     thresholds. This refactors contrast_check.py into the gate pattern so it
     can be composed into the full validation pipeline.
"""

from __future__ import annotations

import json
from pathlib import Path

from validators.base import (
    CheckResult,
    GateResult,
    Severity,
    Status,
    ValidatorGate,
)


# ---------------------------------------------------------------------------
# Pure WCAG utilities (extracted from tools/contrast_check.py)
# ---------------------------------------------------------------------------


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    s = hex_str.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    R = _srgb_to_linear(r / 255.0)
    G = _srgb_to_linear(g / 255.0)
    B = _srgb_to_linear(b / 255.0)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    L1 = relative_luminance(hex_to_rgb(fg_hex))
    L2 = relative_luminance(hex_to_rgb(bg_hex))
    light, dark = max(L1, L2), min(L1, L2)
    return (light + 0.05) / (dark + 0.05)


# ---------------------------------------------------------------------------
# CONTRAST gate
# ---------------------------------------------------------------------------

WCAG_AA_NORMAL = 4.5
WCAG_AA_LARGE = 3.0
WCAG_AAA_NORMAL = 7.0


class ContrastGate(ValidatorGate):
    """GATE-002: CONTRAST - blocking WCAG contrast check.

    Validates foreground/background color pairs from a color token JSON file
    against WCAG 2.1 AA thresholds (4.5:1 for normal text, 3:1 for large text).

    Usage
    -----
    gate = ContrastGate(tokens_json_path)
    result = gate.validate()
    print(result)
    """

    gate_id = "GATE-002"
    gate_name = "CONTRAST"
    severity = Severity.BLOCKING

    def __init__(self, tokens_json_path: Path | None = None):
        if tokens_json_path is None:
            # Default: look relative to repository root
            tokens_json_path = (
                Path(__file__).resolve().parents[2] / "tokens" / "color-tokens.json"
            )
        self.tokens_path = tokens_json_path

    def _check_variant(self, variant_name: str, data: dict) -> list[CheckResult]:
        brand = data.get("brand", {})
        gray = data.get("gray", {})

        pairs: list[tuple[str | None, str | None, str, float]] = [
            (
                brand.get("text"),
                brand.get("surface"),
                "text on surface",
                WCAG_AA_NORMAL,
            ),
            (
                brand.get("primaryStrong"),
                brand.get("surface"),
                "primaryStrong on surface",
                WCAG_AA_NORMAL,
            ),
            (
                brand.get("accentStrong"),
                brand.get("surface"),
                "accentStrong on surface",
                WCAG_AA_NORMAL,
            ),
            (
                "#FFFFFF",
                brand.get("primaryStrong"),
                "white on primaryStrong",
                WCAG_AA_NORMAL,
            ),
            (
                "#FFFFFF",
                brand.get("accentStrong"),
                "white on accentStrong",
                WCAG_AA_NORMAL,
            ),
            (
                gray.get("700"),
                brand.get("surface"),
                "gray700 on surface",
                WCAG_AA_NORMAL,
            ),
            (
                gray.get("500"),
                brand.get("surface"),
                "gray500 on surface",
                WCAG_AA_LARGE,
            ),
        ]

        results = []
        for fg, bg, label, required_ratio in pairs:
            if not fg or not bg:
                continue
            ratio = contrast_ratio(fg, bg)
            full_label = f"{variant_name}/{label}"
            if ratio >= required_ratio:
                results.append(
                    CheckResult(
                        name=full_label,
                        status=Status.PASS,
                        message=f"{ratio:.2f}:1 (required {required_ratio:.1f}:1)",
                        value=ratio,
                        threshold=required_ratio,
                    )
                )
            else:
                results.append(
                    CheckResult(
                        name=full_label,
                        status=Status.FAIL,
                        message=f"{ratio:.2f}:1 FAILS (required {required_ratio:.1f}:1)",
                        value=ratio,
                        threshold=required_ratio,
                    )
                )
        return results

    def validate(self, **kwargs) -> GateResult:
        result = self._make_result()
        tokens: dict[str, dict] = json.loads(self.tokens_path.read_text())
        for variant_name, variant_data in tokens.items():
            result.checks.extend(self._check_variant(variant_name, variant_data))
        return result


if __name__ == "__main__":
    gate = ContrastGate()
    result = gate.validate()
    print(result)
    raise SystemExit(0 if result.passed else 1)
