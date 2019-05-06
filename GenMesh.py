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

import bmesh
import bpy
import mathutils
import math
from . import Utils
from . import GenUtils


class ParamsGeneral:
    """
    Overall/general parameters of the building
    Used in multiple generating functions
    """
    def __init__(self, building_width, building_depth, building_chamfer, building_wedge_depth, building_wedge_width,
                 floor_count, floor_height, floor_first_offset, floor_separator_height, floor_separator_width,
                 floor_separator_include):
        self.building_width = building_width
        self.building_depth = building_depth
        self.building_chamfer = building_chamfer
        self.building_wedge_depth = building_wedge_depth
        self.building_wedge_width = building_wedge_width
        self.floor_count = floor_count
        self.floor_height = floor_height
        self.floor_first_offset = floor_first_offset
        self.floor_separator_height = floor_separator_height
        self.floor_separator_width = floor_separator_width
        self.floor_separator_include = floor_separator_include
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsGeneral(
            properties.building_width,
            properties.building_depth,
            properties.building_chamfer,
            properties.building_wedge_depth,
            properties.building_wedge_width,
            properties.floor_count,
            properties.floor_height,
            properties.floor_first_offset,
            properties.floor_separator_height,
            properties.floor_separator_width,
            properties.floor_separator_include
        )
        return params
    # end from_ui
# end ParamsGeneral


class ParamsPillar:
    # TODO: docstring
    # horizontal separator: bool which defines whether or not to include the horizontal separator in the pillar profile
    # offset_size - size of the offset
    # offset - position of the offset
    def __init__(self, pillar_width, pillar_depth, pillar_chamfer, pillar_offset_height,
                 pillar_offset_size, pillar_include_floor_separator, pillar_include_first_floor):
        self.pillar_width = pillar_width
        self.pillar_depth = pillar_depth
        self.pillar_chamfer = pillar_chamfer
        self.pillar_offset_height = pillar_offset_height
        self.pillar_offset_size = pillar_offset_size
        self.pillar_include_floor_separator = pillar_include_floor_separator
        self.pillar_include_first_floor = pillar_include_first_floor
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsPillar(
            properties.pillar_width,
            properties.pillar_depth,
            properties.pillar_chamfer,
            properties.pillar_offset_height,
            properties.pillar_offset_size,
            properties.pillar_include_floor_separator,
            properties.pillar_include_first_floor,
        )
        return params
    # end from_ui
# end ParamsPillar


class ParamsWalls:
    # TODO: docstring
    def __init__(self, wall_type, wall_mortar_size, wall_section_size, wall_row_count, wall_offset_size,
                 wall_offset_type, wall_offset_mortar_size, wall_offset_section_size, wall_offset_row_count):
        self.wall_type = wall_type
        self.wall_mortar_size = wall_mortar_size
        self.wall_section_size = wall_section_size
        self.wall_row_count = wall_row_count
        self.wall_offset_size = wall_offset_size
        self.wall_offset_type = wall_offset_type
        self.wall_offset_mortar_size = wall_offset_mortar_size
        self.wall_offset_section_size = wall_offset_section_size
        self.wall_offset_row_count = wall_offset_row_count
    # end init

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsWalls(
            properties.wall_type,
            properties.wall_mortar_size,
            properties.wall_section_size,
            properties.wall_row_count,
            properties.wall_offset_size,
            properties.wall_offset_type,
            properties.wall_offset_mortar_size,
            properties.wall_offset_section_size,
            properties.wall_offset_row_count
        )
        return params
    # end from_ui
# end ParamsWalls


class ParamsWindows:
    def __init__(self, window_total_width: float, window_total_height: float, window_vertical_offset: float):
        self.window_total_width = window_total_width
        self.window_total_height = window_total_height
        self.window_vertical_offset = window_vertical_offset
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsWindows(
            properties.window_width,
            properties.window_height,
            properties.window_offset
        )
        return params
    # end from_ui
# end ParamsWindows


