"""
GATE-007: ACHROMAT - luminance contrast validation for the mono token variant.

WHY: Achromatopsia (rod monochromacy) leaves no colour discrimination; the
     only remaining perceptual channel is luminance contrast.  GATE-002
     (CONTRAST) validates the default/CVD variants against a white surface,
     but it does NOT inspect the mono variant specifically, and it does not
     verify that individual semantic roles carry sufficient contrast to remain
     usable in a fully-achromatic rendering.  GATE-007 fills that gap.

     Consistent with Simulator_Achromat and dl_simulate_cvd_achromat, which
     both use BT.709 photopic luminance.  Consistent with GATE-002's
     relative_luminance(), which also follows BT.709 / WCAG 2.1.

WHAT:
     - Reads the 'mono' variant from color-tokens.json
     - Checks each semantically-active foreground against brand.surface (white)
     - PASS:  ratio >= 4.5:1  (WCAG 2.1 AA normal text)
     - WARN:  ratio >= 3.0:1  (WCAG 2.1 AA large text / non-text UI)
     - FAIL:  ratio <  3.0:1
     - Raises a WARN if two adjacent viz.categorical entries collapse to the
       same gray (color-only distinction is gone, but marker/dash redundancy
       exists in the mono variant)

HOW:
     python tools/validators/achromat.py
     make validate   # integrates via validator_registry.py
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
from validators.contrast import contrast_ratio


# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------

CONTRAST_PASS = 4.5   # WCAG 2.1 AA normal text
CONTRAST_WARN = 3.0   # WCAG 2.1 AA large text / non-text UI components


# ---------------------------------------------------------------------------
# AchromatGate
# ---------------------------------------------------------------------------

class AchromatGate(ValidatorGate):
    """GATE-007: ACHROMAT - luminance contrast in the mono token variant.

    Validates that every semantically-active foreground in the achromatic
    (mono) token variant carries adequate luminance contrast against the
    white surface defined by brand.surface.

    Threshold: 4.5:1 PASS, 3.0:1 WARN, below FAIL.
    Severity: WARNING (advisory; does not block CI).
    """

    gate_id = "GATE-007"
    gate_name = "ACHROMAT"
    severity = Severity.WARNING

    def __init__(self, tokens_json_path: Path | None = None):
        if tokens_json_path is None:
            tokens_json_path = (
                Path(__file__).resolve().parents[2] / "tokens" / "color-tokens.json"
            )
        self.tokens_path = tokens_json_path

    def _check_fg_on_surface(
        self,
        result: GateResult,
        *,
        label: str,
        fg: str | None,
        surface: str,
    ) -> None:
        if not fg:
            result.checks.append(
                CheckResult(
                    name=label,
                    status=Status.WARN,
                    message="Missing token; skipping contrast check",
                )
            )
            return

        ratio = contrast_ratio(fg, surface)
        if ratio >= CONTRAST_PASS:
            result.checks.append(
                CheckResult(
                    name=label,
                    status=Status.PASS,
                    message=f"{ratio:.2f}:1 (required {CONTRAST_PASS:.1f}:1 WCAG AA)",
                    value=ratio,
                    threshold=CONTRAST_PASS,
                )
            )
        elif ratio >= CONTRAST_WARN:
            result.checks.append(
                CheckResult(
                    name=label,
                    status=Status.WARN,
                    message=(
                        f"{ratio:.2f}:1 meets large-text threshold "
                        f"({CONTRAST_WARN:.1f}:1) but not normal-text "
                        f"threshold ({CONTRAST_PASS:.1f}:1)"
                    ),
                    value=ratio,
                    threshold=CONTRAST_PASS,
                )
            )
        else:
            result.checks.append(
                CheckResult(
                    name=label,
                    status=Status.FAIL,
                    message=(
                        f"{ratio:.2f}:1 FAILS both thresholds "
                        f"(WCAG AA normal: {CONTRAST_PASS:.1f}:1, "
                        f"large: {CONTRAST_WARN:.1f}:1)"
                    ),
                    value=ratio,
                    threshold=CONTRAST_PASS,
                )
            )

    def validate(self, **kwargs) -> GateResult:
        result = self._make_result()

        tokens: dict[str, dict] = json.loads(self.tokens_path.read_text())
        mono = tokens.get("mono")
        if mono is None:
            result.checks.append(
                CheckResult(
                    name="mono/variant-present",
                    status=Status.FAIL,
                    message="'mono' variant not found in color-tokens.json",
                )
            )
            return result

        brand = mono.get("brand", {})
        surface = brand.get("surface", "#FFFFFF")

        # --- semantic foreground checks ---
        fg_roles: list[tuple[str, str | None]] = [
            ("mono/brand.text on surface",         brand.get("text")),
            ("mono/brand.primary on surface",      brand.get("primary")),
            ("mono/brand.primaryStrong on surface", brand.get("primaryStrong")),
            ("mono/brand.accent on surface",       brand.get("accent")),
            ("mono/brand.accentStrong on surface",  brand.get("accentStrong")),
            ("mono/brand.link on surface",         brand.get("link")),
        ]

        for label, fg in fg_roles:
            self._check_fg_on_surface(result, label=label, fg=fg, surface=surface)

        # --- viz.categorical collapse warning ---
        categorical = mono.get("viz", {}).get("categorical", [])
        if len(categorical) >= 2:
            c0, c1 = categorical[0], categorical[1]
            if c0 == c1:
                result.checks.append(
                    CheckResult(
                        name="mono/viz.categorical[0-1] collapse",
                        status=Status.WARN,
                        message=(
                            f"viz.categorical[0] and [1] both map to {c0} in mono mode "
                            "(expected: marker/dash redundancy compensates for colour loss)"
                            " -- see docs/KNOWN_ISSUES.md KI-008"
                        ),
                    )
                )
            else:
                ratio = contrast_ratio(c0, c1)
                # For non-text visual elements use 3:1 threshold
                status = Status.PASS if ratio >= CONTRAST_WARN else Status.WARN
                ki_ref = " -- see docs/KNOWN_ISSUES.md KI-008" if status == Status.WARN else ""
                result.checks.append(
                    CheckResult(
                        name="mono/viz.categorical[0-1] contrast",
                        status=status,
                        message=(
                            f"{ratio:.2f}:1 between categorical[0] ({c0}) and [1] ({c1}){ki_ref}"
                        ),
                        value=ratio,
                        threshold=CONTRAST_WARN,
                    )
                )

        return result


if __name__ == "__main__":
    gate = AchromatGate()
    result = gate.validate()
    print(result)
    raise SystemExit(0 if result.status != Status.FAIL else 1)
