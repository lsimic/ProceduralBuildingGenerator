import bpy
import bmesh
import mathutils
from . import GenerateSection
from . import GenerateHorizontalLayout
from . import Utils
from . import GenerateVerticalLayout


class GeneratorParams:
    def __init__(self, value):
        self.value = value
    # end __init__
# end GeneratorParams


class Generator(bpy.types.Operator):
    # TODO: docstring

    bl_idname = "pbg.generate_building"
    bl_label = "Generate Building"

    def invoke(self, context, event):
        # generate stuff needed for other functions that generate geometry
        layout_params = GenerateHorizontalLayout.GenerateHorizontalLayoutParams.from_ui()
        separator_params = GenerateHorizontalSeparatorsParams.from_ui()
        vertical_layout_params = GenerateVerticalLayout.GenerateVerticalLayoutParams.from_ui()
        section_params = GenerateSection.GenerateSectionParamsFactory.horizontal_separator_params_normalized()
        pillar_params = GeneratePillarsParams.from_ui()

        horizontal_layout = GenerateHorizontalLayout.generate_horizontal_layout(layout_params)
        vertical_layout = GenerateVerticalLayout.generate_vertical_layout(vertical_layout_params, horizontal_layout)
        section = GenerateSection.generate_section(section_params)
        section_mesh = GenerateSection.generate_section_mesh(section, separator_params.height, separator_params.width)

        # generate geometry
        generate_horizontal_separators(context, horizontal_layout, separator_params, section_mesh.copy())
        generate_walls(vertical_layout["wall_layout_loops"], context, separator_params)
        if vertical_layout_params.generate_pillar == True:
            generate_pillars(pillar_params, separator_params, section_mesh, vertical_layout["pillar_positions"], context)
        # end if

        return {"FINISHED"}
    # end invoke
# end Generator


class GenerateHorizontalSeparatorsParams:
    # TODO: docstring

    def __init__(self, width, height, separator_between_floors, first_floor_offset, floor_count, floor_height):
        self.width = width
        self.height = height
        self.separator_between_floors = separator_between_floors
        self.first_floor_offset = first_floor_offset
        self.floor_count = floor_count
        self.floor_height = floor_height
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = GenerateHorizontalSeparatorsParams(
            properties.separator_width,
            properties.separator_height,
            properties.separator_between_floors,
            properties.first_floor_offset,
            properties.floor_count,
            properties.floor_height
        )
        return params
    # end from_ui
# end GenerateHorizontalSeparatorsParams


def generate_horizontal_separators(context, layout, params, section_mesh):
    # TODO: docstring

    # generate the section(profile) which will be extruded, and extrude it to create a single separator
    section_mesh_extruded = Utils.extrude_along_edges(section_mesh, layout, True)

    # create a bmesh so we can edit
    separators_bmesh = bmesh.new()
    separators_bmesh.from_mesh(section_mesh_extruded)

    # move the mesh to the desired height
    bmesh.ops.translate(separators_bmesh, verts=separators_bmesh.verts,
                        vec=(0.0, 0.0, params.floor_height + params.first_floor_offset - params.height))
    geom_to_duplicate = separators_bmesh.verts[:] + separators_bmesh.edges[:] + separators_bmesh.faces[:]

    # duplicate the separators for each floor, and translate them, or translate straight to top based on params.
    i = 1
    while i <= params.floor_count:
        if params.separator_between_floors is False:
            ret_dup = bmesh.ops.duplicate(separators_bmesh, geom=geom_to_duplicate)
            verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
            bmesh.ops.translate(separators_bmesh, verts=verts_to_translate,
                                vec=(0.0, 0.0, params.floor_count * params.floor_height))
            break
        else:
            ret_dup = bmesh.ops.duplicate(separators_bmesh, geom=geom_to_duplicate)
            verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
            bmesh.ops.translate(separators_bmesh, verts=verts_to_translate, vec=(0.0, 0.0, params.floor_height))
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
# end generate_horizontal_separators


def generate_walls(wall_loops, context, separator_params):
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
    while i <= separator_params.floor_count:
        vert_start = (0.0, 0.0, separator_params.first_floor_offset
                      + i * separator_params.floor_height)
        vert_end = (0.0, 0.0, vert_start[2] + separator_params.floor_height)
        verts.append(vert_start)
        verts.append(vert_end)

        edges.append((2*i, 2*i + 1))
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
# end generate_walls


class GeneratePillarsParams:

    # horizontal separator: bool which defines whether or not to include the horizontal separator in the pillar profile
    # offset_size - size of the offset
    # offset - position of the offset
    def __init__(self, width, depth, chamfer, offset, offset_size, horizontal_separator):
        self.width = width
        self.depth = depth
        self.chamfer = chamfer
        self.offset = offset
        self.offset_size = offset_size
        self.horizontal_separator = horizontal_separator
    # end init

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = GeneratePillarsParams(
            properties.pillar_width,
            properties.pillar_depth,
            properties.pillar_chamfer,
            properties.pillar_offset,
            properties.pillar_offset_size,
            properties.pillar_horizontal_separator
        )
        return params
    # end from_ui
# end GeneratePillarsParams


