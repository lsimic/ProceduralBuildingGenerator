import bpy
import bmesh
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
        layout_params = GenerateHorizontalLayout.GenerateHorizontalLayoutParams.from_ui()
        layout = GenerateHorizontalLayout.generate_horizontal_layout(layout_params)

        vertical_layout_params = GenerateVerticalLayout.GenerateVerticalLayoutParams.from_ui()
        vertical_layout = GenerateVerticalLayout.generate_vertical_layout(vertical_layout_params, layout)

        params = GenerateHorizontalSeparatorsParams.from_ui()

        generate_horizontal_separators(context, layout, params)

        generate_walls(vertical_layout["wall_layout_loops"], context, params)

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


def generate_horizontal_separators(context, layout, params):
    # TODO: docstring

    # generate the section(profile) which will be extruded, and extrude it to create a single separator
    section_params = GenerateSection.GenerateSectionParamsFactory.horizontal_separator_params_normalized()
    section = GenerateSection.generate_section(section_params)
    section_mesh = GenerateSection.generate_section_mesh(section, params.height, params.width)
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
