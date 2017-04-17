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


class PillarFormula(Enum):
    """
    The various formula that are used in calculating pillar strength
    The value of each enumeration is a tuple of the constants that
    are used along with the formula
    """
    hardy_agapito = (0.118, 0.933)
    salamon_munro = (7.18, 0.46, -0.66)
    bieniawski = (0.64, 0.36)
    stacey_page = (0.5, 0.7)
    cmri = (1, -1)
    obert_duval = (0.778, 0.22)
    holland_gaddy = (0.5, -1)
    holland = (0.5, -0.5)


if __name__ == '__main__':
    print(len(PillarFormula))
