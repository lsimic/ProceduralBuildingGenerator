import bpy
import bmesh
from . import GenerateSection
from . import GenerateHorizontalLayout
from . import Utils


class GeneratorParams:
    def __init__(self, value):
        self.value = value
    # end __init__
# end GeneratorParams


class Generator(bpy.types.Operator):
    bl_idname = "pbg.generate_building"
    bl_label = "Generate Building"

    def invoke(self, context, event):
        layout_params = GenerateHorizontalLayout.GenerateHorizontalLayoutParams.from_ui()
        layout = GenerateHorizontalLayout.generate_horizontal_layout(layout_params)

        params = GenerateHorizontalSeparatorsParams.from_ui()

        generate_horizontal_separators(context, layout, params)
        return {"FINISHED"}
    # end invoke
# end Generator


class GenerateHorizontalSeparatorsParams:
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

    section_params = GenerateSection.GenerateSectionParamsFactory.horizontal_separator_params_normalized()
    section = GenerateSection.generate_section(section_params)

    section_mesh = GenerateSection.generate_section_mesh(section, params.height, params.width)
    section_mesh_extruded = Utils.extrude_along_edges(section_mesh, layout, True)

    separators_bmesh = bmesh.new()
    separators_bmesh.from_mesh(section_mesh_extruded)

    bmesh.ops.translate(separators_bmesh, verts=separators_bmesh.verts,
                        vec=(0.0, 0.0, params.floor_height + params.first_floor_offset))
    geom_to_duplicate = separators_bmesh.verts[:] + separators_bmesh.edges[:] + separators_bmesh.faces[:]

    i = 1
    while i <= params.floor_count:
        if params.separator_between_floors is False:
            ret_dup = bmesh.ops.duplicate(separators_bmesh, geom=geom_to_duplicate)
            verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
            bmesh.ops.translate(separators_bmesh, verts=verts_to_translate,
                                vec=(0.0, 0.0, params.floor_count * params.floor_height))
            break
        else:
            print("iteration :" + str(i))
            ret_dup = bmesh.ops.duplicate(separators_bmesh, geom=geom_to_duplicate)
            verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
            bmesh.ops.translate(separators_bmesh, verts=verts_to_translate, vec=(0.0, 0.0, params.floor_height))
            geom_to_duplicate = [ele for ele in ret_dup["geom"] if (isinstance(ele, bmesh.types.BMVert)
                                                                    or isinstance(ele, bmesh.types.BMEdge)
                                                                    or isinstance(ele, bmesh.types.BMFace))]
        # end if
        i += 1
    # end while
    separators_bmesh.to_mesh(section_mesh_extruded)
    separators_bmesh.free()

    ob = bpy.data.objects.get("PBGProfile")
    if ob is not None:
        context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    new_obj = bpy.data.objects.new("PBGProfile", section_mesh_extruded)
    context.scene.objects.link(new_obj)
# end generate_horizontal_separators