class ParamsWindowsUnder:
    def __init__(self, windows_under_type: str, windows_under_width: float, windows_under_height: float,
                 windows_under_depth: float, windows_under_inset_depth: float, windows_under_amplitude: float,
                 windows_under_period_count: int, windows_under_simple_width: float, windows_under_simple_depth: float,
                 windows_under_pillar_base_diameter: float, windows_under_pillar_base_height: float,
                 windows_under_pillar_min_diameter: float, windows_under_pillar_max_diameter: float):
        self.windows_under_type = windows_under_type
        self.windows_under_width = windows_under_width
        self.windows_under_height = windows_under_height
        self.windows_under_depth = windows_under_depth
        self.windows_under_inset_depth = windows_under_inset_depth
        self.windows_under_amplitude = windows_under_amplitude
        self.windows_under_period_count = windows_under_period_count
        self.windows_under_simple_width = windows_under_simple_width
        self.windows_under_simple_depth = windows_under_simple_depth
        self.windows_under_pillar_base_diameter = windows_under_pillar_base_diameter
        self.windows_under_pillar_base_height = windows_under_pillar_base_height
        self.windows_under_pillar_min_diameter = windows_under_pillar_min_diameter
        self.windows_under_pillar_max_diameter = windows_under_pillar_max_diameter
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsWindowsUnder(
            properties.windows_under_type,
            properties.windows_under_width,
            properties.windows_under_height,
            properties.windows_under_depth,
            properties.windows_under_inset_depth,
            properties.windows_under_amplitude,
            properties.windows_under_period_count,
            properties.windows_under_simple_width,
            properties.windows_under_simple_depth,
            properties.windows_under_pillar_base_diameter,
            properties.windows_under_pillar_base_height,
            properties.windows_under_pillar_min_diameter,
            properties.windows_under_pillar_max_diameter
        )
        return params
    # end from_ui
# end ParamsWindowsUnder


def gen_mesh_floor_separator(context: bpy.types.Context, params_general: ParamsGeneral, layout: list,
                             section_mesh: bpy.types.Mesh):
    # TODO: docstring

    # generate the section(profile) which will be extruded, and extrude it to create a single separator
    section_mesh_extruded = Utils.extrude_along_edges(section_mesh, layout, True)

    # create a bmesh so we can edit
    separators_bmesh = bmesh.new()
    separators_bmesh.from_mesh(section_mesh_extruded)

    # move the mesh to the desired height
    vec_trans = (0.0, 0.0, params_general.floor_height + params_general.floor_first_offset -
                 params_general.floor_separator_height)
    bmesh.ops.translate(separators_bmesh, verts=separators_bmesh.verts, vec=vec_trans)
    geom_to_duplicate = separators_bmesh.verts[:] + separators_bmesh.edges[:] + separators_bmesh.faces[:]

    # duplicate the separators for each floor, and translate them, or translate straight to top based on params.
    i = 1
    while i <= params_general.floor_count:
        ret_dup = bmesh.ops.duplicate(separators_bmesh, geom=geom_to_duplicate)
        verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        vec_trans = (0.0, 0.0, params_general.floor_height)
        bmesh.ops.translate(separators_bmesh, verts=verts_to_translate, vec=vec_trans)
        geom_to_duplicate = [ele for ele in ret_dup["geom"] if (isinstance(ele, bmesh.types.BMVert)
                                                                or isinstance(ele, bmesh.types.BMEdge)
                                                                or isinstance(ele, bmesh.types.BMFace))]
        # end if
        i += 1
    # end while

    # convert back from bmesh to mesh, crate an object using the mesh
    separators_bmesh.to_mesh(section_mesh_extruded)
    separators_bmesh.free()
    ob = bpy.data.objects.get("PBGHorizontalSeparators")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGHorizontalSeparators", section_mesh_extruded)
    context.scene.objects.link(new_obj)
# end gen_mesh_floor_separator