def generate_pillars(pillar_params, separator_params, separator_mesh, pillar_positions, context):
    # TODO: how to generate pillar section mesh
    pillar_section_bmesh = bmesh.new()

    if pillar_params.horizontal_separator == True:
        # add separator section mesh to bmesh and move it to the appropriate place (up on Z)
        pillar_section_bmesh.from_mesh(separator_mesh)
        bmesh.ops.translate(pillar_section_bmesh, vec=(0.0, 0.0, separator_params.floor_height -
                                                       separator_params.height), verts=pillar_section_bmesh.verts)
    else:
        # we don't have a separator mesh, add a straight line
        mesh = bpy.data.meshes.new(name="PBGPillarSeparatorSection")
        verts = list()
        edges = list()
        verts.append((0.0, 0.0, separator_params.floor_height - separator_params.height))
        verts.append((0.0, 0.0, separator_params.floor_height))
        edges.append((0, 1))
        mesh.from_pydata(verts, edges, [])
        pillar_section_bmesh.from_mesh(mesh)
    # end if

    if pillar_params.offset_size > 0:
        # generate a pillar_section mesh
        pillar_offset_params = GenerateSection.GenerateSectionParamsFactory.horizontal_separator_params_large()
        pillar_offset_section = GenerateSection.generate_section(pillar_offset_params)
        pillar_offset_mesh = GenerateSection.generate_section_mesh(pillar_offset_section, pillar_params.offset_size,
                                                                   pillar_params.offset_size)
        # add it to new bmesh
        bm = bmesh.new()
        bm.from_mesh(pillar_offset_mesh)

        # remove last vertex
        bm.verts.ensure_lookup_table()
        last_vert = bm.verts[len(bm.verts)-1]
        bm.verts.remove(last_vert)

        # move up on Z, and on -Y for offset.
        bmesh.ops.translate(bm, vec=(0.0, -pillar_params.offset_size, separator_params.floor_height -
                                     separator_params.height - pillar_params.offset_size), verts=bm.verts)

        # duplicate, flip and move down
        mat_loc = mathutils.Matrix.Translation((0.0, pillar_params.offset_size, - separator_params.floor_height +
                                                separator_params.height + pillar_params.offset_size))
        geom_to_duplicate = bm.verts[:] + bm.edges[:] + bm.faces[:]
        ret_dup = bmesh.ops.duplicate(bm, geom=geom_to_duplicate)
        verts_to_transform = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.scale(bm, vec=(1.0, 1.0, -1.0), space=mat_loc, verts=verts_to_transform)
        z_dist = separator_params.floor_height - separator_params.height - pillar_params.offset - 2 * pillar_params.offset_size
        bmesh.ops.translate(bm, vec=(0.0, 0.0, - z_dist), verts=verts_to_transform)

        # add fillet between the two sections and below the lower section
        mesh_filler = bpy.data.meshes.new("PBGPillarFiller")
        mesh_filler_verts = list()
        mesh_filler_edges = list()
        mesh_filler_verts.append((0.0, 0.0, 0.0))
        mesh_filler_verts.append((0.0, 0.0, pillar_params.offset))
        mesh_filler_edges.append((0, 1))
        mesh_filler_verts.append((0.0, -pillar_params.offset_size, pillar_params.offset + pillar_params.offset_size))
        mesh_filler_verts.append((0.0, -pillar_params.offset_size, separator_params.floor_height -
                                  separator_params.height - pillar_params.offset_size))
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
        mesh_filler_verts.append((0.0, 0.0, separator_params.floor_height - separator_params.height))
        mesh_filler_edges.append((0, 1))
        m.from_pydata(mesh_filler_verts, mesh_filler_edges, [])
        pillar_section_bmesh.from_mesh(m)
    # end if

    # create the horizontal layout for extruding along
    layout = list()
    layout.append((-0.5 * pillar_params.width, 0.0, 0.0))
    if pillar_params.chamfer > 0:
        layout.append((-0.5 * pillar_params.width, pillar_params.depth - pillar_params.chamfer, 0.0))
        layout.append((-0.5 * pillar_params.width + pillar_params.chamfer, pillar_params.depth, 0.0))
        layout.append((0.5 * pillar_params.width - pillar_params.chamfer, pillar_params.depth, 0.0))
        layout.append((0.5 * pillar_params.width, pillar_params.depth - pillar_params.chamfer, 0.0))
    else:
        layout.append((-0.5 * pillar_params.width, pillar_params.depth, 0.0))
        layout.append((0.5 * pillar_params.width, pillar_params.depth, 0.0))
    # end if
    layout.append((0.5 * pillar_params.width, 0.0, 0.0))

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
    bmesh.ops.translate(pillar_bmesh, vec=(0.0, 0.0, separator_params.floor_height +
                                           separator_params.first_floor_offset), verts=pillar_bmesh.verts)

    # duplicate number of floors - 1 times, move each time for n*floor_height.
    geom = pillar_bmesh.verts[:] + pillar_bmesh.edges[:] + pillar_bmesh.faces[:]
    i = 1
    while i < separator_params.floor_count:
        ret_dup = bmesh.ops.duplicate(pillar_bmesh, geom=geom)
        verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        bmesh.ops.translate(pillar_bmesh, verts=verts_to_translate, vec=(0.0, 0.0, separator_params.floor_height))
        geom = ret_dup["geom"]
        i += 1
    # end while

    # duplicate and rotate appropriatly based on coordinates and rotation
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
