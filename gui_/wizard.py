from __future__ import division
from __future__ import generators
from __future__ import absolute_import

import sys
from os.path import (dirname, join)
from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

WIZARD_DIR = dirname(__file__)

if __name__ == '__main__':
    import wizard_ui
    module_path = join(WIZARD_DIR, "..")
    sys.path.append(module_path)
else:
    from . import wizard_ui

from rpm.constants import (ALL_FORMULA, OreTypes, Countries)
# from rpm.rpm_oop import (Sample, Pillar)


def text_to_enum(enum, text, sep=" "):
    """
    Converts a string to a value in an enumeration by converting the string
     to lowercase and replacing spaces with underscores
    enum_name: case-sensitive string of the enumeration name
    text: case-insensitive string probably formatted for human use
    """
    text = text.lower().replace(sep, "_")
    for enum_ in enum:
        if enum_.name == text:
            return enum_
    raise ValueError("{} has no {} attribute".format(enum, text))


def enum_to_text(enum, sep=" "):
    """
    Converts an enumeration to a format for display in gui
    """
    enum_name = enum.name
    return enum_name.replace("_", sep).title()


def name_to_formula(name):

    for formula in ALL_FORMULA:
        if formula.name == name:
            return formula
    raise ValueError("No formula called {}".format(name))


class ProjectWizard(QWizard, wizard_ui.Ui_Wizard):

    def __init__(self, parent=None):
        super(ProjectWizard, self).__init__(parent)
        self.setupUi(self)
        self._configure_widgets()
        self._bindings()
        self.update_constant()
        watermark = QPixmap(join(WIZARD_DIR,"watermark.png"))
        logo = QPixmap(join(WIZARD_DIR, "icon.png"))
        self.setPixmap(QWizard.LogoPixmap, logo)
        self.setPixmap(QWizard.WatermarkPixmap, watermark)
        self.setOption(QWizard.ExtendedWatermarkPixmap)
        self.setMinimumSize(QSize(650, 500))
        self.setWindowTitle("New RAP Project Wizard")
        if parent:
            self.setWindowIcon(parent.windowIcon())
            self.center_on_parent(parent)

    def _bindings(self):
        self.connect(self.pillarFormulaCombo, SIGNAL("currentIndexChanged(QString)"), self.update_constant)

    def center_on_parent(self, parent):
        qr = self.frameGeometry()
        cp = parent.frameGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_constant(self):
        formula_name = self.pillarFormulaCombo.currentText()
        formula = name_to_formula(formula_name)
        k, a, b = formula.k, formula.alpha, formula.beta
        self.constantKSpin.setEnabled(k is not None)
        if self.constantKSpin.isEnabled():
            self.constantKSpin.setValue(k)
        self.constantASpin.setValue(a)
        self.constantBSpin.setValue(b)

    def get_constants(self):
        k = self.constantKSpin.value()
        a = self.constantASpin.value()
        b = self.constantBSpin.value()
        return k, a, b

    def _configure_widgets(self):
        self.introPage.setTitle("Read, Very Important!")
        self.introPage.setSubTitle("The information on this page will help you understand how to use the wizard")
        self.projectDetailsPage.setTitle("Project Details")
        self.projectDetailsPage.setSubTitle("Project Details")
        self.geoPage.setTitle("Geotechnical & Geological Details")
        self.geoPage.setSubTitle("Geotechnical & Geological Details")
        self.pillarStrengthPage.setTitle("Pillar Strength Formula")
        self.pillarStrengthPage.setSubTitle("Pillar Strength Formula")

        self.locationCombo.addItems([enum_to_text(country) for country in Countries])
        self.locationCombo.setEditable(False)
        self.oreTypeCombo.addItems([enum_to_text(ore_type) for ore_type in OreTypes])
        self.oreTypeCombo.setEditable(False)
        self.pillarFormulaCombo.addItems([formula.name for formula in ALL_FORMULA])
        self.projectNameLineEdit.setText("New RAP Project")
        self.projectNameLineEdit.selectAll()
        self.drillBlastRadio.setChecked(True)
        self.cylindricalSampleRadio.setChecked(True)
        self.constantKSpin.setRange(1.0, 5000.0)

    def nextId(self, *args, **kwargs):
        """For room and pillar systems that are being designed for the first time there is limited
        geotechnical knowledge it better to skip the pillar strength formula selection page (PAGE 2)."""
        current_page = self.currentId()
        if current_page == 3:
            return -1
        elif current_page == 1 and self.initialDesignRadio.isChecked():
            return 3
        else:
            return current_page + 1

    # def get_dynamic_combo_data(self):
    #     str_loc = self.locationCombo.currentText()
    #     location = text_to_enum(Countries, str_loc)
    #     str_ore__type = self.oreTypeCombo.currentText()
    #     ore_type = text_to_enum(OreTypes, str_ore__type)
    #     value = (location, ore_type)
    #
    #     if self.redesignRadio.isChecked():
    #         formula = text_to_enum(PillarFormula, self.pillarFormulaCombo.currentText(), "-")
    #         k, a, b = self.get_constants()
    #         value = (location, ore_type, (formula, k, a, b))
    #
    #     return value


def main():
    app = QApplication(sys.argv)
    top = ProjectWizard()
    top.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
