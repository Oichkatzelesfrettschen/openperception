#!/usr/bin/env python3
"""Generate real science-use-case panels for the Blender showcase."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = REPO_ROOT / "artifacts" / "blender_showcase" / "generated"
MANIFEST_PATH = GENERATED_DIR / "physics_views_manifest.json"

VIEW_SPECS = (
    {
        "id": "gw_chirp",
        "case_title": "GW Chirp",
        "mode_label": "Color-safe",
        "source_repo": "compact-common",
        "source_path": Path("/home/eirikr/Github/compact-common/.cache/blender/renders/gw_strain_ribbon/gw_strain_ribbon.png"),
        "source_box": (80, 270, 520, 760),
        "main_box": (620, 180, 1730, 800),
    },
    {
        "id": "neutrino_cooling",
        "case_title": "Neutrino Cooling",
        "mode_label": "Symbol-guided",
        "source_repo": "compact-common",
        "source_path": Path("/home/eirikr/Github/compact-common/dist/releases/neutrino-processes-latest.png"),
        "contact_sheet_path": Path("/home/eirikr/Github/compact-common/dist/releases/neutrino-processes-explainer-contact-sheet-latest.png"),
        "source_box": (40, 120, 540, 940),
        "main_box": (160, 80, 1760, 1020),
    },
    {
        "id": "blackhole_lensing",
        "case_title": "Black Hole Lensing",
        "mode_label": "Depth-safe",
        "source_repo": "Blackhole",
        "source_path": Path("/home/eirikr/Github/Blackhole/build/Release/reports/octane_harsh_benchmark_artifacts/render_engine_final.png"),
        "source_box": (200, 80, 460, 310),
        "main_box": (140, 40, 500, 330),
    },
)

PANEL_SIZE = (1400, 860)
SOURCE_INSET_SIZE = (320, 240)
MAIN_REGION_BOX = (420, 90, 1320, 770)


def _cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def _open_crop(path: Path, box: tuple[int, int, int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return image.crop(box)


def _dim_source(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    source = _cover_crop(image, size)
    source = ImageOps.grayscale(source).convert("RGB")
    source = ImageEnhance.Contrast(source).enhance(0.72)
    source = ImageEnhance.Brightness(source).enhance(0.82)
    return source


def _compose_panel(source_inset: Image.Image, main_panel: Image.Image, accent: str) -> Image.Image:
    panel = Image.new("RGB", PANEL_SIZE, "#111827")
    draw = ImageDraw.Draw(panel)
    draw.rounded_rectangle((18, 18, PANEL_SIZE[0] - 18, PANEL_SIZE[1] - 18), radius=32, fill="#0F172A", outline=accent, width=10)
    draw.rounded_rectangle((42, 64, 372, 314), radius=24, fill="#1F2937", outline="#D1D5DB", width=4)
    panel.paste(source_inset, (47, 69))
    draw.line((360, 190, 430, 190), fill=accent, width=8)
    draw.polygon(((430, 190), (396, 168), (396, 212)), fill=accent)
    draw.rounded_rectangle((MAIN_REGION_BOX[0], MAIN_REGION_BOX[1], MAIN_REGION_BOX[2], MAIN_REGION_BOX[3]), radius=28, fill="#E5E7EB", outline=accent, width=8)
    panel.paste(main_panel, (MAIN_REGION_BOX[0] + 16, MAIN_REGION_BOX[1] + 16))
    return panel


def _build_gw_panel(spec: dict) -> dict[str, str]:
    source_crop = _open_crop(spec["source_path"], spec["source_box"])
    main_crop = _open_crop(spec["source_path"], spec["main_box"])
    source_inset = _dim_source(source_crop, SOURCE_INSET_SIZE)
    transformed = _cover_crop(main_crop, (MAIN_REGION_BOX[2] - MAIN_REGION_BOX[0] - 32, MAIN_REGION_BOX[3] - MAIN_REGION_BOX[1] - 32))
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
        draw.ellipse((x - 24, y - 24, x + 24, y + 24), fill=("#1D4ED8", "#7C3AED", "#DB2777")[idx], outline="#F8FAFC", width=4)
    for idx, y in enumerate((int(height * 0.24), int(height * 0.5), int(height * 0.74))):
        draw.rectangle((18, y - 16, 110, y + 16), fill="#111827" if idx % 2 == 0 else "#374151")
    panel = _compose_panel(source_inset, transformed, "#3730A3")
    output_path = GENERATED_DIR / "gw_chirp_panel.png"
    panel.save(output_path)
    return {"panel_texture": str(output_path), "source_path": str(spec["source_path"])}


def _build_neutrino_panel(spec: dict) -> dict[str, str]:
    source_crop = _open_crop(spec["source_path"], spec["source_box"])
    main_crop = _open_crop(spec["source_path"], spec["main_box"])
    contact_sheet = Image.open(spec["contact_sheet_path"]).convert("RGB")
    source_inset = _dim_source(source_crop, SOURCE_INSET_SIZE)
    transformed = _cover_crop(main_crop, (MAIN_REGION_BOX[2] - MAIN_REGION_BOX[0] - 32, MAIN_REGION_BOX[3] - MAIN_REGION_BOX[1] - 32))
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
    draw.rounded_rectangle((40, height - 162, width - 40, height - 22), radius=22, outline="#111827", width=6)
    panel = _compose_panel(source_inset, transformed, "#7C3AED")
    output_path = GENERATED_DIR / "neutrino_cooling_panel.png"
    panel.save(output_path)
    return {"panel_texture": str(output_path), "source_path": str(spec["source_path"])}


def _build_blackhole_panel(spec: dict) -> dict[str, str]:
    source_crop = _open_crop(spec["source_path"], spec["source_box"])
    main_crop = _open_crop(spec["source_path"], spec["main_box"])
    source_inset = _dim_source(source_crop, SOURCE_INSET_SIZE)
    transformed = _cover_crop(main_crop, (MAIN_REGION_BOX[2] - MAIN_REGION_BOX[0] - 32, MAIN_REGION_BOX[3] - MAIN_REGION_BOX[1] - 32))
    transformed = ImageEnhance.Brightness(transformed).enhance(1.75)
    transformed = ImageEnhance.Contrast(transformed).enhance(2.3)
    transformed = transformed.filter(ImageFilter.GaussianBlur(radius=0.4))
    draw = ImageDraw.Draw(transformed)
    width, height = transformed.size
    cx = width * 0.54
    cy = height * 0.47
    for radius, color in ((120, "#FB923C"), (170, "#F59E0B"), (230, "#FDE68A")):
        draw.arc((cx - radius, cy - radius, cx + radius, cy + radius), start=30, end=330, fill=color, width=7)
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
    output_path = GENERATED_DIR / "blackhole_lensing_panel.png"
    panel.save(output_path)
    return {"panel_texture": str(output_path), "source_path": str(spec["source_path"])}


BUILDERS = {
    "gw_chirp": _build_gw_panel,
    "neutrino_cooling": _build_neutrino_panel,
    "blackhole_lensing": _build_blackhole_panel,
}


def build_showcase_physics_views(output_dir: Path = GENERATED_DIR) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "concept": "real physics use cases turned into real accessible and animated views showcase",
        "generated_dir": str(output_dir),
        "views": [],
    }
    for spec in VIEW_SPECS:
        result = BUILDERS[spec["id"]](spec)
        manifest["views"].append(
            {
                "id": spec["id"],
                "case_title": spec["case_title"],
                "mode_label": spec["mode_label"],
                "source_repo": spec["source_repo"],
                **result,
            }
        )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(GENERATED_DIR))
    parser.add_argument("--output-manifest", default=str(MANIFEST_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    manifest = build_showcase_physics_views(output_dir)
    output_manifest = Path(args.output_manifest)
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    output_manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
