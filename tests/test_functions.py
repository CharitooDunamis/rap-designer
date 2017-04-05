import pytest
from rpm import rpm_functions as rpmf


def test_salamon_pillar_strength_against_known_values():
    width = height = 5
    assert round(rpmf.salamon(width, height), 4) == 5.2039


def test_bieniawski_pillar_strength_against_known_results():
    assert rpmf.bieniawski(10, 5, 5) == 10


def test_square_pillar_extraction_ratio_against_known_values():
    result = round(rpmf.square_pillar_extraction_ratio(4, 2.35), 2)
    assert result == 0.37


def test_tributary_square_pillar_stress_against_known_values():
    result = round(rpmf.square_pillar_stress(3, 6, 4), 2)
    assert result == 18.75


def test_shape_factor_gamma_against_known_values():
    pass


def test_shape_factor_g_against_known_values():
    pass


def test_strength_factor_ng_against_known_values():
    pass


if __name__ == '__main__':
    pytest.main()