def gen_mesh_pillar(context: bpy.types.Context, params_pillar: ParamsPillar, params_general: ParamsGeneral,
                    floor_separator_mesh, pillar_positions: list):
    # TODO: docstring
    # TODO: improve pillar generation,
    pillar_section_bmesh = bmesh.new()

    if params_pillar.pillar_include_floor_separator:
        # add separator section mesh to bmesh and move it to the appropriate place (up on Z)
        pillar_section_bmesh.from_mesh(floor_separator_mesh)
        vec_trans = (0.0, 0.0, params_general.floor_height - params_general.floor_separator_height)
        bmesh.ops.translate(pillar_section_bmesh, vec=vec_trans, verts=pillar_section_bmesh.verts)
    else:
        # we don't have a separator mesh, add a straight line
        mesh = bpy.data.meshes.new(name="PBGPillarSeparatorSection")
        verts = list()
        edges = list()
        verts.append((0.0, 0.0, params_general.floor_height - params_general.floor_separator_height))
        verts.append((0.0, 0.0, params_general.floor_height))
        edges.append((0, 1))
        mesh.from_pydata(verts, edges, [])
        pillar_section_bmesh.from_mesh(mesh)
    # end if

    if params_pillar.pillar_offset_size > 0:
        # generate a pillar_section mesh
        pillar_offset_params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
        pillar_offset_section = GenUtils.gen_section_element_list(pillar_offset_params)
        pillar_offset_mesh = GenUtils.gen_section_mesh(pillar_offset_section, params_pillar.pillar_offset_size,
                                                       params_pillar.pillar_offset_size)
        # add it to new bmesh
        bm = bmesh.new()
        bm.from_mesh(pillar_offset_mesh)

        # remove last vertex
        bm.verts.ensure_lookup_table()
        last_vert = bm.verts[len(bm.verts) - 1]
        bm.verts.remove(last_vert)

        # move up on Z, and on -Y for offset.
        vec_trans = (0.0, -params_pillar.pillar_offset_size, params_general.floor_height -
                     params_general.floor_separator_height - params_pillar.pillar_offset_size)
        bmesh.ops.translate(bm, vec=vec_trans, verts=bm.verts)

        # duplicate, flip and move down
        mat_loc = mathutils.Matrix.Translation((0.0, params_pillar.pillar_offset_size, - params_general.floor_height +
                                                params_general.floor_separator_height +
                                                params_pillar.pillar_offset_size))
        geom_to_duplicate = bm.verts[:] + bm.edges[:] + bm.faces[:]
        ret_dup = bmesh.ops.duplicate(bm, geom=geom_to_duplicate)
        verts_to_transform = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.scale(bm, vec=(1.0, 1.0, -1.0), space=mat_loc, verts=verts_to_transform)
        z_dist = (params_general.floor_height - params_general.floor_separator_height -
                  params_pillar.pillar_offset_height - 2 * params_pillar.pillar_offset_size)
        bmesh.ops.translate(bm, vec=(0.0, 0.0, - z_dist), verts=verts_to_transform)

        # add fillet between the two sections and below the lower section
        mesh_filler = bpy.data.meshes.new("PBGPillarFiller")
        mesh_filler_verts = list()
        mesh_filler_edges = list()
        mesh_filler_verts.append((0.0, 0.0, 0.0))
        mesh_filler_verts.append((0.0, 0.0, params_pillar.pillar_offset_height))
        mesh_filler_edges.append((0, 1))
        mesh_filler_verts.append((0.0, -params_pillar.pillar_offset_size,
                                  params_pillar.pillar_offset_height + params_pillar.pillar_offset_size))
        mesh_filler_verts.append((0.0, -params_pillar.pillar_offset_size, params_general.floor_height -
                                  params_general.floor_separator_height - params_pillar.pillar_offset_size))
        mesh_filler_edges.append((2, 3))
        mesh_filler.from_pydata(mesh_filler_verts, mesh_filler_edges, [])

        # add the filler to bmesh
        bm.from_mesh(mesh_filler)

        # bmesh to mesh and append to existing bmesh
        m = bpy.data.meshes.new("PBGPillarMesh")
        bm.to_mesh(m)
        bm.free()
        pillar_section_bmesh.from_mesh(m)
    else:
        m = bpy.data.meshes.new("PBGPillarMesh")
        mesh_filler_verts = list()
        mesh_filler_edges = list()
        mesh_filler_verts.append((0.0, 0.0, 0.0))
        mesh_filler_verts.append((0.0, 0.0, params_general.floor_height - params_general.floor_separator_height))
        mesh_filler_edges.append((0, 1))
        m.from_pydata(mesh_filler_verts, mesh_filler_edges, [])
        pillar_section_bmesh.from_mesh(m)
    # end if

    # initial move on Z, set counter
    if params_pillar.pillar_include_first_floor:
        vec_trans = (0.0, 0.0, params_general.floor_first_offset)
        i = 0
    else:
        vec_trans = (0.0, 0.0, params_general.floor_height + params_general.floor_first_offset)
        i = 1
    # end if
    bmesh.ops.translate(pillar_section_bmesh, vec=vec_trans, verts=pillar_section_bmesh.verts)

    # duplicate number of floors - 1 times, move each time for n*floor_height.
    geom = pillar_section_bmesh.verts[:] + pillar_section_bmesh.edges[:] + pillar_section_bmesh.faces[:]
    while i < params_general.floor_count:
        ret_dup = bmesh.ops.duplicate(pillar_section_bmesh, geom=geom)
        verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.translate(pillar_section_bmesh, verts=verts_to_translate, vec=(0.0, 0.0, params_general.floor_height))
        geom = ret_dup["geom"]
        i += 1
    # end while

    # if we have pillar on first floor, append a line so it goes to the bottom
    if params_pillar.pillar_include_first_floor:
        mesh_filler_verts = list()
        mesh_filler_edges = list()
        mesh_filler_verts.append((0.0, 0.0, 0.0))
        mesh_filler_verts.append((0.0, 0.0, params_general.floor_first_offset))
        mesh_filler_edges.append((0, 1))
        m = bpy.data.meshes.new("PBGPillarMesh")
        m.from_pydata(mesh_filler_verts, mesh_filler_edges, [])
        pillar_section_bmesh.from_mesh(m)
    # end if

    # remove doubles before extruding
    bmesh.ops.remove_doubles(pillar_section_bmesh, verts=pillar_section_bmesh.verts, dist=0.0001)

    # create the horizontal layout for extruding along
    layout = list()
    layout.append((-0.5 * params_pillar.pillar_width, 0.0, 0.0))
    if params_pillar.pillar_chamfer > 0:
        layout.append((-0.5 * params_pillar.pillar_width,
                       params_pillar.pillar_depth - params_pillar.pillar_chamfer, 0.0))
        layout.append((-0.5 * params_pillar.pillar_width + params_pillar.pillar_chamfer,
                       params_pillar.pillar_depth, 0.0))
        layout.append((0.5 * params_pillar.pillar_width - params_pillar.pillar_chamfer,
                       params_pillar.pillar_depth, 0.0))
        layout.append((0.5 * params_pillar.pillar_width,
                       params_pillar.pillar_depth - params_pillar.pillar_chamfer, 0.0))
    else:
        layout.append((-0.5 * params_pillar.pillar_width, params_pillar.pillar_depth, 0.0))
        layout.append((0.5 * params_pillar.pillar_width, params_pillar.pillar_depth, 0.0))
    # end if
    layout.append((0.5 * params_pillar.pillar_width, 0.0, 0.0))

    # convert to mesh, extrude along, free bmesh, then populate with extruded
    pillar_section_mesh = bpy.data.meshes.new("PBGPillarSection")
    pillar_section_bmesh.to_mesh(pillar_section_mesh)
    pillar_section_bmesh.free()
    pillar_extruded = Utils.extrude_along_edges(pillar_section_mesh, layout, False)
    pillar_bmesh = bmesh.new()
    pillar_bmesh.from_mesh(pillar_extruded)

    # duplicate and rotate appropriately based on coordinates and rotation
    geom_initial = pillar_bmesh.verts[:] + pillar_bmesh.edges[:] + pillar_bmesh.faces[:]

    for pos in pillar_positions:
        # duplicate the initial pillar
        ret_dup = bmesh.ops.duplicate(pillar_bmesh, geom=geom_initial)
        verts_to_transform = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        # translate it to the desired position
        bmesh.ops.translate(pillar_bmesh, vec=(pos[0], pos[1], 0.0), verts=verts_to_transform)
        # initialize the center point and rotation matrix
        mat_loc = mathutils.Matrix.Translation((-pos[0], -pos[1], 0.0))
        mat_rot = mathutils.Matrix.Rotation(pos[2], 3, "Z")
        # rotate it at the desired position
        bmesh.ops.rotate(pillar_bmesh, cent=(0, 0, 0), matrix=mat_rot, verts=verts_to_transform, space=mat_loc)
    # end for

    # delete first pillar(one with all floors, used for duplicate and rotate)
    bmesh.ops.delete(pillar_bmesh, geom=geom_initial, context=1)

    # convert to mesh and create object
    pillar_mesh = bpy.data.meshes.new("PBGPillarMesh")
    pillar_bmesh.to_mesh(pillar_mesh)
    pillar_bmesh.free()
    ob = bpy.data.objects.get("PBGPillars")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGPillars", pillar_mesh)
    context.scene.objects.link(new_obj)
