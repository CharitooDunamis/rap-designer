from __future__ import division
from __future__ import generators
from __future__ import absolute_import

import sys
from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

from rpm.constants import *
from rpm.rpm_oop import Sample
from rpm.rpm_oop import Pillar

# Because of from __future__ import absolute_import python 2
# translator may complain of attempting to do relative import in
# a directory that is not package. try ... except handles that
try:
    from . import wizard_ui
except (SystemError, ValueError) as e:
    import wizard_ui


def text_to_enum(enum, text, sep="_"):
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


class ProjectWizard(QWizard, wizard_ui.Ui_Wizard):

    def __init__(self, parent=None):
        super(ProjectWizard, self).__init__(parent)
        self.setupUi(self)
        self._configure_widgets()
        watermark = QPixmap("watermark.jpg")
        logo = QPixmap("icon.png")
        self.setPixmap(QWizard.LogoPixmap, logo)
        self.setPixmap(QWizard.WatermarkPixmap, watermark)
        self.setOption(QWizard.ExtendedWatermarkPixmap)
        self.setMinimumSize(QSize(650, 400))
        self._bindings()
        self.update_constant()
        self.setWindowTitle("New RAP Project Wizard")

    def _bindings(self):
        self.connect(self.pillarFormulaComboBox, SIGNAL("currentIndexChanged(QString)"), self.update_constant)

    def update_constant(self):
        k, a, b = 0, 0, 0
        form_text = self.pillarFormulaComboBox.currentText()
        enum = text_to_enum(PillarFormula, form_text, sep="-")
        try:
            k, a, b = enum.value
        except ValueError as e:
            a, b = enum.value
            k = 0
        self.constantKDoubleSpinBox.setValue(k)
        self.constantADoubleSpinBox.setValue(a)
        self.constantBDoubleSpinBox.setValue(b)

    def get_constants(self):
        k = self.constantKDoubleSpinBox.value()
        a = self.constantADoubleSpinBox.value()
        b = self.constantBDoubleSpinBox.value()
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
        self.locationComboBox.addItems([enum_to_text(country) for country in Countries])
        self.oreTypeComboBox.addItems([enum_to_text(ore_type) for ore_type in OreTypes])
        self.pillarFormulaComboBox.addItems([enum_to_text(formula, "-") for formula in PillarFormula])
        self.projectNameLineEdit.setText("New RAP Project")
        self.projectNameLineEdit.selectAll()

    def nextId(self, *args, **kwargs):
        """For room and pillar systems that are being designed for the first time there is limited
        geotechnical knowledge it better to skip the pillar strength formula selection page (PAGE 2)."""
        current_page = self.currentId()
        if current_page == 3:
            return -1
        elif current_page == 1 and self.stateRadio.isChecked():
            return 3
        else:
            return current_page + 1

    def get_data(self):
        # Page 1 Data
        project_name = self.projectNameLineEdit.text()
        str_loc = self.locationComboBox.currentText()
        location = text_to_enum(Countries, str_loc)
        str_ore__type = self.oreTypeComboBox.currentText()
        ore_type = text_to_enum(OreTypes, str_ore__type)
        min_extraction = self.minExtractionSpinBox.value()
        room_span = self.roomWidthSpinBox.value()
        drill_blast = self.drillBlastRadio.isChecked()
        # Page 2 Data
        sample_height = self.sampleHeightDoubleSpinBox.value()
        sample_diameter = self.sampleDiameterDoubleSpinBox.value()
        sample_strength = self.uniaxStrengthDoubleSpinBox.value()
        is_cylinder = self.cylindricalSampleRadio.isChecked()

        cohesion = self.cohesionDoubleSpinBox.value()
        rmr = self.rmrSpinBox.value()
        friction_angle = self.frictionAngleDoubleSpinBox.value()

        depth = self.oreDepthDoubleSpin.value()
        overburden_sg = self.overburdenDensityDoubleSpinBox.value()
        seam_dip = self.seamDipDoubleSpin.value()
        seam_height = self.seamHeightDoubleSpin.value()

        sample = Sample(sample_strength, sample_height, sample_diameter, is_cylinder)
        pillar = Pillar(sample, seam_height, 0)

        if self.redesignRadio.isChecked():
            formula = text_to_enum(PillarFormula, self.pillarFormulaComboBox.currentText())
            k, a, b = self.get_constants()


def main():
    app = QApplication(sys.argv)
    top = ProjectWizard()
    top.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
