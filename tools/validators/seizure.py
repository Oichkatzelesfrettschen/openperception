"""
SEIZURE gate (GATE-001) - first-pass flash safety analysis over frame sequences.

WHY: The validator framework declares a blocking seizure-safety gate, but the
runtime previously had no executable implementation. This module provides a
conservative, frame-sequence-based subset that checks:

- flash frequency,
- red flash saturation,
- affected flash area,
- cumulative flashing exposure.

It intentionally does not yet implement pattern-oscillation analysis.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

from validators.base import (
    CheckResult,
    GateResult,
    Severity,
    Status,
    ValidatorGate,
)


DEFAULT_LUMINANCE_DELTA_THRESHOLD = 0.10
FLASH_FREQUENCY_THRESHOLD_HZ = 3.0
FLASH_AREA_THRESHOLD_RATIO = 0.25
CUMULATIVE_EXPOSURE_THRESHOLD_SECONDS = 5.0
RED_CHANNEL_THRESHOLD = 0.80
RED_DOMINANCE_THRESHOLD = 0.80
RED_FLASH_AREA_THRESHOLD_RATIO = 0.25


@dataclass(frozen=True)
class SeizureManifest:
    frame_rate_hz: float
    frames: tuple[Path, ...]
    luminance_delta_threshold: float


def _srgb_to_linear(arr: np.ndarray) -> np.ndarray:
    return np.where(
        arr <= 0.04045,
        arr / 12.92,
        ((arr + 0.055) / 1.055) ** 2.4,
    )


def _relative_luminance(image: np.ndarray) -> np.ndarray:
    rgb = image.astype(np.float32) / 255.0
    linear = _srgb_to_linear(rgb)
    return (
        0.2126 * linear[..., 0]
        + 0.7152 * linear[..., 1]
        + 0.0722 * linear[..., 2]
    )


def load_manifest(manifest_path: Path) -> SeizureManifest:
    payload = json.loads(manifest_path.read_text())
    frame_rate_hz = float(payload["frame_rate_hz"])
    frames = tuple((manifest_path.parent / rel_path).resolve() for rel_path in payload["frames"])
    luminance_delta_threshold = float(
        payload.get("luminance_delta_threshold", DEFAULT_LUMINANCE_DELTA_THRESHOLD)
    )
    return SeizureManifest(
        frame_rate_hz=frame_rate_hz,
        frames=frames,
        luminance_delta_threshold=luminance_delta_threshold,
    )


def load_rgb_frames(frame_paths: tuple[Path, ...]) -> list[np.ndarray]:
    frames: list[np.ndarray] = []
    for path in frame_paths:
        with Image.open(path) as image:
            frames.append(np.asarray(image.convert("RGB")))
    return frames


class SeizureGate(ValidatorGate):
    """GATE-001: SEIZURE - frame-sequence flash safety analysis."""

    gate_id = "GATE-001"
    gate_name = "SEIZURE"
    severity = Severity.BLOCKING

    def __init__(self, manifest_path: Path):
        self.manifest_path = manifest_path

    def validate(self, **kwargs) -> GateResult:
        manifest = load_manifest(self.manifest_path)
        result = self._make_result()

        if manifest.frame_rate_hz <= 0:
            result.checks.append(
                CheckResult(
                    name="seizure/frame_rate_hz",
                    status=Status.FAIL,
                    message="Manifest frame_rate_hz must be > 0",
                )
            )
            return result

        if len(manifest.frames) < 2:
            result.checks.append(
                CheckResult(
                    name="seizure/frame_count",
                    status=Status.FAIL,
                    message="Manifest must provide at least 2 frames",
                )
            )
            return result

        frames = load_rgb_frames(manifest.frames)
        first_shape = frames[0].shape
        if any(frame.shape != first_shape for frame in frames[1:]):
            result.checks.append(
                CheckResult(
                    name="seizure/frame_dimensions",
                    status=Status.FAIL,
                    message="All frames must share identical dimensions",
                )
            )
            return result

        luminances = [_relative_luminance(frame) for frame in frames]
        flash_count = 0
        max_area_ratio = 0.0
        max_red_flash_ratio = 0.0

        for _previous_frame, current_frame, prev_lum, curr_lum in zip(
            frames[:-1],
            frames[1:],
            luminances[:-1],
            luminances[1:],
            strict=True,
        ):
            delta = np.abs(curr_lum - prev_lum)
            changed_mask = delta > manifest.luminance_delta_threshold
            area_ratio = float(changed_mask.mean())
            if area_ratio <= 0.0:
                continue

            max_area_ratio = max(max_area_ratio, area_ratio)
            flash_count += 1

            current_rgb = current_frame.astype(np.float32) / 255.0
            red_mask = (
                changed_mask
                & (current_rgb[..., 0] >= RED_CHANNEL_THRESHOLD)
                & ((current_rgb[..., 0] - current_rgb[..., 1] - current_rgb[..., 2]) >= RED_DOMINANCE_THRESHOLD)
            )
            red_ratio = float(red_mask.mean())
            max_red_flash_ratio = max(max_red_flash_ratio, red_ratio)

        duration_seconds = (len(frames) - 1) / manifest.frame_rate_hz
        flash_frequency_hz = flash_count / duration_seconds if duration_seconds > 0 else 0.0
        cumulative_exposure_seconds = flash_count / manifest.frame_rate_hz

        result.checks.append(
            CheckResult(
                name="seizure/flash_frequency",
                status=Status.PASS if flash_frequency_hz <= FLASH_FREQUENCY_THRESHOLD_HZ else Status.FAIL,
                message=(
                    f"{flash_frequency_hz:.2f} flashes/sec (required <= {FLASH_FREQUENCY_THRESHOLD_HZ:.1f})"
                ),
                value=flash_frequency_hz,
                threshold=FLASH_FREQUENCY_THRESHOLD_HZ,
            )
        )
        result.checks.append(
            CheckResult(
                name="seizure/red_flash_saturation",
                status=Status.PASS if max_red_flash_ratio < RED_FLASH_AREA_THRESHOLD_RATIO else Status.FAIL,
                message=(
                    f"max red flash area ratio {max_red_flash_ratio:.3f} "
                    f"(required < {RED_FLASH_AREA_THRESHOLD_RATIO:.2f})"
                ),
                value=max_red_flash_ratio,
                threshold=RED_FLASH_AREA_THRESHOLD_RATIO,
            )
        )
        result.checks.append(
            CheckResult(
                name="seizure/flash_area",
                status=Status.PASS if max_area_ratio < FLASH_AREA_THRESHOLD_RATIO else Status.FAIL,
                message=(
                    f"max flash area ratio {max_area_ratio:.3f} "
                    f"(required < {FLASH_AREA_THRESHOLD_RATIO:.2f})"
                ),
                value=max_area_ratio,
                threshold=FLASH_AREA_THRESHOLD_RATIO,
            )
        )
        result.checks.append(
            CheckResult(
                name="seizure/cumulative_exposure",
                status=Status.PASS if cumulative_exposure_seconds < CUMULATIVE_EXPOSURE_THRESHOLD_SECONDS else Status.FAIL,
                message=(
                    f"{cumulative_exposure_seconds:.2f}s cumulative flashing "
                    f"(required < {CUMULATIVE_EXPOSURE_THRESHOLD_SECONDS:.1f}s)"
                ),
                value=cumulative_exposure_seconds,
                threshold=CUMULATIVE_EXPOSURE_THRESHOLD_SECONDS,
            )
        )
        return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run seizure validation on a frame manifest.")
    parser.add_argument("manifest", help="Path to seizure manifest JSON")
    args = parser.parse_args()

    gate = SeizureGate(Path(args.manifest))
    gate_result = gate.validate()
    print(gate_result)
    raise SystemExit(0 if gate_result.status != Status.FAIL else 1)
