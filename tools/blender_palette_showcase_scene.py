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
    _add_box(
        bpy,
        "HeaderBand",
        location=(0.0, 2.08, 0.88),
        scale=(3.18, 0.038, 0.76),
        material=plaque_mat,
        bevel=0.03,
    )
    _add_box(
        bpy,
        "DepthLegendPlaque",
        location=(0.0, -2.42, 0.14),
        scale=(3.35, 0.68, 0.09),
        material=plaque_mat,
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
    camera.location = (0.0, -12.15, 6.08)
    camera.rotation_euler = (math.radians(57.8), 0.0, 0.0)
    camera.data.lens = 35

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
    for connector_x in (-lane_spacing, 0.0, lane_spacing):
        _add_depth_strip(
            bpy,
            f"PlaqueConnector_{connector_x:+.2f}",
            location=(connector_x, -1.82, -0.02),
            scale=(0.55, 0.025, 0.014),
            material=rail_mid,
        )
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
    research_source_count = _bounded_count(metrics.get("source_cache_doc_count", 5), 4, 7)
    validation_input_count = _bounded_count(metrics.get("primary_source_notes_count", 5), 4, 7)
    validation_gate_count = _bounded_count(metrics.get("source_cache_doc_count", 3), 3, 5)
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
            scale=(1.34, 0.46, 0.024),
            material=plaque_mat,
            bevel=0.03,
        )
        _add_box(
            bpy,
            f"{lane_id}_label_beacon",
            location=(x - 0.92, -1.78, 0.37),
            scale=(0.09, 0.09, 0.03),
            material=primary_mat,
            bevel=0.02,
        )

        if lane_id == "production-indigo-magenta":
            source_offsets = []
            spacing = 0.4
            half_span = (research_source_count - 1) * spacing / 2.0
            for source_index in range(research_source_count):
                source_offsets.append(-half_span + source_index * spacing)
            for source_index, source_offset in enumerate(source_offsets):
                tile = _add_box(
                    bpy,
                    f"{lane_id}_source_tile_{source_index}",
                    location=(x + source_offset, 1.28 + (source_index % 2) * 0.12, 0.56 + (source_index % 3) * 0.03),
                    scale=(0.22, 0.16, 0.03),
                    material=marker_materials[source_index % len(marker_materials)],
                    bevel=0.022,
                )
                tile.rotation_euler.z = math.radians(-13.0 + source_index * 4.0)
                feeder = _add_box(
                    bpy,
                    f"{lane_id}_feeder_{source_index}",
                    location=(x + source_offset * 0.58, 0.92, 0.5),
                    scale=(0.025, 0.32, 0.018),
                    material=border_mat,
                    bevel=0.012,
                )
                feeder.rotation_euler.z = math.radians(source_offset * -7.5)
            _add_box(
                bpy,
                f"{lane_id}_synthesis_back",
                location=(x - 0.18, 0.42, 0.44),
                scale=(1.0, 0.3, 0.08),
                material=primary_mat,
                bevel=0.04,
            )
            _add_box(
                bpy,
                f"{lane_id}_synthesis_mid",
                location=(x, 0.62, 0.58),
                scale=(0.92, 0.28, 0.075),
                material=accent_mat,
                bevel=0.04,
            )
            _add_box(
                bpy,
                f"{lane_id}_synthesis_front",
                location=(x + 0.16, 0.82, 0.72),
                scale=(0.82, 0.25, 0.07),
                material=tertiary_mat,
                bevel=0.04,
            )
            _add_box(
                bpy,
                f"{lane_id}_synthesis_spine",
                location=(x - 0.58, 0.62, 0.68),
                scale=(0.055, 0.24, 0.22),
                material=border_mat,
                bevel=0.02,
            )
            _add_box(
                bpy,
                f"{lane_id}_summary_plate",
                location=(x, -0.22, 0.4),
                scale=(1.04, 0.18, 0.06),
                material=plaque_mat,
                bevel=0.03,
            )
            for tab_index, tab_x in enumerate((-0.34, 0.0, 0.34)):
                _add_box(
                    bpy,
                    f"{lane_id}_summary_tab_{tab_index}",
                    location=(x + tab_x, -0.08, 0.48),
                    scale=(0.12, 0.06, 0.03),
                    material=marker_materials[tab_index],
                    bevel=0.015,
                )
        elif lane_id == "accessible-mauve-burgundy":
            queue_offsets = []
            intake_spacing = 0.34
            queue_half = (validation_input_count - 1) * intake_spacing / 2.0
            for queue_index in range(validation_input_count):
                queue_offsets.append(-queue_half + queue_index * intake_spacing)
            for queue_index, queue_offset in enumerate(queue_offsets):
                intake_tile = _add_box(
                    bpy,
                    f"{lane_id}_intake_tile_{queue_index}",
                    location=(x + queue_offset, 1.18, 0.55 + (queue_index % 2) * 0.035),
                    scale=(0.18, 0.12, 0.028),
                    material=marker_materials[queue_index % len(marker_materials)],
                    bevel=0.018,
                )
                intake_tile.rotation_euler.z = math.radians(-9.0 + queue_index * 3.0)
            _add_box(
                bpy,
                f"{lane_id}_intake_belt",
                location=(x, 0.9, 0.45),
                scale=(1.05, 0.05, 0.03),
                material=border_mat,
                bevel=0.014,
            )
            gate_spacing = 0.54
            gate_half = (validation_gate_count - 1) * gate_spacing / 2.0
            for gate_index in range(validation_gate_count):
                gate_x = -gate_half + gate_index * gate_spacing
                gate_mat = (primary_mat, accent_mat, tertiary_mat, primary_mat, accent_mat)[gate_index]
                _add_box(
                    bpy,
                    f"{lane_id}_gate_post_l_{gate_index}",
                    location=(x + gate_x - 0.13, 0.34, 0.56),
                    scale=(0.05, 0.14, 0.32),
                    material=gate_mat,
                    bevel=0.02,
                )
                _add_box(
                    bpy,
                    f"{lane_id}_gate_post_r_{gate_index}",
                    location=(x + gate_x + 0.13, 0.34, 0.56),
                    scale=(0.05, 0.14, 0.32),
                    material=gate_mat,
                    bevel=0.02,
                )
                _add_box(
                    bpy,
                    f"{lane_id}_gate_bar_{gate_index}",
                    location=(x + gate_x, 0.34, 0.83),
                    scale=(0.18, 0.14, 0.05),
                    material=gate_mat,
                    bevel=0.02,
                )
            _add_box(
                bpy,
                f"{lane_id}_accepted_channel",
                location=(x - 0.18, -0.1, 0.44),
                scale=(0.86, 0.05, 0.028),
                material=accent_mat,
                bevel=0.012,
            )
            _add_box(
                bpy,
                f"{lane_id}_accepted_arrow_stem",
                location=(x - 0.18, -0.18, 0.51),
                scale=(0.08, 0.02, 0.018),
                material=accent_mat,
                bevel=0.01,
            )
            _add_box(
                bpy,
                f"{lane_id}_accepted_arrow_head",
                location=(x + 0.04, -0.18, 0.51),
                scale=(0.03, 0.06, 0.018),
                material=accent_mat,
                bevel=0.01,
            ).rotation_euler.z = math.radians(45.0)
            approved_panel = _add_box(
                bpy,
                f"{lane_id}_approved_panel",
                location=(x - 0.18, -0.34, 0.54),
                scale=(0.58, 0.22, 0.09),
                material=plaque_mat,
                bevel=0.03,
            )
            approved_panel.rotation_euler.z = math.radians(-4.0)
            _add_box(
                bpy,
                f"{lane_id}_approved_seal",
                location=(x - 0.18, -0.34, 0.64),
                scale=(0.11, 0.11, 0.035),
                material=primary_mat,
                bevel=0.018,
            )
            _add_box(
                bpy,
                f"{lane_id}_reject_chute",
                location=(x + 0.66, 0.05, 0.46),
                scale=(0.04, 0.34, 0.018),
                material=neutral_dark,
                bevel=0.012,
            ).rotation_euler.z = math.radians(-28.0)
            for reject_index, reject_y in enumerate((0.1, -0.12, -0.34)):
                reject_tile = _add_box(
                    bpy,
                    f"{lane_id}_reject_tile_{reject_index}",
                    location=(x + 0.92 + reject_index * 0.08, reject_y, 0.36),
                    scale=(0.14, 0.09, 0.028),
                    material=neutral_dark,
                    bevel=0.015,
                )
                reject_tile.rotation_euler.z = math.radians(18.0 - reject_index * 7.0)
        else:
            source_mat = _ensure_material(
                bpy, f"{lane_id}_source", brand["border"], roughness=0.3
            )
            connector_mat = _ensure_material(
                bpy, f"{lane_id}_connector", brand["focusRing"], roughness=0.42
            )
            _add_box(
                bpy,
                f"{lane_id}_source_panel",
                location=(x, 0.72, 0.86),
                scale=(1.14, 0.26, 0.075),
                material=source_mat,
                bevel=0.035,
            )
            _add_box(
                bpy,
                f"{lane_id}_source_inset",
                location=(x, 0.76, 0.95),
                scale=(0.88, 0.12, 0.02),
                material=plaque_mat,
                bevel=0.018,
            )
            for tab_index, tab_x in enumerate((-0.32, 0.0, 0.32)):
                _add_box(
                    bpy,
                    f"{lane_id}_source_tab_{tab_index}",
                    location=(x + tab_x, 0.9, 1.0),
                    scale=(0.1, 0.05, 0.022),
                    material=(primary_mat, accent_mat, tertiary_mat)[tab_index],
                    bevel=0.012,
                )
            _add_box(
                bpy,
                f"{lane_id}_spine",
                location=(x, 0.36, 0.68),
                scale=(0.06, 0.05, 0.26),
                material=connector_mat,
                bevel=0.02,
            )
            _add_box(
                bpy,
                f"{lane_id}_fan_bar",
                location=(x, 0.12, 0.58),
                scale=(0.98, 0.05, 0.03),
                material=connector_mat,
                bevel=0.02,
            )
            output_specs = (
                ("contrast", -0.72, primary_mat, "#FBF6F1"),
                ("guided", 0.0, accent_mat, brand["surface"]),
                ("depth_safe", 0.72, tertiary_mat, "#FBF6F1"),
            )
            for output_name, x_shift, body_mat, inset_hex in output_specs:
                branch = _add_box(
                    bpy,
                    f"{lane_id}_{output_name}_branch",
                    location=(x + x_shift * 0.48, 0.0, 0.56),
                    scale=(0.03, 0.24, 0.018),
                    material=connector_mat,
                    bevel=0.012,
                )
                if x_shift != 0.0:
                    branch.rotation_euler.z = math.radians(-23.0 if x_shift > 0 else 23.0)
                inset_mat = _ensure_material(
                    bpy,
                    f"{lane_id}_{output_name}_inset",
                    inset_hex,
                    roughness=0.5,
                )
                _add_box(
                    bpy,
                    f"{lane_id}_{output_name}_connector",
                    location=(x + x_shift, -0.08, 0.5),
                    scale=(0.05, 0.05, 0.18),
                    material=connector_mat,
                    bevel=0.018,
                )
                _add_box(
                    bpy,
                    f"{lane_id}_{output_name}_panel",
                    location=(x + x_shift, -0.42, 0.45),
                    scale=(0.62, 0.32, 0.11),
                    material=body_mat,
                    bevel=0.03,
                )
                _add_box(
                    bpy,
                    f"{lane_id}_{output_name}_inset_obj",
                    location=(x + x_shift, -0.37, 0.54),
                    scale=(0.46, 0.18, 0.024),
                    material=inset_mat,
                    bevel=0.015,
                )
                if output_name == "contrast":
                    _add_box(
                        bpy,
                        f"{lane_id}_{output_name}_frame_left",
                        location=(x + x_shift - 0.18, -0.42, 0.6),
                        scale=(0.045, 0.22, 0.07),
                        material=source_mat,
                        bevel=0.014,
                    )
                    _add_box(
                        bpy,
                        f"{lane_id}_{output_name}_frame_right",
                        location=(x + x_shift + 0.18, -0.42, 0.6),
                        scale=(0.045, 0.22, 0.07),
                        material=plaque_mat,
                        bevel=0.014,
                    )
                elif output_name == "guided":
                    _add_box(
                        bpy,
                        f"{lane_id}_{output_name}_path_stem",
                        location=(x + x_shift - 0.18, -0.42, 0.61),
                        scale=(0.035, 0.035, 0.11),
                        material=accent_mat,
                        bevel=0.012,
                    )
                    _add_box(
                        bpy,
                        f"{lane_id}_{output_name}_path_arm",
                        location=(x + x_shift, -0.2, 0.68),
                        scale=(0.22, 0.03, 0.022),
                        material=accent_mat,
                        bevel=0.012,
                    )
                    _add_box(
                        bpy,
                        f"{lane_id}_{output_name}_path_tip",
                        location=(x + x_shift + 0.24, -0.2, 0.68),
                        scale=(0.035, 0.035, 0.022),
                        material=accent_mat,
                        bevel=0.012,
                    )
                    bpy.context.active_object.rotation_euler.z = math.radians(45.0)
                else:
                    for ridge_index, ridge_x in enumerate((-0.15, 0.0, 0.15)):
                        _add_box(
                            bpy,
                            f"{lane_id}_{output_name}_ridge_{ridge_index}",
                            location=(x + x_shift + ridge_x, -0.46 + ridge_index * 0.03, 0.62 - ridge_index * 0.035),
                            scale=(0.05, 0.2, 0.04 + ridge_index * 0.02),
                            material=tertiary_mat,
                            bevel=0.012,
                        )
            _add_box(
                bpy,
                f"{lane_id}_contrast_dark_zone",
                location=(x - 0.82, -0.4, 0.57),
                scale=(0.12, 0.15, 0.018),
                material=source_mat,
                bevel=0.012,
            )
            _add_box(
                bpy,
                f"{lane_id}_contrast_light_zone",
                location=(x - 0.56, -0.4, 0.57),
                scale=(0.12, 0.15, 0.018),
                material=plaque_mat,
                bevel=0.012,
            )
            for icon_index, icon_x in enumerate((-0.78, 0.0, 0.78)):
                _add_box(
                    bpy,
                    f"{lane_id}_output_badge_{icon_index}",
                    location=(x + icon_x, -0.76, 0.64),
                    scale=(0.08, 0.08, 0.034),
                    material=(primary_mat, accent_mat, tertiary_mat)[icon_index],
                    bevel=0.018,
                )
            for cue_index, cue_x in enumerate((-0.65, -0.47)):
                _add_box(
                    bpy,
                    f"{lane_id}_contrast_cue_{cue_index}",
                    location=(x + cue_x - 0.1, -0.34, 0.66),
                    scale=(0.05, 0.14, 0.06),
                    material=source_mat if cue_index == 0 else primary_mat,
                    bevel=0.012,
                )
            _add_box(
                bpy,
                f"{lane_id}_contrast_bar_top",
                location=(x - 0.7, -0.54, 0.67),
                scale=(0.2, 0.03, 0.02),
                material=primary_mat,
                bevel=0.01,
            )
            _add_box(
                bpy,
                f"{lane_id}_contrast_bar_bottom",
                location=(x - 0.7, -0.26, 0.67),
                scale=(0.2, 0.03, 0.02),
                material=source_mat,
                bevel=0.01,
            )
            _add_box(
                bpy,
                f"{lane_id}_guided_path",
                location=(x, -0.3, 0.6),
                scale=(0.16, 0.02, 0.014),
                material=accent_mat,
                bevel=0.01,
            )
            _add_box(
                bpy,
                f"{lane_id}_guided_tip",
                location=(x + 0.18, -0.3, 0.6),
                scale=(0.035, 0.035, 0.014),
                material=accent_mat,
                bevel=0.01,
            )
            bpy.context.active_object.rotation_euler.z = math.radians(45.0)
            for cue_index, cue_x in enumerate((-0.12, 0.0, 0.12)):
                _add_marker(
                    bpy,
                    f"{lane_id}_guided_cue_{cue_index}",
                    ("circle", "triangle", "square")[cue_index],
                    location=(x + cue_x, -0.3, 0.67),
                    size=0.22,
                    material=(accent_mat, primary_mat, tertiary_mat)[cue_index],
                )
            _add_box(
                bpy,
                f"{lane_id}_depth_contour",
                location=(x + 0.72, -0.56, 0.67),
                scale=(0.22, 0.025, 0.018),
                material=tertiary_mat,
                bevel=0.01,
            )
            for step_index, step_x in enumerate((0.54, 0.72, 0.9)):
                _add_box(
                    bpy,
                    f"{lane_id}_depth_step_{step_index}",
                    location=(x + step_x, -0.34 + step_index * 0.06, 0.66 - step_index * 0.05),
                    scale=(0.065, 0.1, 0.04 + step_index * 0.015),
                    material=tertiary_mat,
                    bevel=0.012,
                )

        _add_text(
            bpy,
            f"{lane_id}_title",
            lane["label"],
            location=(x, -1.82, 0.44),
            scale=(0.26, 0.26, 0.26),
            material=label_mat,
        )

        if lane_id != "atmosphere-red-mahogany":
            marker_x_offsets = (-0.75, -0.25, 0.25, 0.75)
            for marker_index, marker_name in enumerate(viz["markers"][:4]):
                _add_marker(
                    bpy,
                    f"{lane_id}_marker_{marker_index}",
                    marker_name,
                    location=(x + marker_x_offsets[marker_index], 1.64, 0.36),
                    size=0.34,
                    material=marker_materials[marker_index],
                )


    _add_text(
        bpy,
        "ShowcaseHeader",
        concept.get("scene_header", "OpenPerception accessibility system"),
        location=(0.0, 1.96, 0.82),
        scale=(0.32, 0.32, 0.32),
        material=text_dark,
    )
    _add_text(
        bpy,
        "LegendStatic",
        concept.get("plaque_text", "same source, adapted views"),
        location=(0.0, -2.36, 0.24),
        scale=(0.2, 0.2, 0.2),
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
