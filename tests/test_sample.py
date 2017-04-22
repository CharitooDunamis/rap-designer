import pytest

from rpm.rpm_oop import Sample
from rpm import Q_


@pytest.fixture
def sample(request):
    return Sample(strength=Q_("5.2MPa"), height=Q_("0.4inches"), diameter=Q_("0.12inches"))


@pytest.fixture
def c_sample(request):
    """Returns a cylindrical sample"""
    return Sample(strength=Q_("5.2m"), height=Q_("0.4m"), diameter=Q_("0.12m"), cylindrical=True)


@pytest.fixture
def sample2(request):
    return Sample(strength=Q_("3822psi"), height=Q_("40in"), diameter=Q_("54mm"))


def test_diameter_is_an_alias_for_length_of_samples(sample):
    assert sample.diameter == sample.length == sample.width


def test_non_cubical_sample_returns_false_for_is_cubical_method(sample):
    assert sample.is_cubic() is False


def test_cubical_sample_returns_true_for_is_cubical_method():
    sample = Sample(strength=Q_("5.2m"), height=Q_("0.2m"), diameter=Q_("0.2m"))
    assert sample.is_cubic()


def test_cylindrical_sample_returns_correct_volume(c_sample):
    assert round(c_sample.volume, 6) == Q_("0.004524meter**3")


def test_non_cylindrical_sample_return_correct_volume(sample):
    assert round(sample.volume, 6) == Q_("0.00576in**3")


def test_sample_returns_correct_gaddy_factor(sample2):
    expected = Q_("5573psi")
    result = round(sample2.gaddy_factor, 0)
    assert result == expected


def test_sample_returns_corret_cubical_strength(sample2):
    expected = Q_("929.0psi")
    result = round(sample2.cubical_strength, 0)
    assert expected == result
