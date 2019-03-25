from bpy.types import Panel, PropertyGroup
from bpy.props import FloatProperty, BoolProperty


class PBGPropertyGroup(PropertyGroup):
    # TODO: docstring

    building_width = FloatProperty(
        name="Building width",
        default=25.0
    )

    building_depth = FloatProperty(
        name="Building depth",
        default=15.0
    )

    building_chamfer = FloatProperty(
        name="Chamfer size",
        default=1
    )

    building_wedge_depth = FloatProperty(
        name="Wedge depth",
        default=1.5
    )

    building_wedge_width = FloatProperty(
        name="Wedge width",
        default=8
    )

    floor_first_offset = FloatProperty(
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

    floor_separator_include = BoolProperty(
        name="Separator between floors",
        default=True
    )

    floor_separator_height = FloatProperty(
        name="Separator height",
        default=0.5
    )

    floor_separator_width = FloatProperty(
        name="Separator width",
        default=0.5
    )

    window_width = FloatProperty(
        name="Total window width",
        default=1.2
    )

    distance_window_window = FloatProperty(
        name="Distance between windows",
        default=2.5
    )

    generate_pillar = BoolProperty(
        name="Generate Pillar",
        default=True
    )

    distance_window_pillar = FloatProperty(
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

    pillar_offset_height = FloatProperty(
        name="Pillar Offset Height",
        default=0.7
    )

    pillar_offset_size = FloatProperty(
        name="Pillar Offset Size",
        default=0.05
    )

    pillar_include_floor_separator = BoolProperty(
        name="Include floor separator",
        default=True
    )
# end PBGPropertyGroup


class PBGToolbarGeneralPanel(Panel):
    # TODO: docstring
    bl_label = "General Settings"
    bl_category = "PBG"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.label(text="Overall Building Dimensions")
        col.prop(properties, "building_width")
        col.prop(properties, "building_depth")
        col.prop(properties, "building_chamfer")
        col.prop(properties, "building_wedge_depth")
        col.prop(properties, "building_wedge_width")

        col.label(text="Floor and separator layout")
        col.prop(properties, "floor_count")
        col.prop(properties, "floor_height")
        col.prop(properties, "floor_first_offset")
        col.prop(properties, "floor_separator_include")
        col.prop(properties, "floor_separator_width")
        col.prop(properties, "floor_separator_height")
    # end draw
# end PBGToolbarPanel


class PBGToolbarLayoutPanel(Panel):
    # TODO: docstring
    bl_label = "Layout Settings"
    bl_category = "PBG"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        # TODO: move window_width to separate window panel
        col.prop(properties, "window_width")
        col.prop(properties, "distance_window_window")
        col.prop(properties, "distance_window_pillar")
    # end draw
# end PBGLayoutPanel


class PBGToolbarPillarPanel(Panel):
    # TODO: docstring
    bl_label = "Pillar Settings"
    bl_category = "PBG"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.prop(properties, "generate_pillar")
        col.prop(properties, "pillar_width")
        col.prop(properties, "pillar_depth")
        col.prop(properties, "pillar_chamfer")
        col.prop(properties, "pillar_offset_height")
        col.prop(properties, "pillar_offset_size")
        col.prop(properties, "pillar_include_floor_separator")
    # end draw
# end PBGPillarPanel


class PBGToolbarGeneratePanel(Panel):
    # TODO: docstring
    bl_label = "Generate"
    bl_category = "PBG"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator("pbg.generate_building", text="Generate")
    # end draw
# end PBGGeneratePanel
