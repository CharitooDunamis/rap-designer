from __future__ import division
from __future__ import generators
from __future__ import absolute_import
# from enum import Enum

from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from rpm.constants import *
# from pprint import pprint

import qtawesome as qta
import sys
try:
    from . import widgets
    from . import intropage_ui
    from . import mineinfo_ui
    from . import geotech_ui
    from . import  wizard_ui
except (SystemError, ValueError) as e:
    import widgets
    import intropage_ui
    import geotech_ui
    import mineinfo_ui
    import wizard_ui


class GridFormLayout(QGridLayout):

    def __init__(self):
        super(GridFormLayout, self).__init__()
        self.curRow = 0

    def addRow(self, widget1, widget2):
        self._addVariant(widget1, self.curRow, 0)
        self._addVariant(widget2, self.curRow, 1)
        self.curRow += 1

    def _addVariant(self, item, row, col):
        if isinstance(item, QLayoutItem):
            self.addItem(item, row, col)
        elif isinstance(item, QLayout):
            self.addLayout(item, row, col)
        else:
            self.addWidget(item, row, col)


def create_false_icon_label(text, icon_name, size=16, icon_options=None):
    pixmap = qta.icon(icon_name).pixmap(QSize(size, size))
    label = QLabel(text)
    label2 = QLabel()
    label2.setPixmap(pixmap)
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    label2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignRight)
    layout.addWidget(label2)
    layout.addWidget(label)
    return layout


class ProjectWizard(QWizard, wizard_ui.Ui_Wizard):

    def __init__(self, parent=None):
        super(ProjectWizard, self).__init__(parent)
        self.setupUi(self)
        watermark = QPixmap("watermark.jpg")
        # logo = QPixmap("icon.png")
        self.setPixmap(QWizard.WatermarkPixmap, watermark)
        self.setOption(QWizard.ExtendedWatermarkPixmap)
        # self.setPixmap(QWizard.LogoPixmap, logo)
        self.setMinimumSize(QSize(600, 400))
        self._configureWidgets()
        self.setWindowTitle("New RAP Project Wizard")

    def _configureWidgets(self):
        # self.introPage.setTitle("Read, Very Important!")
        # self.introPage.setSubTitle("The information on this page will help you understand how to use the wizard")
        # self.projectDetailsPage.setTitle("Project Details")
        # self.projectDetailsPage.setSubTitle("Project Details")
        # self.geoPage.setTitle("Geotechnical & Geological Details")
        # self.geoPage.setSubTitle("Geotechnical & Geological Details")
        # self.pillarStrengthPage.setTitle("Pillar Strength Formula")
        # self.pillarStrengthPage.setSubTitle("Pillar Strength Formula")
        self.locationComboBox.addItems([country.name.replace("_", " ").title() for country in Countries])
        self.oreTypeComboBox.addItems([mine_type.name.replace("_", " ").title() for mine_type in MineTypes])
        self.pillarFormulaComboBox.addItems([formula.name.replace("_", " ").title() for formula in PillarFormula])

    def nextId(self, *args, **kwargs):
        curPage = self.currentId()
        if curPage == 3:
            return -1
        elif curPage == 1 and self.stateRadio.isChecked():
            return 3
        else:
            return curPage + 1


def main():
    app = QApplication(sys.argv)
    top = ProjectWizard()
    top.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
