from rpm.utils import *
import pytest


def test_mpa_to_psi_returns_correct_value():
    assert round(mpa_to_psi(3.5), 3) == 507.632


def test_psi_to_mpa():
    assert round(psi_to_mpa(230), 3) == 1.586


def test_feet_to_meters():
    m = feet_to_meters(8.43)
    assert round(m, 3) == 2.569


def test_meters_to_feet():
    ft = meters_to_feet(1.234567)
    assert round(ft, 5) == 4.05042


def test_meters_to_inches():
    inches = meters_to_inches(1.234567)
    assert round(inches, 5) == 48.605


def test_converting_meter_to_both_feet_and_inches_maintains_proportion():
    meters = 1.23456789
    ft = meters_to_feet(meters)
    inches = meters_to_inches(meters)
    assert round(ft, 5) == round(inches / 12, 5)


if __name__ == '__main__':
    pytest.main()
