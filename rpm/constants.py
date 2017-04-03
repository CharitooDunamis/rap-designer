from enum import Enum
# from pprint import pprint
# from collections import namedtuple

HARDY_AGAPITO = (0.118, 0.933)
SALAMON_MUNRO = (7.18, -0.66, 0.46)
ORBET_DUVAL_BETA = 0.0513


class Countries(Enum):
    estonia = 1
    india = 2
    south_africa = 3
    other = 4


class MineTypes(Enum):
    hard_rock = 1
    coal = 2
    oil_shale = 3
    other = 4


class PillarFormula(Enum):
    hardy_agapito = (None, 1, 1)
    salamon_munro = (7.18, -0.66, 0.46)
    bieniawski = (None, 1, 3)
    stacey_page = (None, 1, 4)
    cmri = (None, 1, 5)
    obert_duval = (None, 1, 6)
    holland_gaddy = (None,)
    holland = (None, None)


# salamon_constants = namedtuple("SalamonConstants", ["g", "t", "r"])
# hardy_agapito = namedtuple("HardyAgapito", ["a", "b"])
# expo_constants = namedtuple("Exponential_Pillar_Strength_Constants", ['k', 'a', 'b'])
if __name__ == '__main__':
    print(PillarFormula.salamon_munro)
    print(len(PillarFormula))
