"""Tests for the first partial temporal/depth gate."""
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validators.base import Status
from validators.temporal_depth import TemporalDepthGate


def write_motion(path: Path, *, reduced_motion_enabled: bool = False) -> None:
    payload = {
        "units": {"time": "milliseconds", "frequency": "hertz"},
        "durations": {"profile_multipliers": {"standard": 1.0, "eink": 3.0, "flicker_sensitive": 1.5, "reduced_motion": 0}},
        "frequency_caps": {
            "flash_hard_cap": {"value_hz": 3},
            "high_risk_band": {"min_hz": 10, "max_hz": 25},
            "luminance_modulation_cap": {"flicker_sensitive_hz": 1},
        },
        "display_mode_overrides": {
            "reduced_motion": {
                "animation_enabled": reduced_motion_enabled,
                "pulse_enabled": False,
                "parallax_enabled": False,
            },
            "flicker_sensitive": {
                "animation_enabled": True,
                "pulse_enabled": False,
                "parallax_enabled": False,
            },
            "eink": {
                "animation_enabled": False,
                "pulse_enabled": False,
                "parallax_enabled": False,
            },
        },
        "frame_rate_independence": {
            "principle": "Define motion in time (ms), not frames",
        },
    }
    path.write_text(json.dumps(payload))


def write_profiles(path: Path, *, reduced_motion_hz: int = 0) -> None:
    payload = {
        "profiles": {
            "reduced-motion": {
                "caps": {
                    "max_animation_hz": reduced_motion_hz,
                    "max_luminance_modulation_hz": 0,
                    "min_transition_duration_ms": 0,
                }
            },
            "flicker-sensitive": {
                "caps": {
                    "max_animation_hz": 30,
                    "max_luminance_modulation_hz": 1,
                    "min_transition_duration_ms": 300,
                }
            },
            "eink": {
                "caps": {
                    "max_animation_hz": 1,
                    "max_luminance_modulation_hz": 0.5,
                    "min_transition_duration_ms": 500,
                    "pattern_encoding_required": True,
                }
            },
        }
    }
    path.write_text(json.dumps(payload))


def test_temporal_depth_gate_passes_on_safe_motion_policy(tmp_path: Path) -> None:
    motion = tmp_path / "motion.json"
    profiles = tmp_path / "profiles.json"
    write_motion(motion)
    write_profiles(profiles)

    result = TemporalDepthGate(motion, profiles).validate()

    assert result.status == Status.PASS


def test_temporal_depth_gate_fails_on_bad_reduced_motion_policy(tmp_path: Path) -> None:
    motion = tmp_path / "motion.json"
    profiles = tmp_path / "profiles.json"
    write_motion(motion, reduced_motion_enabled=True)
    write_profiles(profiles, reduced_motion_hz=12)

    result = TemporalDepthGate(motion, profiles).validate()

    assert result.status == Status.FAIL
    assert any(
        check.name == "temporal/reduced_motion_disables_animation" and check.status == Status.FAIL
        for check in result.checks
    )
    assert any(
        check.name == "temporal/profile_reduced_motion_caps" and check.status == Status.FAIL
        for check in result.checks
    )
