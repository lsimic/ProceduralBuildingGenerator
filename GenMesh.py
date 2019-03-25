import bmesh
import bpy
import mathutils
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
            properties.width,
            properties.depth,
            properties.chamfer_size,
            properties.wedge_depth,
            properties.wedge_width,
            properties.floor_count,
            properties.floor_height,
            properties.first_floor_offset,
            properties.separator_height,
            properties.separator_width,
            properties.separator_between_floors
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
                 pillar_offset_size, pillar_include_floor_separator):
        self.pillar_width = pillar_width
        self.pillar_depth = pillar_depth
        self.pillar_chamfer = pillar_chamfer
        self.pillar_offset_height = pillar_offset_height
        self.pillar_offset_size = pillar_offset_size
        self.pillar_include_floor_separator = pillar_include_floor_separator
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsPillar(
            properties.pillar_width,
            properties.pillar_depth,
            properties.pillar_chamfer,
            properties.pillar_offset,
            properties.pillar_offset_size,
            properties.pillar_horizontal_separator
        )
        return params
    # end from_ui
# end ParamsPillar


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
        if params_general.floor_separator_include is False:
            ret_dup = bmesh.ops.duplicate(separators_bmesh, geom=geom_to_duplicate)
            verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
            vec_trans = (0.0, 0.0, params_general.floor_count * params_general.floor_height)
            bmesh.ops.translate(separators_bmesh, verts=verts_to_translate, vec=vec_trans)
            break
        else:
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
                    floor_separator_mesh, pillar_positions):
    # TODO: docstring
    # TODO: improve pillar generation,
    # TODO: generate extruded sections separately from the pillars and copy them around if necessary...
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

    # remove doubles before extruding
    bmesh.ops.remove_doubles(pillar_section_bmesh, verts=pillar_section_bmesh.verts, dist=0.0001)

    # convert to mesh, extrude along, free bmesh, then populate with extruded
    pillar_section_mesh = bpy.data.meshes.new("PBGPillarSection")
    pillar_section_bmesh.to_mesh(pillar_section_mesh)
    pillar_section_bmesh.free()
    pillar_extruded = Utils.extrude_along_edges(pillar_section_mesh, layout, False)
    pillar_bmesh = bmesh.new()
    pillar_bmesh.from_mesh(pillar_extruded)

    # move up on Z for floor height + first_floor_offset
    bmesh.ops.translate(pillar_bmesh, vec=(0.0, 0.0, params_general.floor_height + params_general.floor_first_offset),
                        verts=pillar_bmesh.verts)

    # duplicate number of floors - 1 times, move each time for n*floor_height.
    geom = pillar_bmesh.verts[:] + pillar_bmesh.edges[:] + pillar_bmesh.faces[:]
    i = 1
    while i < params_general.floor_count:
        ret_dup = bmesh.ops.duplicate(pillar_bmesh, geom=geom)
        verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.translate(pillar_bmesh, verts=verts_to_translate, vec=(0.0, 0.0, params_general.floor_height))
        geom = ret_dup["geom"]
        i += 1
    # end while

    # duplicate and rotate appropriately based on coordinates and rotation
    geom_initial = pillar_bmesh.verts[:] + pillar_bmesh.edges[:] + pillar_bmesh.faces[:]

    for pos in pillar_positions:
        print(pos)
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


def gen_mesh_wall(context: bpy.types.Context, wall_loops: list, params_general: ParamsGeneral):
    # TODO: docstring
    # TODO: params class
    if len(wall_loops) == 1:
        is_loop = True
    else:
        is_loop = False
    # end if

    i = 0
    verts = list()
    edges = list()

    # TODO: more advanced method for generating walls
    while i <= params_general.floor_count:
        vert_start = (0.0, 0.0, params_general.floor_first_offset + i * params_general.floor_height)
        vert_end = (0.0, 0.0, vert_start[2] + params_general.floor_height)
        verts.append(vert_start)
        verts.append(vert_end)

        edges.append((2 * i, 2 * i + 1))
        i += 1
    # end while

    wall_section_mesh = bpy.data.meshes.new(name="PBGWallSection")
    wall_section_mesh.from_pydata(verts, edges, [])

    # check if the object for walls already exists
    ob = bpy.data.objects.get("PBGWalls")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # TODO: find a better solution for joining meshes
    wall_bmesh = bmesh.new()
    for loop in wall_loops:
        mesh = Utils.extrude_along_edges(wall_section_mesh.copy(), loop, is_loop)
        wall_bmesh.from_mesh(mesh)
    # end for

    wall_mesh = bpy.data.meshes.new("PBGWall")
    wall_bmesh.to_mesh(wall_mesh)
    wall_bmesh.free()
    # link the created object to the scene
    new_obj = bpy.data.objects.new("PBGWalls", wall_mesh)
    context.scene.objects.link(new_obj)
# end gen_mesh_walls
