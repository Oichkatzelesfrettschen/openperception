#!/usr/bin/env python3
"""Generate real science-use-case still and animated views for the showcase."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = REPO_ROOT / "artifacts" / "blender_showcase" / "generated"
ANIMATED_DIR = REPO_ROOT / "artifacts" / "blender_showcase" / "animated"
MANIFEST_NAME = "physics_views_manifest.json"
ANIMATED_MANIFEST_NAME = "animated_views_manifest.json"

VIEW_SPECS = (
    {
        "id": "gw_chirp",
        "case_title": "GW Chirp",
        "mode_label": "Color-safe",
        "source_repo": "compact-common",
        "source_path": Path(
            "/home/eirikr/Github/compact-common/.cache/blender/renders/"
            "gw_strain_ribbon/gw_strain_ribbon.png"
        ),
        "data_path": Path(
            "/home/eirikr/Github/compact-common/blender/data/gw170817_processed.json"
        ),
        "source_box": (80, 270, 520, 760),
        "main_box": (620, 180, 1730, 800),
        "animation_output": "gw_chirp_accessible.gif",
    },
    {
        "id": "neutrino_cooling",
        "case_title": "Neutrino Cooling",
        "mode_label": "Symbol-guided",
        "source_repo": "compact-common",
        "source_path": Path(
            "/home/eirikr/Github/compact-common/dist/releases/neutrino-processes-latest.png"
        ),
        "contact_sheet_path": Path(
            "/home/eirikr/Github/compact-common/dist/releases/"
            "neutrino-processes-explainer-contact-sheet-latest.png"
        ),
        "source_box": (40, 120, 540, 940),
        "main_box": (160, 80, 1760, 1020),
        "animation_output": "neutrino_cooling_guided.gif",
    },
    {
        "id": "blackhole_lensing",
        "case_title": "Black Hole Lensing",
        "mode_label": "Depth-safe",
        "source_repo": "Blackhole",
        "source_path": Path(
            "/home/eirikr/Github/Blackhole/logs/compare/compare_8_compute.png"
        ),
        "source_box": (1880, 460, 2940, 1520),
        "main_box": (1180, 120, 3540, 1780),
        "animation_frames": tuple(
            Path(
                f"/home/eirikr/Github/Blackhole/.cache/showcase_motion_compare_orbit_near/"
                f"frame_{frame_index:06d}.png"
            )
            for frame_index in range(8)
        ),
        "animation_output": "blackhole_lensing_depth_safe.gif",
    },
)

PANEL_SIZE = (1400, 860)
SOURCE_INSET_SIZE = (320, 240)
MAIN_REGION_BOX = (420, 90, 1320, 770)
ANIMATION_SIZE = (1280, 720)
ANIMATION_SOURCE_BOX = (48, 48, 300, 220)
ANIMATION_MAIN_BOX = (340, 40, 1236, 680)


def _manifest_path_for(output_dir: Path, name: str) -> Path:
    return output_dir / name


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(
        image,
        size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )


def _open_crop(path: Path, box: tuple[int, int, int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return image.crop(box)


def _dim_source(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    source = _cover_crop(image, size)
    source = ImageOps.grayscale(source).convert("RGB")
    source = ImageEnhance.Contrast(source).enhance(0.72)
    source = ImageEnhance.Brightness(source).enhance(0.82)
    return source


def _compose_panel(
    source_inset: Image.Image,
    main_panel: Image.Image,
    accent: str,
) -> Image.Image:
    panel = Image.new("RGB", PANEL_SIZE, "#111827")
    draw = ImageDraw.Draw(panel)
    draw.rounded_rectangle(
        (18, 18, PANEL_SIZE[0] - 18, PANEL_SIZE[1] - 18),
        radius=32,
        fill="#0F172A",
        outline=accent,
        width=10,
    )
    draw.rounded_rectangle(
        (42, 64, 372, 314),
        radius=24,
        fill="#1F2937",
        outline="#D1D5DB",
        width=4,
    )
    panel.paste(source_inset, (47, 69))
    draw.line((360, 190, 430, 190), fill=accent, width=8)
    draw.polygon(((430, 190), (396, 168), (396, 212)), fill=accent)
    draw.rounded_rectangle(
        (MAIN_REGION_BOX[0], MAIN_REGION_BOX[1], MAIN_REGION_BOX[2], MAIN_REGION_BOX[3]),
        radius=28,
        fill="#E5E7EB",
        outline=accent,
        width=8,
    )
    panel.paste(main_panel, (MAIN_REGION_BOX[0] + 16, MAIN_REGION_BOX[1] + 16))
    return panel


def _compose_animation_frame(
    source_inset: Image.Image,
    main_panel: Image.Image,
    accent: str,
) -> Image.Image:
    frame = Image.new("RGB", ANIMATION_SIZE, "#0B1220")
    draw = ImageDraw.Draw(frame)
    draw.rounded_rectangle(
        (14, 14, ANIMATION_SIZE[0] - 14, ANIMATION_SIZE[1] - 14),
        radius=28,
        fill="#0F172A",
        outline=accent,
        width=8,
    )
    draw.rounded_rectangle(
        ANIMATION_SOURCE_BOX,
        radius=22,
        fill="#1F2937",
        outline="#CBD5E1",
        width=4,
    )
    frame.paste(source_inset, (ANIMATION_SOURCE_BOX[0] + 4, ANIMATION_SOURCE_BOX[1] + 4))
    draw.line(
        (
            ANIMATION_SOURCE_BOX[2] + 18,
            140,
            ANIMATION_MAIN_BOX[0] - 18,
            140,
        ),
        fill=accent,
        width=8,
    )
    draw.polygon(
        (
            (ANIMATION_MAIN_BOX[0] - 18, 140),
            (ANIMATION_MAIN_BOX[0] - 48, 120),
            (ANIMATION_MAIN_BOX[0] - 48, 160),
        ),
        fill=accent,
    )
    draw.rounded_rectangle(
        ANIMATION_MAIN_BOX,
        radius=24,
        fill="#E5E7EB",
        outline=accent,
        width=8,
    )
    frame.paste(main_panel, (ANIMATION_MAIN_BOX[0] + 16, ANIMATION_MAIN_BOX[1] + 16))
    return frame


def _build_gw_panel(spec: dict, output_dir: Path) -> dict[str, str]:
    source_crop = _open_crop(spec["source_path"], spec["source_box"])
    main_crop = _open_crop(spec["source_path"], spec["main_box"])
    source_inset = _dim_source(source_crop, SOURCE_INSET_SIZE)
    transformed = _cover_crop(
        main_crop,
        (MAIN_REGION_BOX[2] - MAIN_REGION_BOX[0] - 32, MAIN_REGION_BOX[3] - MAIN_REGION_BOX[1] - 32),
    )
    transformed = ImageOps.grayscale(transformed)
    transformed = ImageOps.autocontrast(transformed).convert("RGB")
    transformed = ImageEnhance.Contrast(transformed).enhance(2.6)
    transformed = ImageEnhance.Brightness(transformed).enhance(1.15)
    draw = ImageDraw.Draw(transformed)
    width, height = transformed.size
    for x in (int(width * 0.72), int(width * 0.82), int(width * 0.92)):
        draw.line((x, 40, x, height - 40), fill="#F59E0B", width=10)
    for idx, x in enumerate((int(width * 0.16), int(width * 0.34), int(width * 0.54))):
        y = int(height * (0.25 + 0.15 * idx))
        draw.ellipse(
            (x - 24, y - 24, x + 24, y + 24),
            fill=("#1D4ED8", "#7C3AED", "#DB2777")[idx],
            outline="#F8FAFC",
            width=4,
        )
    for idx, y in enumerate((int(height * 0.24), int(height * 0.5), int(height * 0.74))):
        draw.rectangle(
            (18, y - 16, 110, y + 16),
            fill="#111827" if idx % 2 == 0 else "#374151",
        )
    panel = _compose_panel(source_inset, transformed, "#3730A3")
    output_path = output_dir / "gw_chirp_panel.png"
    panel.save(output_path)
    return {"panel_texture": str(output_path), "source_path": str(spec["source_path"])}


def _build_neutrino_panel(spec: dict, output_dir: Path) -> dict[str, str]:
    source_crop = _open_crop(spec["source_path"], spec["source_box"])
    main_crop = _open_crop(spec["source_path"], spec["main_box"])
    contact_sheet = Image.open(spec["contact_sheet_path"]).convert("RGB")
    source_inset = _dim_source(source_crop, SOURCE_INSET_SIZE)
    transformed = _cover_crop(
        main_crop,
        (MAIN_REGION_BOX[2] - MAIN_REGION_BOX[0] - 32, MAIN_REGION_BOX[3] - MAIN_REGION_BOX[1] - 32),
    )
    transformed = ImageEnhance.Contrast(transformed).enhance(1.18)
    transformed = ImageEnhance.Brightness(transformed).enhance(1.08)
    draw = ImageDraw.Draw(transformed)
    width, height = transformed.size
    accent = "#901C32"
    for x0, y0, x1, y1 in (
        (int(width * 0.58), int(height * 0.18), int(width * 0.83), int(height * 0.1)),
        (int(width * 0.6), int(height * 0.45), int(width * 0.9), int(height * 0.45)),
        (int(width * 0.5), int(height * 0.7), int(width * 0.82), int(height * 0.86)),
    ):
        draw.line((x0, y0, x1, y1), fill=accent, width=14)
        draw.polygon(((x1, y1), (x1 - 28, y1 - 18), (x1 - 28, y1 + 18)), fill=accent)
    for x, y, color in (
        (int(width * 0.58), int(height * 0.18), "#FDE68A"),
        (int(width * 0.6), int(height * 0.45), "#A7F3D0"),
        (int(width * 0.5), int(height * 0.7), "#FCE7F3"),
    ):
        draw.ellipse((x - 28, y - 28, x + 28, y + 28), fill=color, outline="#111827", width=4)
    strip = _cover_crop(contact_sheet, (width - 100, 120))
    transformed.paste(strip, (50, height - 150))
    draw.rounded_rectangle(
        (40, height - 162, width - 40, height - 22),
        radius=22,
        outline="#111827",
        width=6,
    )
    panel = _compose_panel(source_inset, transformed, "#7C3AED")
    output_path = output_dir / "neutrino_cooling_panel.png"
    panel.save(output_path)
    return {"panel_texture": str(output_path), "source_path": str(spec["source_path"])}


def _build_blackhole_panel(spec: dict, output_dir: Path) -> dict[str, str]:
    source_crop = _open_crop(spec["source_path"], spec["source_box"])
    main_crop = _open_crop(spec["source_path"], spec["main_box"])
    source_inset = _dim_source(source_crop, SOURCE_INSET_SIZE)
    transformed = _cover_crop(
        main_crop,
        (MAIN_REGION_BOX[2] - MAIN_REGION_BOX[0] - 32, MAIN_REGION_BOX[3] - MAIN_REGION_BOX[1] - 32),
    )
    transformed = ImageEnhance.Brightness(transformed).enhance(1.75)
    transformed = ImageEnhance.Contrast(transformed).enhance(2.3)
    transformed = transformed.filter(ImageFilter.GaussianBlur(radius=0.4))
    draw = ImageDraw.Draw(transformed)
    width, height = transformed.size
    cx = width * 0.54
    cy = height * 0.47
    for radius, color in ((120, "#FB923C"), (170, "#F59E0B"), (230, "#FDE68A")):
        draw.arc(
            (cx - radius, cy - radius, cx + radius, cy + radius),
            start=30,
            end=330,
            fill=color,
            width=7,
        )
    for x, y in (
        (int(width * 0.18), int(height * 0.48)),
        (int(width * 0.48), int(height * 0.18)),
        (int(width * 0.82), int(height * 0.48)),
        (int(width * 0.48), int(height * 0.82)),
    ):
        draw.line((x, y, cx, cy), fill="#E5E7EB", width=5)
        draw.rectangle((x - 18, y - 18, x + 18, y + 18), fill="#111827", outline="#F8FAFC", width=3)
    draw.line((60, height - 80, width - 60, height - 80), fill="#111827", width=10)
    panel = _compose_panel(source_inset, transformed, "#7C2D12")
    output_path = output_dir / "blackhole_lensing_panel.png"
    panel.save(output_path)
    return {"panel_texture": str(output_path), "source_path": str(spec["source_path"])}


def _build_blackhole_animation(spec: dict, output_dir: Path) -> dict[str, object]:
    source_crop = _open_crop(spec["source_path"], spec["source_box"])
    source_inset = _dim_source(
        source_crop,
        (ANIMATION_SOURCE_BOX[2] - ANIMATION_SOURCE_BOX[0] - 8, ANIMATION_SOURCE_BOX[3] - ANIMATION_SOURCE_BOX[1] - 8),
    )
    inner_size = (
        ANIMATION_MAIN_BOX[2] - ANIMATION_MAIN_BOX[0] - 32,
        ANIMATION_MAIN_BOX[3] - ANIMATION_MAIN_BOX[1] - 32,
    )
    frames: list[Image.Image] = []
    total = len(spec["animation_frames"])
    for frame_index, frame_path in enumerate(spec["animation_frames"]):
        transformed = _cover_crop(Image.open(frame_path).convert("RGB"), inner_size)
        transformed = ImageEnhance.Brightness(transformed).enhance(1.2)
        transformed = ImageEnhance.Contrast(transformed).enhance(1.55)
        draw = ImageDraw.Draw(transformed)
        width, height = transformed.size
        cx = width * 0.5
        cy = height * 0.5
        for radius, color in ((150, "#FDE68A"), (220, "#FB923C"), (290, "#F8FAFC")):
            draw.arc(
                (cx - radius, cy - radius, cx + radius, cy + radius),
                start=24,
                end=336,
                fill=color,
                width=5,
            )
        progress = (frame_index + 1) / max(total, 1)
        for angle_fraction in (0.12, 0.37, 0.68):
            x = int(cx + math.cos(progress * math.pi * 0.35 + angle_fraction * math.tau) * width * 0.34)
            y = int(cy + math.sin(progress * math.pi * 0.28 + angle_fraction * math.tau) * height * 0.24)
            draw.line((x, y, cx, cy), fill="#E5E7EB", width=4)
            draw.rectangle((x - 16, y - 16, x + 16, y + 16), fill="#111827", outline="#F8FAFC", width=3)
        frames.append(_compose_animation_frame(source_inset, transformed, "#7C2D12"))
    output_path = output_dir / spec["animation_output"]
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=180,
        loop=0,
        disposal=2,
    )
    return {
        "animation_path": str(output_path),
        "animation_basis": [str(path) for path in spec["animation_frames"]],
        "frame_count": len(frames),
    }


def _load_gw_waveform_points(spec: dict, width: int, height: int) -> list[tuple[float, float]]:
    payload = json.loads(Path(spec["data_path"]).read_text(encoding="utf-8"))
    times = payload["arrays"]["real_time_s"]
    whitened = payload["arrays"]["detector_strain_whitened_visual"]
    active = [(t, value) for t, value in zip(times, whitened, strict=False) if abs(value) > 0.5]
    if not active:
        active = list(zip(times, whitened, strict=False))
    window = active[-420:]
    values = [value for _, value in window]
    max_abs = max(max(abs(value) for value in values), 1.0)
    count = max(len(window) - 1, 1)
    points: list[tuple[float, float]] = []
    for index, (_time_s, value) in enumerate(window):
        x = 40 + index / count * (width - 80)
        y = height / 2 - (value / max_abs) * (height * 0.32)
        points.append((x, y))
    return points


def _build_gw_animation(spec: dict, output_dir: Path) -> dict[str, object]:
    source_crop = _open_crop(spec["source_path"], spec["source_box"])
    source_inset = _dim_source(source_crop, (ANIMATION_SOURCE_BOX[2] - ANIMATION_SOURCE_BOX[0] - 8, ANIMATION_SOURCE_BOX[3] - ANIMATION_SOURCE_BOX[1] - 8))
    inner_size = (
        ANIMATION_MAIN_BOX[2] - ANIMATION_MAIN_BOX[0] - 32,
        ANIMATION_MAIN_BOX[3] - ANIMATION_MAIN_BOX[1] - 32,
    )
    waveform_points = _load_gw_waveform_points(spec, inner_size[0], inner_size[1])
    colors = ["#93C5FD", "#7C3AED", "#F59E0B"]
    frames: list[Image.Image] = []
    n_frames = 14
    for frame_index in range(n_frames):
        transformed = Image.new("RGB", inner_size, "#F8FAFC")
        draw = ImageDraw.Draw(transformed)
        draw.line(waveform_points, fill="#CBD5E1", width=3)
        reveal = max(24, int(len(waveform_points) * (0.18 + 0.82 * (frame_index + 1) / n_frames)))
        draw.line(waveform_points[:reveal], fill="#111827", width=6)
        beacon_x = waveform_points[reveal - 1][0]
        draw.line((beacon_x, 24, beacon_x, inner_size[1] - 24), fill="#F59E0B", width=8)
        for color_index, fraction in enumerate((0.38, 0.62, 0.82)):
            marker_index = min(reveal - 1, max(0, int(reveal * fraction)))
            marker_x, marker_y = waveform_points[marker_index]
            draw.ellipse(
                (marker_x - 18, marker_y - 18, marker_x + 18, marker_y + 18),
                fill=colors[color_index],
                outline="#FFFFFF",
                width=3,
            )
        for band_index, y in enumerate((int(inner_size[1] * 0.22), int(inner_size[1] * 0.5), int(inner_size[1] * 0.78))):
            draw.rectangle(
                (16, y - 12, 98, y + 12),
                fill="#0F172A" if band_index % 2 == 0 else "#475569",
            )
        frames.append(_compose_animation_frame(source_inset, transformed, "#3730A3"))
    output_path = output_dir / spec["animation_output"]
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0,
        disposal=2,
    )
    return {
        "animation_path": str(output_path),
        "animation_basis": str(spec["data_path"]),
        "frame_count": n_frames,
    }


def _extract_contact_sheet_tiles(contact_sheet: Image.Image) -> list[Image.Image]:
    width, height = contact_sheet.size
    header = 72
    gutter = 20
    cols = 3
    rows = 2
    tile_w = (width - gutter * (cols + 1)) // cols
    tile_h = (height - header - gutter * (rows + 1)) // rows
    tiles: list[Image.Image] = []
    for row in range(rows):
        for col in range(cols):
            left = gutter + col * (tile_w + gutter)
            top = header + gutter + row * (tile_h + gutter)
            tiles.append(contact_sheet.crop((left, top, left + tile_w, top + tile_h)))
    return tiles


def _build_neutrino_animation(spec: dict, output_dir: Path) -> dict[str, object]:
    source_crop = _open_crop(spec["source_path"], spec["source_box"])
    source_inset = _dim_source(source_crop, (ANIMATION_SOURCE_BOX[2] - ANIMATION_SOURCE_BOX[0] - 8, ANIMATION_SOURCE_BOX[3] - ANIMATION_SOURCE_BOX[1] - 8))
    inner_size = (
        ANIMATION_MAIN_BOX[2] - ANIMATION_MAIN_BOX[0] - 32,
        ANIMATION_MAIN_BOX[3] - ANIMATION_MAIN_BOX[1] - 32,
    )
    contact_sheet = Image.open(spec["contact_sheet_path"]).convert("RGB")
    tiles = _extract_contact_sheet_tiles(contact_sheet)
    frames: list[Image.Image] = []
    for frame_index, tile in enumerate(tiles):
        transformed = _cover_crop(tile, inner_size)
        transformed = ImageEnhance.Contrast(transformed).enhance(1.08)
        draw = ImageDraw.Draw(transformed)
        accent = "#901C32"
        width, height = transformed.size
        progress = (frame_index + 1) / len(tiles)
        for x0, y0, x1, y1 in (
            (int(width * 0.58), int(height * 0.18), int(width * (0.58 + 0.22 * progress)), int(height * 0.1)),
            (int(width * 0.6), int(height * 0.45), int(width * (0.6 + 0.28 * progress)), int(height * 0.45)),
            (int(width * 0.5), int(height * 0.7), int(width * (0.5 + 0.24 * progress)), int(height * 0.84)),
        ):
            draw.line((x0, y0, x1, y1), fill=accent, width=12)
            draw.polygon(((x1, y1), (x1 - 24, y1 - 14), (x1 - 24, y1 + 14)), fill=accent)
        for x, y, color in (
            (int(width * 0.58), int(height * 0.18), "#FDE68A"),
            (int(width * 0.6), int(height * 0.45), "#A7F3D0"),
            (int(width * 0.5), int(height * 0.7), "#FCE7F3"),
        ):
            draw.ellipse((x - 22, y - 22, x + 22, y + 22), fill=color, outline="#111827", width=3)
        bar_right = 40 + int((width - 80) * progress)
        draw.rounded_rectangle((40, height - 84, bar_right, height - 44), radius=16, fill="#0F172A")
        frames.append(_compose_animation_frame(source_inset, transformed, "#7C3AED"))
    output_path = output_dir / spec["animation_output"]
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=260,
        loop=0,
        disposal=2,
    )
    return {
        "animation_path": str(output_path),
        "animation_basis": str(spec["contact_sheet_path"]),
        "frame_count": len(frames),
    }


PANEL_BUILDERS = {
    "gw_chirp": _build_gw_panel,
    "neutrino_cooling": _build_neutrino_panel,
    "blackhole_lensing": _build_blackhole_panel,
}

ANIMATION_BUILDERS = {
    "gw_chirp": _build_gw_animation,
    "neutrino_cooling": _build_neutrino_animation,
    "blackhole_lensing": _build_blackhole_animation,
}


def iter_showcase_source_inputs() -> list[dict[str, object]]:
    inputs: list[dict[str, object]] = []
    for spec in VIEW_SPECS:
        inputs.append(
            {
                "id": spec["id"],
                "path": spec["source_path"],
                "kind": "image",
                "role": "source_view",
            }
        )
        if "contact_sheet_path" in spec:
            inputs.append(
                {
                    "id": spec["id"],
                    "path": spec["contact_sheet_path"],
                    "kind": "image",
                    "role": "animation_contact_sheet",
                }
            )
        if "data_path" in spec:
            inputs.append(
                {
                    "id": spec["id"],
                    "path": spec["data_path"],
                    "kind": "json",
                    "role": "animation_data",
                }
            )
        if "animation_frames" in spec:
            for frame_path in spec["animation_frames"]:
                inputs.append(
                    {
                        "id": spec["id"],
                        "path": frame_path,
                        "kind": "image",
                        "role": "animation_frame",
                    }
                )
    return inputs


def validate_showcase_source_inputs() -> list[str]:
    violations: list[str] = []
    for entry in iter_showcase_source_inputs():
        path = Path(entry["path"])
        if not path.exists():
            violations.append(f"{entry['id']} missing {entry['role']}: {path}")
            continue
        if path.stat().st_size <= 0:
            violations.append(f"{entry['id']} unreadable empty {entry['role']}: {path}")
            continue
        if entry["kind"] == "image":
            try:
                with Image.open(path) as image:
                    image.verify()
            except Exception as exc:
                violations.append(f"{entry['id']} unreadable image {path}: {exc}")
        elif entry["kind"] == "json":
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                violations.append(f"{entry['id']} unreadable json {path}: {exc}")
                continue
            if not isinstance(payload, dict):
                violations.append(f"{entry['id']} json source is not an object: {path}")
    return violations


def _write_manifest(manifest: dict, output_dir: Path, name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = _manifest_path_for(output_dir, name)
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def build_showcase_physics_views(output_dir: Path = GENERATED_DIR) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 2,
        "concept": "real physics use cases turned into real accessible and animated views showcase",
        "generated_dir": str(output_dir),
        "views": [],
    }
    for spec in VIEW_SPECS:
        result = PANEL_BUILDERS[spec["id"]](spec, output_dir)
        manifest["views"].append(
            {
                "id": spec["id"],
                "case_title": spec["case_title"],
                "mode_label": spec["mode_label"],
                "source_repo": spec["source_repo"],
                **result,
            }
        )
    _write_manifest(manifest, output_dir, MANIFEST_NAME)
    return manifest


def build_showcase_animated_views(output_dir: Path = ANIMATED_DIR) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "concept": "animated accessible views derived from real sibling-repo physics artifacts",
        "generated_dir": str(output_dir),
        "views": [],
        "deferred_views": [],
    }
    for spec in VIEW_SPECS:
        builder = ANIMATION_BUILDERS.get(spec["id"])
        if builder is None:
            manifest["deferred_views"].append(
                {
                    "id": spec["id"],
                    "case_title": spec["case_title"],
                    "mode_label": spec["mode_label"],
                    "source_repo": spec["source_repo"],
                    "reason": (
                        "No real sibling-repo motion source is currently registered for this case; "
                        "keep it as a still-only accessibility view until that changes."
                    ),
                    "source_path": str(spec["source_path"]),
                }
            )
            continue
        result = builder(spec, output_dir)
        manifest["views"].append(
            {
                "id": spec["id"],
                "case_title": spec["case_title"],
                "mode_label": spec["mode_label"],
                "source_repo": spec["source_repo"],
                **result,
            }
        )
    _write_manifest(manifest, output_dir, ANIMATED_MANIFEST_NAME)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(GENERATED_DIR))
    parser.add_argument("--output-manifest", default=str(_manifest_path_for(GENERATED_DIR, MANIFEST_NAME)))
    parser.add_argument("--animated-output-dir", default=str(ANIMATED_DIR))
    parser.add_argument(
        "--animated-output-manifest",
        default=str(_manifest_path_for(ANIMATED_DIR, ANIMATED_MANIFEST_NAME)),
    )
    parser.add_argument("--skip-animations", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    violations = validate_showcase_source_inputs()
    if violations:
        raise SystemExit("\n".join(violations))
    output_dir = Path(args.output_dir)
    manifest = build_showcase_physics_views(output_dir)
    output_manifest = Path(args.output_manifest)
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    output_manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    animated_manifest = None
    if not args.skip_animations:
        animated_output_dir = Path(args.animated_output_dir)
        animated_manifest = build_showcase_animated_views(animated_output_dir)
        animated_output_manifest = Path(args.animated_output_manifest)
        animated_output_manifest.parent.mkdir(parents=True, exist_ok=True)
        animated_output_manifest.write_text(
            json.dumps(animated_manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    payload = {"physics_views": manifest}
    if animated_manifest is not None:
        payload["animated_views"] = animated_manifest
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
