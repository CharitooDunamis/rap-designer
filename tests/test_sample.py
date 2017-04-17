import pytest

from rpm.rpm_oop import Sample
from gui_ import Q_


@pytest.fixture
def sample(request):
    return Sample(strength=Q_(5.2), height=Q_(0.4), diameter=Q_(0.12))


@pytest.fixture
def c_sample(request):
    """Returns a cylindrical sample"""
    return Sample(strength=Q_(5.2), height=Q_(0.4), diameter=Q_(0.12), cylindrical=True)


def test_diameter_is_an_alias_for_length_of_samples(sample):
    assert sample.diameter == sample.length == sample.width


def test_non_cubical_sample_returns_false_for_is_cubical_method(sample):
    assert sample.is_cubical() is False


def test_cubical_sample_returns_true_for_is_cubical_method():
    sample = Sample(strength=Q_(5.2), height=Q_(0.2), diameter=Q_(0.2))
    assert sample.is_cubical()


def test_cylindrical_sample_returns_correct_volume(c_sample):
    assert round(c_sample.volume, 6) == 0.004524


def test_non_cylindrical_sample_return_correct_volume(sample):
    pytest.skip("WIP")
    assert round(sample.volume, 6) == 0.00576


def test_sample_returns_correct_gaddy_factor(sample):
    pytest.skip("WIP")
    sample = Sample(strength=5580, height=0.4, diameter=2.132)
    assert round(sample.gaddy_factor, 0) == 5580


def test_sample_returns_corret_cubical_strength(sample):
    pytest.skip("WIP")
    assert round(sample.cubical_strength, 10) == 413.0903262969
