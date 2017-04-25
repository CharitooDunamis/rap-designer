from __future__ import division
from datetime import datetime
from collections import namedtuple
import math
from os.path import (dirname, join)

from mpmath import findroot

from . import (Q_, unit_reg, ZERO_LENGTH)
from .utils import cotangent
from .constants import OreTypes, Countries


rpm_dir = join(dirname(__file__), "..")
MISC_DIR = join(rpm_dir, "misc")
print(MISC_DIR)

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


fos_tuple = namedtuple("SafetyTuple", ("lower", "recommended", "upper"))


class StrengthFormula(object):

    CUBICAL, UNIAXIAL, GADDY, OTHER = "cubical", "uniaxial", "gaddy", "other"
    METRIC, IMPERIAL = "metric", "imperial"
    LINEAR, EXPONENTIAL, ODD = "linear", "exponential", "odd"
    __slots__ = ("k_type", "beta", "alpha", "category", "fos", "unit_system", "k", "name")

    def __init__(self, alpha, beta, k_type, category,  fos=(1.0, 1.5, 2.0),
                 unit_system=None, k=None, name=None):
        self.alpha = alpha
        self.beta = beta
        self.k_type = k_type
        self.category = category
        self.fos = fos_tuple(lower=fos[0], recommended=fos[1], upper=fos[-1])
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
        return "{}, k={}, a={} and b={}".format(self.name, self.k or self.k_type, self.alpha, self.beta)

    def pillar_strength(self, pillar, k=None):
        k = self.get_correct_k(pillar, k)

        a_base, b_base = pillar.width, pillar.height
        if self.unit_system == self.METRIC:
            a_base = a_base.to(unit_reg.metre).magnitude
            b_base = b_base.to(unit_reg.metre).magnitude
        else:
            a_base = a_base.to(unit_reg.foot).magnitude
            b_base = b_base.to(unit_reg.foot).magnitude

        if self.category == self.LINEAR:
            # print("using linear relation in pillar strength")
            strength = self.linear_strength(k, a_base, b_base)
        else:
            # print("using exponential relation in pillar strength")
            strength = self.exponential_strength(k, a_base, b_base)
        # print("Pillar strength incoming!:", strength)

        if self.unit_system == self.METRIC:
            return strength * unit_reg("megapascal")
        else:
            return strength * unit_reg.psi

    def linear_strength(self, k, a_base, b_base):
        # print("using a linear relation")
        return k * (self.alpha + self.beta * (a_base / b_base))

    def exponential_strength(self, k, a_base, b_base):
        # print("using an exponential relation in exponential strength.")
        # print(k, a_base, self.alpha, b_base, self.beta)
        # print(a_base ** self.alpha)
        # print(b_base ** self.beta)
        return k * a_base ** self.alpha * b_base ** self.beta

    def is_good_factor_of_safety(self, fos):
        return self.fos.lower <= fos <= self.fos.upper

    @property
    def recommended_fos(self):
        return self.fos.recommended

    def get_correct_k(self, pillar=None, default=None):
        """
        The various properties that can be used in place of constant k, the material constant
        are properties of the pillar sample. Where this is not the case, they are empirical
        values determined for the formula.
        If no pillar object is provided it assumes the formula has a defined k which it tries
        to return. If that too is not provided, then the function can be given a default value
        which it returns.
        When all the above, it raises an AttributeError.
        """
        print("Trying to get correct k")
        if pillar is not None:
            print("Pillar is not None")
            sample = pillar.sample
            if self.k_type == self.CUBICAL:
                k_value = sample.cubical_strength
            elif self.k_type == self.GADDY:
                k_value = sample.gaddy_factor
            elif self.k_type == self.UNIAXIAL:
                k_value = sample.strength
            # convert to the right unit system so that final calculation can be done blindly
            # trying to do final calculation with 'wise' units raises several errors
            try:
                # for cases when all the above conditionals fail
                if self.unit_system == self.METRIC:
                    k_value.ito(unit_reg.mpa)
                else:
                    k_value.ito(unit_reg.psi)
                return k_value.magnitude
            except Exception as e:
                print(e)
        # These values as raw values and do not need any unit conversion
        if self.k:
            print("Pillar is none or formula has k")
            return self.k
        elif default:
            print("Pillar is none or formula has default")
            return default
        raise AttributeError("Attribute k for Pillar Strength formula is None.\n{}".format(self))


# The various formula that are used in calculating pillar strength
# The value of each enumeration is a tuple of the constants that
# are used along with the formula

