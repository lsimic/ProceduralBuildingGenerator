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
from . import GenLayout


class ParamsPillar:
    # horizontal separator: bool which defines whether or not to include the horizontal separator in the pillar profile
    # offset_size - size of the offset
    # offset - position of the offset
    def __init__(self, pillar_width, pillar_depth, pillar_chamfer, pillar_offset_height,
                 pillar_offset_size, pillar_include_floor_separator, pillar_include_first_floor):
        self.width = pillar_width
        self.depth = pillar_depth
        self.chamfer = pillar_chamfer
        self.offset_height = pillar_offset_height
        self.offset_size = pillar_offset_size
        self.include_floor_separator = pillar_include_floor_separator
        self.include_first_floor = pillar_include_first_floor
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
    def __init__(self, wall_type, wall_mortar_size, wall_section_size, wall_row_count, wall_offset_size,
                 wall_offset_type, wall_offset_mortar_size, wall_offset_section_size, wall_offset_row_count):
        self.type = wall_type
        self.mortar_size = wall_mortar_size
        self.section_size = wall_section_size
        self.row_count = wall_row_count
        self.offset_size = wall_offset_size
        self.offset_type = wall_offset_type
        self.offset_mortar_size = wall_offset_mortar_size
        self.offset_section_size = wall_offset_section_size
        self.offset_row_count = wall_offset_row_count
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


class ParamsWindowsUnder:
    def __init__(self, windows_under_type: str, windows_under_width: float, windows_under_height: float,
                 windows_under_depth: float, windows_under_inset_depth: float, windows_under_amplitude: float,
                 windows_under_period_count: int, windows_under_simple_width: float, windows_under_simple_depth: float,
                 windows_under_pillar_base_diameter: float, windows_under_pillar_base_height: float,
                 windows_under_pillar_min_diameter: float, windows_under_pillar_max_diameter: float):
        self.type = windows_under_type
        self.width = windows_under_width
        self.height = windows_under_height
        self.depth = windows_under_depth
        self.inset_depth = windows_under_inset_depth
        self.amplitude = windows_under_amplitude
        self.period_count = windows_under_period_count
        self.simple_width = windows_under_simple_width
        self.simple_depth = windows_under_simple_depth
        self.pillar_base_diameter = windows_under_pillar_base_diameter
        self.pillar_base_height = windows_under_pillar_base_height
        self.pillar_min_diameter = windows_under_pillar_min_diameter
        self.pillar_max_diameter = windows_under_pillar_max_diameter
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


class ParamsWindowsAbove:
    def __init__(self, windows_above_type: str, windows_above_width: float, windows_above_height: float,
                 windows_above_depth: float, windows_above_inset_depth: float, windows_above_amplitude: float,
                 windows_above_period_count: int, windows_above_simple_width: float, windows_above_simple_depth: float):
        self.type = windows_above_type
        self.width = windows_above_width
        self.height = windows_above_height
        self.depth = windows_above_depth
        self.inset_depth = windows_above_inset_depth
        self.amplitude = windows_above_amplitude
        self.period_count = windows_above_period_count
        self.simple_width = windows_above_simple_width
        self.simple_depth = windows_above_simple_depth
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsWindowsAbove(
            properties.windows_above_type,
            properties.windows_above_width,
            properties.windows_above_height,
            properties.windows_above_depth,
            properties.windows_above_inset_depth,
            properties.windows_above_amplitude,
            properties.windows_above_period_count,
            properties.windows_above_simple_width,
            properties.windows_above_simple_depth,
        )
        return params
    # end from_ui
# end ParamsWindowsAbove


class ParamsStairs:
    def __init__(self, layout_width: float, layout_depth: float, stair_count: int, width: float):
        self.layout_width = layout_width
        self.layout_depth = layout_depth
        self.stair_count = stair_count
        self.width = width
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsStairs(
            properties.stairs_layout_width,
            properties.stairs_layout_depth,
            properties.stairs_stair_count,
            properties.stairs_width
        )
        return params
    # end from_ui
# end ParamsStairs


class ParamsWindows:
    def __init__(self, section_height: float, section_width: float, pillar_width: float, inner_depth: float,
                 outer_depth: float, frame_width: float, frame_depth: float, window_ratio: float,
                 window_count: int, split_top: bool):
        self.section_height = section_height
        self.section_width = section_width
        self.pillar_width = pillar_width
        self.inner_depth = inner_depth
        self.outer_depth = outer_depth
        self.frame_width = frame_width
        self.frame_depth = frame_depth
        self.window_ratio = window_ratio
        self.window_count = window_count
        self.split_top = split_top
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsWindows(
            properties.windows_around_section_height,
            properties.windows_around_section_width,
            properties.windows_around_pillar_width,
            properties.windows_around_inner_depth,
            properties.windows_around_outer_depth,
            properties.window_frame_width,
            properties.window_frame_depth,
            properties.window_ratio,
            properties.window_count,
            properties.window_split_top
        )
        return params
    # end from_ui
# end ParamsWindowsAround


class ParamsRoof:
    def __init__(self, offset_width: float, offset_wedge: float, height: float):
        self.offset_width = offset_width
        self.offset_wedge = offset_wedge
        self.height = height
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsRoof(
            properties.roof_offset_width,
            properties.roof_offset_wedge,
            properties.roof_height
        )
        return params
    # end from_ui
# end ParamsRoof


def gen_mesh_floor_separator(context: bpy.types.Context, footprint: list,
                             section_mesh: bpy.types.Mesh) -> bpy.types.Object:
    """
        Creates the floor separator object
        floor separator will be placed at the origin (0, 0, 0)
    Args:
        context: bpy.types.Context
        footprint: list(tuple(x,y,z)) - building footprint
        section_mesh: cross section/side profile of the separator
    Returns:
        bpy.types.Object - single separator object placed at origin
    """

    # extrude the section along the footprint to create the separator
    m = Utils.extrude_along_edges(section_mesh, footprint, True)

    # create a new object, link it to the scene and return it
    obj = bpy.data.objects.new("PBGFloorSeparator", m)
    context.scene.objects.link(obj)
    return obj
# end gen_mesh_floor_separator


