import pytest
import sys

from qtpy.QtTest import QTest
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from gui_.wizard import ProjectWizard
from rpm.constants import *


app = QApplication(sys.argv)


@pytest.fixture
def wizard(request):
    return ProjectWizard()
#
# def test_wizard_skips_formula_page_if_it_is_initial_design(wizard):
#     QTest.mouseClick(wizard.button(QWizard.BackButton), Qt.LeftButton)
#     print("THIS IS THE CURRENT ID: %d" % wizard.currentId)
#     wizard.stateRadio.setChecked(True)
#     QTest.mouseClick(wizard.button(QWizard.BackButton), Qt.LeftButton)
#     assert wizard.currentId() == 3


def test_forms_project_details_page_have_correct_defaults(wizard):
    assert wizard.redesignRadio.isChecked() is False
    assert wizard.stateRadio.isChecked() is True
    assert wizard.minExtractionSpinBox.value() == 50
    assert wizard.roomWidthSpinBox.value() == 6.0


def test_geo_technical_forms_have_correct_defaults(wizard):
    assert wizard.uniaxStrengthDoubleSpinBox.value() == 38.47
    assert wizard.cohesionDoubleSpinBox.value() == 0.2
    assert wizard.frictionAngleDoubleSpinBox.value() == 19.0
    assert wizard.rmrSpinBox.value() == 44
    assert wizard.sampleDiameterDoubleSpinBox.value() == 1.0
    assert wizard.sampleHeightDoubleSpinBox.value() == 1.0


def test_geological_forms_have_correct_defaults(wizard):
    assert wizard.overburdenDensityDoubleSpinBox.value() == 20.0
    assert wizard.oreDepthDoubleSpin.value() == 150.0
    assert wizard.seamDipDoubleSpin.value() == 15.0
    assert wizard.seamHeightDoubleSpin.value() == 4.0


def test_ore_type_combo_has_correct_number_of_items(wizard):
    item_no = len(MineTypes)
    for i in range(item_no):
        wizard.oreTypeComboBox.setCurrentIndex(i)
        assert wizard.oreTypeComboBox.currentText() != ""
    wizard.oreTypeComboBox.setCurrentIndex(item_no + 1)
    assert wizard.oreTypeComboBox.currentText() == ""


def test_pillar_formula_combo_has_correct_number_of_items(wizard):
    wizard = ProjectWizard()
    item_no = len(PillarFormula)
    for i in range(item_no):
        wizard.pillarFormulaComboBox.setCurrentIndex(i)
        assert wizard.pillarFormulaComboBox.currentText() != ""
    wizard.pillarFormulaComboBox.setCurrentIndex(item_no + 1)
    assert wizard.pillarFormulaComboBox.currentText() == ""


def test_pillar_location_combo_has_correct_number_of_items(wizard):
    wizard = ProjectWizard()
    item_no = len(Countries)
    for i in range(item_no):
        wizard.locationComboBox.setCurrentIndex(i)
        assert wizard.locationComboBox.currentText() != ""
    wizard.locationComboBox.setCurrentIndex(item_no + 1)
    assert wizard.locationComboBox.currentText() == ""


if __name__ == '__main__':
    pytest.main()
    # crazy_test_dummy()
