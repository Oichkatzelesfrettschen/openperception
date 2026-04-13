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


# Allow running this module directly from the tools/ directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from okcolor import hex_to_srgb, srgb_to_oklab
from semantic_tokens import (
    DEFAULT_SEMANTIC_TOKENS,
    get_variant_roles,
    load_semantic_tokens,
)

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
FOCUS_DISABLED_THRESHOLD = 0.10
FOCUS_DISABLED_WARN = 0.14


def derive_semantic_roles(
    variant_name: str,
    variant_tokens: dict[str, object],
    default_tokens: dict[str, object],
) -> dict[str, str | None]:
    del variant_name
    brand = variant_tokens.get("brand", {})
    default_brand = default_tokens.get("brand", {})
    gray = variant_tokens.get("gray", default_tokens.get("gray", {}))

    return {
        "danger": brand.get("accentStrong") or brand.get("accent"),
        "ally": brand.get("primaryStrong") or brand.get("primary"),
        "focus": brand.get("focusRing") or default_brand.get("focusRing"),
        "disabled": (
            brand.get("border")
            or gray.get("400")
            or gray.get("500")
            or default_brand.get("border")
        ),
        "interactable": brand.get("link")
        or brand.get("primaryStrong")
        or brand.get("primary"),
        "warning": brand.get("accent") or brand.get("accentStrong"),
        "info": brand.get("primary") or brand.get("primaryStrong") or brand.get("link"),
        "progress": brand.get("primaryStrong") or brand.get("primary"),
    }


def _role_color(role: object) -> str | None:
    if isinstance(role, dict):
        return role.get("color")
    if isinstance(role, str):
        return role
    return None