def gen_mesh_pillar(context: bpy.types.Context, params_pillar: ParamsPillar, params_general: GenLayout.ParamsGeneral,
                    floor_separator_mesh) -> bpy.types.Object:
    """
        Creates the pillar object
        pillar will be placed ar the origin (0, 0, 0)
    Args:
        context: bpy.types.Context
        params_pillar: instance of the ParamsPillar class
        params_general: instance of the ParamsGeneral class
        floor_separator_mesh: cross section/side profile of the separator
    Returns:
        Pillar object
    """
    bm = bmesh.new()

    if params_pillar.include_floor_separator:
        # add separator section mesh to bmesh and move it to the appropriate place (up on Z)
        bm.from_mesh(floor_separator_mesh)
        vec_trans = (0.0, 0.0, params_general.floor_height - params_general.separator_height)
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.translate(bm, vec=vec_trans, verts=bm.verts, space=mat_loc)
    else:
        # we don't have a separator mesh, add a straight line
        m = bpy.data.meshes.new(name="PBGPillarSeparatorSection")
        verts = list()
        edges = list()
        verts.append((0.0, 0.0, params_general.floor_height - params_general.separator_height))
        verts.append((0.0, 0.0, params_general.floor_height))
        edges.append((0, 1))
        m.from_pydata(verts, edges, [])
        bm.from_mesh(m)
    # end if

    if params_pillar.offset_size > 0:
        # generate a pillar_section mesh
        pillar_offset_params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
        pillar_offset_section = GenUtils.gen_section_element_list(pillar_offset_params)
        pillar_offset_mesh = GenUtils.gen_section_mesh(pillar_offset_section, params_pillar.offset_size,
                                                       params_pillar.offset_size)
        # add it to new bmesh
        bm_offset = bmesh.new()
        bm_offset.from_mesh(pillar_offset_mesh)

        # remove last vertex
        bm_offset.verts.ensure_lookup_table()
        last_vert = bm_offset.verts[len(bm_offset.verts) - 1]
        bm_offset.verts.remove(last_vert)

        # move up on Z, and on -Y for offset.
        vec_trans = (0.0, -params_pillar.offset_size, params_general.floor_height -
                     params_general.separator_height - params_pillar.offset_size)
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.translate(bm_offset, vec=vec_trans, verts=bm_offset.verts, space=mat_loc)

        # duplicate, flip and move down
        mat_loc = mathutils.Matrix.Translation((0.0, params_pillar.offset_size, - params_general.floor_height +
                                                params_general.separator_height +
                                                params_pillar.offset_size))
        geom_to_duplicate = bm_offset.verts[:] + bm_offset.edges[:] + bm_offset.faces[:]
        ret_dup = bmesh.ops.duplicate(bm_offset, geom=geom_to_duplicate)
        verts_to_transform = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.scale(bm_offset, vec=(1.0, 1.0, -1.0), space=mat_loc, verts=verts_to_transform)
        z_dist = (params_general.floor_height - params_general.separator_height -
                  params_pillar.offset_height - 2 * params_pillar.offset_size)
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.translate(bm_offset, vec=(0.0, 0.0, - z_dist), verts=verts_to_transform, space=mat_loc)

        # add filler between the two sections and below the lower section
        m_filler = bpy.data.meshes.new("PBGPillarFiller")
        m_filler_verts = list()
        m_filler_edges = list()
        m_filler_verts.append((0.0, 0.0, 0.0))
        m_filler_verts.append((0.0, 0.0, params_pillar.offset_height))
        m_filler_edges.append((0, 1))
        m_filler_verts.append((0.0, -params_pillar.offset_size,
                               params_pillar.offset_height + params_pillar.offset_size))
        m_filler_verts.append((0.0, -params_pillar.offset_size, params_general.floor_height -
                               params_general.separator_height - params_pillar.offset_size))
        m_filler_edges.append((2, 3))
        m_filler.from_pydata(m_filler_verts, m_filler_edges, [])

        # add the filler to bmesh
        bm_offset.from_mesh(m_filler)

        # bmesh to mesh and append to existing bmesh
        m_offset = bpy.data.meshes.new("PBGPillarMesh")
        bm_offset.to_mesh(m_offset)
        bm_offset.free()
        bm.from_mesh(m_offset)
    else:
        m = bpy.data.meshes.new("PBGPillarMesh")
        mesh_filler_verts = list()
        mesh_filler_edges = list()
        mesh_filler_verts.append((0.0, 0.0, 0.0))
        mesh_filler_verts.append((0.0, 0.0, params_general.floor_height - params_general.separator_height))
        mesh_filler_edges.append((0, 1))
        m.from_pydata(mesh_filler_verts, mesh_filler_edges, [])
        bm.from_mesh(m)
    # end if

    # remove doubles before extruding
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

    # create the horizontal layout for extruding along
    layout = list()
    layout.append((-0.5 * params_pillar.width, 0.0, 0.0))
    if params_pillar.chamfer > 0:
        layout.append((-0.5 * params_pillar.width,
                       params_pillar.depth - params_pillar.chamfer, 0.0))
        layout.append((-0.5 * params_pillar.width + params_pillar.chamfer,
                       params_pillar.depth, 0.0))
        layout.append((0.5 * params_pillar.width - params_pillar.chamfer,
                       params_pillar.depth, 0.0))
        layout.append((0.5 * params_pillar.width,
                       params_pillar.depth - params_pillar.chamfer, 0.0))
    else:
        layout.append((-0.5 * params_pillar.width, params_pillar.depth, 0.0))
        layout.append((0.5 * params_pillar.width, params_pillar.depth, 0.0))
    # end if
    layout.append((0.5 * params_pillar.width, 0.0, 0.0))

    # convert to mesh, extrude along, free bmesh
    m = bpy.data.meshes.new("PBGPillarSection")
    bm.to_mesh(m)
    bm.free()
    m_pillar_extruded = Utils.extrude_along_edges(m, layout, False)

    # create object and link it to the scene, return the object
    obj = bpy.data.objects.get("PBGPillar")
    if obj is not None:
        context.scene.objects.unlink(obj)
        bpy.data.objects.remove(obj)
    obj = bpy.data.objects.new("PBGPillar", m_pillar_extruded)
    context.scene.objects.link(obj)
    return obj
# end generate_pillars


def gen_mesh_wall(context: bpy.types.Context, wall_loops: list, section_mesh: bpy.types.Mesh) -> bpy.types.Object:
    """
    Creates the wall object
    All walls will be generated, and there is no need to duplicate/move them
    Args:
        context: bpy.types.Context
        wall_loops: list(list(tuple(x,y,z))) - list of wall loops, result of gen_layout.
        section_mesh: cross section/side profile of the wall
    Returns:
        The wall object
    """

    bm = bmesh.new()
    for loop in wall_loops:
        mesh = Utils.extrude_along_edges(section_mesh.copy(), loop, False)
        bm.from_mesh(mesh)
    # end for

    # check if the object for walls already exists
    obj = bpy.data.objects.get("PBGWalls")
    if obj is not None:
        context.scene.objects.unlink(obj)
        bpy.data.objects.remove(obj)
    # end if

    m = bpy.data.meshes.new("PBGWall")
    bm.to_mesh(m)
    bm.free()

    # link the created object to the scene
    obj = bpy.data.objects.new("PBGWalls", m)
    context.scene.objects.link(obj)
    return obj
# end gen_mesh_walls


