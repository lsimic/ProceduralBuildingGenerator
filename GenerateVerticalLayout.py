import bpy
import math
import mathutils
from . import Utils


class GenerateVerticalLayoutParams:
    """
        Params for generate_vertical_layout() function.

        Attributes:
            total_window_width (float): width of the window and surrounding geometry
            window_window_distance (float): distance between centers of neighbouring windows
            generate_pillar (bool): Whether to generate pillars or not
            pillar_width (float): width of the single pillar, excluding base and top, which are wider
            window_pillar_distance (float): Distance from edge of window supporting geometry, to center of pillar
                Set this to 0 in order to have a single pillar between windows.
    """
    def __init__(self, window_window_distance, total_window_width, generate_pillar, pillar_width, window_pillar_distance):
        self.total_window_width = total_window_width
        self.window_window_distance = window_window_distance
        self.generate_pillar = generate_pillar
        self.pillar_width = pillar_width
        self.window_pillar_distance = window_pillar_distance
    # end_init

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = GenerateVerticalLayoutParams(
            total_window_width=properties.total_window_width,
            window_window_distance=properties.window_window_distance,
            generate_pillar=properties.generate_pillar,
            pillar_width=properties.pillar_width,
            window_pillar_distance=properties.window_pillar_distance
        )
        return params
    # end from_ui
# end GenerateVerticalLayoutParams


def generate_vertical_layout(params, h_layout_verts):
    # TODO: docstring. Honestly, this method really needs one, the most hackish one... so far.

    i = 0
    window_positions = list()
    pillar_positions = list()
    wall_layout_loops = list()
    wall_layout_verts = list()
    wall_layout_verts_initial = list()
    is_first_loop = True
    while i < len(h_layout_verts):
        # assign start and end vertex
        v1 = h_layout_verts[i]
        if i == len(h_layout_verts) - 1:
            v2 = h_layout_verts[0]
        else:
            v2 = h_layout_verts[i+1]
        # end if

        # push the first vert into the array
        if is_first_loop:
            wall_layout_verts_initial.append(v1)
        else:
            wall_layout_verts.append(v1)
        # end if;

        # calculate length of edge
        dist_x = v2[0] - v1[0]
        dist_y = v2[1] - v1[1]
        edge_length = math.sqrt(dist_x * dist_x + dist_y * dist_y)

        # calculate number of windows for this edge
        if params.generate_pillar:
            window_count = math.floor((edge_length - 2 * params.window_pillar_distance - params.pillar_width) /
                                      params.window_window_distance) + 1
        else:
            window_count = math.floor((edge_length - params.total_window_width) / params.window_window_distance) + 1
        # end if

        # calculate distance between windows on x and y axis
        ww_dist_x = (params.window_window_distance / edge_length) * dist_x
        ww_dist_y = (params.window_window_distance / edge_length) * dist_y
        window_width_x = (params.total_window_width / edge_length) * dist_x
        window_width_y = (params.total_window_width / edge_length) * dist_y
        # calculate distance from window to pillar on x and y axis
        wp_dist_x = (params.window_pillar_distance / edge_length) * dist_x
        wp_dist_y = (params.window_pillar_distance / edge_length) * dist_y
        # check wether to generate one or two pillars between windows
        if 2 * params.window_pillar_distance >= params.window_window_distance:
            has_single_pillar = True
        else:
            has_single_pillar = False
        # end if

        # calculate window and pillar rotation(it's always the same
        vec_edge = Utils.vec_from_verts(v2, v1)
        vec_0 = mathutils.Vector((0.0, 1.0, 0.0))
        rot = vec_edge.xy.angle_signed(vec_0.xy) - 0.5 * math.pi

        j = 0
        while j < window_count:
            # calculate window positions for this edge
            window_x = (v1[0] + ((dist_x - (window_count - 1) * ww_dist_x) / 2) + j * ww_dist_x)
            window_y = (v1[1] + ((dist_y - (window_count - 1) * ww_dist_y) / 2) + j * ww_dist_y)
            window_positions.append((window_x, window_y, rot))

            # calculate the last vert of this loop, because it is broken by the window
            edge_vert_x = window_x - 0.5 * window_width_x
            edge_vert_y = window_y - 0.5 * window_width_y
            # push it into the loops array
            if is_first_loop:
                wall_layout_verts_initial.append((edge_vert_x, edge_vert_y, 0))
                is_first_loop = False
            else:
                wall_layout_verts.append((edge_vert_x, edge_vert_y, 0))
                wall_layout_loops.append(list(wall_layout_verts))
                wall_layout_verts.clear()
            # end if

            # calculate the first vert of the next loop
            edge_vert_x = window_x + 0.5 * window_width_x
            edge_vert_y = window_y + 0.5 * window_width_y
            # push it into the loops array
            wall_layout_verts.append((edge_vert_x, edge_vert_y, 0))

            # calculate pillar positions
            if j == 0 or has_single_pillar is False:
                pillar_x = window_x - wp_dist_x
                pillar_y = window_y - wp_dist_y
                pillar_positions.append((pillar_x, pillar_y, rot))
            # end if
            pillar_x = window_x + wp_dist_x
            pillar_y = window_y + wp_dist_y
            pillar_positions.append((pillar_x, pillar_y, rot))

            # increment counter
            j += 1
        # end while

        # check if this is the last edge, append the layout_verts_inital to the current layout_verts
        if i == len(h_layout_verts) - 1:
            verts = wall_layout_verts + wall_layout_verts_initial
            wall_layout_loops.append(list(verts))
        # end if

        # increment counter
        i += 1
    # end for

    # put all results in a dictionary and return it
    result = {
        "window_positions": window_positions,
        "pillar_positions": pillar_positions,
        "wall_layout_loops": wall_layout_loops
    }
    return result
# end generate_vertical_layout
