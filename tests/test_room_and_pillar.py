import pytest
# from unittest import mock

from rpm.rpm_oop import (RoomAndPillar, Pillar, Sample, ALL_FORMULA)
from rpm import unit_reg, Q_


@pytest.fixture
def rap_object(request):
    sample = Sample(strength=Q_("3822psi"), height=Q_("40in"), diameter=Q_("54mm"))
    pillar = Pillar(sample, height=Q_("7ft"), length=Q_("80ft"), width=Q_("60ft"))
    rap = RoomAndPillar(pillar=pillar, room_span=Q_("18ft"))
    rap.seam_height = Q_("7ft")
    rap.mine_depth = Q_("500ft")
    return rap


def test_room_and_pillar_object_returns_correct_bieniawski_pillar_strength(rap_object):
    rap_object.formula = ALL_FORMULA[2] # bieniawski
    expected = rap_object.pillar_strength
    assert round(expected, 0) == Q_("3460psi")


def test_room_and_pillar_object_returns_correct_pillar_stress(rap_object):
    result = rap_object.pillar_stress
    expected = Q_("876psi")
    assert round(result, 0) == expected


def test_room_and_pillar_object_has_correct_factor_of_safety_when_bieniawski_is_used(rap_object):
    rap_object.formula = ALL_FORMULA[2]
    result = rap_object.factor_of_safety
    assert round(result, 2) == 3.95