def gen_mesh_offset_wall(context: bpy.types.Context, footprint: list, params_general: GenLayout.ParamsGeneral,
                         params_walls: ParamsWalls) -> bpy.types.Object:
    """
    Generate Floor offset wall object
    Args:
        context: bpy.types.Context
        footprint: list(tuple(x,y,z)) - building footprint
        params_general: instance of GenLayout.ParamsGeneral class
        params_walls: instance of paramsWalls class
    Returns:
        the Floor offset wall object
    """
    # generate wall section mesh
    m_section = GenUtils.gen_wall_section_mesh(params_walls.offset_type, params_general.floor_offset,
                                               params_walls.offset_section_size,
                                               params_walls.offset_mortar_size,
                                               params_walls.offset_row_count)
    bm = bmesh.new()
    bm.from_mesh(m_section)

    # offset it on y axis
    vec_trans = mathutils.Vector((0.0, params_walls.offset_size, 0.0))
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    bmesh.ops.translate(bm, vec=vec_trans, verts=bm.verts, space=mat_loc)

    # append the top edge
    verts = list()
    edges = list()
    verts.append((0.0, 0.0, params_general.floor_offset))
    verts.append((0.0, params_walls.offset_size, params_general.floor_offset))
    edges.append((0, 1))
    m_edge = bpy.data.meshes.new("PBGWallOffsetEdge")
    m_edge.from_pydata(verts, edges, [])
    bm.from_mesh(m_edge)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    # convert to mesh, extrude along
    m = bpy.data.meshes.new("PbgWallOffset")
    bm.to_mesh(m)
    bm.free()
    m_extruded = Utils.extrude_along_edges(m, footprint, True)

    # check if the object for walls already exists
    obj = bpy.data.objects.get("PBGOffset")
    if obj is not None:
        context.scene.objects.unlink(obj)
        bpy.data.objects.remove(obj)
    # end if

    # link the created object to the scene
    obj = bpy.data.objects.new("PBGOffset", m_extruded)
    context.scene.objects.link(obj)
    return obj
# end gen_mesh_offset_wall


