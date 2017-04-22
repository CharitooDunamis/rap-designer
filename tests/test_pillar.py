import pytest

from rpm.rpm_oop import (Sample, Pillar)
from rpm import (Q_, unit_reg)


@pytest.fixture
def pillar(request):
    sample = Sample(strength=Q_("3822psi"), height=Q_("1in"), diameter=Q_("1.125in"))
    return Pillar(sample, height=Q_("7ft"), length=Q_("80ft"), width=Q_("60ft"))


def test_pillar_strength(pillar):
    pass