def semantic_redundancy_available_pair(
    role_a_name: str,
    role_b_name: str,
    variant_tokens: dict[str, object],
    semantic_roles: dict[str, object] | None = None,
) -> tuple[bool, str]:
    if semantic_roles is not None:
        role_a = semantic_roles.get(role_a_name, {})
        role_b = semantic_roles.get(role_b_name, {})
        redundancy_a = role_a.get("redundancy", {}) if isinstance(role_a, dict) else {}
        redundancy_b = role_b.get("redundancy", {}) if isinstance(role_b, dict) else {}

        if (
            redundancy_a.get("marker")
            and redundancy_b.get("marker")
            and redundancy_a.get("dash") is not None
            and redundancy_b.get("dash") is not None
        ):
            if redundancy_a.get("marker") == redundancy_b.get(
                "marker"
            ) and redundancy_a.get("dash") == redundancy_b.get("dash"):
                return (
                    False,
                    f"{role_a_name.title()} and {role_b_name} collapse to the same marker and dash",
                )
            return (
                True,
                f"Distinct semantic marker/dash backups exist for {role_a_name} and {role_b_name}",
            )

        icon_a = redundancy_a.get("icon")
        icon_b = redundancy_b.get("icon")
        pattern_a = redundancy_a.get("pattern")
        pattern_b = redundancy_b.get("pattern")
        label_a = redundancy_a.get("label")
        label_b = redundancy_b.get("label")
        if (
            (icon_a and icon_b and icon_a != icon_b)
            or (pattern_a and pattern_b and pattern_a != pattern_b)
            or (label_a and label_b and label_a != label_b)
        ):
            return (
                True,
                f"Distinct semantic icon/pattern backups exist for {role_a_name} and {role_b_name}",
            )
        return (
            False,
            f"{role_a_name.title()} and {role_b_name} lack distinct non-color redundancy",
        )

    viz = variant_tokens.get("viz", {})
    markers = viz.get("markers", [])
    dashes = viz.get("dashes", [])
    if len(markers) < 2 or len(dashes) < 2:
        return (
            False,
            f"Missing viz markers/dashes for {role_a_name}/{role_b_name} redundancy",
        )
    if markers[0] == markers[1] and dashes[0] == dashes[1]:
        return False, f"Fallback viz series collapse for {role_a_name}/{role_b_name}"
    return (
        True,
        f"Distinct fallback marker/dash backups exist for {role_a_name} and {role_b_name}",
    )


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

    def __init__(
        self,
        tokens_json_path: Path | None = None,
        semantic_tokens_path: Path | None = None,
    ):
        if tokens_json_path is None:
            tokens_json_path = (
                Path(__file__).resolve().parents[2] / "tokens" / "color-tokens.json"
            )
        self.tokens_path = tokens_json_path
        self.semantic_tokens_path = semantic_tokens_path or DEFAULT_SEMANTIC_TOKENS

    def _append_distance_check(
        self,
        result: GateResult,
        *,
        name: str,
        color_a: str | None,
        color_b: str | None,
        fail_threshold: float,
        warn_threshold: float,
    ) -> None:
        if not color_a or not color_b:
            result.checks.append(
                CheckResult(
                    name=name,
                    status=Status.WARN,
                    message="Missing semantic color token(s)",
                )
            )
            return

        try:
            dist = oklab_distance(color_a, color_b)
        except (ValueError, Exception) as exc:
            result.checks.append(
                CheckResult(
                    name=name,
                    status=Status.FAIL,
                    message=f"Error computing distance: {exc}",
                )
            )
            return

        if dist >= warn_threshold:
            status = Status.PASS
            msg = f"Oklab distance {dist:.3f} >= {warn_threshold:.2f} (adequate)"
        elif dist >= fail_threshold:
            status = Status.WARN
            msg = (
                f"Oklab distance {dist:.3f} in borderline range "
                f"[{fail_threshold:.2f}, {warn_threshold:.2f})"
                " -- see docs/KNOWN_ISSUES.md KI-007"
            )
        else:
            status = Status.FAIL
            msg = (
                f"Oklab distance {dist:.3f} < {fail_threshold:.2f} "
                "(insufficient separation)"
                " -- see docs/KNOWN_ISSUES.md KI-007"
            )

        result.checks.append(
            CheckResult(
                name=name,
                status=status,
                message=msg,
                value=dist,
                threshold=fail_threshold,
            )
        )

    def validate(self, **kwargs) -> GateResult:
        result = self._make_result()
        tokens = json.loads(self.tokens_path.read_text())
        default_tokens = tokens["default"]
        semantic_payload = None
        if self.semantic_tokens_path.exists():
            semantic_payload = load_semantic_tokens(self.semantic_tokens_path)

        for variant_name, data in tokens.items():
            brand = data.get("brand", {})
            primary = brand.get("primaryStrong") or brand.get("primary")
            accent = brand.get("accentStrong") or brand.get("accent")
            self._append_distance_check(
                result,
                name=f"{variant_name}/primary-vs-accent",
                color_a=primary,
                color_b=accent,
                fail_threshold=CVD_DISTANCE_THRESHOLD,
                warn_threshold=CVD_DISTANCE_WARN,
            )

            semantic_roles = (
                get_variant_roles(semantic_payload, variant_name)
                if semantic_payload is not None
                and variant_name in semantic_payload.get("variants", {})
                else derive_semantic_roles(variant_name, data, default_tokens)
            )
            self._append_distance_check(
                result,
                name=f"{variant_name}/danger-vs-ally",
                color_a=_role_color(semantic_roles["danger"]),
                color_b=_role_color(semantic_roles["ally"]),
                fail_threshold=CVD_DISTANCE_THRESHOLD,
                warn_threshold=CVD_DISTANCE_WARN,
            )
            self._append_distance_check(
                result,
                name=f"{variant_name}/focus-vs-disabled",
                color_a=_role_color(semantic_roles["focus"]),
                color_b=_role_color(semantic_roles["disabled"]),
                fail_threshold=FOCUS_DISABLED_THRESHOLD,
                warn_threshold=FOCUS_DISABLED_WARN,
            )
            self._append_distance_check(
                result,
                name=f"{variant_name}/interactable-vs-disabled",
                color_a=_role_color(semantic_roles["interactable"]),
                color_b=_role_color(semantic_roles["disabled"]),
                fail_threshold=CVD_DISTANCE_THRESHOLD,
                warn_threshold=CVD_DISTANCE_WARN,
            )
            self._append_distance_check(
                result,
                name=f"{variant_name}/warning-vs-info",
                color_a=_role_color(semantic_roles.get("warning")),
                color_b=_role_color(semantic_roles.get("info")),
                fail_threshold=CVD_DISTANCE_THRESHOLD,
                warn_threshold=CVD_DISTANCE_WARN,
            )
            self._append_distance_check(
                result,
                name=f"{variant_name}/progress-vs-disabled",
                color_a=_role_color(semantic_roles.get("progress")),
                color_b=_role_color(semantic_roles["disabled"]),
                fail_threshold=CVD_DISTANCE_THRESHOLD,
                warn_threshold=CVD_DISTANCE_WARN,
            )

            redundancy_ok, redundancy_message = semantic_redundancy_available_pair(
                "danger",
                "ally",
                data,
                semantic_roles if semantic_payload is not None else None,
            )
            result.checks.append(
                CheckResult(
                    name=f"{variant_name}/danger-ally_redundancy",
                    status=Status.PASS if redundancy_ok else Status.FAIL,
                    message=redundancy_message,
                )
            )
            warning_redundancy_ok, warning_redundancy_message = (
                semantic_redundancy_available_pair(
                    "warning",
                    "info",
                    data,
                    semantic_roles if semantic_payload is not None else None,
                )
            )
            result.checks.append(
                CheckResult(
                    name=f"{variant_name}/warning-info_redundancy",
                    status=Status.PASS if warning_redundancy_ok else Status.FAIL,
                    message=warning_redundancy_message,
                )
            )
            progress_redundancy_ok, progress_redundancy_message = (
                semantic_redundancy_available_pair(
                    "progress",
                    "disabled",
                    data,
                    semantic_roles if semantic_payload is not None else None,
                )
            )
            result.checks.append(
                CheckResult(
                    name=f"{variant_name}/progress-disabled_redundancy",
                    status=Status.PASS if progress_redundancy_ok else Status.FAIL,
                    message=progress_redundancy_message,
                )
            )

        return result


if __name__ == "__main__":
    gate = CVDGate()
    result = gate.validate()
    print(result)
    raise SystemExit(0 if result.status != Status.FAIL else 1)
