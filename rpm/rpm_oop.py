from __future__ import division
from datetime import datetime
import math

from . import (Q_, unit_reg, ZERO_LENGTH)


def requires(obj, attrib_list):
    """
    Raises an error if any of the attributes has a value of None or has not been actually set
    attributes: a list of attributes that are needed to calculate a specific value
    """
    for attrib in attrib_list:
        if not getattr(obj, attrib, None):
            raise ValueError("{} of {} has not been set".format(obj, attrib))


def left_align_pad(string, size):
    str_size = len(string)
    diff = size - str_size
    padded = string if diff <= 0 else string + " " * diff
    return padded


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
        width = width if (width and width > ZERO_LENGTH) else ZERO_LENGTH
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
        return 2.0 * (self.length + self.width)

    @property
    def cross_section_area(self):
        return self.length * self.width


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
        super(Sample, self).__init__(height, diameter, diameter)
        self.strength = strength
        self.is_cylinder = cylindrical

    @property
    def cubical_strength(self):
        # because of the behaviour of pint, perform operations on the magnitudes of the parameter
        # after all operations are performed multiply the result by 1 psi to convert it to uniaxial
        # compressive strength
        height = self.height.to(unit_reg.inch).magnitude
        gaddy = self.gaddy_factor.magnitude
        if height > 36:
            cubical = gaddy / 6
        else:
            cubical = gaddy / math.sqrt(height)
        return cubical * unit_reg.psi

    @property
    def diameter(self):
        return self.length

    def is_cubic(self):
        return self.height == self.length

    @property
    def volume(self):
        if self.is_cylinder:
            return math.pi * (self.diameter / 2) ** 2 * self.height
        else:
            return super(Sample, self).volume

    @property
    def gaddy_factor(self):
        strength = self.strength.to(unit_reg.psi).magnitude
        diameter = self.diameter.to(unit_reg.inch).magnitude
        result = strength * diameter ** 0.5
        return result * unit_reg.psi


class RoomAndPillar(object):

    HUMAN_FRIENDLY = {
        "room_span": "Length of room",
        "project_name": "Name of the Project",
        "design_type": "Type of Design",
        "location": "Location of the Project",
        "ore_type": "Substance being Mined",
        "min_extraction": "Least extraction required",
        "fragment_method": "Method of Fragmentation",
        "friction_angle": "Friction Angle",
        "cohesion": "Cohesion",
        "rmr": "Rock Mass Rating",
        "seam_height": "Height of the Orebody",
        "seam_dip": "Dip Angle of the Orebody",
        "mine_depth": "Depth of the Ore",
        "floor_density": "Specific Gravity of the Floor",
        "overburden_density": "Specific Gravity of the Overburden",
        "pillar_formula": "Information on Pillar formula to use",
    }
    DRILL_BLAST, CONTINUOUS_MINER = range(233583, 233585)
    INITIAL, REDESIGN = "initial", "redesign"

    def __init__(self, pillar=None, formula=None, room_span=None):
        for attrib in RoomAndPillar.HUMAN_FRIENDLY.keys():
            self.__setattr__(attrib, None)
        self.pillar = pillar
        self.room_span = room_span
        self.formula = formula

    def print_data(self):
        for attrib, friendly_name in RoomAndPillar.HUMAN_FRIENDLY.items():
            attribute = self.__getattribute__(attrib)
            try:
                print("{}\t{}\t{}".format(attrib, friendly_name, attribute))
            except Exception as e:
                print(attrib, e)

    def input_to_txt(self):
        with open("data.txt", "w") as data_input:
            data_input.write("{space}INPUT{space}\n".format(space="=" * 15))
            data_input.write("%s\n\n\n" % datetime.today())
            biggest_space = len(sorted(self.HUMAN_FRIENDLY.values(), key=len)[-1])
            print(biggest_space)
            for attrib, friendly_name in self.HUMAN_FRIENDLY.items():
                attribute = getattr(self, attrib)
                try:
                    unit = attribute.unit if attribute.unit != "dimensionless" else ""
                    magnitude = unit.magnitude
                except AttributeError as e:
                    unit = ""
                    magnitude = attribute
                data_input.write("{}:{} {}\n".format(left_align_pad(friendly_name, biggest_space), magnitude, unit))

    @property
    def vertical_pre_mining_stress(self):
        requires(self, ["mine_depth", "overburden_density"])
        return self.mine_depth * self.overburden_density

    def pillar_stress(self):
        requires(self, ["vertical_pre_mining_stress", "pillar", "room_span"])
        pillar = self.pillar
        numerator = (pillar.length + self.room_span) * (pillar.width + self.room_span)
        denominator = pillar.length * pillar.width
        return self.vertical_pre_mining_stress * (numerator / denominator)

    @property
    def extraction_ratio(self):
        """Returns the extraction ratio in percentage rounded to 2 decimal places"""
        requires(self, ["room_span", "pillar"])
        pillar = self.pillar
        first = pillar.width / (pillar.width + self.room_span)
        second = pillar.length / (pillar.length + self.room_span)
        return round(100 * (1 - first * second), 2)

    def pillar_strength(self):
        pass

    def pillar_strength2(self):
        return self.vertical_pre_mining_stress / (1 - (self.extraction_ratio / 100))


