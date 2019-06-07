# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Procedural building generator
#  Copyright (C) 2019 Luka Simic
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from . import GenLayout
from . import GenMesh
from . import GenUtils
import time
import os


class Generator(bpy.types.Operator):
    # TODO: docstring

    bl_idname = "pbg.generate_building"
    bl_label = "Generate Building"

    def invoke(self, context, event):
        group = bpy.data.groups.get("pbg_group")
        if not group:
            bpy.ops.group.create(name="pbg_group")
            group = bpy.data.groups.get("pbg_group")
        # delete all objects from group
        for obj in group.objects:
            bpy.data.objects.remove(obj)

        # generate stuff needed for other functions that generate geometry
        time_start = time.time()
        params_general = GenLayout.ParamsGeneral.from_ui()
        params_section = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
        params_pillar = GenMesh.ParamsPillar.from_ui()
        params_walls = GenMesh.ParamsWalls.from_ui()
        params_windows_under = GenMesh.ParamsWindowsUnder.from_ui()
        params_windows_above = GenMesh.ParamsWindowsAbove.from_ui()
        params_footprint = GenLayout.ParamsFootprint.from_ui()
        params_stairs = GenMesh.ParamsStairs.from_ui()
        params_windows = GenMesh.ParamsWindows.from_ui()
        params_roof = GenMesh.ParamsRoof.from_ui()
        params_door = GenMesh.ParamsDoor.from_ui()

        door_position = ((0.0, 0.5*params_footprint.building_depth+params_footprint.building_wedge_depth,
                          params_general.floor_offset), 0)
        door_positions = list()
        # TODO: fix this door position mess, not sure if the zero above is critical
        door_positions.append((door_position[0], door_position[1], params_general.floor_offset))

        footprint = GenLayout.gen_footprint(params_footprint)
        layout = GenLayout.gen_layout(params_general, footprint, door_position)
        section_element_list = GenUtils.gen_section_element_list(params_section)
        section_mesh = GenUtils.gen_section_mesh(section_element_list, params_general.separator_height,
                                                 params_general.separator_width)
        if params_general.generate_separator == True:
            wall_section_height = params_general.floor_height - params_general.separator_height
        else:
            wall_section_height = params_general.floor_height
        # end if
        wall_section_mesh = GenUtils.gen_wall_section_mesh(params_walls.type, wall_section_height,
                                                           params_walls.section_size,
                                                           params_walls.mortar_size,
                                                           params_walls.row_count)

        # generate geometry
        obj_separator = None
        if params_general.generate_separator == True:
            obj_separator = GenMesh.gen_mesh_floor_separator(context, footprint, section_mesh.copy())
            group.objects.link(obj_separator)
            separator_positions = list()
            for i in range(0, params_general.floor_count+1):
                separator_positions.append(((0, 0, params_general.floor_offset + wall_section_height +
                                            i*params_general.floor_height), 0))
            apply_positions(obj_separator, separator_positions, group)
            obj_separator.hide = True
        # end if
        obj_wall = GenMesh.gen_mesh_wall(context, layout["wall_loops"], wall_section_mesh.copy())
        group.objects.link(obj_wall)
        obj_offset_wall = GenMesh.gen_mesh_offset_wall(context, footprint, params_general, params_walls)
        group.objects.link(obj_offset_wall)
        obj_stairs = GenMesh.gen_mesh_stairs(context, params_general, params_footprint, params_stairs)
        group.objects.link(obj_stairs)

        obj_window_under = GenMesh.gen_mesh_windows_under(context, params_general, params_windows_under, wall_section_mesh)
        group.objects.link(obj_window_under)
        apply_positions(obj_window_under, layout["window_positions"], group)
        obj_window_under.hide = True

        obj_window_above = GenMesh.gen_mesh_windows_above(context, params_general, params_windows_above, wall_section_mesh)
        group.objects.link(obj_window_above)
        apply_positions(obj_window_above, layout["window_positions"], group)
        obj_window_above.hide = True

        obj_window_around = GenMesh.gen_mesh_windows_around(context, params_general, params_windows)
        group.objects.link(obj_window_around)
        apply_positions(obj_window_around, layout["window_positions"], group)
        obj_window_around.hide = True

        obj_window = GenMesh.gen_mesh_windows(context, params_general, params_windows)
        group.objects.link(obj_window)
        apply_positions(obj_window, layout["window_positions"], group)
        obj_window.hide = True

        obj_door_above = GenMesh.gen_mesh_door_above(context, params_general, wall_section_mesh)
        group.objects.link(obj_door_above)
        apply_positions(obj_door_above, door_positions, group)
        obj_door_above.hide = True

        obj_door_around = GenMesh.gen_mesh_door_around(context, params_general, params_door)
        group.objects.link(obj_door_around)
        apply_positions(obj_door_around, door_positions, group)
        obj_door_around.hide = True

        obj_door = GenMesh.gen_mesh_door(context, params_general, params_door)
        group.objects.link(obj_door)
        apply_positions(obj_door, door_positions, group)
        obj_door.hide = True

        obj_pillar = None
        if params_general.generate_pillar == True:
            obj_pillar = GenMesh.gen_mesh_pillar(context, params_pillar, params_general, section_mesh.copy())
            group.objects.link(obj_pillar)
            apply_positions(obj_pillar, layout["pillar_positions"], group)
            obj_pillar.hide = True
        # end if

        obj_roof = GenMesh.gen_mesh_roof(context, params_general, footprint, params_footprint, params_roof)
        group.objects.link(obj_roof)

        time_end = time.time()
        msg = "generation finished in " + str(time_end - time_start) + " seconds"
        print(msg)

        time_start = time.time()
        material_dict = load_materials()
        time_end = time.time()
        msg = "loading materials finished in " + str(time_end - time_start) + " seconds"

        # apply materials to objects
        time_start = time.time()
        if obj_separator:
            obj_separator.data.materials.append(material_dict["pbg_color2"])
        obj_wall.data.materials.append(material_dict["pbg_color1"])
        obj_offset_wall.data.materials.append(material_dict["pbg_color2"])
        obj_stairs.data.materials.append(material_dict["pbg_color2"])
        obj_window_around.data.materials.append(material_dict["pbg_color2"])
        obj_door_above.data.materials.append(material_dict["pbg_color1"])
        obj_door_around.data.materials.append(material_dict["pbg_color2"])
        obj_door.data.materials.append(material_dict["pbg_wood"])
        obj_roof.data.materials.append(material_dict["pbg_roof"])
        if obj_pillar:
            obj_pillar.data.materials.append(material_dict["pbg_color2"])
        # TODO:
        if params_windows_under.type == "WALL" or params_windows_under.type == "PILLARS":
            obj_window_under.data.materials.append(material_dict["pbg_color1"])
        else:
            obj_window_under.data.materials.append(material_dict["pbg_color2"])
        if params_windows_above.type == "WALL":
            obj_window_above.data.materials.append(material_dict["pbg_color1"])
        else:
            obj_window_above.data.materials.append(material_dict["pbg_color2"])
        obj_window.data.materials.append(material_dict["pbg_wood"])
        obj_window.data.materials.append(material_dict["pbg_glass"])
        time_end = time.time()
        msg = "applying materials finished in " + str(time_end - time_start) + " seconds"
        print(msg)
        return {"FINISHED"}
    # end invoke