# TODO: this uses pretty much everything from the gen_mesh_windows_under, with slight value changes
# TODO: extract these parts to separate functions *later*
def gen_mesh_windows_above(context: bpy.types.Context, params_general: GenLayout.ParamsGeneral,
                           params_window_above: ParamsWindowsAbove, wall_section_mesh: bpy.types.Mesh):
    bm = bmesh.new()
    if params_window_above.type == "WALL":
        # start with the wall mesh
        bm.from_mesh(wall_section_mesh)

        # bisect on offset_height+window_height, remove outer geometry
        # NOTE, the normal is -Z, in other function it's +Z
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        plane_co = (0.0, 0.0, params_general.window_offset + params_general.window_height)
        plane_no = (0.0, 0.0, -1.0)
        bmesh.ops.bisect_plane(bm, geom=geom, clear_outer=True, plane_co=plane_co, plane_no=plane_no)

        # move it on x axis half the width
        vec_trans = (-0.5 * params_general.window_width, 0.0, 0.0)
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.translate(bm, vec=vec_trans, verts=bm.verts, space=mat_loc)

        # extrude on x axis, to fill width
        vec_ext = (params_general.window_width, 0.0, 0.0)
        ret_extrude = bmesh.ops.extrude_edge_only(bm, edges=bm.edges, use_select_history=True)
        verts_to_translate = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=verts_to_translate, vec=vec_ext, space=mat_loc)
    else:
        # make the cube, same for all types
        # create the first loop, append it to bmesh
        if params_general.generate_separator == True:
            co_z_end = params_general.floor_height - params_general.separator_height
        else:
            co_z_end = params_general.floor_height
        # end if
        co_z_start =  params_general.window_offset + params_general.window_height
        verts = list()
        verts.append((-0.5*params_general.window_width, 0.0, co_z_start))
        verts.append((-0.5*params_general.window_width, 0.0, co_z_end))
        verts.append((0.5*params_general.window_width, 0.0, co_z_end))
        verts.append((0.5*params_general.window_width, 0.0, co_z_start))
        m = bpy.data.meshes.new("PBGWindowsAboveMesh")
        m.from_pydata(verts, [(0, 1), (1, 2), (2, 3), (3, 0)], [])
        bm.from_mesh(m)

        # extrude on y forwards
        vec_ext = (0.0, params_window_above.depth, 0.0)
        ret_ext = bmesh.ops.extrude_edge_only(bm, edges=bm.edges, use_select_history=True)
        verts_to_translate = [ele for ele in ret_ext["geom"] if isinstance(ele, bmesh.types.BMVert)]
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.translate(bm, verts=verts_to_translate, vec=vec_ext, space=mat_loc)

        # extrude, scale down so it fits width and height
        size_z = co_z_end - co_z_start
        scale_x = (params_general.window_width - 2*params_window_above.width)/params_general.window_width
        scale_z = (size_z - 2*params_window_above.height)/size_z
        edges_to_extrude = [ele for ele in ret_ext["geom"] if isinstance(ele, bmesh.types.BMEdge)]
        ret_ext = bmesh.ops.extrude_edge_only(bm, edges=edges_to_extrude, use_select_history=True)
        verts_to_scale = [ele for ele in ret_ext["geom"] if isinstance(ele, bmesh.types.BMVert)]
        mat_loc = mathutils.Matrix.Translation((0.0, -params_window_above.depth, -co_z_end + 0.5*size_z))
        bmesh.ops.scale(bm, space=mat_loc, verts=verts_to_scale, vec=(scale_x, 1.0, scale_z))

        # extrude inwards
        edges_to_extrude = [ele for ele in ret_ext["geom"] if isinstance(ele, bmesh.types.BMEdge)]
        ret_ext = bmesh.ops.extrude_edge_only(bm, edges=edges_to_extrude, use_select_history=True)
        verts_to_translate = [ele for ele in ret_ext["geom"] if isinstance(ele, bmesh.types.BMVert)]
        vec_ext = (0.0, -params_window_above.inset_depth, 0.0)
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.translate(bm, verts=verts_to_translate, vec=vec_ext, space=mat_loc)

        # make a face
        bmesh.ops.contextual_create(bm, geom=ret_ext["geom"])

        if params_window_above.type in {"CYCLOID", "SINE"}:
            period_width = (params_general.window_width - 2*params_window_above.width)/params_window_above.period_count
            bm_filler = bmesh.new()

            # generate single sine/cycloid
            if params_window_above.type == "CYCLOID":
                # create a single vert, spin it to make half circle
                v_co_x = -0.5*params_general.window_width + params_window_above.width
                v_co_y = params_window_above.depth
                v_co_z = params_window_above.height + co_z_start
                bmesh.ops.create_vert(bm_filler, co=(v_co_x, v_co_y, v_co_z))
                geom = bm_filler.verts[:]
                bmesh.ops.spin(bm_filler, geom=geom, angle=math.radians(180), steps=12, axis=(0.0, 0.0, 1.0),
                               cent=(v_co_x + period_width/2, v_co_y, v_co_z))
                sf = (2*params_window_above.amplitude)/period_width
                mat_loc = mathutils.Matrix.Translation((0.0, -params_window_above.depth, 0.0))
                bmesh.ops.scale(bm_filler, vec=(1.0, sf, 1.0), space=mat_loc, verts=bm_filler.verts)
            else:
                # create a single sine wave
                co_start_x = -0.5 * params_general.window_width + params_window_above.width
                co_y = params_window_above.depth - 0.5 * params_window_above.amplitude
                verts = list()
                edges = list()
                n = 12
                for i in range(0, n + 1):
                    v_co_x = co_start_x + period_width * (i / n)
                    v_co_y = co_y + math.sin(2 * math.pi * (i / n)) * params_window_above.amplitude * 0.5
                    verts.append((v_co_x, v_co_y, params_window_above.height + co_z_start))
                    if i > 0:
                        edges.append((i - 1, i))
                # end for
                m = bpy.data.meshes.new("PBGWindowsAboveMeshSine")
                m.from_pydata(verts, edges, [])
                bm_filler.from_mesh(m)
            # end if
            # extrude on z
            ret_ext = bmesh.ops.extrude_edge_only(bm_filler, edges=bm_filler.edges, use_select_history=True)
            verts_to_translate = [ele for ele in ret_ext["geom"] if isinstance(ele, bmesh.types.BMVert)]
            vec_trans = (0.0, 0.0, size_z - 2*params_window_above.height)
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            bmesh.ops.translate(bm_filler, vec=vec_trans, space=mat_loc, verts=verts_to_translate)

            # duplicate and move on x
            geom = bm_filler.verts[:] + bm_filler.edges[:] + bm_filler.faces[:]
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            for i in range(1, params_window_above.period_count):
                ret_dup = bmesh.ops.duplicate(bm_filler, geom=geom)
                verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
                bmesh.ops.translate(bm_filler, vec=(i*period_width, 0.0, 0.0), space=mat_loc, verts=verts_to_translate)
            # end for

            # remove doubles
            bmesh.ops.remove_doubles(bm_filler, verts=bm_filler.verts, dist=0.0001)

            # append to original bmesh
            m_filler = bpy.data.meshes.new("PBGWindowsAboveSineCycle")
            bm_filler.to_mesh(m_filler)
            bm_filler.free()
            bm.from_mesh(m_filler)
        else:
            bm_filler = bmesh.new()
            # create layout for extruding
            layout = list()
            size_x = params_general.window_width - 2*params_window_above.width
            size_y = size_z - 2*params_window_above.height
            layout.append((0.5 * size_x, 0.5 * size_y, 0.0))
            layout.append((-0.5 * size_x, 0.5 * size_y, 0.0))
            layout.append((-0.5 * size_x, -0.5 * size_y, 0.0))
            layout.append((0.5 * size_x, -0.5 * size_y, 0.0))

            # create a section and extrude it in x-y plane
            params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
            sequence = GenUtils.gen_section_element_list(params)
            m_filler = GenUtils.gen_section_mesh(sequence, params_window_above.simple_depth,
                                                 params_window_above.simple_width)
            bm_filler.from_mesh(m_filler)
            bm_filler.verts.ensure_lookup_table()
            last_vert = bm_filler.verts[len(bm_filler.verts) - 1]
            bm_filler.verts.remove(last_vert)
            bm_filler.to_mesh(m_filler)
            m_extruded = Utils.extrude_along_edges(m_filler, layout, True)
            bm_filler.free()
            bm_filler = bmesh.new()
            bm_filler.from_mesh(m_extruded)

            # create the filler face
            verts = list()
            v_co_x = 0.5 * size_x - params_window_above.simple_width
            v_co_y = 0.5 * size_y - params_window_above.simple_width
            verts.append((v_co_x, v_co_y, params_window_above.simple_depth))
            verts.append((-v_co_x, v_co_y, params_window_above.simple_depth))
            verts.append((-v_co_x, -v_co_y, params_window_above.simple_depth))
            verts.append((v_co_x, -v_co_y, params_window_above.simple_depth))
            m_face = bpy.data.meshes.new("PBGWindowsAboveMeshSimpleFillFace")
            m_face.from_pydata(verts, [(0, 1), (1, 2), (2, 3), (3, 0)], [(0, 1, 2, 3)])
            bm_filler.from_mesh(m_face)
            bmesh.ops.remove_doubles(bm_filler, verts=bm_filler.verts, dist=0.0001)

            # rotate, move and offset on y
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            mat_rot = mathutils.Matrix.Rotation(math.radians(-90), 3, "X")
            bmesh.ops.rotate(bm_filler, cent=(0, 0, 0), matrix=mat_rot, verts=bm_filler.verts, space=mat_loc)
            vec_trans = (0.0, params_window_above.depth, co_z_start + 0.5*size_z)
            bmesh.ops.translate(bm_filler, vec=vec_trans, space=mat_loc, verts=bm_filler.verts)

            # append to main bmesh
            m_filler = bpy.data.meshes.new("PBGWindowsAboveSineCycle")
            bm_filler.to_mesh(m_filler)
            bm_filler.free()
            bm.from_mesh(m_filler)
        # end if
    # end if

    # recalculate normals
    # TODO: normals are sometimes recalculated differently when height changes while using "WALL" type.
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # convert to mesh and create object
    m = bpy.data.meshes.new("PBGWindowsAboveMesh")
    bm.to_mesh(m)
    bm.free()
    ob = bpy.data.objects.get("PBGWindowsAbove")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGWindowsAbove", m)
    context.scene.objects.link(new_obj)
    return new_obj
# end gen_mesh_windows_above


