import pytest
# from unittest.mock import MagicMock

from rpm.rpm_oop import (RoomAndPillar, Pillar, Sample, StrengthFormula, ALL_FORMULA)
from rpm import unit_reg, Q_


@pytest.fixture
def rap_object(request):
    sample = Sample(strength=Q_("3822psi"), height=Q_("40in"), diameter=Q_("54mm"))
    pillar = Pillar(sample, height=Q_("7ft"), length=Q_("80ft"), width=Q_("60ft"))
    rap = RoomAndPillar(pillar=pillar, room_span=Q_("18ft"))
    rap.seam_height = Q_("7ft")
    rap.mine_depth = Q_("500ft")
    return rap


@pytest.fixture
def rap_obj2(request):
    formula = StrengthFormula(alpha=0.5, beta=-0.7, k=10.44, unit_system=StrengthFormula.METRIC,
                              category=StrengthFormula.EXPONENTIAL, k_type=StrengthFormula.OTHER)
    sample = Sample(strength=Q_("3822psi"), height=Q_("40in"), diameter=Q_("54mm"))
    pillar = Pillar(sample, height=Q_("3m"), length=Q_("7m"), width=Q_("7m"))
    rap = RoomAndPillar(pillar=pillar, room_span=Q_("6m"))
    rap.seam_height = Q_("3m")
    rap.mine_depth = Q_("150m")
    rap.overburden_density = Q_("22.5kilonewton per metre ** 3")
    rap.formula = formula
    return rap


@pytest.fixture
def amoako_rap(request):
    formula = StrengthFormula(alpha=0.4, beta=-0.6, k=15, k_type=StrengthFormula.OTHER, fos=(1, 1.5, 2.0),
                              unit_system=StrengthFormula.METRIC, category=StrengthFormula.EXPONENTIAL)
    sample = Sample(strength=Q_("3822psi"), height=Q_("40in"), diameter=Q_("54mm"))
    pillar = Pillar(sample, height=Q_("4m"), length=Q_("4m"), width=Q_("4m"))
    amoako = RoomAndPillar(pillar, formula, Q_("6m"))
    amoako.overburden_density = Q_("20kilonewton per metre ** 3")
    amoako.mine_depth = Q_("150m")
    amoako.seam_dip = Q_("15degrees")
    return amoako


@pytest.fixture
def rap_for_bearing_cap(request):
    sample = Sample(strength=Q_("3822psi"), height=Q_("40in"), diameter=Q_("54mm"))
    pillar = Pillar(sample=sample, height=Q_("3m"), length=Q_("10m"))
    rap_object = RoomAndPillar(pillar=pillar)
    rap_object.cohesion = Q_("1.2megapascal")
    rap_object.friction_angle = Q_("28degrees")
    rap_object.floor_density = Q_("22kilonewton per metre ** 3")
    rap_object.room_span = Q_("6m")
    rap_object.mine_depth = Q_("150m")
    rap_object.seam_height = Q_("3m")
    rap_object.overburden_density = Q_("22.5kilonewton per metre ** 3")
    return rap_object


def test_room_and_pillar_object_returns_correct_bieniawski_pillar_strength(rap_object):
    rap_object.formula = ALL_FORMULA[2] # bieniawski
    expected = rap_object.pillar_strength
    assert round(expected, 0) == Q_("3460psi")


def test_room_and_pillar_returns_correct_vertical_pre_mining_stress(rap_for_bearing_cap):
    result = rap_for_bearing_cap.vertical_pre_mining_stress
    expected = Q_("3.38megapascal").to(unit_reg.psi)
    assert round(result, 2) == expected


def test_room_and_pillar_object_returns_correct_pillar_stress(rap_object):
    result = rap_object.pillar_stress
    expected = Q_("876psi")
    assert round(result, 0) == expected


def test_room_and_pillar_object_has_correct_factor_of_safety_when_bieniawski_is_used(rap_object):
    rap_object.formula = ALL_FORMULA[2]
    result = rap_object.factor_of_safety
    assert round(result, 2) == 3.95


def test_rap_object_extraction_ratio(rap_object):
    rap_object.formula = ALL_FORMULA[2]
    result = rap_object.extraction_ratio
    assert round(result, 2) == 37.21


def test_room_and_pillar_returns_correct_fos_for_defined_strength_formula(amoako_rap):
    assert round(amoako_rap.factor_of_safety, 2) == 0.61


def test_room_and_pillar_returns_correct_pillar_strength_for_defined_strength_formula(amoako_rap):
    assert round(amoako_rap.pillar_strength, 2) == Q_("11.37megapascal")


def test_room_and_pillar_width_from_stress_and_fos(amoako_rap):
    amoako_rap.pillar_width_from_fos_and_stress()
    result = amoako_rap.pillar.width
    assert round(result, 1) == Q_("7.5m")

# --- Shape Factor Test -----------


def test_room_and_pillar_returns_correct_sf_gamma(rap_for_bearing_cap):
    expected = rap_for_bearing_cap.sf_gamma
    assert round(expected, 2) == 0.6


def test_room_and_pillar_returns_correct_sf_q(rap_for_bearing_cap):
    expected = rap_for_bearing_cap.sf_q
    assert round(expected, 2) == 1.47

# ------- Bearing Capacity Factor Tests -----------------


def test_room_and_pillar_returns_correct_bcf_q(rap_for_bearing_cap):
    expected = rap_for_bearing_cap.bcf_q
    assert round(expected, 2) == 14.72


def test_room_and_pillar_returns_correct_bcf_gamma(rap_for_bearing_cap):
    expected = rap_for_bearing_cap.bcf_gamma
    assert round(expected, 2) == 10.94


def test_room_and_pillar_returns_correct_bcf_c(rap_for_bearing_cap):
    expected = rap_for_bearing_cap.bcf_c
    assert round(expected, 2) == 25.80


def test_room_and_pillar_returns_correct_bearing_capacity_fos(rap_for_bearing_cap):
    expected = 5.47
    result = rap_for_bearing_cap.bearing_capacity_factor_of_safety
    assert round(result, 2) == expected
