from pint import UnitRegistry
from pint.errors import DimensionalityError

unit_reg = UnitRegistry()
Q_ = unit_reg.Quantity
DimError = DimensionalityError

ZERO_LENGTH = Q_("0.0 metres")
ZERO_FORCE = Q_("0.0 psi")