# end Generator


def apply_positions(obj: bpy.types.Object, positions: list, group):
    """
        Duplicates (linked duplicate) the given object onto the given positions
        applies the given rotation
    Args:
        group: group where to keep the object
        obj: object to duplicate, origin should be in (0, 0, 0)
        positions: list(tuple(tuple(x,y,z), rot)) - object positions and rotations
    Returns:

    """
    for position in positions:
        dup = obj.copy()
        group.objects.link(dup)
        # move it
        dup.location.x = position[0][0]
        dup.location.y = position[0][1]
        dup.location.z = position[0][2]
        # rotate it
        dup.rotation_euler.z = position[1]
        # link it to the scene
        bpy.context.scene.objects.link(dup)
# end apply_positions


def load_materials() -> dict:
    """
        list of materials:
            pbg_wood
            pbg_glass
            pbg_color1
            pbg_color2
            pbg_roof
    Returns:
        dictionary, containing the materials
    """
    directory = os.path.dirname(os.path.realpath(__file__))
    file_path = directory + "\\" + "default_materials.blend"
    materials = dict()
    with bpy.data.libraries.load(file_path, link=False) as (data_from, data_to):
        for material_name in data_from.materials:
            is_imported = False
            for c_material in bpy.data.materials:
                if c_material.name.startswith(material_name):
                    is_imported = True
                    materials[material_name] = c_material
                    break

            if not is_imported:
                bpy.ops.wm.append(filename=material_name, directory=file_path + "\\Material\\")
                materials[material_name] = bpy.data.materials[material_name]
    return materials
