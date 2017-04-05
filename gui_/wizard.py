from __future__ import division
from __future__ import generators
from __future__ import absolute_import

import sys
from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

from rpm.constants import *

# Because of from __future__ import absolute_import python 2
# translator may complain of attempting to do relative import in
# a directory that is not package. try ... except handles that
try:
    from . import wizard_ui
except (SystemError, ValueError) as e:
    import wizard_ui


class ProjectWizard(QWizard, wizard_ui.Ui_Wizard):

    def __init__(self, parent=None):
        super(ProjectWizard, self).__init__(parent)
        self.setupUi(self)
        watermark = QPixmap("watermark.jpg")
        logo = QPixmap("icon.png")
        self.setPixmap(QWizard.LogoPixmap, logo)
        self.setPixmap(QWizard.WatermarkPixmap, watermark)
        self.setOption(QWizard.ExtendedWatermarkPixmap)
        self.setMinimumSize(QSize(600, 400))
        self._configureWidgets()
        self.setWindowTitle("New RAP Project Wizard")

    def _configureWidgets(self):
        self.introPage.setTitle("Read, Very Important!")
        self.introPage.setSubTitle("The information on this page will help you understand how to use the wizard")
        self.projectDetailsPage.setTitle("Project Details")
        self.projectDetailsPage.setSubTitle("Project Details")
        self.geoPage.setTitle("Geotechnical & Geological Details")
        self.geoPage.setSubTitle("Geotechnical & Geological Details")
        self.pillarStrengthPage.setTitle("Pillar Strength Formula")
        self.pillarStrengthPage.setSubTitle("Pillar Strength Formula")
        self.locationComboBox.addItems([country.name.replace("_", " ").title() for country in Countries])
        self.oreTypeComboBox.addItems([mine_type.name.replace("_", " ").title() for mine_type in MineTypes])
        self.pillarFormulaComboBox.addItems([formula.name.replace("_", " ").title() for formula in PillarFormula])

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


def main():
    app = QApplication(sys.argv)
    top = ProjectWizard()
    top.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