# end generate_pillars


def gen_mesh_wall(context: bpy.types.Context, wall_loops: list, params_general: ParamsGeneral,
                  wall_section_mesh: bpy.types.Mesh):
    # TODO: docstring

    # check for edge case without windows
    if len(wall_loops) == 1:
        is_loop = True
    else:
        is_loop = False
    # end if

    wall_bmesh = bmesh.new()
    # TODO: add a cut if there is no special element below/above windows,
    # TODO: so it could be appended to same mesh to keep nice and clean geometry
    for loop in wall_loops:
        mesh = Utils.extrude_along_edges(wall_section_mesh.copy(), loop, is_loop)
        wall_bmesh.from_mesh(mesh)
    # end for

    # move the wall bmesh up on Z for floor offset
    bmesh.ops.translate(wall_bmesh, verts=wall_bmesh.verts, vec=(0.0, 0.0, params_general.floor_first_offset))

    # duplicate the wall bmesh to other floors.
    geom = wall_bmesh.verts[:] + wall_bmesh.edges[:] + wall_bmesh.faces[:]
    i = 0
    while i < params_general.floor_count:
        ret_dup = bmesh.ops.duplicate(wall_bmesh, geom=geom)
        verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.translate(wall_bmesh, verts=verts_to_translate, vec=(0.0, 0.0, params_general.floor_height))
        geom = ret_dup["geom"]
        i += 1
    # end while

    # check if the object for walls already exists
    ob = bpy.data.objects.get("PBGWalls")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)
    # end if

    wall_mesh = bpy.data.meshes.new("PBGWall")
    wall_bmesh.to_mesh(wall_mesh)
    wall_bmesh.free()

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGWalls", wall_mesh)
    context.scene.objects.link(new_obj)
