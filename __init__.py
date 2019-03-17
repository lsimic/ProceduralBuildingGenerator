import bpy
from . import UI
from . import Generator


bl_info = {
    "name": "Procedural building generator",
    "description": "Proceduraly generate and edit buildings",
    "author": "Luka Šimić",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Toolbox > PBG",
    "warning": "Under development. Might cause stability issues.",
    "wiki_url": "https://lsimic.github.io/ProceduralBuildingGenerator/index.html",
    "tracker_url": "https://github.com/lsimic/ProceduralBuildingGenerator/issues",
    "support": "COMMUNITY",
    "category": "Add Mesh"
}


def register():
    bpy.utils.register_class(UI.PBGPropertyGroup)
    bpy.types.Scene.PBGPropertyGroup = bpy.props.PointerProperty(type=UI.PBGPropertyGroup)
    bpy.utils.register_class(UI.PBGToolbarGeneralPanel)
    bpy.utils.register_class(UI.PBGToolbarSettingsPanel)
    bpy.utils.register_class(Generator.Generator)


def unregister():
    del bpy.types.Scene.PBGPropertyGroup
    bpy.utils.unregister_class(UI.PBGPropertyGroup)
    bpy.utils.unregister_class(UI.PBGToolbarGeneralPanel)
    bpy.utils.unregister_class(UI.PBGToolbarSettingsPanel)
    bpy.utils.unregister_class(Generator.Generator)
