import pytest
from math import (radians, pi)

from rpm.utils import cotangent


def test_cotangent_returns_1_for_45_degrees():
    angle = radians(45)
    assert round(cotangent(angle), 0) == 1
