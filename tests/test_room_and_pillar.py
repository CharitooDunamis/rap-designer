import pytest
# from unittest import mock

from rpm.rpm_oop import (RoomAndPillar, Pillar, Sample, StrengthFormula)
from rpm import unit_reg, Q_
from rpm.constants import ALL_FORMULA


@pytest.fixture
def rap_object(request):
    sample = Sample(strength=Q_("3822psi"), height=Q_("1in"), diameter=Q_("1.125in"))
    pillar = Pillar(sample, height=Q_("7ft"), length=Q_("80ft"), width=Q_("60ft"))
    rap = RoomAndPillar(pillar=pillar, room_span=Q_("18ft"))
    rap.seam_height = Q_("7ft")
    rap.mine_depth = Q_("500ft")
    return rap


