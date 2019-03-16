import bpy


class GenerateHorizontalLayoutParams:
    """
        Params for generate_horizontal_layout() function.

        Attributes:
            width (float): width of the building, in blender units (size on X axis)
            depth (float): depth of the building, in blender units (size on Y axis)
            chamfer_size (float): size of the chamfer, in blender units
            wedge_depth (float): depth of the wedge, in blneder units
            wedge_width (float): width of the wedge, in blender units

    """
    def __init__(self, width, depth, chamfer_size, wedge_depth, wedge_width):
        self.width = width
        self.depth = depth
        self.chamfer_size = chamfer_size
        self.wedge_depth = wedge_depth
        self.wedge_width = wedge_width
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = GenerateHorizontalLayoutParams(
            properties.width,
            properties.depth,
            properties.chamfer_size,
            properties.wedge_depth,
            properties.wedge_width
        )
        return params
    # end from_ui
# end GenerateHorizontalLayoutParams


def generate_horizontal_layout(params):
    layout = list()
    # bottom left corner
    if params.chamfer_size > 0:
        layout.append((-0.5 * params.width + params.chamfer_size, -0.5 * params.depth, 0))
        layout.append((-0.5 * params.width, -0.5 * params.depth + params.chamfer_size, 0))
    else:
        layout.append((-0.5 * params.width, -0.5 * params.depth, 0))

    # top left corner
    if params.chamfer_size > 0:
        layout.append((-0.5 * params.width, 0.5 * params.depth - params.chamfer_size, 0))
        layout.append((-0.5 * params.width + params.chamfer_size, 0.5 * params.depth, 0))
    else:
        layout.append((-0.5 * params.width, 0.5 * params.depth, 0))

    # wedge
    if params.wedge_depth > 0 and params.wedge_width > 0:
        layout.append((-0.5 * params.wedge_width, 0.5 * params.depth, 0))
        layout.append((-0.5 * params.wedge_width, 0.5 * params.depth + params.wedge_depth, 0))
        layout.append((0.5 * params.wedge_width, 0.5 * params.depth + params.wedge_depth, 0))
        layout.append((0.5 * params.wedge_width, 0.5 * params.depth, 0))

    # top right corner
    if params.chamfer_size > 0:
        layout.append((0.5 * params.width - params.chamfer_size, 0.5 * params.depth, 0))
        layout.append((0.5 * params.width, 0.5 * params.depth - params.chamfer_size, 0))
    else:
        layout.append((0.5 * params.width, 0.5 * params.depth, 0))

    # bottom right corner
    if params.chamfer_size > 0:
        layout.append((0.5 * params.width, -0.5 * params.depth + params.chamfer_size, 0))
        layout.append((0.5 * params.width - params.chamfer_size, -0.5 * params.depth, 0))
    else:
        layout.append((0.5 * params.width, -0.5 * params.depth, 0))

    # return the list
    return layout
# end generate_horizontal_layout
