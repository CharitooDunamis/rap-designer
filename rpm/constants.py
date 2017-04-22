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


# The various formula that are used in calculating pillar strength
# The value of each enumeration is a tuple of the constants that
# are used along with the formula

SF = StrengthFormula
hardy_agapito = SF(alpha=-0.118, beta=0.833, k_type=SF.CUBICAL, fos=2.0, category=SF.EXPONENTIAL, name="Hardy-Agapito")
salamon_munro = SF(alpha=0.46, beta=-0.66, k_type=SF.OTHER, fos=1.6, category=SF.EXPONENTIAL, k=1320, name="Salamon-Munro")
bieniawski = SF(alpha=0.64, beta=0.36, k_type=SF.CUBICAL, fos=1.5, category=SF.LINEAR, name="Bieniawski")
stacey_page = SF(alpha=0.5, beta=0.7, k_type=SF.GADDY, fos=2.0, category=SF.EXPONENTIAL, name="Stacey-Page")
cmri = SF(1, -1, k_type=SF.OTHER, fos=1, category=SF.ODD, name="C.M.R.I.")
obert_duval = SF(alpha=0.778, beta=0.22, category=SF.LINEAR, k_type=SF.CUBICAL, fos=2.0, name="Obert-Duval")
holland_gaddy = SF(alpha=0.5, beta=-1, k_type=SF.GADDY, fos=2.0, category=SF.EXPONENTIAL, name="Holland-Gaddy")
holland = SF(alpha=0.5, beta=-0.5, k_type=SF.CUBICAL, fos=2.0, category=SF.EXPONENTIAL, name="Holland")

ALL_FORMULA = (hardy_agapito, salamon_munro, bieniawski, stacey_page, cmri, obert_duval, holland, holland_gaddy)

if __name__ == '__main__':
    print(len(ALL_FORMULA))