# end gen_mesh_walls


def gen_mesh_offset_wall(context: bpy.types.Context, wall_loop: list, params_general: ParamsGeneral,
                         params_walls: ParamsWalls):
    # TODO: docstring
    # generate wall section mesh
    wall_section_mesh = GenUtils.gen_wall_section_mesh(params_walls.wall_offset_type, params_general.floor_first_offset,
                                                       params_walls.wall_offset_section_size,
                                                       params_walls.wall_offset_mortar_size,
                                                       params_walls.wall_offset_row_count)
    wall_offset_bmesh = bmesh.new()
    wall_offset_bmesh.from_mesh(wall_section_mesh)
    # offset it on y axis
    vec_trans = mathutils.Vector((0.0, params_walls.wall_offset_size, 0.0))
    bmesh.ops.translate(wall_offset_bmesh, vec=vec_trans, verts=wall_offset_bmesh.verts)
    # append the top edge
    verts = list()
    edges = list()
    verts.append((0.0, 0.0, params_general.floor_first_offset))
    verts.append((0.0, params_walls.wall_offset_size, params_general.floor_first_offset))
    edges.append((0, 1))
    mesh_edge = bpy.data.meshes.new("PBGWallOffsetEdge")
    mesh_edge.from_pydata(verts, edges, [])
    wall_offset_bmesh.from_mesh(mesh_edge)
    bmesh.ops.remove_doubles(wall_offset_bmesh, verts=wall_offset_bmesh.verts, dist=0.0001)
    # convert to mesh, extrude along
    wall_offset_mesh = bpy.data.meshes.new("PbgWallOffset")
    wall_offset_bmesh.to_mesh(wall_offset_mesh)
    wall_offset_bmesh.free()
    mesh = Utils.extrude_along_edges(wall_offset_mesh, wall_loop, True)

    # check if the object for walls already exists
    ob = bpy.data.objects.get("PBGOffset")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)
    # end if

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGOffset", mesh)
    context.scene.objects.link(new_obj)
# end gen_mesh_offset_wall


