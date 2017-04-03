import sys

import pytest
from qtpy.QtTest import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from qtpy.QtCore import *

from gui_ import widgets as wd

app = QApplication(sys.argv)


def test_create_labelled_spin_has_correct_default_value():
    _, spin = wd.createLabelledSpin(label="Label", double=False, suffix="m", default=10)
    assert spin.value() == 10


def test_labelled_spin_does_not_allow_value_to_be_set_below_minimum_value():
    _, spin = wd.createLabelledSpin(label="Label", double=True, max_=10, min_=2)
    QTest.keyClicks(spin, "1.2")
    assert spin.value() == 2.0


def test_create_labelled_spin_returns_correct_value_after_value_entry_with_keyboard():
    # pytest.skip("Keyboard clicks seem not to be working.\n Always returns a vlaue that is related to min_")
    _, spin = wd.createLabelledSpin(label="Label", double=True, max_=100, min_=50)
    assert spin.value() == 50
    spin.clear()
    QTest.keyClicks(spin, "55")
    # QTest.keyClick(spin, Qt.Key_4)
    assert spin.value() == 55.0


def test_labelled_spin_responds_to_keyboard_arrow_events():
    _, spin = wd.createLabelledSpin(label="Label", double=True, max_=10, min_=2)
    QTest.keyClick(spin, Qt.Key_Up)
    assert spin.value() == 3.0


def test_labelled_spin_does_not_allow_value_to_be_set_above_maximum_value():
    _, spin = wd.createLabelledSpin(label="Label", double=True, max_=10, min_=2)
    QTest.keyClicks(spin, "10.2")
    assert spin.value() == 2


def test_setting_double_to_false_creates_a_spin_box():
    _, spin = wd.createLabelledSpin(label="Label", double=False)
    assert isinstance(spin, QSpinBox) is True


def test_setting_double_to_true_creates_double_spin_box():
    _, spin = wd.createLabelledSpin("Me", double=True)
    assert isinstance(spin, QDoubleSpinBox) is True


if __name__ == '__main__':
    pytest.main()