SF = StrengthFormula
hardy_agapito = SF(alpha=-0.118, beta=0.833, k_type=SF.CUBICAL, fos=(1.0, 2.0, 2.0), unit_system=SF.METRIC,
                   category=SF.EXPONENTIAL, name="Hardy-Agapito")
salamon_munro = SF(alpha=0.46, beta=-0.66, k_type=SF.OTHER, fos=(1.31, 1.6, 1.88), unit_system=SF.IMPERIAL,
                   category=SF.EXPONENTIAL, k=1320, name="Salamon-Munro")
bieniawski = SF(alpha=0.64, beta=0.36, k_type=SF.CUBICAL, fos=(1.5, 1.5, 2.0), unit_system=SF.IMPERIAL,
                category=SF.LINEAR, name="Bieniawski")
stacey_page = SF(alpha=0.5, beta=0.7, k_type=SF.GADDY, fos=(1.0, 1.5, 2.0), unit_system=SF.METRIC,
                 category=SF.EXPONENTIAL, name="Stacey-Page")
cmri = SF(1, -1, k_type=SF.OTHER, fos=(1, 1, 1), category=SF.ODD, name="C.M.R.I.")
obert_duval = SF(alpha=0.778, beta=0.22, category=SF.LINEAR, k_type=SF.CUBICAL, fos=(1.5, 2.0, 4.0),
                 unit_system=SF.IMPERIAL, name="Obert-Duval")
holland_gaddy = SF(alpha=0.5, beta=-1, k_type=SF.GADDY, fos=(1.8, 2.0, 2.2), unit_system=SF.IMPERIAL,
                   category=SF.EXPONENTIAL, name="Holland-Gaddy")
holland = SF(alpha=0.5, beta=-0.5, k_type=SF.CUBICAL, fos=(1.0, 2.0, 2.0), unit_system=SF.IMPERIAL,
             category=SF.EXPONENTIAL, name="Holland")
msalamon_munro = SF(alpha=0.46, beta=-0.66, k_type=SF.OTHER, fos=(1.31, 1.6, 1.88), unit_system=SF.METRIC,
                   category=SF.EXPONENTIAL, k=7.2, name="Salamon-Munro (metric)")

