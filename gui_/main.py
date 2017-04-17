from __future__ import absolute_import

import sys

from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *
import qtawesome as qta

from .wizard import ProjectWizard
from .dialogs import *
from .wizard import enum_to_text
from .wizard import text_to_enum
from . import (unit_reg, Q_, NamedQuantity, NamedStr, NamedInt, NamedFloat)
from rpm.rpm_oop import *
from rpm.constants import (Countries, PillarFormula, OreTypes)


def spin_to_named_quantity(spin_widget, name=None):
    magnitude = spin_widget.value()
    unit = spin_widget.suffix() if spin_widget.suffix() else ""
    string = "{} {}".format(magnitude, unit)
    return NamedQuantity(string.strip(), name=name)


class MineRapper(QMainWindow):

    def __init__(self, parent=None):
        super(MineRapper, self).__init__(parent)
        self.setMinimumSize(QSize(400, 300))
        self.setGeometry(QRect(100, 100, 800, 600))
        self.setWindowTitle(QApplication.applicationName())
        self.setWindowIcon(QIcon("icon.png"))

        # Children
        self.wiz = ProjectWizard()
        self.status_bar = self.statusBar()
        self.create_toolbars()
        self.canvas = QGraphicsView(self)
        self.setCentralWidget(self.canvas)

        # DATA
        self.pillar = None
        self.projectName = None
        self.designType = None
        self.roomWidth = None
        self.location = None
        self.oreType = None
        self.roomSpan = None
        self.minExtraction = None
        self.fragmentMethod = None

        self.frictionAngle = None
        self.cohesion = None
        self.rmr = None
        self.seamHeight = None
        self.seamDip = None
        self.mineDepth = None
        self.floorDensity = None
        self.overburdenDensity = None
        self.pillarFormula = None

        # set to True when any data is modified
        self.dirty = False
        # set to True when the system has data to work with
        self.hasData = False
        self.bindings()


    def bindings(self):
        self.connect(self.wiz, SIGNAL("finished(int)"), self.get_wiz_data)

    def create_action(self, text, slot=None, icon=None, shortcut=None, tip=None, checkable=False, signal='triggered()',
                      icn_options=None):
        """
        Returns a QAction, which can be added to a menu or a toolbar
        :param text: The text that appears if the action is added to a menu
        :param slot: The slot the action is connected to
        :param icon: The name of the awesome font to use
        :param shortcut: The shortcut for the action
        :param tip: The tooltip and status tip for the action
        :param checkable: Set to true if the action is checkable
        :param signal: The signal which should trigger the slot
        :param icn_options: qt awesome options to be applied to the font awesome icon
        :return: QAction
        """
        action = QAction(text, self)
        action.setCheckable(checkable)
        if slot:
            self.connect(action, SIGNAL(signal), slot)
        if icon:
            icon = qta.icon(icon, **icn_options)
            action.setIcon(icon)
        if shortcut:
            action.setShortcut(shortcut)
        if tip:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        return action

    def create_toolbars(self):
        all_tools = self.addToolBar("Main")
        all_tools.setObjectName("MainToolbar")
        all_tools.setIconSize(QSize(32, 32))
        new_action = self.create_action("&New", icon='fa.file-text', shortcut=QKeySequence.New,
                                        tip="Create a new RAP project.", icn_options={"color": "black"},
                                        slot=self.new_project)
        info_action = self.create_action("&About", icon="fa.info-circle", shortcut="Shift + A", tip="About Mine RAPPa",
                                         slot=self.about, icn_options={"color": "black"})
        save_action = self.create_action("&Save", icon="fa.save", shortcut=QKeySequence.Save, tip="Save RAP Project",
                                         slot=self.save, icn_options={"color": "black"})
        graph_action = self.create_action("&Sensitivity", icon="fa.line-chart",
                                          tip="Sensitivity Analysis for current plan", icn_options={})
        export_action = self.create_action("&Export Results", icon="fa.file-pdf-o", tip="Export results",
                                           slot=self.export, icn_options={})
        config_action = self.create_action("&Settings", icon="fa.cog", tip="Change settings", icn_options={})
        all_tools.addActions([new_action, save_action])
        all_tools.addSeparator()
        all_tools.addActions([export_action, graph_action])
        all_tools.addSeparator()
        all_tools.addActions([config_action, info_action])

    def new_project(self):
        self.wiz.exec_()

    def get_wiz_data(self):
        self.projectName = self.wiz.projectNameLineEdit.text()
        str_loc = self.wiz.locationCombo.currentText()
        str_ore__type = self.wiz.oreTypeCombo.currentText()
        self.location = text_to_enum(Countries, str_loc)
        self.oreType = text_to_enum(OreTypes, str_ore__type)

        self.roomSpan = spin_to_named_quantity(self.wiz.roomWidthSpin, name="Room Span")
        self.minExtraction = spin_to_named_quantity(self.wiz.minExtractionSpin, name="Minimum Extraction")

        fragmentation = "Drill Blast" if self.wiz.drillBlastRadio.isChecked() else "Continuous Miner"
        self.fragmentMethod = NamedStr(fragmentation, name="Method of Fragmenting")

        # Page 2 Data
        sample_height = spin_to_named_quantity(self.wiz.sampleHeightSpin, name="Sample Height")
        sample_diameter = spin_to_named_quantity(self.wiz.sampleDiameterSpin, name="Sample Diameter")
        sample_strength = spin_to_named_quantity(self.wiz.uniaxStrengthSpin, name="Sample Strength")
        is_cylinder = self.wiz.cylindricalSampleRadio.isChecked()

        self.frictionAngle = NamedInt(self.wiz.frictionAngleSpin.value(), name="Friction Angle")
        self.cohesion = spin_to_named_quantity(self.wiz.cohesionSpin, name="Cohesion")
        self.rmr = spin_to_named_quantity(self.wiz.rmrSpin, name="RMR")

        self.seamHeight = spin_to_named_quantity(self.wiz.seamHeightSpin, name="Seam Height")
        self.seamDip = NamedInt(self.wiz.seamDipSpin.value(), name="Seam Dip")
        self.mineDepth = spin_to_named_quantity(self.wiz.oreDepthSpin, name="Mine Depth")
        self.floorDensity = NamedFloat(self.wiz.floorDensitySpin.value(), name="Specific Gravity of Floor")
        self.overburdenDensity = NamedFloat(self.wiz.overburdenDensitySpin.value(),
                                            name="Specific Gravity of Overburden")

        sample = Sample(sample_strength, sample_height, sample_diameter, is_cylinder)
        self.pillar = Pillar(sample, self.seamHeight, 0)

    def save(self):
        if not self.dirty:
            return
        pass

    def export(self, format=None):
        pass

    def about(self):
        about_dlg = AboutDialog(self)
        about_dlg.show()


class RapparApp(QApplication):

    def __init__(self, args):
        super(RapparApp, self).__init__(args)
        self.setApplicationName("Mine RAPAR")
        self.setApplicationVersion("0.0.1")
        self.setOrganizationName("Charis Optimal Systems")
        self.setOrganizationDomain("charitoodunamis.github.io")
        top = MineRapper()
        top.show()
        sys.exit(self.exec_())


def main():
    app = RapparApp(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
