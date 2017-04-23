"""
This file contains constants needed in various operations.
Where other is added to an enumeration, it is to be regarded
as the default case to cover everything else.
"""
from enum import Enum
from .rpm_oop import StrengthFormula


class Countries(Enum):
    """
    These are the countries that in which the general pillar formulas were developed
    or these countries have a special pillar formula that are applicable to their mines
    This is to help determine the pillar formula to use
    """
    estonia = 1
    india = 2
    south_africa = 3
    other = 4


class OreTypes(Enum):
    """
    The various types of mines or ore for which formulas have been developed
    """
    hard_rock = 1
    coal = 2
    oil_shale = 3
    other = 4