# TODO: refactor naming a bit in this function, extract some things to separate functions...
def gen_mesh_windows_under(context: bpy.types.Context, params_general: GenLayout.ParamsGeneral,
                           params_window_under: ParamsWindowsUnder, wall_section_mesh: bpy.types.Mesh):
    # generate the mesh, centered, lowest point at 0
    windows_under_bmesh = bmesh.new()
    if params_window_under.type == "WALL":
        # start with the wall mesh
        windows_under_bmesh.from_mesh(wall_section_mesh)

        # bisect it on offset height, remove the outer geometry
        geom = windows_under_bmesh.verts[:] + windows_under_bmesh.edges[:] + windows_under_bmesh.faces[:]
        plane_co = (0.0, 0.0, params_general.window_offset)
        plane_no = (0.0, 0.0, 1.0)
        bmesh.ops.bisect_plane(windows_under_bmesh, geom=geom, clear_outer=True, plane_co=plane_co, plane_no=plane_no)

        # move it on x axis half the width
        vec_trans = (-0.5 * params_general.window_width, 0.0, 0.0)
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.translate(windows_under_bmesh, vec=vec_trans, verts=windows_under_bmesh.verts, space=mat_loc)

        # extrude on x axis, to fill width
        vec_ext = (params_general.window_width, 0.0, 0.0)
        ret_extrude = bmesh.ops.extrude_edge_only(windows_under_bmesh, edges=windows_under_bmesh.edges,
                                                  use_select_history=True)
        verts_to_translate = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.translate(windows_under_bmesh, verts=verts_to_translate, vec=vec_ext, space=mat_loc)
    else:
        # make the cube, it is same for all types (SINE, SIMPLE, PILLARS)
        # first loop, append to bmesh...
        verts = list()
        verts.append((-0.5*params_general.window_width, 0.0, 0.0))
        verts.append((-0.5*params_general.window_width, 0.0, params_general.window_offset))
        verts.append((0.5*params_general.window_width, 0.0, params_general.window_offset))
        verts.append((0.5*params_general.window_width, 0.0, 0.0))
        m = bpy.data.meshes.new("PBGWindowsUnderMesh")
        m.from_pydata(verts, [(0, 1), (1, 2), (2, 3), (3, 0)], [])
        windows_under_bmesh.from_mesh(m)

        # extrude on y forwards
        vec_ext = (0.0, params_window_under.depth, 0.0)
        ret_extrude = bmesh.ops.extrude_edge_only(windows_under_bmesh, edges=windows_under_bmesh.edges,
                                                  use_select_history=True)
        verts_to_translate = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.translate(windows_under_bmesh, verts=verts_to_translate, vec=vec_ext, space=mat_loc)

        # extrude, scale down so it fits the width and height
        scale_x = (params_general.window_width - 2*params_window_under.width)/params_general.window_width
        scale_z = (params_general.window_offset - 2*params_window_under.height)/params_general.window_offset
        edges_to_extrude = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMEdge)]
        ret_extrude = bmesh.ops.extrude_edge_only(windows_under_bmesh, edges=edges_to_extrude, use_select_history=True)
        verts_to_scale = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        mat_loc = mathutils.Matrix.Translation((0.0, -params_window_under.depth, -0.5*params_general.window_offset))
        bmesh.ops.scale(windows_under_bmesh, space=mat_loc, verts=verts_to_scale, vec=(scale_x, 0, scale_z))

        # extrude inwards
        edges_to_extrude = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMEdge)]
        ret_extrude = bmesh.ops.extrude_edge_only(windows_under_bmesh, edges=edges_to_extrude, use_select_history=True)
        verts_to_translate = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        vec_ext = (0.0, -params_window_under.inset_depth, 0.0)
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.translate(windows_under_bmesh, verts=verts_to_translate, vec=vec_ext, space=mat_loc)

        # make a face
        bmesh.ops.contextual_create(windows_under_bmesh, geom=ret_extrude["geom"])

        if params_window_under.type in {"CYCLOID", "SINE"}:
            period_width = (params_general.window_width - 2*params_window_under.width)/params_window_under.period_count
            bm = bmesh.new()
            # create a single vert, spin it to make half a circle
            if params_window_under.type == "CYCLOID":
                v_co_x = -0.5*params_general.window_width + params_window_under.width
                v_co_y = params_window_under.depth
                v_co_z = params_window_under.height
                bmesh.ops.create_vert(bm, co=(v_co_x, v_co_y, v_co_z))
                geom = bm.verts[:]
                bmesh.ops.spin(bm, geom=geom, angle=math.radians(180), steps=12, axis=(0.0, 0.0, 1.0),
                               cent=(v_co_x + period_width/2, v_co_y, v_co_z))
                sf = (params_window_under.amplitude*2)/period_width
                mat_loc = mathutils.Matrix.Translation((0.0, -params_window_under.depth, 0.0))
                bmesh.ops.scale(bm, vec=(1.0, sf, 1.0), space=mat_loc, verts=bm.verts)
            else:
                co_start_x = -0.5*params_general.window_width + params_window_under.width
                co_y = params_window_under.depth - 0.5*params_window_under.amplitude
                verts = list()
                edges = list()
                n = 12
                for i in range(0, n+1):
                    v_co_x = co_start_x + period_width*(i/n)
                    v_co_y = co_y + math.sin(2*math.pi*(i/n))*params_window_under.amplitude*0.5
                    verts.append((v_co_x, v_co_y, params_window_under.height))
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
            vec_trans = (0.0, 0.0, params_general.window_offset - 2*params_window_under.height)
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            bmesh.ops.translate(bm, verts=verts_to_translate, vec=vec_trans, space=mat_loc)

            # duplicate and move on x
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            for i in range(1, params_window_under.period_count):
                ret_dup = bmesh.ops.duplicate(bm, geom=geom)
                verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
                bmesh.ops.translate(bm, vec=(i*period_width, 0.0, 0.0), space=mat_loc, verts=verts_to_translate)

            # remove doubles
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

            # append to original bmesh
            sine_cycle_mesh = bpy.data.meshes.new("PBGWindowsUnderMeshSineCycle")
            bm.to_mesh(sine_cycle_mesh)
            bm.free()
            windows_under_bmesh.from_mesh(sine_cycle_mesh)
        elif params_window_under.type == "PILLARS":
            # create a single pillar section(quite a lot of work here)
            params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
            sequence = GenUtils.gen_section_element_list(params)
            mesh = GenUtils.gen_section_mesh(sequence, params_window_under.pillar_base_height,
                                             0.5*params_window_under.pillar_base_diameter
                                             - 0.5*params_window_under.pillar_min_diameter)
            bm = bmesh.new()
            bm.from_mesh(mesh)
            bm.verts.ensure_lookup_table()
            last_vert = bm.verts[len(bm.verts) - 1]
            bm.verts.remove(last_vert)

            # move, on y and z, so the middle is on the bottom and goes through the center.
            vec_trans = (0.0, 0.5 * params_window_under.pillar_min_diameter,
                         params_general.window_offset - 2 * params_window_under.height
                         - params_window_under.pillar_base_height)
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            bmesh.ops.translate(bm, vec=vec_trans, space=mat_loc, verts=bm.verts)

            # generate pillar mesh
            verts = list()
            edges = list()
            start_y = vec_trans[1]
            start_z = vec_trans[2]
            end_z = 0.5*params_general.window_offset - params_window_under.height
            end_y = 0.5*params_window_under.pillar_max_diameter
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
            width = params_general.window_width - 2*params_window_under.width
            pillar_count = int(width/params_window_under.pillar_base_diameter)
            total_pillar_width = width/pillar_count

            # duplicate original geometry and translate
            geom_initial = bm.verts[:] + bm.edges[:] + bm.faces[:]
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            for i in range(0, pillar_count):
                v_co_x = -0.5*width + total_pillar_width*(i+0.5)
                ret_dup = bmesh.ops.duplicate(bm, geom=geom_initial)
                verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
                v_co_y = 0.5*(params_window_under.depth + (params_window_under.depth - params_window_under.inset_depth))
                vec_trans = (v_co_x, v_co_y, params_window_under.height)
                bmesh.ops.translate(bm, vec=vec_trans, verts=verts_to_translate, space=mat_loc)

            # remove original geometry
            bmesh.ops.delete(bm, geom=geom_initial, context=1)

            # append to original bmesh
            pillar_mesh = bpy.data.meshes.new("PBGWindowsUnderMeshPillar")
            bm.to_mesh(pillar_mesh)
            bm.free()
            windows_under_bmesh.from_mesh(pillar_mesh)
        else:
            # create layout for extruding
            layout = list()
            size_x = params_general.window_width - 2*params_window_under.width
            size_y = params_general.window_offset - 2*params_window_under.height
            layout.append((0.5 * size_x, 0.5 * size_y, 0.0))
            layout.append((-0.5 * size_x, 0.5 * size_y, 0.0))
            layout.append((-0.5 * size_x, -0.5 * size_y, 0.0))
            layout.append((0.5 * size_x, -0.5 * size_y, 0.0))

            # create a section and extrude it in x-y plane
            params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
            sequence = GenUtils.gen_section_element_list(params)
            mesh = GenUtils.gen_section_mesh(sequence, params_window_under.simple_depth,
                                             params_window_under.simple_width)
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
            v_co_x = 0.5 * size_x - params_window_under.simple_width
            v_co_y = 0.5 * size_y - params_window_under.simple_width
            verts.append((v_co_x, v_co_y, params_window_under.simple_depth))
            verts.append((-v_co_x, v_co_y, params_window_under.simple_depth))
            verts.append((-v_co_x, -v_co_y, params_window_under.simple_depth))
            verts.append((v_co_x, -v_co_y, params_window_under.simple_depth))
            m = bpy.data.meshes.new("PBGWindowsUnderMeshSimpleFillFace")
            m.from_pydata(verts, [(0, 1), (1, 2), (2, 3), (3, 0)], [(0, 1, 2, 3)])
            simple_bmesh.from_mesh(m)
            bmesh.ops.remove_doubles(simple_bmesh, verts=simple_bmesh.verts, dist=0.0001)

            # rotate, move and offset on y
            mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
            mat_rot = mathutils.Matrix.Rotation(math.radians(-90), 3, "X")

            # rotate it, move to the desired position, append to main bmesh
            bmesh.ops.rotate(simple_bmesh, cent=(0, 0, 0), matrix=mat_rot, verts=simple_bmesh.verts, space=mat_loc)
            vec_trans = (0.0, params_window_under.depth, 0.5*params_general.window_offset)
            bmesh.ops.translate(simple_bmesh, vec=vec_trans, space=mat_loc, verts=simple_bmesh.verts)

            simple_mesh = bpy.data.meshes.new("PBGWindowsUnderMeshSimple")
            simple_bmesh.to_mesh(simple_mesh)
            simple_bmesh.free()
            windows_under_bmesh.from_mesh(simple_mesh)
    # end if

    # recalculate normals
    # TODO: normals are sometimes recalculated differently when height changes while using "WALL" type.
    bmesh.ops.recalc_face_normals(windows_under_bmesh, faces=windows_under_bmesh.faces)

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
    return new_obj
