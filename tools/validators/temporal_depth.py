"""
TEMPORAL/DEPTH gate (GATE-005) - first partial token/profile policy validation.

WHY: The repo had no executable runtime for GATE-005. This first partial
implementation validates motion-token safety and display-profile compatibility.
It intentionally does not yet validate rendered motion paths or monocular depth
cues in content.
"""
# ruff: noqa: I001
from __future__ import annotations

import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from base import CheckResult, GateResult, Severity, Status, ValidatorGate
else:
    from .base import CheckResult, GateResult, Severity, Status, ValidatorGate


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MOTION_JSON = REPO_ROOT / "specs" / "tokens" / "temporal" / "motion.json"
DEFAULT_PROFILE_MANIFEST = REPO_ROOT / "specs" / "tokens" / "profiles" / "axis-profiles.json"


class TemporalDepthGate(ValidatorGate):
    """GATE-005: TEMPORAL_DEPTH - token/profile temporal policy validation."""

    gate_id = "GATE-005"
    gate_name = "TEMPORAL_DEPTH"
    severity = Severity.WARNING

    def __init__(
        self,
        motion_json_path: Path | None = None,
        profile_manifest_path: Path | None = None,
    ):
        self.motion_json_path = motion_json_path or DEFAULT_MOTION_JSON
        self.profile_manifest_path = profile_manifest_path or DEFAULT_PROFILE_MANIFEST

    def validate(self, **kwargs) -> GateResult:
        result = self._make_result()
        motion = json.loads(self.motion_json_path.read_text())
        profiles = json.loads(self.profile_manifest_path.read_text())["profiles"]

        units = motion["units"]
        result.checks.append(
            CheckResult(
                name="temporal/units_time_based",
                status=Status.PASS
                if units.get("time") == "milliseconds" and units.get("frequency") == "hertz"
                else Status.FAIL,
                message=f"time={units.get('time')} frequency={units.get('frequency')}",
            )
        )

        flash_cap = float(motion["frequency_caps"]["flash_hard_cap"]["value_hz"])
        result.checks.append(
            CheckResult(
                name="temporal/flash_hard_cap",
                status=Status.PASS if flash_cap <= 3.0 else Status.FAIL,
                message=f"{flash_cap:g} Hz hard cap (required <= 3 Hz)",
                value=flash_cap,
                threshold=3.0,
            )
        )

        high_risk = motion["frequency_caps"]["high_risk_band"]
        result.checks.append(
            CheckResult(
                name="temporal/high_risk_band",
                status=Status.PASS
                if high_risk.get("min_hz") == 10 and high_risk.get("max_hz") == 25
                else Status.WARN,
                message=f"{high_risk.get('min_hz')}..{high_risk.get('max_hz')} Hz",
            )
        )

        overrides = motion["display_mode_overrides"]
        reduced_motion = overrides["reduced_motion"]
        result.checks.append(
            CheckResult(
                name="temporal/reduced_motion_disables_animation",
                status=Status.PASS
                if not reduced_motion.get("animation_enabled")
                and not reduced_motion.get("pulse_enabled")
                and not reduced_motion.get("parallax_enabled")
                else Status.FAIL,
                message="reduced_motion disables animation, pulse, and parallax",
            )
        )

        profile_multipliers = motion["durations"]["profile_multipliers"]
        result.checks.append(
            CheckResult(
                name="temporal/reduced_motion_multiplier",
                status=Status.PASS if profile_multipliers.get("reduced_motion") == 0 else Status.FAIL,
                message=f"reduced_motion multiplier {profile_multipliers.get('reduced_motion')}",
                value=float(profile_multipliers.get("reduced_motion", -1)),
                threshold=0.0,
            )
        )

        flicker_sensitive = overrides["flicker_sensitive"]
        result.checks.append(
            CheckResult(
                name="temporal/flicker_sensitive_caps",
                status=Status.PASS
                if not flicker_sensitive.get("pulse_enabled")
                and not flicker_sensitive.get("parallax_enabled")
                else Status.FAIL,
                message="flicker_sensitive disables pulse and parallax",
            )
        )

        eink = overrides["eink"]
        result.checks.append(
            CheckResult(
                name="temporal/eink_state_semantics",
                status=Status.PASS
                if not eink.get("animation_enabled")
                and profile_multipliers.get("eink", 0) >= 3.0
                else Status.FAIL,
                message="eink disables animation and stretches durations",
            )
        )

        reduced_profile = profiles["reduced-motion"]["caps"]
        result.checks.append(
            CheckResult(
                name="temporal/profile_reduced_motion_caps",
                status=Status.PASS
                if reduced_profile["max_animation_hz"] == 0
                and reduced_profile["max_luminance_modulation_hz"] == 0
                and reduced_profile["min_transition_duration_ms"] == 0
                else Status.FAIL,
                message="reduced-motion profile caps are fully disabled/instant",
            )
        )

        flicker_profile = profiles["flicker-sensitive"]["caps"]
        luminance_sensitive_cap = float(
            motion["frequency_caps"]["luminance_modulation_cap"]["flicker_sensitive_hz"]
        )
        result.checks.append(
            CheckResult(
                name="temporal/profile_flicker_sensitive_caps",
                status=Status.PASS
                if flicker_profile["max_animation_hz"] <= 30
                and flicker_profile["max_luminance_modulation_hz"] <= luminance_sensitive_cap
                else Status.FAIL,
                message=(
                    "flicker-sensitive profile caps respect motion token ceilings"
                ),
            )
        )

        eink_profile = profiles["eink"]["caps"]
        result.checks.append(
            CheckResult(
                name="temporal/profile_eink_caps",
                status=Status.PASS
                if eink_profile["max_animation_hz"] <= 1
                and eink_profile["pattern_encoding_required"]
                else Status.FAIL,
                message="eink profile constrains animation and requires pattern encoding",
            )
        )

        frame_independence = motion["frame_rate_independence"]["principle"]
        result.checks.append(
            CheckResult(
                name="temporal/time_based_motion",
                status=Status.PASS if "time" in frame_independence.lower() else Status.WARN,
                message=frame_independence,
            )
        )

        return result


if __name__ == "__main__":
    gate = TemporalDepthGate()
    gate_result = gate.validate()
    print(gate_result)
    raise SystemExit(0 if gate_result.status != Status.FAIL else 1)
