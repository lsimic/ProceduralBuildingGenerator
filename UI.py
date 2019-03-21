from bpy.types import Panel, PropertyGroup
from bpy.props import FloatProperty, BoolProperty


class PBGPropertyGroup(PropertyGroup):
    # TODO: docstring

    width = FloatProperty(
        name="Width",
        default=25.0
    )

    depth = FloatProperty(
        name="Depth",
        default=15.0
    )

    chamfer_size = FloatProperty(
        name="Chamfer size",
        default=1
    )

    wedge_depth = FloatProperty(
        name="Wedge depth",
        default=1.5
    )

    wedge_width = FloatProperty(
        name="Wedge width",
        default=8
    )

    first_floor_offset = FloatProperty(
        name="FIrst floor offset",
        default=0.7
    )

    floor_height = FloatProperty(
        name="Floor height",
        default=3
    )

    floor_count = FloatProperty(
        name="Number of floors",
        default=2
    )

    separator_between_floors = BoolProperty(
        name="Separator between floors",
        default=True
    )

    separator_height = FloatProperty(
        name="Separator height",
        default=0.5
    )

    separator_width = FloatProperty(
        name="Separator width",
        default=0.5
    )

    total_window_width = FloatProperty(
        name="Total window width",
        default=1.2
    )

    window_window_distance = FloatProperty(
        name="Distance between windows",
        default=2.5
    )

    generate_pillar = BoolProperty(
        name="Generate Pillar",
        default=True
    )

    window_pillar_distance = FloatProperty(
        name="Distance Window to Pillar",
        default=0.8
    )

    pillar_width = FloatProperty(
        name="Pillar width",
        default=0.2
    )

    pillar_depth = FloatProperty(
        name="Pillar depth",
        default=0.15
    )

    pillar_chamfer = FloatProperty(
        name="Pillar Chamfer",
        default=0.05
    )

    pillar_offset = FloatProperty(
        name="Pillar Offset",
        default=0.7
    )

    pillar_offset_size = FloatProperty(
        name="Pillar Offset Size",
        default=0.05
    )

    pillar_horizontal_separator = BoolProperty(
        name="Pillar Horizontal separator",
        default=True
    )
# end PBGPropertyGroup


class PBGToolbarGeneralPanel(Panel):
    # TODO: docstring
    bl_label = "General"
    bl_category = "PBG"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.label(text="Overall Dimensions")
        col.prop(properties, "width")
        col.prop(properties, "depth")
        col.prop(properties, "chamfer_size")
        col.prop(properties, "wedge_depth")
        col.prop(properties, "wedge_width")

        col.label(text="Floor layout")
        col.prop(properties, "floor_count")
        col.prop(properties, "floor_height")
        col.prop(properties, "first_floor_offset")

        col.label(text="Floor separator")
        col.prop(properties, "separator_between_floors")
        col.prop(properties, "separator_width")
        col.prop(properties, "separator_height")

        col.label(text="Vertical layout")
        col.prop(properties, "total_window_width")
        col.prop(properties, "window_window_distance")
        col.prop(properties, "generate_pillar")
        col.prop(properties, "pillar_width")
        col.prop(properties, "window_pillar_distance")

        row = layout.row(align=True)
        row.operator("pbg.generate_building", text="Generate")
    # end draw
# end PBGToolbarPanel


class PBGToolbarSettingsPanel(Panel):
    # TODO: docstring
    bl_label = "Settings"
    bl_category = "PBG"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="đšćčž moe moe kyun :3")
    # end draw
# end PBGToolbarPanel