def gen_mesh_windows_under(context: bpy.types.Context, window_positions: list, params_general: ParamsGeneral,
                           params_windows: ParamsWindows, params_window_under: ParamsWindowsUnder,
                           wall_section_mesh: bpy.types.Mesh):
    # generate the mesh, centered, lowest point at 0
    windows_under_bmesh = bmesh.new()
    if params_window_under.windows_under_type == "WALL":
        # start with the wall mesh
        windows_under_bmesh.from_mesh(wall_section_mesh)
        # bisect it on offset height, remove the outer geometry
        geom = windows_under_bmesh.verts[:] + windows_under_bmesh.edges[:] + windows_under_bmesh.faces[:]
        plane_co = (0.0, 0.0, params_windows.window_vertical_offset)
        plane_no = (0.0, 0.0, 1.0)
        bmesh.ops.bisect_plane(windows_under_bmesh, geom=geom, clear_outer=True, plane_co=plane_co, plane_no=plane_no)
        # move it on x axis half the width
        vec_trans = (-0.5 * params_windows.window_total_width, 0.0, 0.0)
        bmesh.ops.translate(windows_under_bmesh, vec=vec_trans, verts=windows_under_bmesh.verts)
        # extrude on x axis, to fill width
        vec_ext = (params_windows.window_total_width, 0.0, 0.0)
        ret_extrude = bmesh.ops.extrude_edge_only(windows_under_bmesh, edges=windows_under_bmesh.edges,
                                                  use_select_history=True)
        verts_to_translate = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.translate(windows_under_bmesh, verts=verts_to_translate, vec=vec_ext)
    else:
        # make the cube, it is same for all types (SINE, SIMPLE, PILLARS)
        # first loop, append to bmesh...
        verts = list()
        verts.append((-0.5*params_windows.window_total_width, 0.0, 0.0))
        verts.append((-0.5*params_windows.window_total_width, 0.0, params_windows.window_vertical_offset))
        verts.append((0.5*params_windows.window_total_width, 0.0, params_windows.window_vertical_offset))
        verts.append((0.5*params_windows.window_total_width, 0.0, 0.0))
        m = bpy.data.meshes.new("PBGWindowsUnderMesh")
        m.from_pydata(verts, [(0, 1), (1, 2), (2, 3), (3, 0)], [])
        windows_under_bmesh.from_mesh(m)
        # extrude on y forwards
        vec_ext = (0.0, params_window_under.windows_under_depth, 0.0)
        ret_extrude = bmesh.ops.extrude_edge_only(windows_under_bmesh, edges=windows_under_bmesh.edges,
                                                  use_select_history=True)
        verts_to_translate = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.translate(windows_under_bmesh, verts=verts_to_translate, vec=vec_ext)
        # extrude, scale down so it fits the width and height
        scale_x = (params_windows.window_total_width -
                   2*params_window_under.windows_under_width)/params_windows.window_total_width
        scale_z = (params_windows.window_vertical_offset -
                   2*params_window_under.windows_under_height)/params_windows.window_vertical_offset
        edges_to_extrude = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMEdge)]
        ret_extrude = bmesh.ops.extrude_edge_only(windows_under_bmesh, edges=edges_to_extrude, use_select_history=True)
        verts_to_scale = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        mat_loc = mathutils.Matrix.Translation((0.0, -params_window_under.windows_under_depth,
                                                -0.5*params_windows.window_vertical_offset))
        bmesh.ops.scale(windows_under_bmesh, space=mat_loc, verts=verts_to_scale, vec=(scale_x, 0, scale_z))
        # extrude inwards
        edges_to_extrude = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMEdge)]
        ret_extrude = bmesh.ops.extrude_edge_only(windows_under_bmesh, edges=edges_to_extrude, use_select_history=True)
        verts_to_translate = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        vec_ext = (0.0, -params_window_under.windows_under_inset_depth, 0.0)
        bmesh.ops.translate(windows_under_bmesh, verts=verts_to_translate, vec=vec_ext)
        # make a face
        bmesh.ops.contextual_create(windows_under_bmesh, geom=ret_extrude["geom"])

        # TODO: generate sine/pillar/simple mesh to fill the geometry...
        if params_window_under.windows_under_type in {"CYCLOID", "SINE"}:
            period_width = (params_windows.window_total_width
                            - 2*params_window_under.windows_under_width)/params_window_under.windows_under_period_count
            # TODO. when moving the circle/sine, the highest point should be on the edge of the hole.
            bm = bmesh.new()
            # create a single vert, spin it to make half a circle
            if params_window_under.windows_under_type == "CYCLOID":
                v_co_x = -0.5*params_windows.window_total_width + params_window_under.windows_under_width
                v_co_y = params_window_under.windows_under_depth
                v_co_z = params_window_under.windows_under_height
                bmesh.ops.create_vert(bm, co=(v_co_x, v_co_y, v_co_z))
                geom = bm.verts[:]
                bmesh.ops.spin(bm, geom=geom, angle=math.radians(180), steps=12, axis=(0.0, 0.0, 1.0),
                               cent=(v_co_x + period_width/2, v_co_y, v_co_z))
                sf = (params_window_under.windows_under_amplitude*2)/period_width
                mat_loc = mathutils.Matrix.Translation((0.0, -params_window_under.windows_under_depth, 0.0))
                bmesh.ops.scale(bm, vec=(1.0, sf, 1.0), space=mat_loc, verts=bm.verts)
            else:
                co_start_x = -0.5*params_windows.window_total_width + params_window_under.windows_under_width
                co_y = params_window_under.windows_under_depth - 0.5*params_window_under.windows_under_amplitude
                verts = list()
                edges = list()
                n = 12
                for i in range(0, n+1):
                    v_co_x = co_start_x + period_width*(i/n)
                    v_co_y = co_y + math.sin(2*math.pi*(i/n))*params_window_under.windows_under_amplitude*0.5
                    verts.append((v_co_x, v_co_y, params_window_under.windows_under_height))
                    if i > 0:
                        edges.append((i-1, i))
                # end for
                m = bpy.data.meshes.new("PBGWindowsUnderMeshSine")
                m.from_pydata(verts, edges, [])
                bm.from_mesh(m)
            # end if
            # extrude on z
            ret_ext = bmesh.ops.extrude_edge_only(bm, edges=bm.edges, use_select_history=True)
            verts_to_translate = [ele for ele in ret_ext["geom"] if isinstance(ele, bmesh.types.BMVert)]
            vec_trans = (0.0, 0.0, params_windows.window_vertical_offset - 2*params_window_under.windows_under_height)
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            bmesh.ops.translate(bm, verts=verts_to_translate, vec=vec_trans, space=mat_loc)
            # duplicate and move on x
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            for i in range(1, params_window_under.windows_under_period_count):
                ret_dup = bmesh.ops.duplicate(bm, geom=geom)
                verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
                bmesh.ops.translate(bm, vec=(i*period_width, 0.0, 0.0), space=mat_loc, verts=verts_to_translate)
            # remove doubles
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
            # append to original bmesh
            # TODO: find a better way to join these two bmeshes
            sine_cycle_mesh = bpy.data.meshes.new("PBGWindowsUnderMeshSineCycle")
            bm.to_mesh(sine_cycle_mesh)
            bm.free()
            windows_under_bmesh.from_mesh(sine_cycle_mesh)
        elif params_window_under.windows_under_type == "PILLARS":
            # create a single pillar section(quite a lot of work here)
            params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
            sequence = GenUtils.gen_section_element_list(params)
            mesh = GenUtils.gen_section_mesh(sequence, params_window_under.windows_under_pillar_base_height,
                                             0.5*params_window_under.windows_under_pillar_base_diameter
                                             - 0.5*params_window_under.windows_under_pillar_min_diameter)
            bm = bmesh.new()
            bm.from_mesh(mesh)
            bm.verts.ensure_lookup_table()
            last_vert = bm.verts[len(bm.verts) - 1]
            bm.verts.remove(last_vert)
            # move, on y and z, so the middle is on the bottom and goes through the center.
            vec_trans = (0.0, 0.5 * params_window_under.windows_under_pillar_min_diameter,
                         params_windows.window_vertical_offset - 2 * params_window_under.windows_under_height
                         - params_window_under.windows_under_pillar_base_height)
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            bmesh.ops.translate(bm, vec=vec_trans, space=mat_loc, verts=bm.verts)
            # generate pillar mesh
            verts = list()
            edges = list()
            start_y = vec_trans[1]
            start_z = vec_trans[2]
            end_z = 0.5*params_windows.window_vertical_offset - params_window_under.windows_under_height
            end_y = 0.5*params_window_under.windows_under_pillar_max_diameter
            dist_z = start_z - end_z
            dist_y = end_y - start_y
            n = 5
            for i in range(0, n+1):
                v_co_z = start_z - (dist_z/n)*i
                v_co_y = start_y + math.sin((0.5*math.pi*i)/n)*dist_y
                verts.append((0.0, v_co_y, v_co_z))
                if i > 0:
                    edges.append((i-1, i))
            # end for
            # append to bmesh
            m = bpy.data.meshes.new("PBGWindowsUnderMeshPillar")
            m.from_pydata(verts, edges, [])
            bm.from_mesh(m)
            # duplicate and mirror
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            ret_dup = bmesh.ops.duplicate(bm, geom=geom)
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, -end_z))
            verts_to_scale = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
            bmesh.ops.scale(bm, verts=verts_to_scale, space=mat_loc, vec=(1.0, 1.0, -1.0))
            # remove doubles and spin
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
            geom_spin = bm.verts[:] + bm.edges[:]
            ret_spin = bmesh.ops.spin(bm, geom=geom_spin, angle=math.radians(360), steps=16, axis=(0.0, 0.0, 1.0),
                                      cent=(0.0, 0.0, 0.0))
            # calculate the pillar positions
            width = params_windows.window_total_width - 2*params_window_under.windows_under_width
            pillar_count = int(width/params_window_under.windows_under_pillar_base_diameter)
            total_pillar_width = width/pillar_count
            # duplicate original geometry and translate
            geom_initial = bm.verts[:] + bm.edges[:] + bm.faces[:]
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            print(width)
            print(pillar_count)
            print(total_pillar_width)
            for i in range(0, pillar_count):
                v_co_x = -0.5*width + total_pillar_width*(i+0.5)
                ret_dup = bmesh.ops.duplicate(bm, geom=geom_initial)
                verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
                # TODO: fix y coordinate of this trans vector
                v_co_y = 0.5*(params_window_under.windows_under_depth + (params_window_under.windows_under_depth
                                                                         - params_window_under.windows_under_inset_depth))
                vec_trans = (v_co_x, v_co_y, params_window_under.windows_under_height)
                bmesh.ops.translate(bm, vec=vec_trans, verts=verts_to_translate, space=mat_loc)
            # remove original geometry
            bmesh.ops.delete(bm, geom=geom_initial, context=1)
            # append to original bmesh
            # TODO: find a better way to join these two bmeshes
            pillar_mesh = bpy.data.meshes.new("PBGWindowsUnderMeshPillar")
            bm.to_mesh(pillar_mesh)
            bm.free()
            windows_under_bmesh.from_mesh(pillar_mesh)
        else:
            # create layout for extruding
            layout = list()
            size_x = params_windows.window_total_width - 2*params_window_under.windows_under_width
            size_y = params_windows.window_vertical_offset - 2*params_window_under.windows_under_height
            layout.append((0.5 * size_x, 0.5 * size_y, 0.0))
            layout.append((-0.5 * size_x, 0.5 * size_y, 0.0))
            layout.append((-0.5 * size_x, -0.5 * size_y, 0.0))
            layout.append((0.5 * size_x, -0.5 * size_y, 0.0))
            # create a section and extrude it in x-y plane
            params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
            sequence = GenUtils.gen_section_element_list(params)
            mesh = GenUtils.gen_section_mesh(sequence, params_window_under.windows_under_simple_depth,
                                             params_window_under.windows_under_simple_width)
            bm = bmesh.new()
            bm.from_mesh(mesh)
            bm.verts.ensure_lookup_table()
            last_vert = bm.verts[len(bm.verts) - 1]
            bm.verts.remove(last_vert)
            bm.to_mesh(mesh)
            extruded = Utils.extrude_along_edges(mesh, layout, True)
            simple_bmesh = bmesh.new()
            simple_bmesh.from_mesh(extruded)
            # create the filler face
            verts = list()
            v_co_x = 0.5 * size_x - params_window_under.windows_under_simple_width
            v_co_y = 0.5 * size_y - params_window_under.windows_under_simple_width
            verts.append((v_co_x, v_co_y, params_window_under.windows_under_simple_depth))
            verts.append((-v_co_x, v_co_y, params_window_under.windows_under_simple_depth))
            verts.append((-v_co_x, -v_co_y, params_window_under.windows_under_simple_depth))
            verts.append((v_co_x, -v_co_y, params_window_under.windows_under_simple_depth))
            m = bpy.data.meshes.new("PBGWindowsUnderMeshSimpleFillFace")
            m.from_pydata(verts, [(0, 1), (1, 2), (2, 3), (3, 0)], [(0, 1, 2, 3)])
            simple_bmesh.from_mesh(m)
            bmesh.ops.remove_doubles(simple_bmesh, verts=simple_bmesh.verts, dist=0.0001)
            # rotate, move and offset on y
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            mat_rot = mathutils.Matrix.Rotation(math.radians(-90), 3, "X")
            # rotate it, move to the desired position, append to main bmesh
            bmesh.ops.rotate(simple_bmesh, cent=(0, 0, 0), matrix=mat_rot, verts=simple_bmesh.verts, space=mat_loc)
            vec_trans = (0.0, params_window_under.windows_under_depth, 0.5*params_windows.window_vertical_offset)
            bmesh.ops.translate(simple_bmesh, vec=vec_trans, space=mat_loc, verts=simple_bmesh.verts)
            # TODO: find a better way to join these two bmeshes
            simple_mesh = bpy.data.meshes.new("PBGWindowsUnderMeshSimple")
            simple_bmesh.to_mesh(simple_mesh)
            simple_bmesh.free()
            windows_under_bmesh.from_mesh(simple_mesh)
    # end if

    # recalculate normals
    # TODO: normals are sometimes recalculated differently when height changes while using "WALL" type.
    bmesh.ops.recalc_face_normals(windows_under_bmesh, faces=windows_under_bmesh.faces)

    # move on Z for offset
    vec_trans = (0.0, 0.0, params_general.floor_first_offset)
    bmesh.ops.translate(windows_under_bmesh, verts=windows_under_bmesh.verts, vec=vec_trans)
    # duplicate for each floor
    geom = windows_under_bmesh.verts[:] + windows_under_bmesh.edges[:] + windows_under_bmesh.faces[:]
    for i in range(0, params_general.floor_count):
        ret_dup = bmesh.ops.duplicate(windows_under_bmesh, geom=geom)
        verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.translate(windows_under_bmesh, verts=verts_to_translate, vec=(0.0, 0.0, params_general.floor_height))
        geom = ret_dup["geom"]
    # end for

    # duplicate for each window
    geom_initial = windows_under_bmesh.verts[:] + windows_under_bmesh.edges[:] + windows_under_bmesh.faces[:]
    for pos in window_positions:
        # duplicate the initial mesh
        ret_dup = bmesh.ops.duplicate(windows_under_bmesh, geom=geom_initial)
        verts_to_transform = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        # translate it to the desired position
        bmesh.ops.translate(windows_under_bmesh, vec=(pos[0], pos[1], 0.0), verts=verts_to_transform)
        # initialize the center point and rotation matrix
        mat_loc = mathutils.Matrix.Translation((-pos[0], -pos[1], 0.0))
        mat_rot = mathutils.Matrix.Rotation(pos[2], 3, "Z")
        # rotate it at the desired position
        bmesh.ops.rotate(windows_under_bmesh, cent=(0, 0, 0), matrix=mat_rot, verts=verts_to_transform, space=mat_loc)
    # end for
    bmesh.ops.delete(windows_under_bmesh, geom=geom_initial, context=1)

    # convert to mesh and create object
    windows_under_mesh = bpy.data.meshes.new("PBGWindowsUnderMesh")
    windows_under_bmesh.to_mesh(windows_under_mesh)
    windows_under_bmesh.free()
    ob = bpy.data.objects.get("PBGWindowsUnder")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGWindowsUnder", windows_under_mesh)
    context.scene.objects.link(new_obj)
# end gen_mesh_windows_under
