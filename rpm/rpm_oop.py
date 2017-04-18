from __future__ import division
import math

from . import (Q_, unit_reg)


ZERO_LENGTH = Q_("0.0 metres")


class Solid(object):
    """A class to represent a solid/3D body such as pillars and core samples
    Most of the classes that subclass this one usually have square cross-section
    so when one the y dimension is left out, it is assumed to have the same value
     as the x dimension.
    """

    def __init__(self, height, length, width=None):
        """
        None of the following dimensions is allowed to be negative
        and they are to be the dimensions of the cube/cuboid that will totally enclose
        the solid. i.e. they are to be the dimension of the same solid in regular form
        :param height: the height of the bounding cube/cuboid
        :param length: the length of the bounding cube/cuboid
        :param width: the width of the bounding cube/cuboid
        """

        height = height if height > ZERO_LENGTH else ZERO_LENGTH
        length = length if length > ZERO_LENGTH else ZERO_LENGTH
        width = width if width and width > ZERO_LENGTH else ZERO_LENGTH
        self.height = height
        self.length = length
        self.width = width if width else length

    def is_square(self):
        """Returns True if the solid has a square cross-section"""
        return self.length == self.width

    @property
    def volume(self):
        return self.length * self.width * self.height


class Pillar(Solid):

    def __init__(self, sample, height, length, width=None):
        """
        :param sample: sample of pillar material used in compressive test
         It must be an instance of the Sample class
        :param height: height of the pillar
        :param length: length of the pillar
        :param width: width of the pillar
        """
        assert isinstance(sample, Sample)
        self.sample = sample
        super(Pillar, self).__init__(height, length, width)

    @property
    def width_height_ratio(self):
        return self.width / self.height

    @property
    def cross_section_perimeter(self):
        return 2 * (self.length + self.width)

    @property
    def cross_section_area(self):
        return self.length * self.width

    @property
    def strength(self):
        return None


class Sample(Solid):
    """
    This class represents the cylindrical, cube or cuboidal samples used
    in uniaxial compressive tests.
    """

    def __init__(self, strength, height, diameter, cylindrical=False):
        """
        None of the following dimensions is allowed to be negative
        and they are to be the dimensions of the cube/cuboid that will totally enclose
        the solid. i.e. they are to be the dimension of the same solid in regular form
        :param strength: uniaxial compressive of the sample
        :param height: the height of the bounding cube/cuboid (inches)
        :param diameter: for circular samples, this is the diameter of the circular (inches)
         cross-section. For cube/cuboid samples, it is an alias for the length since (inches)
         it will have the same value
        :param cylindrical: set to True if the sample is cylindrical
        """
        super(Sample, self).__init__(height, diameter)
        self.strength = strength
        self.is_cylinder = cylindrical

    @property
    def cubical_strength(self):
        if self.height > Q_("36 inch"):
            strength = self.gaddy_factor / 6
        else:
            strength = self.gaddy_factor / math.sqrt(self.height)
        return strength

    @property
    def diameter(self):
        return self.length

    def is_cubical(self):
        return self.height == self.length

    @property
    def volume(self):
        if self.is_cylinder:
            return math.pi * (self.diameter / 2) ** 2 * self.height
        else:
            return super(Sample, self).volume

    @property
    def gaddy_factor(self):
        return self.strength * math.sqrt(self.diameter)


class RoomAndPillar(object):

    def __init__(self, pillar=None, room_span=None):

        # DATA
        self.pillar = pillar
        self.room_span = room_span
        self.project_name = None
        self.design_type = None
        self.room_width = None
        self.location = None
        self.ore_type = None
        self.minExtraction = None
        self.fragment_method = None

        self.friction_angle = None
        self.cohesion = None
        self.rmr = None
        self.seam_height = None
        self.seam_dip = None
        self.mine_depth = None
        self.floor_density = None
        self.overburden_density = None
        self.pillar_formula = None


class StrengthFormula(object):

    CUBICAL, UNIAXIAL, GADDY, OTHER = range(4)
    METRIC, IMPERIAL = range(23283482, 23283484)
    LINEAR, EXPONENTIAL, ODD = range(4374, 4377)

    def __init__(self, alpha, beta, k_type, fos, category, k=None, name=None):
        self.alpha = alpha
        self.beta = beta
        self.k_type = k_type
        self.category = category
        self.fos = fos
        self.k = k
        self.name = name

        # k should have a value only when k type is other
        # all the other types are calculated from data
        # some odd formulas use do not have k defined
        if self.category != StrengthFormula.ODD:
            assert ((self.k_type == StrengthFormula.OTHER and k is not None) or
                   (self.k_type != StrengthFormula.OTHER and k is None))

    @property
    def constants(self):
        return self.k, self.alpha, self.beta
