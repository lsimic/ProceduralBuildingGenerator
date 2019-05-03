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


class Generator(bpy.types.Operator):
    # TODO: docstring

    bl_idname = "pbg.generate_building"
    bl_label = "Generate Building"

    def invoke(self, context, event):
        # generate stuff needed for other functions that generate geometry
        params_general = GenMesh.ParamsGeneral.from_ui()
        params_layout = GenLayout.ParamsLayout.from_ui()
        params_section = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
        params_pillar = GenMesh.ParamsPillar.from_ui()
        params_walls = GenMesh.ParamsWalls.from_ui()
        params_windows = GenMesh.ParamsWindows.from_ui()
        params_windows_under = GenMesh.ParamsWindowsUnder.from_ui()

        footprint = GenLayout.gen_footprint(params_general)
        layout = GenLayout.gen_layout(params_layout, footprint)
        section_element_list = GenUtils.gen_section_element_list(params_section)
        section_mesh = GenUtils.gen_section_mesh(section_element_list, params_general.floor_separator_height,
                                                 params_general.floor_separator_width)
        wall_section_height = params_general.floor_height - params_general.floor_separator_height
        wall_section_mesh = GenUtils.gen_wall_section_mesh(params_walls.wall_type, wall_section_height,
                                                           params_walls.wall_section_size,
                                                           params_walls.wall_mortar_size,
                                                           params_walls.wall_row_count)

        # generate geometry
        GenMesh.gen_mesh_floor_separator(context, params_general, footprint, section_mesh.copy())
        GenMesh.gen_mesh_wall(context, layout["wall_layout_loops"], params_general, params_walls,
                              wall_section_mesh.copy())
        GenMesh.gen_mesh_offset_wall(context, footprint, params_general, params_walls)
        GenMesh.gen_mesh_windows_under(context, layout["window_positions"], params_general, params_windows,
                                       params_windows_under, wall_section_mesh)

        print(params_layout.generate_pillar)
        if params_layout.generate_pillar == True:
            GenMesh.gen_mesh_pillar(context, params_pillar, params_general, section_mesh.copy(),
                                    layout["pillar_positions"])
        # end if

        return {"FINISHED"}
    # end invoke
# end Generator
