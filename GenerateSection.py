import math
import bpy
import random
import bmesh
import mathutils
from . import Constants


class GenerateSectionParams:
    """
    Params for generate_section() function.

    Note:
        Each attribute is treated as a percentage in range [0,1].
        Limit values indicate the cutoff points[0,1] for generating a certain element

    Attributes:
        s_min_size (float): min size of small element.
        s_max_size (float): max size of small element.
        m_min_size (float): min size of medium element.
        m_max_size (float): max size of medium element.
        l_min_size (float): min size of large element.
        l_max_size (float): max size of large element.
        ss_limit (float): cutoff value for generating a small square element.
        sc_limit (float): cutoff value for generating a small round element. Must be greater than ss_limit.
        ms_limit (float): cutoff value for generating a medium square element. Must be greater than sc_limit.
        mc_limit (float): cutoff value for generating a medium round element. Must be greater than ms_limit.
        ls_limit (float): cutoff value for generating a large square element. Must be equal to 1.
    """

    def __init__(self, s_min_size, s_max_size, m_min_size, m_max_size, l_min_size, l_max_size, ss_limit, sc_limit,
                 ms_limit, mc_limit):
        self.s_min_size = s_min_size
        self.s_max_size = s_max_size
        self.m_min_size = m_min_size
        self.m_max_size = m_max_size
        self.l_min_size = l_min_size
        self.l_max_size = l_max_size
        self.ss_limit = ss_limit
        self.sc_limit = sc_limit
        self.ms_limit = ms_limit
        self.mc_limit = mc_limit
        self.ls_limit = 1
    # end __init__

    # TODO: load params from ui here...
    # def from_ui(self):
# end GenerateSectionParams


class SectionElement:
    """
    Element of a Section.

    Note:
        Section element holds type of the element(square or circle) and the size as a percentage[0,1]

    Attributes:
        element_type (string in {"round", "square"): type of the element
        width (float): width of the element
        height (float): height of the element
    """
    def __init__(self, element_type, width, height):
        self.element_type = element_type
        self.width = width
        self.height = height
    # end __init__
# end SectionElement


class GenerateSectionParamsFactory:
    @staticmethod
    def horizontal_separator_params():
        params = GenerateSectionParams(
            s_min_size=0.05,
            s_max_size=0.1,
            m_min_size=0.2,
            m_max_size=0.3,
            l_min_size=0.4,
            l_max_size=0.6,
            ss_limit=0.55,
            sc_limit=0.62,
            ms_limit=0.69,
            mc_limit=0.87
        )
        return params
    # end horizontal_separator_params

    @staticmethod
    def horizontal_separator_params_normalized():
        params = GenerateSectionParams(
            s_min_size=0.05,
            s_max_size=0.1,
            m_min_size=0.2,
            m_max_size=0.3,
            l_min_size=0.4,
            l_max_size=0.6,
            ss_limit=0.2,
            sc_limit=0.4,
            ms_limit=0.6,
            mc_limit=0.8
        )
        return params
    # end horizontal_separator_params_normalized
# GenerateSectionParamsFactory


