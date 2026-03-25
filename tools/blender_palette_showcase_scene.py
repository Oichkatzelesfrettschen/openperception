#!/usr/bin/env python3
"""
Build and render the OpenPerception palette showcase scene inside Blender.

Run through Blender:
  blender --background --factory-startup \
    --python tools/blender_palette_showcase_scene.py -- \
    --spec artifacts/blender_showcase/openperception_palette_showcase_spec.json \
    --output artifacts/blender_showcase/openperception_palette_showcase_render.png \
    --blend-output artifacts/blender_showcase/openperception_palette_showcase_scene.blend
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render the OpenPerception palette showcase inside Blender.",
    )
    parser.add_argument("--spec", required=True, help="Path to showcase JSON spec.")
    parser.add_argument("--output", required=True, help="Path to rendered PNG output.")
    parser.add_argument(
        "--engine",
        choices=("auto", "eevee", "octane", "cycles"),
        default="auto",
        help="Preferred renderer. 'auto' prefers Octane when available, then Eevee, then Cycles.",
    )
    parser.add_argument(
        "--blend-output",
        help="Optional path for saving the generated .blend scene.",
    )
    return parser.parse_args(argv)


def _blender_args() -> list[str]:
    import sys

    argv = sys.argv
    if "--" not in argv:
        return []
    return argv[argv.index("--") + 1 :]


def _srgb_channel_to_linear(value: float) -> float:
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def _hex_to_rgba(hex_code: str, alpha: float = 1.0) -> tuple[float, float, float, float]:
    hex_code = hex_code.lstrip("#")
    rgb = [int(hex_code[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]
    linear = [_srgb_channel_to_linear(component) for component in rgb]
    return (*linear, alpha)


def _hex_to_rgb(hex_code: str) -> tuple[float, float, float]:
    red, green, blue, _alpha = _hex_to_rgba(hex_code)
    return (red, green, blue)


def _clear_scene(bpy) -> None:
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for datablock_group in (
        bpy.data.meshes,
        bpy.data.curves,
        bpy.data.materials,
        bpy.data.cameras,
        bpy.data.lights,
    ):
        for datablock in list(datablock_group):
            if getattr(datablock, "users", 0) == 0:
                datablock_group.remove(datablock)


def _ensure_material(bpy, name: str, hex_code: str, roughness: float = 0.42):
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    if bpy.context.scene.render.engine == "octane":
        shader = nodes.new("OctaneUniversalMaterial")
        shader.inputs["Albedo"].default_value = _hex_to_rgb(hex_code)
        shader.inputs["Roughness"].default_value = roughness
        shader.inputs["Specular"].default_value = 0.04
        links.new(shader.outputs[0], output.inputs["Surface"])
    else:
        shader = nodes.new("ShaderNodeBsdfPrincipled")
        shader.inputs["Base Color"].default_value = _hex_to_rgba(hex_code)
        shader.inputs["Roughness"].default_value = roughness
        links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    return material


def _assign_material(obj, material) -> None:
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)


def _add_box(bpy, name: str, location: tuple[float, float, float], scale, material, bevel=0.04):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    _assign_material(obj, material)
    modifier = obj.modifiers.new(name="Bevel", type="BEVEL")
    modifier.width = bevel
    modifier.segments = 3
    return obj


def _add_marker(bpy, name: str, marker_type: str, location, size: float, material):
    if marker_type == "circle":
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=48, radius=size * 0.55, depth=size * 0.28, location=location
        )
    elif marker_type == "triangle":
        bpy.ops.mesh.primitive_cone_add(
            vertices=3, radius1=size * 0.72, radius2=0.0, depth=size * 0.42, location=location
        )
        bpy.context.active_object.rotation_euler.z = math.radians(30.0)
    elif marker_type == "square":
        bpy.ops.mesh.primitive_cube_add(location=location)
        bpy.context.active_object.scale = (size * 0.48, size * 0.48, size * 0.16)
    elif marker_type == "diamond":
        bpy.ops.mesh.primitive_cube_add(location=location)
        bpy.context.active_object.scale = (size * 0.42, size * 0.42, size * 0.16)
        bpy.context.active_object.rotation_euler.z = math.radians(45.0)
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=size * 0.4, location=location)
    obj = bpy.context.active_object
    obj.name = name
    _assign_material(obj, material)
    return obj


def _add_text(bpy, name: str, text: str, location, scale, material):
    bpy.ops.object.text_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.body = text
    obj.data.align_x = "CENTER"
    obj.data.extrude = 0.02
    obj.scale = scale
    obj.rotation_euler = (math.radians(90.0), 0.0, 0.0)
    _assign_material(obj, material)
    return obj


def _add_depth_strip(bpy, name: str, location, scale, material):
    return _add_box(
        bpy,
        name,
        location=location,
        scale=scale,
        material=material,
        bevel=0.025,
    )


def _add_area_light(bpy, scene, name: str, location, rotation, energy: float, size_x: float, size_y: float):
    if scene.render.engine == "octane":
        bpy.ops.octane.quick_add_octane_area_light()
        light = bpy.context.active_object
        light.name = name
        light.data.name = name
    else:
        light_data = bpy.data.lights.new(name=name, type="AREA")
        light = bpy.data.objects.new(name, light_data)
        scene.collection.objects.link(light)
    light.data.energy = energy
    light.data.shape = "RECTANGLE"
    light.data.size = size_x
    light.data.size_y = size_y
    light.location = location
    light.rotation_euler = rotation
    return light


def _select_render_engine(scene, preferred: str) -> str:
    eevee_engine = "BLENDER_EEVEE_NEXT"

    if preferred == "octane":
        order = ["octane", eevee_engine, "CYCLES"]
    elif preferred == "eevee":
        order = [eevee_engine, "octane", "CYCLES"]
    elif preferred == "cycles":
        order = ["CYCLES", eevee_engine, "octane"]
    else:
        order = ["octane", eevee_engine, "CYCLES"]

    for engine_name in order:
        if not engine_name:
            continue
        try:
            scene.render.engine = engine_name
            return engine_name
        except TypeError:
            continue
        except ValueError:
            continue
    enum_items = [item.identifier for item in scene.render.bl_rna.properties["engine"].enum_items]
    raise RuntimeError(f"No supported render engine found in {enum_items}")


def build_scene(bpy, spec: dict, render_engine: str = "auto") -> None:
    scene = bpy.context.scene
    selected_engine = _select_render_engine(scene, render_engine)
    scene.render.resolution_x = 1800
    scene.render.resolution_y = 1200
    scene.render.film_transparent = False
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = 64
        if hasattr(scene.eevee, "use_gtao"):
            scene.eevee.use_gtao = True
        if hasattr(scene.eevee, "use_bloom"):
            scene.eevee.use_bloom = True

    _clear_scene(bpy)

    world = scene.world
    if world is None:
        world = bpy.data.worlds.new("OpenPerceptionWorld")
        scene.world = world
    world.use_nodes = True
    world_nodes = world.node_tree.nodes
    world_links = world.node_tree.links
    world_nodes.clear()
    world_output = world_nodes.new("ShaderNodeOutputWorld")
    world_bg = world_nodes.new("ShaderNodeBackground")
    world_bg.inputs["Color"].default_value = _hex_to_rgba("#F4F1ED")
    world_bg.inputs["Strength"].default_value = 0.5
    world_links.new(world_bg.outputs["Background"], world_output.inputs["Surface"])

    floor_mat = _ensure_material(bpy, "Floor", "#BBB2AB", roughness=0.96)
    wall_mat = _ensure_material(bpy, "BackdropWall", "#E8E1DA", roughness=0.94)
    rail_near = _ensure_material(bpy, "DepthRailNear", "#A89D95", roughness=0.88)
    rail_mid = _ensure_material(bpy, "DepthRailMid", "#C7BDB4", roughness=0.9)
    rail_far = _ensure_material(bpy, "DepthRailFar", "#DED5CE", roughness=0.92)
    text_dark = _ensure_material(bpy, "TextDark", "#1F2937", roughness=0.55)
    text_warm = _ensure_material(bpy, "TextWarm", "#2A2321", roughness=0.55)
    neutral_dark = _ensure_material(bpy, "NeutralDark", "#2E3440", roughness=0.55)

    bpy.ops.mesh.primitive_plane_add(size=36, location=(0.0, 0.0, -0.35))
    floor = bpy.context.active_object
    floor.name = "Floor"
    _assign_material(floor, floor_mat)
    _add_box(
        bpy,
        "BackdropWall",
        location=(0.0, 2.55, 1.28),
        scale=(8.8, 0.08, 1.4),
        material=wall_mat,
        bevel=0.02,
    )
    _add_box(
        bpy,
        "DepthLegendPlaque",
        location=(0.0, -3.08, 0.16),
        scale=(2.9, 0.56, 0.08),
        material=wall_mat,
        bevel=0.04,
    )
    for rail_name, rail_y, rail_z, rail_mat in (
        ("DepthRailNear", -1.35, -0.16, rail_near),
        ("DepthRailMid", -0.1, -0.1, rail_mid),
        ("DepthRailFar", 1.15, -0.04, rail_far),
    ):
        _add_depth_strip(
            bpy,
            rail_name,
            location=(0.0, rail_y, rail_z),
            scale=(8.5, 0.06, 0.02),
            material=rail_mat,
        )

    camera_data = bpy.data.cameras.new("PaletteCamera")
    camera = bpy.data.objects.new("PaletteCamera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera.location = (0.0, -12.35, 6.1)
    camera.rotation_euler = (math.radians(62.0), 0.0, 0.0)
    camera.data.lens = 38

    key_energy = 250.0 if selected_engine == "octane" else 2550.0
    rim_energy = 55.0 if selected_engine == "octane" else 950.0
    _add_area_light(
        bpy,
        scene,
        "KeyLight",
        location=(-3.2, -6.35, 10.6),
        rotation=(math.radians(60.0), math.radians(13.0), math.radians(-11.0)),
        energy=key_energy,
        size_x=8.0,
        size_y=8.0,
    )
    _add_area_light(
        bpy,
        scene,
        "RimLight",
        location=(-0.6, 4.55, 5.4),
        rotation=(math.radians(-116.0), math.radians(3.0), math.radians(6.0)),
        energy=rim_energy,
        size_x=6.0,
        size_y=6.0,
    )

    lane_spacing = 4.6
    start_x = -lane_spacing
    swatch_depth_positions = (
        ("primary", -0.32, 0.42, (1.08, 0.31, 0.13)),
        ("accent", 0.0, 0.61, (0.96, 0.29, 0.13)),
        ("tertiary", 0.32, 0.8, (0.84, 0.27, 0.13)),
    )

    for index, lane in enumerate(spec["lanes"]):
        x = start_x + index * lane_spacing
        brand = lane["brand"]
        viz = lane["viz"]
        surface_mat = _ensure_material(
            bpy, f"{lane['scheme_id']}_surface", brand["surface"], roughness=0.72
        )
        border_mat = _ensure_material(
            bpy, f"{lane['scheme_id']}_border", brand["border"], roughness=0.68
        )
        primary_mat = _ensure_material(
            bpy, f"{lane['scheme_id']}_primary", brand["primaryStrong"], roughness=0.38
        )
        accent_mat = _ensure_material(
            bpy, f"{lane['scheme_id']}_accent", brand["accentStrong"], roughness=0.38
        )
        tertiary_color = brand["tertiaryStrong"] or brand["focusRing"]
        tertiary_mat = _ensure_material(
            bpy, f"{lane['scheme_id']}_tertiary", tertiary_color, roughness=0.38
        )
        marker_materials = [
            _ensure_material(bpy, f"{lane['scheme_id']}_marker_{i}", color, roughness=0.34)
            for i, color in enumerate(viz["categorical"][:4])
        ]
        label_mat = text_warm if lane["scheme_id"] == "atmosphere-red-mahogany" else text_dark

        _add_box(
            bpy,
            f"{lane['scheme_id']}_card",
            location=(x, 0.0, 0.15),
            scale=(1.65, 2.25, 0.18),
            material=surface_mat,
            bevel=0.08,
        )
        _add_box(
            bpy,
            f"{lane['scheme_id']}_outline",
            location=(x, 0.0, -0.04),
            scale=(1.74, 2.34, 0.04),
            material=border_mat,
            bevel=0.05,
        )

        for shelf_index, (shelf_name, shelf_y, shelf_z, shelf_scale) in enumerate(swatch_depth_positions):
            _add_box(
                bpy,
                f"{lane['scheme_id']}_{shelf_name}_shelf",
                location=(x, shelf_y, shelf_z - 0.08),
                scale=(shelf_scale[0] + 0.12, shelf_scale[1] + 0.05, 0.035),
                material=border_mat,
                bevel=0.03,
            )
        for swatch_name, swatch_y, swatch_z, swatch_scale in swatch_depth_positions:
            swatch_mat = {
                "primary": primary_mat,
                "accent": accent_mat,
                "tertiary": tertiary_mat,
            }[swatch_name]
            _add_box(
                bpy,
                f"{lane['scheme_id']}_{swatch_name}",
                location=(x, swatch_y, swatch_z),
                scale=swatch_scale,
                material=swatch_mat,
                bevel=0.06,
            )

        _add_text(
            bpy,
            f"{lane['scheme_id']}_title",
            lane["label"],
            location=(x, -1.7, 0.62),
            scale=(0.22, 0.22, 0.22),
            material=label_mat,
        )
        _add_text(
            bpy,
            f"{lane['scheme_id']}_subtitle",
            lane["scheme_id"],
            location=(x, -2.05, 0.48),
            scale=(0.1, 0.1, 0.1),
            material=neutral_dark,
        )

        marker_x_offsets = (-0.75, -0.25, 0.25, 0.75)
        for marker_index, marker_name in enumerate(viz["markers"][:4]):
            _add_marker(
                bpy,
                f"{lane['scheme_id']}_marker_{marker_index}",
                marker_name,
                location=(x + marker_x_offsets[marker_index], 1.72, 0.48),
                size=0.46,
                material=marker_materials[marker_index],
            )

        variant_names = lane["available_variants"]
        chip_start_x = x - 1.05
        chip_gap = 0.55
        for variant_index, variant_name in enumerate(variant_names):
            chip_x = chip_start_x + variant_index * chip_gap
            variant_brand = lane["variants"][variant_name]["brand"]
            chip_mat = _ensure_material(
                bpy,
                f"{lane['scheme_id']}_{variant_name}_chip",
                variant_brand["primaryStrong"],
                roughness=0.36,
            )
            _add_box(
                bpy,
                f"{lane['scheme_id']}_{variant_name}_chip_obj",
                location=(chip_x, -1.32, 0.43),
                scale=(0.2, 0.12, 0.08),
                material=chip_mat,
                bevel=0.03,
            )

    _add_text(
        bpy,
        "ShowcaseHeader",
        "OpenPerception Palette And Depth Showcase",
        location=(0.0, 2.18, 0.72),
        scale=(0.34, 0.34, 0.34),
        material=text_dark,
    )
    _add_text(
        bpy,
        "ShowcaseSubheader",
        "production | accessibility-first | warm lane | shared depth",
        location=(0.0, 1.82, 0.54),
        scale=(0.16, 0.16, 0.16),
        material=neutral_dark,
    )
    _add_text(
        bpy,
        "DepthPrinciple",
        "Static cues first: occlusion | scale | shadows | ground plane | labels",
        location=(0.0, 1.5, 0.44),
        scale=(0.124, 0.124, 0.124),
        material=neutral_dark,
    )
    _add_text(
        bpy,
        "DepthStereoRole",
        "Stereo enriches, motion reinforces, essential meaning stays readable without stereopsis",
        location=(0.0, 1.2, 0.33),
        scale=(0.102, 0.102, 0.102),
        material=neutral_dark,
    )
    _add_text(
        bpy,
        "LegendStatic",
        "Static cues carry the shared spatial meaning",
        location=(0.0, -3.2, 0.28),
        scale=(0.12, 0.12, 0.12),
        material=text_dark,
    )
    _add_text(
        bpy,
        "LegendStereo",
        "Stereo is optional enrichment, not the only path",
        location=(0.0, -3.42, 0.22),
        scale=(0.1, 0.1, 0.1),
        material=neutral_dark,
    )
    _add_text(
        bpy,
        "LegendMotion",
        "Motion helps, but labels, scale, shadows, and anchors stay primary",
        location=(0.0, -3.63, 0.18),
        scale=(0.092, 0.092, 0.092),
        material=neutral_dark,
    )

    bpy.context.view_layer.update()


def main() -> int:
    args = parse_args(_blender_args())
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))

    try:
        import bpy
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(f"This script must be run inside Blender: {exc}") from exc

    build_scene(bpy, spec, render_engine=args.engine)
    bpy.context.scene.render.filepath = str(Path(args.output))
    bpy.ops.render.render(write_still=True)
    if args.blend_output:
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(args.blend_output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