# end gen_mesh_windows_under


def gen_mesh_stairs(context: bpy.types.Context, params_general: GenLayout.ParamsGeneral,
                    params_footprint: GenLayout.ParamsFootprint, params_stairs: ParamsStairs):
    # generate the profile to be extruded
    verts = list()
    edges = list()
    stair_height = params_general.floor_offset / params_stairs.stair_count
    verts.append((0, 0, params_general.floor_offset))
    for i in range(0, params_stairs.stair_count):
        verts.append((0, (i+1)*params_stairs.width, params_general.floor_offset-i*stair_height))
        verts.append((0, (i+1)*params_stairs.width, params_general.floor_offset-(i+1)*stair_height))
    for i in range(0, len(verts)-1):
        edges.append((i, i+1))
    m_section = bpy.data.meshes.new("PBGStairSection")
    m_section.from_pydata(verts, edges, [])

    # generate the layout
    layout = list()
    layout.append((-0.5*params_stairs.layout_width, 0.5*params_footprint.building_depth, 0))
    layout.append((-0.5*params_stairs.layout_width, 0.5*params_footprint.building_depth+params_stairs.layout_depth, 0))
    layout.append((0.5*params_stairs.layout_width, 0.5*params_footprint.building_depth+params_stairs.layout_depth, 0))
    layout.append((0.5*params_stairs.layout_width, 0.5*params_footprint.building_depth, 0))

    # extrude, create bmesh
    m = Utils.extrude_along_edges(m_section, layout, False)
    bm = bmesh.new()
    bm.from_mesh(m)

    # generate top filler face, append to bmesh
    verts.clear()
    for vert in layout:
        verts.append((vert[0], vert[1], params_general.floor_offset))
    m_filler_face = bpy.data.meshes.new("PBGStairFiller")
    m_filler_face.from_pydata(verts, [(0, 1), (1, 2), (2, 3), (3, 0)], [(0, 1, 2, 3)])
    bm.from_mesh(m_filler_face)

    # remove doubles
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

    m = bpy.data.meshes.new("PBGStairs")
    bm.to_mesh(m)
    bm.free()
    ob = bpy.data.objects.get("PBGStairs")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGStairs", m)
    context.scene.objects.link(new_obj)
    return new_obj
# end gen_mesh_stairs


