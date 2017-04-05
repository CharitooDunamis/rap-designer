from __future__ import division

import math

from .constants import *

"""
sample_height
sample_diameter
sample_density
deposit_depth   #overburden height
unicomp_strength
initial_room_width
max_pillar_strength
factor_of_safety
angle_of_friction
cohesion
bearing_capacity
"""


def pre_mining_field_stress(unit_weight, height):
    return unit_weight * height


def factor_of_safety(pillar_strength, pillar_stress):
    return pillar_strength/pillar_stress


def good_factor_of_safety(factor):
    return 1 <= factor <= 2

# Pillar Strength Methods---------------------------------------------------------


def expo_pillar_strength(k, width, a, height, b):
    return k * (width ** a) * (height ** b)


def linear_pillar_strength(k, width, a, height, b):
    return k * (a + b * (width / height))


def low_stacey_page(k, width, height):
    return expo_pillar_strength(k, width, 0.5, height, -0.7)


def high_stacey_page(constant_k, width, breadth, height):
    effective_width = (4 * width * breadth) / (2 * width + 2 * breadth)
    bracket_out = constant_k * (2.5 / (effective_width * height) ** 0.07)
    inner_bracket = (effective_width / (4.5 * height)) ** 4.5 - 1
    bracket_value = 0.13 * inner_bracket + 1
    return bracket_out * bracket_value


def stacey_page(constant_k, width, height, breadth):
    if width / height <= 4.5:
        return low_stacey_page(constant_k, width, height)
    else:
        return high_stacey_page(constant_k, width, height, breadth)


def cmri(uniaxial, height, depth, width):
    """
    :param uniaxial: uniaxial compressive strength of sample
    :param height: height of pillar or orebody
    :param depth: depth of ore deposit
    :param width: width of pillar
    :return: strength according to CMRI formula
    """
    _p = 0.27 * uniaxial * height ** -0.36
    _p2 = (depth / 160) * (width / height - 1)
    return _p + _p2


def hardy_agapito(uniaxial, pillar_sample_vol_ratio,
                  pillar_width_height_ratio, sample_height_width_ratio, constants=None):
    a, b = constants if constants else PillarFormula.salamon_munro.value
    first_portion = uniaxial * pillar_sample_vol_ratio ** a
    second_portion = (pillar_width_height_ratio * sample_height_width_ratio) ** b
    return first_portion * second_portion


def salamon(width, height, constants=None):
    k, a, b = constants if constants else PillarFormula.salamon_munro.value
    return expo_pillar_strength(k, width, a, height, b)


def bieniawski(cubic_strength, width, height):
    """
    :param cubic_strength: strength of cubic sample
    :param width: width of pillar
    :param height: height of pillar
    :return: Pillar strength according to Benniawski (1969)
    """
    return cubic_strength * (0.64 + 0.36 * (width / height))


def orbet_duval(uniaxial, width, height):
    """
    Calculate the strength of a pillar according to orbert-duval (1967)
    :return: strength of pillar
    """
    # return uniaxial * (0.778 + 0.222 * (width / height))
    return linear_pillar_strength(uniaxial, width, 0.778, height, 0.222)


def holland_gaddy(gaddy_factor, width, height):
    """
    Returns pillar strength according to Holland & Gaddy (1964 & 1956)
    :param gaddy_factor: Gaddy factor for rock type
    :param width: width of pillar
    :param height: height of pillar
    :return: strength of pillar
    """
    return gaddy_factor * (math.sqrt(width) / height)


def holland(cubical_strength, width, height):
    """
    Returns strength of pillar according to holland (1973)
    :param cubical_strength: strength of cubical specimen i.e w = h
    :param width: width of pillar
    :param height: heighth of pillar
    :return: strength of pillar
    """
    return cubical_strength * math.sqrt(width / height)


# Pillar Stress Functions-----------------------------------------------


def square_pillar_stress(pre_mine_stress, room_width, pillar_width):
    return pre_mine_stress * ((room_width + pillar_width) / pillar_width) ** 2


# untested
def inclined_seam_square_pillar_stress(pre_mine_stress, room_width, pillar_width, angle, poisson):
    flat_seam_stress = square_pillar_stress(pre_mine_stress, room_width, pillar_width)
    angle = math.radians(angle)
    return flat_seam_stress * (math.cos(angle) + poisson * math.sin(angle))


def rectangular_pillar_stress(pre_mine_stress, room_width, room_length, pillar_width, pillar_length):
    numerator = pre_mine_stress * (pillar_width + pillar_length) * (room_width + room_length)
    return numerator/(pillar_width + pillar_length)


def square_pillar_extraction_ratio(pillar_width, room_width):
    return 1 - (pillar_width/(pillar_width + room_width))


def extraction_ratio(pillar_width, pillar_length, room_width):
    numerator = (pillar_width + room_width) * (pillar_length + room_width) - (room_width * pillar_length)
    denominator = (pillar_width + room_width) * (pillar_length + room_width)
    return numerator / denominator

# Bearing Capacity Calculation---------------------------------------------------


def strength_factor_ng(angle_of_friction):
    constant_n = 1
    radian_angle = math.radians(angle_of_friction)
    first_part = math.e ** (constant_n * math.tan(radian_angle))
    second_part = math.tan(math.radians(45) + radian_angle/2) ** 2
    return first_part * second_part


def strength_factor_ny(strength_fact_ng, angle_of_friction):
    radian_angle = math.radians(angle_of_friction)
    return 1.5 * (strength_fact_ng - 1) * math.tan(radian_angle)


def shape_factor_gamma(pillar_width, pillar_length):
    return 1.0 - 0.4 * (pillar_width / pillar_length)


def shape_factor_g(friction_angle, pillar_width, pillar_length):
    print("\nFriction Angle:%d\tPillar Width:%d\tPillar Length:%d" % (friction_angle, pillar_width, pillar_length))
    a = math.sin(friction_angle)
    b = pillar_width / pillar_length
    print("Print values:\n", a, b)
    return 1.0 + (a * b)


def max_tensile_stress(sample_unit_weight, span, roof_thickness):
    return (6 * ORBET_DUVAL_BETA * sample_unit_weight * span ** 2) / roof_thickness


def is_good_roof_span_fos(factor):
    print(factor)
    pass


# def roof_floor_bearing_capacity(rock_density, pillar_width, pillar_length, friction_angle, cohesion):
#     n_g = strength_factor_ng(friction_angle)
#     n_y = strength_factor_ny(n_g, friction_angle)
#     s_gam = shape_factor_gamma(pillar_width, pillar_length)
#     s_g = shape_factor_g(rock_density, pillar_width, pillar_length)
#     return 0.5 * (rock_density * pillar_width * n_y * s_gam + 2 * math.cosh())
