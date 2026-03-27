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


def _load_image(bpy, image_path: str):
    resolved = str(Path(image_path).resolve())
    for image in bpy.data.images:
        if image.filepath and Path(image.filepath).resolve() == Path(resolved):
            return image
    return bpy.data.images.load(resolved, check_existing=True)


def _configure_octane_image_node(bpy, node, image):
    if hasattr(node, "image"):
        node.image = image
    filepath = image.filepath_from_user() if hasattr(image, "filepath_from_user") else ""
    if filepath:
        if hasattr(node, "a_filename"):
            node.a_filename = filepath
        if hasattr(node, "a_reload"):
            node.a_reload = True
    if hasattr(node, "update_image"):
        try:
            node.update_image(bpy.context)
        except Exception:
            pass
    if hasattr(node, "update_node_tree"):
        try:
            node.update_node_tree(bpy.context)
        except Exception:
            pass


def _ensure_image_material(bpy, name: str, image_path: str):
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    image = _load_image(bpy, image_path)
    if bpy.context.scene.render.engine == "octane":
        diffuse = nodes.new("OctaneDiffuseMaterial")
        diffuse.location = (420, 0)
        if "Diffuse" in diffuse.inputs:
            diffuse.inputs["Diffuse"].default_value = (0.0, 0.0, 0.0)
        emission = nodes.new("OctaneTextureEmission")
        emission.location = (120, -80)
        if "Power" in emission.inputs:
            emission.inputs["Power"].default_value = 1.0
        if "Surface brightness" in emission.inputs:
            emission.inputs["Surface brightness"].default_value = True
        tex = nodes.new("OctaneRGBImage")
        tex.location = (-180, -80)
        _configure_octane_image_node(bpy, tex, image)
        links.new(tex.outputs[0], emission.inputs["Texture"])
        links.new(emission.outputs[0], diffuse.inputs["Emission"])
        links.new(diffuse.outputs[0], output.inputs["Surface"])
    else:
        tex = nodes.new("ShaderNodeTexImage")
        tex.location = (-320, 0)
        tex.image = image
        emission = nodes.new("ShaderNodeEmission")
        emission.location = (-40, 0)
        emission.inputs["Strength"].default_value = 1.0
        links.new(tex.outputs["Color"], emission.inputs["Color"])
        links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return material


def _add_image_plane(bpy, name: str, image_path: str, location, scale):
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    _assign_material(obj, _ensure_image_material(bpy, f"{name}_Mat", image_path))
    return obj


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
    camera.location = (0.0, -10.45, 5.12)
    camera.rotation_euler = (math.radians(60.0), 0.0, 0.0)
    camera.data.lens = 41

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
    lane_spacing = 3.95
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
    source_tab_count = _bounded_count(metrics.get("source_cache_doc_count", 5), 4, 7)
    source_surface = _ensure_material(bpy, "VerifiedSourceSurface", "#F6F0E8", roughness=0.62)
    source_border = _ensure_material(bpy, "VerifiedSourceBorder", "#C5B8AA", roughness=0.7)
    source_primary = _ensure_material(bpy, "VerifiedSourcePrimary", "#3730A3", roughness=0.38)
    source_accent = _ensure_material(bpy, "VerifiedSourceAccent", "#901C32", roughness=0.38)
    source_focus = _ensure_material(bpy, "VerifiedSourceFocus", "#B45309", roughness=0.38)
    source_dark = _ensure_material(bpy, "VerifiedSourceDark", "#111827", roughness=0.44)
    _add_box(
        bpy,
        "SourceRailDeck",
        location=(0.0, 1.05, 0.14),
        scale=(4.8, 0.18, 0.045),
        material=source_surface,
        bevel=0.02,
    )
    tab_spacing = 1.14
    tab_half = (source_tab_count - 1) * tab_spacing / 2.0
    for source_index in range(source_tab_count):
        tab_x = -tab_half + source_index * tab_spacing
        _add_box(
            bpy,
            f"SourceRailTab_{source_index}",
            location=(tab_x, 1.05, 0.22),
            scale=(0.26, 0.1, 0.03),
            material=(source_primary, source_accent, source_focus, source_dark)[source_index % 4],
            bevel=0.012,
        )
    physics_views = {
        view["mode_label"]: view for view in spec.get("physics_views", {}).get("views", [])
    }
    for index, lane in enumerate(spec["lanes"]):
        x = start_x + index * lane_spacing
        label_x = x
        if index == 0:
            label_x += 0.22
        elif index == len(spec["lanes"]) - 1:
            label_x -= 0.22
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
            location=(x * 0.44, 0.38, 0.18),
            scale=(0.026, 0.22, 0.012),
            material=connector_mat,
            bevel=0.01,
        ).rotation_euler.z = math.radians(-14.0 if x > 0 else 14.0)
        _add_box(
            bpy,
            f"{lane_id}_media_frame",
            location=(x, 0.24, 0.56),
            scale=(1.28, 0.82, 0.1),
            material=primary_mat,
            bevel=0.04,
        )
        _add_box(
            bpy,
            f"{lane_id}_media_mount",
            location=(x, 0.24, 0.61),
            scale=(1.16, 0.7, 0.02),
            material=plaque_mat,
            bevel=0.015,
        )
        physics_view = physics_views.get(lane["label"])
        if physics_view:
            _add_image_plane(
                bpy,
                f"{lane_id}_panel_image",
                physics_view["panel_texture"],
                location=(x, 0.24, 0.685),
                scale=(1.08, 0.64, 1.0),
            )

        _add_text(
            bpy,
            f"{lane_id}_case_title",
            lane.get("case_title", lane["label"]),
            location=(label_x, -1.8, 0.46),
            scale=(0.13, 0.13, 0.13),
            material=label_mat,
        )
        _add_text(
            bpy,
            f"{lane_id}_mode_label",
            lane["label"],
            location=(label_x, -2.02, 0.36),
            scale=(0.085, 0.085, 0.085),
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