def gen_mesh_windows_around(context: bpy.types.Context, params_general: GenLayout.ParamsGeneral,
                            params_windows: ParamsWindows):
    bm = bmesh.new()
    # create section
    params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
    sequence = GenUtils.gen_section_element_list(params)
    mesh = GenUtils.gen_section_mesh(sequence, params_windows.section_height,
                                     params_windows.section_width)
    # create layout
    layout = list()
    layout.append((-0.5 * params_general.window_width, -params_windows.inner_depth, 0.0))
    layout.append((-0.5 * params_general.window_width, params_windows.outer_depth, 0.0))
    layout.append((0.5 * params_general.window_width, params_windows.outer_depth, 0.0))
    layout.append((0.5 * params_general.window_width, -params_windows.inner_depth, 0.0))

    # extrude along layout
    m = Utils.extrude_along_edges(mesh, layout, False)
    bm.from_mesh(m)

    # make filler faces
    verts = layout.copy()
    for vert in layout:
        verts.append((vert[0], vert[1], params_windows.section_height))
    m_faces = bpy.data.meshes.new("PBGWindowsAroundFaces")
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4)]
    faces = [(0, 1, 2, 3), (4, 5, 6, 7)]
    m_faces.from_pydata(verts, edges, faces)
    bm.from_mesh(m_faces)

    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

    #  move on Z to bottom
    vec_trans = (0.0, 0.0, params_general.window_offset)
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    bmesh.ops.translate(bm, vec=vec_trans, space=mat_loc, verts=bm.verts)

    # duplicate, move on Z to top
    geom_to_duplicate = bm.verts[:] + bm.edges[:] + bm.faces[:]
    ret_dup = bmesh.ops.duplicate(bm, geom=geom_to_duplicate)
    verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
    vec_trans = (0.0, 0.0, params_general.window_height - params_windows.section_height)
    bmesh.ops.translate(bm, vec=vec_trans, space=mat_loc, verts=verts_to_translate)

    # add cube, scale, move to position on -x, y and z
    bm_pillars = bmesh.new()
    ret_create = bmesh.ops.create_cube(bm_pillars, size=1.0)
    verts_to_transform = ret_create["verts"]
    vec_scale = (params_windows.pillar_width,
                 params_windows.outer_depth + params_windows.inner_depth,
                 params_general.window_height - 2*params_windows.section_height)
    bmesh.ops.scale(bm_pillars, vec=vec_scale, space=mat_loc, verts=verts_to_transform)
    vec_trans = (-0.5*params_general.window_width + 0.5*params_windows.pillar_width,
                 0.5*(params_windows.outer_depth - params_windows.inner_depth),
                 0.5*params_general.window_height + params_general.window_offset)
    bmesh.ops.translate(bm_pillars, vec=vec_trans, space=mat_loc, verts=verts_to_transform)

    # duplicate, move on x
    geom_to_duplicate = bm_pillars.verts[:] + bm_pillars.edges[:] + bm_pillars.faces[:]
    ret_dup = bmesh.ops.duplicate(bm_pillars, geom=geom_to_duplicate)
    verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
    vec_trans = (params_general.window_width - params_windows.pillar_width, 0.0, 0.0)
    bmesh.ops.translate(bm_pillars, vec=vec_trans, space=mat_loc, verts=verts_to_translate)

    # join meshes
    m_pillars = bpy.data.meshes.new("PBGWindowPillars")
    bm_pillars.to_mesh(m_pillars)
    bm_pillars.free()

    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    bm.from_mesh(m_pillars)

    # create object
    m = bpy.data.meshes.new("PBGWindowAround")
    bm.to_mesh(m)
    bm.free()
    ob = bpy.data.objects.get("PBGWindowAround")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGWindowAround", m)
    context.scene.objects.link(new_obj)
    return new_obj
# end gen_mesh_windows_around


def gen_mesh_windows(context: bpy.types.Context, params_general: GenLayout.ParamsGeneral,
                     params_windows: ParamsWindows):
    # keep windows and frame in separate bmesh?
    bm = bmesh.new()
    frame_width = params_general.window_width - 2*params_windows.pillar_width
    frame_height = params_general.window_height - 2*params_windows.section_height
    frame_window_width = frame_width / params_windows.window_count

    # create section
    params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
    sequence = GenUtils.gen_section_element_list(params)
    m_section = GenUtils.gen_section_mesh(sequence, params_windows.frame_width,
                                          params_windows.frame_depth)
    bm_section = bmesh.new()
    bm_section.from_mesh(m_section)
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    mat_rot = mathutils.Matrix.Rotation(math.radians(-90), 3, "X")
    vec_trans = (0.0, -params_windows.frame_width, 0.0)
    bmesh.ops.rotate(bm_section, cent=(0, 0, 0), matrix=mat_rot, verts=bm_section.verts, space=mat_loc)
    bmesh.ops.translate(bm_section, vec=vec_trans, space=mat_loc, verts=bm_section.verts)
    bm_section.to_mesh(m_section)
    bm_section.free()

    # generate single layout for top and bottom, check for splits here
    layout_top = list()
    layout_bottom = list()

    m_bottom_glass = bpy.data.meshes.new("PBGWindowBottomGlass")
    m_top_glass = bpy.data.meshes.new("PBGWindowTopGlass")
    verts_bottom_glass = list()
    verts_top_glass = list()

    if params_windows.split_top == True:
        layout_top.append((0.5 * frame_width, frame_height*params_windows.window_ratio, 0))
        layout_top.append((0.5 * frame_width - frame_window_width, frame_height*params_windows.window_ratio, 0))
        layout_top.append((0.5 * frame_width - frame_window_width, frame_height, 0))
        layout_top.append((0.5 * frame_width, frame_height, 0))
    else:
        layout_top.append((0.5 * frame_width, frame_height * params_windows.window_ratio, 0))
        layout_top.append((-0.5 * frame_width, frame_height * params_windows.window_ratio, 0))
        layout_top.append((-0.5 * frame_width, frame_height, 0))
        layout_top.append((0.5 * frame_width, frame_height, 0))

    layout_bottom.append((0.5*frame_width, 0, 0))
    layout_bottom.append((0.5*frame_width - frame_window_width, 0, 0))
    layout_bottom.append((0.5*frame_width - frame_window_width, frame_height*params_windows.window_ratio, 0))
    layout_bottom.append((0.5*frame_width, frame_height*params_windows.window_ratio, 0))

    # create glass
    verts_top_glass.append((layout_top[0][0] - params_windows.frame_width,
                            layout_top[0][1] + params_windows.frame_width, 0.0))
    verts_top_glass.append((layout_top[1][0] + params_windows.frame_width,
                            layout_top[1][1] + params_windows.frame_width, 0.0))
    verts_top_glass.append((layout_top[2][0] + params_windows.frame_width,
                            layout_top[2][1] - params_windows.frame_width, 0.0))
    verts_top_glass.append((layout_top[3][0] - params_windows.frame_width,
                            layout_top[2][1] - params_windows.frame_width, 0.0))

    verts_bottom_glass.append((layout_bottom[0][0] - params_windows.frame_width,
                               layout_bottom[0][1] + params_windows.frame_width, 0.0))
    verts_bottom_glass.append((layout_bottom[1][0] + params_windows.frame_width,
                               layout_bottom[1][1] + params_windows.frame_width, 0.0))
    verts_bottom_glass.append((layout_bottom[2][0] + params_windows.frame_width,
                               layout_bottom[2][1] - params_windows.frame_width, 0.0))
    verts_bottom_glass.append((layout_bottom[3][0] - params_windows.frame_width,
                               layout_bottom[2][1] - params_windows.frame_width, 0.0))

    m_top_glass.from_pydata(verts_top_glass, [(0, 1), (1, 2), (2, 3), (3, 0)], [(0, 1, 2, 3)])
    m_bottom_glass.from_pydata(verts_bottom_glass, [(0, 1), (1, 2), (2, 3), (3, 0)], [(0, 1, 2, 3)])

    # extrude along layouts
    m_bottom = Utils.extrude_along_edges(m_section.copy(), layout_bottom, True)
    m_top = Utils.extrude_along_edges(m_section, layout_top, True)

    bm.from_mesh(m_bottom)
    bm.from_mesh(m_bottom_glass)
    if params_windows.split_top == True:
        bm.from_mesh(m_top)
        bm.from_mesh(m_top_glass)

    # duplicate and translate frames
    geom_orig = bm.verts[:] + bm.edges[:] + bm.faces[:]
    for i in range(1, params_windows.window_count):
        ret_dup = bmesh.ops.duplicate(bm, geom=geom_orig)
        verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        vec_trans = (-frame_window_width*i, 0, 0)
        bmesh.ops.translate(bm, vec=vec_trans, verts=verts_to_translate, space=mat_loc)

    if params_windows.split_top == False:
        bm.from_mesh(m_top)
        bm.from_mesh(m_top_glass)

    # rotate window, move on z
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    vec_trans = (0.0, -params_windows.inner_depth, params_general.window_offset + params_windows.section_height)
    mat_rot = mathutils.Matrix.Rotation(math.radians(90), 3, "X")
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mat_rot, verts=bm.verts, space=mat_loc)
    bmesh.ops.translate(bm, vec=vec_trans, space=mat_loc, verts=bm.verts)

    # create object
    m = bpy.data.meshes.new("PBGWindow")
    bm.to_mesh(m)
    bm.free()
    ob = bpy.data.objects.get("PBGWindow")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGWindow", m)
    context.scene.objects.link(new_obj)
    return new_obj