class StrengthFormula(object):

    CUBICAL, UNIAXIAL, GADDY, OTHER = "cubical", "uniaxial", "gaddy", "other"
    METRIC, IMPERIAL = "metric", "imperial"
    LINEAR, EXPONENTIAL, ODD = "linear", "exponential", "odd"
    __slots__ = ("k_type", "beta", "alpha", "category", "fos", "unit_system", "k", "name")

    def __init__(self, alpha, beta, k_type, fos, category, owner=None, unit_system=None, k=None, name=None):
        self.alpha = alpha
        self.beta = beta
        self.k_type = k_type
        self.category = category
        self.fos = fos
        self.unit_system = unit_system or self.IMPERIAL
        self.k = k
        self.name = name

        # k should have a value only when k type is other
        # all the other types are calculated from data
        # some odd formulas do not have k defined
        if self.category != StrengthFormula.ODD:
            assert ((self.k_type == StrengthFormula.OTHER and k is not None) or
                   (self.k_type != StrengthFormula.OTHER and k is None))

    @property
    def constants(self):
        return self.k, self.alpha, self.beta

    def __str__(self):
        return "{}, k={}, a={}, b={}".format(self.name, self.k, self.alpha, self.beta)

    def pillar_strength(self, pillar=None, alpha_base=None, beta_base=None, k=None):
        assert (alpha_base and beta_base) or pillar
        k = self._get_correct_k(pillar, k)

        if alpha_base and beta_base:
            a_base, b_base = alpha_base, beta_base
        else:
            a_base, b_base = pillar.width, pillar.height

        if self.category == self.LINEAR:
            return self.linear_strength(k, a_base, b_base)
        else:
            return self.exponential_strength(k, a_base, b_base)

    def linear_strength(self, k, a_base, b_base):
        return k * (self.alpha + self.beta * (a_base * b_base))

    def exponential_strength(self, k, a_base, b_base):
        return k * a_base ** self.alpha * b_base ** self.beta

    def _get_correct_k(self, pillar=None, default=None):
        """
        The various properties that can be used in place of constant k, the material constant
        are properties of the pillar sample. Where this is not the case, they are empirical
        values determined for the formula.
        If no pillar object is provided it assumes the formula has a defined k which it tries
        to return. If that too is not provided, then the function can be given a default value
        which it returns.
        When all the above, it raises an AttributeError.
        """
        if pillar:
            sample = pillar.sample
            if self.k_type == self.CUBICAL:
                return sample.cubical_strength
            elif self.k_type == self.GADDY:
                return sample.gaddy_factor
            elif self.k_type == self.UNIAXIAL:
                return sample.strength
        elif self.k or default:
            return self.k or default
        raise AttributeError("Attribute k for Pillar Strength formula is None.\n{}".format(self))
