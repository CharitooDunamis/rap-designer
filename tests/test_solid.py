import pytest

from rpm.rpm_oop import Solid
from gui_ import Q_


@pytest.fixture
def solid(request):
    return Solid(height=Q_("1.2"), width=Q_(1.4), length=Q_(2.3))


def test_is_square_returns_false_for_non_square_solids(solid):
    assert solid.is_square() is False


def test_is_square_returns_true_for_square_solids():
    solid = Solid(height=Q_(1.2), length=Q_(2.0), width=Q_(2.0))
    assert solid.is_square()


def test_volume(solid):
    assert round(solid.volume, 3) == 3.864


def test_supplying_only_height_and_length_creates_solid_with_square_cross_section():
    solid = Solid(Q_("3"), Q_("4"))
    assert solid.is_square()


def test_initialising_solid_with_negative_dimensions_results_in_zero_dimensions():
    solid = Solid(height=Q_("-1m"), length=Q_("-2m"))
    assert solid.height == 0
    assert solid.length == 0
    assert solid.width == 0


if __name__ == '__main__':
    pytest.main()