# end gen_mesh_windows


def gen_mesh_roof(context: bpy.types.Context, params_general: GenLayout.ParamsGeneral, footprint: list,
                  params_footprint: GenLayout.ParamsFootprint, params_roof: ParamsRoof):
    bm_roof = bmesh.new()
    # get verts on -x side, create edges
    verts = list()
    edges = list()
    if params_footprint.building_chamfer > 0:
        count = 4
        edges.append((0, 1))
        edges.append((1, 2))
        edges.append((2, 3))
    else:
        count = 2
        edges.append((0, 1))

    for i in range(0, count):
        verts.append((
            footprint[i][0],
            footprint[i][1],
            params_general.floor_offset + params_general.floor_height * (1 + params_general.floor_count)
        ))

    # create mesh, append to bmesh
    m_roof = bpy.data.meshes.new("PBGRoof")
    m_roof.from_pydata(verts, edges, [])
    bm_roof.from_mesh(m_roof)

    # extrude, merge, move to position
    ret_extrude = bmesh.ops.extrude_edge_only(bm_roof, edges=bm_roof.edges, use_select_history=True)
    verts_to_scale = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
    pos_x = 0.5*params_footprint.building_width - params_roof.offset_width
    pos_y = 0
    pos_z = params_general.floor_offset + params_general.floor_height * (1 + params_general.floor_count) + params_roof.height
    mat_loc = mathutils.Matrix.Translation((pos_x, pos_y, -pos_z))
    bmesh.ops.scale(bm_roof, space=mat_loc, verts=verts_to_scale, vec=(0.0, 0.0, 0.0))

    # crate edges from first, merged and last verts
    m_roof_filler = bpy.data.meshes.new("PBGRoofFiller")
    verts_filler = list()
    verts_filler.append(verts[0])
    verts_filler.append((-pos_x, pos_y, pos_z))
    verts_filler.append(verts[len(verts)-1])
    m_roof_filler.from_pydata(verts_filler, [(0, 1), (1, 2)], [])
    bm_roof_filler = bmesh.new()
    bm_roof_filler.from_mesh(m_roof_filler)

    # extrude, scale on x to 0 in x=0
    ret_extrude = bmesh.ops.extrude_edge_only(bm_roof_filler, edges=bm_roof_filler.edges, use_select_history=True)
    verts_to_scale = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    bmesh.ops.scale(bm_roof_filler, vec=(0.0, 1.0, 1.0), space=mat_loc, verts=verts_to_scale)

    # append filler to bm_roof
    bm_roof_filler.to_mesh(m_roof_filler)
    bm_roof_filler.free()
    bm_roof.from_mesh(m_roof_filler)

    # duplicate all, mirror
    geom_to_duplicate = bm_roof.verts[:] + bm_roof.edges[:] + bm_roof.faces[:]
    ret_dup = bmesh.ops.duplicate(bm_roof, geom=geom_to_duplicate)
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    verts_to_scale = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
    bmesh.ops.scale(bm_roof, vec=(-1.0, 1.0, 1.0), space=mat_loc, verts=verts_to_scale)

    # remove doubles, recalculate normals
    bmesh.ops.remove_doubles(bm_roof, verts=bm_roof.verts, dist=0.0001)
    bmesh.ops.recalc_face_normals(bm_roof, faces=bm_roof.faces)

    # if there is a wedge, get/create the points
    if params_footprint.building_wedge_depth > 0 and params_footprint.building_wedge_width > 0:
        verts_wedge = list()
        verts_wedge.append((-0.5 * params_footprint.building_wedge_width,
                            0.5 * params_footprint.building_depth + params_footprint.building_wedge_depth,
                            params_general.floor_offset + params_general.floor_height * (1 + params_general.floor_count)))
        verts_wedge.append((0,
                            0.5 * params_footprint.building_depth + params_footprint.building_wedge_depth - params_roof.offset_wedge,
                            params_general.floor_offset + params_general.floor_height * (1 + params_general.floor_count) + params_roof.height))
        verts_wedge.append((0.5 * params_footprint.building_wedge_width,
                            0.5 * params_footprint.building_depth + params_footprint.building_wedge_depth,
                            params_general.floor_offset + params_general.floor_height * (1 + params_general.floor_count)))
        # create mesh and bmesh
        bm_roof_wedge = bmesh.new()
        m_roof_wedge = bpy.data.meshes.new("PBGRoofWedge")
        m_roof_wedge.from_pydata(verts_wedge, [(0, 1), (1, 2), (2, 0)], [(0, 1, 2)])
        bm_roof_wedge.from_mesh(m_roof_wedge)

        # extrude and scale
        bm_roof_wedge.edges.ensure_lookup_table()
        edges_to_extrude = bm_roof_wedge.edges[:2]
        ret_extrude = bmesh.ops.extrude_edge_only(bm_roof_wedge, edges=edges_to_extrude, use_select_history=True)
        verts_to_scale = [ele for ele in ret_extrude["geom"] if isinstance(ele, bmesh.types.BMVert)]
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        bmesh.ops.scale(bm_roof_wedge, vec=(1.0, 0.0, 1.0), space=mat_loc, verts=verts_to_scale)

        # join bmeshes
        bm_roof_wedge.to_mesh(m_roof_wedge)
        bm_roof_wedge.free()
        bm_roof.from_mesh(m_roof_wedge)

    # create object.
    bm_roof.to_mesh(m_roof)
    bm_roof.free()
    ob = bpy.data.objects.get("PBGRoof")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGRoof", m_roof)
    context.scene.objects.link(new_obj)
    return new_obj
# end gen_mesh_roof