ALL_FORMULA = (hardy_agapito, salamon_munro, bieniawski, stacey_page, cmri, obert_duval, holland, holland_gaddy,
               msalamon_munro)


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

    def __str__(self):
        return "Solid: length: {}\twidth: {}\theight: {}".format(self.length, self.width, self.height)


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

    def __str__(self):
        return "Sample: strength:{}\tlength:{}\twidth:{}\theight:{}".format(self.strength, self.length, self.width, self.height)


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
        "floor_density": "Unit Weight of the Floor",
        "overburden_density": "Unit Weight of the Overburden",
        "pillar_formula": "Information on Pillar formula to use",
    }
    PILLAR_DATA = {
        "width": "Pillar Width",
        "length": "Pillar Length",
        "height": "Pillar Height",
    }
    OUTPUT = {
        "extraction_ratio": "Extraction Ratio",
        "vertical_pre_mining_stress": "Vertical Pre-Mining Stress",
        "pillar_strength": "Pillar Strength",
        "pillar_stress": "Pillar Stress",
        "bearing_capacity": "Bearing Capacity of Floor",
        "factor_of_safety": "Factor of Safety for Pillar",
        "bearing_capacity_factor_of_safety": "Factor of Safety for Bearing Capacity"
    }
    DRILL_BLAST, CONTINUOUS_MINER = range(233583, 233585)
    INITIAL, REDESIGN = "initial", "redesign"

    def __init__(self, pillar=None, formula=None, room_span=None):
        for attrib in RoomAndPillar.HUMAN_FRIENDLY.keys():
            self.__setattr__(attrib, None)
        self.pillar = pillar
        self.room_span = room_span
        self.formula = formula
        self.inputIO = ""
        self.outputIO = ""
        self.html_report = ""

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

    def input_to_html(self):
        self.inputIO = ""
        param_string = "<td class='param'>{}</td>"
        q_value_string = "<td class='value'>{:H}</td>"
        value_string = "<td class='value'>{}</td>"
        for attrib, friendly_name in self.HUMAN_FRIENDLY.items():
            attribute = getattr(self, attrib)
            param = param_string.format(friendly_name)
            try:
                good = round(attribute, 2)
            except Exception as e:
                good = attribute
            if isinstance(attribute, Q_):
                value = q_value_string.format(good)
            else:
                value = value_string.format(good)
            self.inputIO += "<tr>{}</tr>".format(param + value)
        # print(self.inputIO.getvalue())

    def output_to_html(self):
        self.outputIO = ""
        param_string = "<td class='param'>{}</td>"
        q_value_string = "<td class='value'>{:H}</td>"
        value_string = "<td class='value'>{}</td>"

        for attrib, friendly_name in self.PILLAR_DATA.items():
            attribute = getattr(self.pillar, attrib)
            param = param_string.format(friendly_name)
            try:
                good = round(attribute, 2)
            except Exception as e:
                good = attribute
            if isinstance(attribute, Q_):
                value = q_value_string.format(good)
            else:
                value = value_string.format(good)
            self.outputIO += "<tr>{}</tr>".format(param + value)

        for attrib, friendly_name in self.OUTPUT.items():
            attribute = getattr(self, attrib)
            param = param_string.format(friendly_name)
            try:
                good = round(attribute, 2)
            except Exception as e:
                good = attribute
            if isinstance(attribute, Q_):
                value = q_value_string.format(good)
            else:
                value = value_string.format(good)
            self.outputIO += "<tr>{}</tr>".format(param + value)

    def to_html(self):
        self.input_to_html()
        self.output_to_html()
        string = "<h2>Input</h2><hr><table>{}</table><h2>Output</h2><hr><table>{}</table>"
        return string.format(self.inputIO, self.outputIO)

    def to_html_with_header(self):
        raw = self.to_html()
        html_template = join(MISC_DIR, "template.html")
        html_file = open(html_template)
        header = html_file.read()
        time =  datetime.today().strftime("%I:%M:%S %p")
        date = datetime.today().strftime("%a, %d/%b/%Y")
        header += "<p>Date: {}</p><p>Time: {}</p>".format(date, time)
        html = header + raw + "</body></html>"
        html_file.close()
        self.html_report = html

    @property
    def vertical_pre_mining_stress(self):
        if self.overburden_density:
            overburden_density = self.overburden_density.to(unit_reg("meganewton per metre ** 3"))
            mine_depth = self.mine_depth.to(unit_reg.metre)
            stress = (overburden_density * mine_depth).magnitude * unit_reg("megapascal")
            return stress

        stress = 1.1 * self.mine_depth.to(unit_reg.foot)
        return stress.magnitude * unit_reg.psi

    @property
    def pillar_stress(self):
        # requires(self, ["vertical_pre_mining_stress", "pillar", "room_span"])
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
        ratio = (1 - first * second).magnitude
        return round(100 * ratio, 2)

    def formula_decide(self):
        if self.design_type == self.REDESIGN:
            return

        if self.ore_type == OreTypes.coal and self.location == Countries.india:
            self.formula = ALL_FORMULA[4]  # c.m.r.i.

        elif self.ore_type == OreTypes.coal:
            self.formula = ALL_FORMULA[2]  # bieniawski

        elif self.ore_type == OreTypes.oil_shale:
            self.formula = ALL_FORMULA[0]  # hardy-agapito

        elif self.ore_type == OreTypes.hard_rock:
            self.formula = ALL_FORMULA[3]   # stacey-page
        else:
            self.formula = ALL_FORMULA[2] # bieniaswki

    @property
    def pillar_strength(self):
        formula = self.formula
        if formula.name == "C.M.R.I":
            print("This is a CMRI Formula")
            bracket_component = self.mine_depth.to("metre").magnitude / 160 * (self.pillar.width_height_ratio - 1)
            outside_bracket = 0.27 * self.pillar.sample.strength.magnitude * self.pillar.height.magnitude ** -0.36
            return (outside_bracket + bracket_component) * unit_reg.mpa

        elif self.pillar.width_height_ratio > 10:
            print("This is a highly squat pillar. Use high stacey-page.")
            return self.high_stacey_page()

        elif formula.name == "Hardy-Agapito":
            print("Use Hardy-Agapito")
            a_base = self.pillar.sample.volume / self.pillar.volume
            b_base = self.pillar.width_height_ratio * self.pillar.sample.height_width_ratio
            self.formula.pillar_strength(a_base, b_base)
        # if formula.name in ("Holland", "Holland-Gaddy", "Bieniawski", "Salamon-Munro", "Orbet-Duval", "Stacey-Page"):
        else:
            print("Other formula must deal with this.")
            return self.formula.pillar_strength(self.pillar)

    def high_stacey_page(self):
        width = self.pillar.width.ito(unit_reg.metre)
        height = self.pillar.height.ito(unit_reg.metre)
        length = self.pillar.length.ito(unit_reg.metre)
        constant_k = self.pillar.sample.gaddy_factor.ito(unit_reg.mpa)
        effective_width = (4 * width * length) / (2 * width + 2 * length)
        bracket_out = constant_k * (2.5 / (effective_width * height) ** 0.07)
        inner_bracket = (effective_width / (4.5 * height)) ** 4.5 - 1
        bracket_value = 0.13 * inner_bracket + 1
        return bracket_out * bracket_value

    @property
    def pillar_strength2(self):
        return self.vertical_pre_mining_stress / (1 - (self.extraction_ratio / 100))

    @property
    def factor_of_safety(self):
        strength = self.pillar_strength.to(unit_reg("megapascal"))
        stress = self.pillar_stress.to(unit_reg("megapascal"))
        return (strength / stress).magnitude

    # ------------------ SHAPE FACTORS ------------------------#

    @property
    def sf_gamma(self):
        return 1.0 - 0.4 * (self.pillar.width / self.pillar.length)

    @property
    def sf_q(self):
        return 1.0 + math.sin(self.friction_angle) * (self.pillar.width / self.pillar.length)

    # ---------- BEARING CAPACITY FACTORS ---------------------#

    @property
    def bcf_c(self):
        friction_angle = math.radians(self.friction_angle.magnitude)
        return (self.bcf_q - 1) * cotangent(self.friction_angle)

    @property
    def bcf_gamma(self):
        friction_angle = math.radians(self.friction_angle.magnitude)
        return 1.5 * (self.bcf_q - 1) * math.tan(friction_angle)

    @property
    def bcf_q(self):
        friction_angle = math.radians(self.friction_angle.magnitude)
        first = math.e ** (math.pi * math.tan(friction_angle))
        second = math.tan((math.pi / 4) + (friction_angle / 2)) ** 2
        value = first * second
        return value

    @property
    def bearing_capacity(self):
        friction_angle = math.radians(self.friction_angle.magnitude)
        addend = self.cohesion * cotangent(friction_angle) * ((self.bcf_q * self.sf_q) - 1)
        product = 0.5 * self.floor_density * self.pillar.width * self.bcf_gamma * self.sf_gamma
        return product + addend

    @property
    def bearing_capacity_factor_of_safety(self):
        bc = self.bearing_capacity.to(unit_reg("megapascal"))
        stress = self.pillar_stress.to(unit_reg("megapascal"))
        # print("Bearing Capacity:", bc)
        # print("Pillar Stress:", stress)
        return (bc / stress).magnitude

    def pillar_width_from_fos_and_stress(self):
        k = self.formula.get_correct_k(self.pillar)
        alpha = self.formula.alpha
        beta = self.formula.beta
        exp_m = self.formula.recommended_fos * self.vertical_pre_mining_stress.to(unit_reg("megapascal")).magnitude
        room_span = self.room_span.to(unit_reg.metre).magnitude
        height = self.pillar.height.to(unit_reg.metre).magnitude

        if self.formula.category == SF.LINEAR:
            other_coef = (k * beta) / height
            other_expo = 3
            square_coef = exp_m - (k * alpha)
        else:
            other_coef = k * height ** beta
            other_expo = alpha + 2
            square_coef = exp_m
        print("alpha", alpha)
        uni_coef = 2 * room_span * exp_m
        constant_c = exp_m * room_span ** 2

        f = lambda x : other_coef * x ** other_expo - square_coef * x ** 2 - uni_coef * x - constant_c
        start = self._starting_point(f)
        pillar_width = findroot(f, start, solver="newton", tol=0.001)
        # print(pillar_width)
        pillar_width = Q_("{}metre".format(round(pillar_width, 2)))
        self.pillar.width = pillar_width
        self.pillar.length = pillar_width

    def _starting_point(self, f):
        cur_x, cur_val = 0, f(0)
        op = "<" if cur_val < 0 else ">"
        str_comp = "{} {} 0".format(cur_val, op)
        while eval(str_comp):
            # print("current x:", cur_x)
            cur_x += 1
            cur_val = f(cur_x)
            str_comp = "{} {} 0".format(cur_val, op)

        # print(cur_x - 1)
        return cur_x - 1
