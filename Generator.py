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

        footprint = GenLayout.gen_footprint(params_general)
        layout = GenLayout.gen_layout(params_layout, footprint)
        section_element_list = GenUtils.gen_section_element_list(params_section)
        section_mesh = GenUtils.gen_section_mesh(section_element_list, params_general.floor_separator_height,
                                                 params_general.floor_separator_width)

        # generate geometry
        GenMesh.gen_mesh_floor_separator(context, params_general, footprint, section_mesh.copy())
        GenMesh.gen_mesh_wall(context, layout["wall_layout_loops"], params_general)

        print(params_layout.generate_pillar)
        if params_layout.generate_pillar == True:
            GenMesh.gen_mesh_pillar(context, params_pillar, params_general, section_mesh.copy(),
                                    layout["pillar_positions"])
        # end if

        return {"FINISHED"}
    # end invoke
# end Generator