def generate_section_mesh(sequence, height, width):
    """
    Generates a mesh from the given list of sectionElements.

    Args:
         sequence (list of SectionElement): a list of SectionElements, to be used for generating the mesh. Likely the
             result of calling the generate_section function.
         height (float): height of the section
         width (float): width of the section

    Returns, bpy.types.Mesh:
        A mesh following the sequence, in Y-Z plane, starting in (0,0,0), with width and height of 1 blender unit.
    """

    verts = list()
    verts.append([0, 0, 0])
    for element in sequence:
        if element.element_type == "square":
            verts.append([0, verts[-1][1]+element.width, verts[-1][2]])
            verts.append([0, verts[-1][1], verts[-1][2]+element.height])
        else:
            # this is where the fun begins
            i = 1
            angle_step = (math.pi/2)/Constants.PROFILE_CIRCLE_PRECISION
            angle = -math.pi/2
            center_y = verts[-1][1]
            center_z = verts[-1][2]+element.height
            while i <= Constants.PROFILE_CIRCLE_PRECISION+1:
                verts.append([0, center_y + element.width*math.cos(angle), center_z + element.height*math.sin(angle)])
                i += 1
                angle += angle_step
            # end while
        # end if
    # end for

    verts.append([0, 0, verts[-1][2]])

    edges = list()
    i = 0
    while i < len(verts)-1:
        edges.append([i, i+1]),
        i += 1
    # end while

    section_mesh = bpy.data.meshes.new(name="PBGSection")
    section_mesh.from_pydata(verts, edges, [])
    section_mesh.update()
    section_bmesh = bmesh.new()
    section_bmesh.from_mesh(section_mesh)

    # scale the mesh so it has the desired width and height.
    mat_loc = mathutils.Matrix.Translation((0, 0, 0))
    bmesh.ops.scale(section_bmesh, vec=(1.0, width, height), space=mat_loc, verts=section_bmesh.verts)

    section_bmesh.to_mesh(section_mesh)
    section_bmesh.free()

    return section_mesh
# end generate_section_mesh


def generate_section(params):
    """
    Generates a list of SectionElements based on the supplied params.

    Args:
        params (GenerateSectionParams): object containing the parameters

    Returns, list of SectionElement:
        A list of SectionElement objects.
    """
    remaining_width = 1
    remaining_height = 1
    sequence = list()

    # generate first element
    e_width = random.uniform(params.s_min_size, params.s_max_size)
    e_height = random.uniform(params.s_min_size, params.s_max_size)
    element = SectionElement("square", e_width, e_height)
    remaining_width -= e_width
    remaining_height -= e_height
    sequence.append(element)

    # generate last element
    e_width = random.uniform(params.s_min_size, params.s_max_size)
    e_height = random.uniform(params.s_min_size, params.s_max_size)
    element = SectionElement("square", e_width, e_height)
    remaining_width -= e_width
    remaining_height -= e_height
    sequence.append(element)

    # generate elements until width or height become limiting factor
    # once the generated element can fill either range, it is scaled up to fill that range
    # no matter if the circle element would become distorted as a result.
    while remaining_height > 0 and remaining_width > 0:
        # pick a pseudo-random element while making sure we do not get an element which would be too big
        if remaining_height > params.l_min_size:
            rand = random.uniform(0, 1)
        elif remaining_height > params.m_min_size:
            rand = random.uniform(0, params.mc_limit)
        else:
            rand = random.uniform(0, params.sc_limit)
        # end if

        # generate correct element
        if rand < params.sc_limit:
            if params.s_max_size >= remaining_height or params.s_max_size >= remaining_width:
                e_width = remaining_width
                e_height = remaining_height
            else:
                e_width = random.uniform(params.s_min_size, params.s_max_size)
                e_height = random.uniform(params.s_min_size, params.s_max_size)
            # end if

            if rand < params.ss_limit:
                element = SectionElement("square", e_width, e_height)
            else:
                element = SectionElement("circle", e_width, e_height)
            # end if
        elif rand < params.mc_limit:
            if params.m_max_size >= remaining_height or params.m_max_size >= remaining_width:
                e_width = remaining_width
                e_height = remaining_height
            else:
                e_width = random.uniform(params.m_min_size, params.m_max_size)
                e_height = random.uniform(params.m_min_size, params.m_max_size)
            # end if

            if rand < params.ms_limit:
                element = SectionElement("square", e_width, e_height)
            else:
                element = SectionElement("circle", e_width, e_height)
            # end if
        else:
            if params.l_max_size >= remaining_height or params.l_max_size >= remaining_width:
                e_width = remaining_width
                e_height = remaining_height
            else:
                e_width = random.uniform(params.l_min_size, params.l_max_size)
                e_height = random.uniform(params.l_min_size, params.l_max_size)
            # end if

            element = SectionElement("square", e_width, e_height)
        # end if

        # update the remaining width and height
        remaining_width -= e_width
        remaining_height -= e_height

        # push the element into the list
        sequence.insert(len(sequence)-1, element)
    # end while
    return sequence
# end generate_section
