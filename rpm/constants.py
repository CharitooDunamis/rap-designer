"""
This file contains constants needed in various operations.
Where other is added to an enumeration, it is to be regarded
as the default case to cover everything else.
"""
from enum import Enum


class Countries(Enum):
    """
    These are the countries that in which the general pillar formulas were developed
    or these countries have a special pillar formula that are applicable to their mines
    This is to help determine the pillar formula to use
    """
    south_africa = 1
    estonia = 2
    india = 3
    united_states = 4
    other = 5


class OreTypes(Enum):
    """
    The various types of mines or ore for which formulas have been developed
    """
    coal = 1
    hard_rock = 2
    oil_shale = 3
    other = 4
