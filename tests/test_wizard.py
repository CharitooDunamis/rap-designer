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
    assert wizard.initialDesignRadio.isChecked() is True
    assert wizard.minExtractionSpin.value() == 50
    assert wizard.roomWidthSpin.value() == 6.0
    assert wizard.drillBlastRadio.isChecked() is False
    assert wizard.redesignRadio.isChecked() is False


def test_geo_technical_forms_have_correct_defaults(wizard):
    assert wizard.uniaxStrengthSpin.value() == 38.47
    assert wizard.cohesionSpin.value() == 0.2
    assert wizard.frictionAngleSpin.value() == 19.0
    assert wizard.rmrSpin.value() == 44
    assert wizard.sampleDiameterSpin.value() == 1.0
    assert wizard.sampleHeightSpin.value() == 1.0


def test_geological_forms_have_correct_defaults(wizard):
    assert wizard.overburdenDensitySpin.value() == 20.0
    assert wizard.oreDepthSpin.value() == 150.0
    assert wizard.seamDipSpin.value() == 15.0
    assert wizard.seamHeightSpin.value() == 4.0


def test_ore_type_combo_has_correct_number_of_items(wizard):
    item_no = len(OreTypes)
    for i in range(item_no):
        wizard.oreTypeCombo.setCurrentIndex(i)
        assert wizard.oreTypeCombo.currentText() != ""
    wizard.oreTypeCombo.setCurrentIndex(item_no + 1)
    assert wizard.oreTypeCombo.currentText() == ""


def test_pillar_formula_combo_has_correct_number_of_items(wizard):
    wizard = ProjectWizard()
    item_no = len(PillarFormula)
    for i in range(item_no):
        wizard.pillarFormulaCombo.setCurrentIndex(i)
        assert wizard.pillarFormulaCombo.currentText() != ""
    wizard.pillarFormulaCombo.setCurrentIndex(item_no + 1)
    assert wizard.pillarFormulaCombo.currentText() == ""


def test_pillar_location_combo_has_correct_number_of_items(wizard):
    wizard = ProjectWizard()
    item_no = len(Countries)
    for i in range(item_no):
        wizard.locationCombo.setCurrentIndex(i)
        assert wizard.locationCombo.currentText() != ""
    wizard.locationCombo.setCurrentIndex(item_no + 1)
    assert wizard.locationCombo.currentText() == ""


if __name__ == '__main__':
    pytest.main()
    # crazy_test_dummy()
