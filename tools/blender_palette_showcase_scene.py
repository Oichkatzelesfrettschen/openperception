#!/usr/bin/env python3
"""
Build and render the OpenPerception living concept scene inside Blender.

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


def _bounded_count(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))


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
    scene.view_settings.exposure = 0.9
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
    world_bg.inputs["Color"].default_value = _hex_to_rgba("#FBF7F1")
    world_bg.inputs["Strength"].default_value = 1.62
    world_links.new(world_bg.outputs["Background"], world_output.inputs["Surface"])

    floor_mat = _ensure_material(bpy, "Floor", "#D8CEC4", roughness=0.96)
    wall_mat = _ensure_material(bpy, "BackdropWall", "#FBF5EE", roughness=0.94)
    plaque_mat = _ensure_material(bpy, "DepthLegendPlaque", "#F1EAE3", roughness=0.84)
    rail_near = _ensure_material(bpy, "DepthRailNear", "#8F847B", roughness=0.84)
    rail_mid = _ensure_material(bpy, "DepthRailMid", "#B6AAA1", roughness=0.88)
    rail_far = _ensure_material(bpy, "DepthRailFar", "#D9D0C8", roughness=0.9)
    text_dark = _ensure_material(bpy, "TextDark", "#111827", roughness=0.55)
    text_warm = _ensure_material(bpy, "TextWarm", "#2A2321", roughness=0.55)
    neutral_dark = _ensure_material(bpy, "NeutralDark", "#2E3440", roughness=0.55)

    bpy.ops.mesh.primitive_plane_add(size=36, location=(0.0, 0.0, -0.35))
    floor = bpy.context.active_object
    floor.name = "Floor"
    _assign_material(floor, floor_mat)
    _add_box(
        bpy,
        "BackdropWall",
        location=(0.0, 2.36, 1.16),
        scale=(8.8, 0.08, 1.22),
        material=wall_mat,
        bevel=0.02,
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
    camera.location = (0.0, -11.5, 5.98)
    camera.rotation_euler = (math.radians(57.8), 0.0, 0.0)
    camera.data.lens = 37

    key_energy = 1000.0 if selected_engine == "octane" else 5600.0
    rim_energy = 420.0 if selected_engine == "octane" else 2850.0
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
    lane_spacing = 4.25
    start_x = -lane_spacing
    for flow_x in (-2.08, 2.08):
        _add_depth_strip(
            bpy,
            f"LaneFlow_{flow_x:+.2f}",
            location=(flow_x, -0.58, 0.0),
            scale=(0.72, 0.022, 0.018),
            material=rail_near,
        )
    concept = spec.get("concept", {})
    metrics = spec.get("repo_stats", {}).get("metrics", {})
    verified_source_count = _bounded_count(metrics.get("source_cache_doc_count", 5), 4, 7)
    verified_note_count = _bounded_count(metrics.get("primary_source_notes_count", 5), 4, 7)
    verified_gate_count = _bounded_count(metrics.get("source_cache_doc_count", 3), 3, 5)
    source_surface = _ensure_material(bpy, "VerifiedSourceSurface", "#F6F0E8", roughness=0.62)
    source_border = _ensure_material(bpy, "VerifiedSourceBorder", "#C5B8AA", roughness=0.7)
    source_primary = _ensure_material(bpy, "VerifiedSourcePrimary", "#3730A3", roughness=0.38)
    source_accent = _ensure_material(bpy, "VerifiedSourceAccent", "#901C32", roughness=0.38)
    source_focus = _ensure_material(bpy, "VerifiedSourceFocus", "#B45309", roughness=0.38)
    source_dark = _ensure_material(bpy, "VerifiedSourceDark", "#111827", roughness=0.44)
    _add_box(
        bpy,
        "VerifiedSourceDeck",
        location=(0.0, 1.1, 0.17),
        scale=(1.95, 0.42, 0.07),
        material=source_surface,
        bevel=0.03,
    )
    source_offsets = []
    source_spacing = 0.42
    source_half = (verified_source_count - 1) * source_spacing / 2.0
    for source_index in range(verified_source_count):
        source_offsets.append(-source_half + source_index * source_spacing)
    for source_index, source_offset in enumerate(source_offsets):
        tile = _add_box(
            bpy,
            f"VerifiedSourceTile_{source_index}",
            location=(source_offset * 0.88, 1.34 + (source_index % 2) * 0.05, 0.31 + (source_index % 3) * 0.02),
            scale=(0.13, 0.09, 0.018),
            material=(source_primary, source_accent, source_focus, source_dark)[source_index % 4],
            bevel=0.012,
        )
        tile.rotation_euler.z = math.radians(-10.0 + source_index * 4.0)
        feeder = _add_box(
            bpy,
            f"VerifiedSourceFeeder_{source_index}",
            location=(source_offset * 0.34, 1.22, 0.24),
            scale=(0.014, 0.14, 0.008),
            material=source_border,
            bevel=0.008,
        )
        feeder.rotation_euler.z = math.radians(source_offset * -8.0)
    note_offsets = []
    note_spacing = 0.32
    note_half = (verified_note_count - 1) * note_spacing / 2.0
    for note_index in range(verified_note_count):
        note_offsets.append(-note_half + note_index * note_spacing)
    for note_index, note_offset in enumerate(note_offsets):
        note_tile = _add_box(
            bpy,
            f"VerifiedNote_{note_index}",
            location=(note_offset * 0.82, 0.98, 0.25 + (note_index % 2) * 0.015),
            scale=(0.09, 0.05, 0.014),
            material=source_border if note_index % 2 == 0 else plaque_mat,
            bevel=0.008,
        )
        note_tile.rotation_euler.z = math.radians(-6.0 + note_index * 2.0)
    gate_spacing = 0.54
    gate_half = (verified_gate_count - 1) * gate_spacing / 2.0
    for gate_index in range(verified_gate_count):
        gate_x = -gate_half + gate_index * gate_spacing
        gate_mat = (source_primary, source_accent, source_focus, source_primary, source_accent)[gate_index]
        _add_box(
            bpy,
            f"VerifiedGatePostL_{gate_index}",
            location=(gate_x * 0.82 - 0.07, 0.78, 0.28),
            scale=(0.028, 0.06, 0.14),
            material=gate_mat,
            bevel=0.01,
        )
        _add_box(
            bpy,
            f"VerifiedGatePostR_{gate_index}",
            location=(gate_x * 0.82 + 0.07, 0.78, 0.28),
            scale=(0.028, 0.06, 0.14),
            material=gate_mat,
            bevel=0.01,
        )
        _add_box(
            bpy,
            f"VerifiedGateBar_{gate_index}",
            location=(gate_x * 0.82, 0.78, 0.39),
            scale=(0.09, 0.06, 0.022),
            material=gate_mat,
            bevel=0.01,
        )
    _add_box(
        bpy,
        "VerifiedSourcePanel",
        location=(0.0, 0.48, 0.34),
        scale=(0.66, 0.12, 0.035),
        material=source_surface,
        bevel=0.02,
    )
    _add_box(
        bpy,
        "VerifiedSourceInset",
        location=(0.0, 0.5, 0.38),
        scale=(0.38, 0.05, 0.01),
        material=plaque_mat,
        bevel=0.008,
    )
    for tab_index, tab_x in enumerate((-0.28, 0.0, 0.28)):
        _add_box(
            bpy,
            f"VerifiedSourceTab_{tab_index}",
            location=(tab_x * 0.62, 0.58, 0.4),
            scale=(0.04, 0.018, 0.008),
            material=(source_primary, source_accent, source_focus)[tab_index],
            bevel=0.006,
        )
    _add_box(
        bpy,
        "VerifiedSourceSpine",
        location=(0.0, 0.12, 0.22),
        scale=(0.03, 0.025, 0.08),
        material=source_dark,
        bevel=0.008,
    )
    _add_box(
        bpy,
        "VerifiedSourceBranchBar",
        location=(0.0, -0.02, 0.2),
        scale=(2.15, 0.022, 0.009),
        material=source_focus,
        bevel=0.007,
    )
    for index, lane in enumerate(spec["lanes"]):
        x = start_x + index * lane_spacing
        brand = lane["brand"]
        viz = lane["viz"]
        lane_id = lane["scheme_id"]
        surface_mat = _ensure_material(
            bpy, f"{lane_id}_surface", brand["surface"], roughness=0.64
        )
        border_mat = _ensure_material(
            bpy, f"{lane_id}_border", brand["border"], roughness=0.68
        )
        primary_mat = _ensure_material(
            bpy, f"{lane_id}_primary", brand["primaryStrong"], roughness=0.38
        )
        accent_mat = _ensure_material(
            bpy, f"{lane_id}_accent", brand["accentStrong"], roughness=0.38
        )
        tertiary_color = brand["tertiaryStrong"] or brand["focusRing"]
        tertiary_mat = _ensure_material(
            bpy, f"{lane_id}_tertiary", tertiary_color, roughness=0.38
        )
        marker_materials = [
            _ensure_material(bpy, f"{lane_id}_marker_{i}", color, roughness=0.34)
            for i, color in enumerate(viz["categorical"][:4])
        ]
        label_mat = text_warm if lane_id == "atmosphere-red-mahogany" else text_dark
        weak_primary_mat = _ensure_material(
            bpy, f"{lane_id}_weak_primary", brand["primary"], roughness=0.62
        )
        weak_accent_mat = _ensure_material(
            bpy, f"{lane_id}_weak_accent", brand["accent"], roughness=0.62
        )
        weak_tertiary_mat = _ensure_material(
            bpy,
            f"{lane_id}_weak_tertiary",
            brand.get("tertiary") or brand["surface"],
            roughness=0.64,
        )

        _add_box(
            bpy,
            f"{lane_id}_card",
            location=(x, 0.0, 0.15),
            scale=(1.65, 2.25, 0.18),
            material=surface_mat,
            bevel=0.08,
        )
        _add_box(
            bpy,
            f"{lane_id}_outline",
            location=(x, 0.0, -0.04),
            scale=(1.74, 2.34, 0.04),
            material=border_mat,
            bevel=0.05,
        )
        _add_box(
            bpy,
            f"{lane_id}_label_band",
            location=(x, -1.88, 0.34),
            scale=(1.04, 0.32, 0.018),
            material=plaque_mat,
            bevel=0.02,
        )
        _add_box(
            bpy,
            f"{lane_id}_label_beacon",
            location=(x - 0.72, -1.79, 0.37),
            scale=(0.055, 0.055, 0.02),
            material=primary_mat,
            bevel=0.012,
        )

        connector_mat = _ensure_material(
            bpy, f"{lane_id}_connector", brand["focusRing"], roughness=0.42
        )
        _add_box(
            bpy,
            f"{lane_id}_branch_connector",
            location=(x * 0.43, -0.16, 0.22),
            scale=(0.026, 0.22, 0.012),
            material=connector_mat,
            bevel=0.01,
        ).rotation_euler.z = math.radians(-18.0 if x > 0 else 18.0)
        _add_box(
            bpy,
            f"{lane_id}_output_panel",
            location=(x, 0.16, 0.54),
            scale=(1.14, 0.58, 0.13),
            material=primary_mat,
            bevel=0.04,
        )
        _add_box(
            bpy,
            f"{lane_id}_output_inset",
            location=(x + 0.03, 0.24, 0.66),
            scale=(0.98, 0.38, 0.03),
            material=plaque_mat,
            bevel=0.015,
        )
        _add_box(
            bpy,
            f"{lane_id}_source_fragment_pad",
            location=(x - 0.44, 0.24, 0.69),
            scale=(0.1, 0.14, 0.01),
            material=surface_mat,
            bevel=0.008,
        )
        _add_box(
            bpy,
            f"{lane_id}_transformed_fragment_pad",
            location=(x + 0.14, 0.24, 0.69),
            scale=(0.66, 0.28, 0.02),
            material=plaque_mat,
            bevel=0.012,
        )
        _add_box(
            bpy,
            f"{lane_id}_panel_arrow_stem",
            location=(x - 0.06, 0.24, 0.7),
            scale=(0.14, 0.014, 0.008),
            material=connector_mat,
            bevel=0.006,
        )
        _add_box(
            bpy,
            f"{lane_id}_panel_arrow_head",
            location=(x + 0.07, 0.24, 0.7),
            scale=(0.03, 0.03, 0.008),
            material=connector_mat,
            bevel=0.006,
        ).rotation_euler.z = math.radians(45.0)
        if lane["label"] == "Color-safe":
            for source_index, source_x in enumerate((-0.49, -0.44, -0.39)):
                _add_box(
                    bpy,
                    f"{lane_id}_source_color_only_{source_index}",
                    location=(x + source_x, 0.24, 0.73),
                    scale=(0.014, 0.08, 0.008),
                    material=(weak_primary_mat, weak_accent_mat, weak_tertiary_mat)[source_index],
                    bevel=0.004,
                )
            _add_box(
                bpy,
                f"{lane_id}_transform_frame",
                location=(x + 0.16, 0.24, 0.72),
                scale=(0.69, 0.3, 0.018),
                material=neutral_dark,
                bevel=0.012,
            )
            for split_name, split_x, split_mat in (
                ("dark", -0.07, neutral_dark),
                ("mid", 0.16, accent_mat),
                ("light", 0.39, plaque_mat),
            ):
                _add_box(
                    bpy,
                    f"{lane_id}_{split_name}_split",
                    location=(x + split_x, 0.24, 0.73),
                    scale=(0.115, 0.24, 0.016),
                    material=split_mat,
                    bevel=0.01,
                )
            for stripe_index, stripe_y in enumerate((-0.07, 0.0, 0.07)):
                _add_box(
                    bpy,
                    f"{lane_id}_stripe_{stripe_index}",
                    location=(x + 0.16, 0.24 + stripe_y, 0.775),
                    scale=(0.36, 0.024, 0.012),
                    material=primary_mat if stripe_index % 2 == 0 else source_dark,
                    bevel=0.008,
                )
            for marker_index, marker_x in enumerate((-0.02, 0.16, 0.34)):
                _add_marker(
                    bpy,
                    f"{lane_id}_cue_marker_{marker_index}",
                    ("circle", "triangle", "square")[marker_index],
                    location=(x + marker_x, 0.04, 0.82),
                    size=0.26,
                    material=(primary_mat, accent_mat, tertiary_mat)[marker_index],
                )
        elif lane["label"] == "Symbol-guided":
            for source_index, source_x in enumerate((-0.49, -0.42, -0.35)):
                _add_box(
                    bpy,
                    f"{lane_id}_source_block_{source_index}",
                    location=(x + source_x, 0.24 - source_index * 0.015, 0.73),
                    scale=(0.018, 0.04, 0.006),
                    material=border_mat,
                    bevel=0.004,
                )
            _add_box(
                bpy,
                f"{lane_id}_route_stem",
                location=(x - 0.06, 0.06, 0.75),
                scale=(0.05, 0.05, 0.16),
                material=accent_mat,
                bevel=0.012,
            )
            _add_box(
                bpy,
                f"{lane_id}_route_path",
                location=(x + 0.16, 0.24, 0.82),
                scale=(0.42, 0.028, 0.014),
                material=accent_mat,
                bevel=0.01,
            )
            _add_box(
                bpy,
                f"{lane_id}_route_tip",
                location=(x + 0.6, 0.24, 0.82),
                scale=(0.06, 0.06, 0.014),
                material=accent_mat,
                bevel=0.01,
            ).rotation_euler.z = math.radians(45.0)
            for cue_index, cue_x in enumerate((-0.02, 0.2, 0.42)):
                _add_marker(
                    bpy,
                    f"{lane_id}_guided_marker_{cue_index}",
                    ("diamond", "circle", "square")[cue_index],
                    location=(x + cue_x, 0.04, 0.8),
                    size=0.24,
                    material=(accent_mat, primary_mat, tertiary_mat)[cue_index],
                )
            _add_box(
                bpy,
                f"{lane_id}_guide_plate",
                location=(x + 0.16, -0.02, 0.74),
                scale=(0.34, 0.065, 0.014),
                material=tertiary_mat,
                bevel=0.01,
            )
        else:
            _add_box(
                bpy,
                f"{lane_id}_source_flat_front",
                location=(x - 0.41, 0.18, 0.72),
                scale=(0.045, 0.08, 0.008),
                material=border_mat,
                bevel=0.004,
            )
            _add_box(
                bpy,
                f"{lane_id}_source_flat_back",
                location=(x - 0.37, 0.24, 0.71),
                scale=(0.045, 0.08, 0.008),
                material=surface_mat,
                bevel=0.004,
            )
            for ridge_index, ridge_x in enumerate((-0.02, 0.26, 0.54)):
                _add_box(
                    bpy,
                    f"{lane_id}_ridge_{ridge_index}",
                    location=(x + ridge_x, 0.16 + ridge_index * 0.055, 0.75 - ridge_index * 0.055),
                    scale=(0.07, 0.22, 0.05 + ridge_index * 0.028),
                    material=tertiary_mat,
                    bevel=0.012,
                )
            _add_box(
                bpy,
                f"{lane_id}_contour_strip",
                location=(x + 0.2, -0.02, 0.84),
                scale=(0.4, 0.032, 0.014),
                material=tertiary_mat,
                bevel=0.01,
            )
            for anchor_index, anchor_x in enumerate((-0.02, 0.56)):
                _add_box(
                    bpy,
                    f"{lane_id}_anchor_{anchor_index}",
                    location=(x + anchor_x, 0.28, 0.79),
                    scale=(0.05, 0.07, 0.17),
                    material=source_dark if anchor_index == 0 else plaque_mat,
                    bevel=0.01,
                )
            _add_box(
                bpy,
                f"{lane_id}_ground_shadow_bar",
                location=(x + 0.2, -0.08, 0.72),
                scale=(0.36, 0.032, 0.012),
                material=neutral_dark,
                bevel=0.01,
            )

        _add_text(
            bpy,
            f"{lane_id}_title",
            lane["label"],
            location=(x, -1.82, 0.44),
            scale=(0.18, 0.18, 0.18),
            material=label_mat,
        )

    scene_header = concept.get("scene_header", "")
    if scene_header:
        _add_text(
            bpy,
            "ShowcaseHeader",
            scene_header,
            location=(0.0, 1.96, 0.82),
            scale=(0.19, 0.19, 0.19),
            material=text_dark,
        )
    plaque_text = concept.get("plaque_text", "")
    if plaque_text:
        _add_text(
            bpy,
            "LegendStatic",
            plaque_text,
            location=(0.0, -2.36, 0.24),
            scale=(0.11, 0.11, 0.11),
            material=text_dark,
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
