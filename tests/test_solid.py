import pytest

from rpm.rpm_oop import Solid
from rpm import (Q_, unit_reg, ZERO_LENGTH)


@pytest.fixture
def solid(request):
    return Solid(height=Q_("1.2m"), width=Q_("1.4m"), length=Q_("2.3m"))


def test_is_square_returns_false_for_non_square_solids(solid):
    assert solid.is_square() is False


def test_is_square_returns_true_for_square_solids():
    solid = Solid(height=Q_("1.2m"), length=Q_("2.0m"), width=Q_("2.0m"))
    assert solid.is_square()


def test_volume_of_solid_returns_correct_volume(solid):
    volume = round(solid.volume.magnitude, 3)
    # expected_volume = 3.864 * solid.units
    assert volume == 3.864


def test_supplying_only_height_and_length_creates_solid_with_square_cross_section():
    solid = Solid(Q_("3m"), Q_("4m"))
    assert solid.is_square()


def test_initialising_solid_with_negative_dimensions_results_in_zero_dimensions():
    solid = Solid(height=Q_("-1m"), length=Q_("-2m"))
    assert solid.height == ZERO_LENGTH
    assert solid.length == ZERO_LENGTH
    assert solid.width == ZERO_LENGTH


if __name__ == '__main__':
    pytest.main()
