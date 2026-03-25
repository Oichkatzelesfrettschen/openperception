"""Tests for the first-pass seizure validator gate."""
import json
import sys
from pathlib import Path

from PIL import Image


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validators.base import Status
from validators.seizure import SeizureGate


def write_frame(path: Path, color: tuple[int, int, int], size: tuple[int, int] = (20, 20)) -> None:
    image = Image.new("RGB", size, color)
    image.save(path)


def write_manifest(path: Path, frame_rate_hz: float, frame_names: list[str]) -> None:
    payload = {
        "frame_rate_hz": frame_rate_hz,
        "frames": frame_names,
    }
    path.write_text(json.dumps(payload))


def test_seizure_gate_passes_low_frequency_small_area(tmp_path: Path) -> None:
    black = tmp_path / "black.png"
    white_small = tmp_path / "white_small.png"
    black_again = tmp_path / "black_again.png"
    write_frame(black, (0, 0, 0))
    image = Image.new("RGB", (20, 20), (0, 0, 0))
    for x in range(5):
        for y in range(5):
            image.putpixel((x, y), (255, 255, 255))
    image.save(white_small)
    write_frame(black_again, (0, 0, 0))

    manifest = tmp_path / "manifest.json"
    write_manifest(manifest, frame_rate_hz=1.0, frame_names=["black.png", "white_small.png", "black_again.png"])

    result = SeizureGate(manifest).validate()

    assert result.status == Status.PASS


def test_seizure_gate_fails_high_frequency_and_large_area(tmp_path: Path) -> None:
    frames = []
    for index, color in enumerate([(0, 0, 0), (255, 255, 255), (0, 0, 0), (255, 255, 255)]):
        path = tmp_path / f"frame_{index}.png"
        write_frame(path, color)
        frames.append(path.name)

    manifest = tmp_path / "manifest.json"
    write_manifest(manifest, frame_rate_hz=10.0, frame_names=frames)

    result = SeizureGate(manifest).validate()

    assert result.status == Status.FAIL
    assert any(check.name == "seizure/flash_frequency" and check.status == Status.FAIL for check in result.checks)
    assert any(check.name == "seizure/flash_area" and check.status == Status.FAIL for check in result.checks)


def test_seizure_gate_fails_red_flash(tmp_path: Path) -> None:
    black = tmp_path / "black.png"
    red = tmp_path / "red.png"
    write_frame(black, (0, 0, 0))
    write_frame(red, (255, 0, 0))

    manifest = tmp_path / "manifest.json"
    write_manifest(manifest, frame_rate_hz=1.0, frame_names=["black.png", "red.png"])

    result = SeizureGate(manifest).validate()

    assert any(check.name == "seizure/red_flash_saturation" and check.status == Status.FAIL for check in result.checks)
