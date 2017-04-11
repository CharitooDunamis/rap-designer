from __future__ import absolute_import

import sys

from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *
import qtawesome as qta

if __name__ == "__main__":
    sys.path.append("../rpm/")
    from wizard import ProjectWizard
    from wizard import enum_to_text
    from wizard import text_to_enum
    from dlg import *
    from __init__ import (unit_reg, Q_)
    from rpm_oop import Sample
else:
    from .wizard import ProjectWizard
    from .dlg import *
    from .wizard import enum_to_text
    from .wizard import text_to_enum
    from . import unit_reg, Q_
    from rpm.rpm_oop import *
    from rpm.constants import (Countries, PillarFormula, OreTypes)



class MineRapper(QMainWindow):

    def __init__(self, parent=None):
        super(MineRapper, self).__init__(parent)
        self.create_children()
        self.setMinimumSize(QSize(400, 300))
        self.setGeometry(QRect(100, 100, 800, 600))
        self.setWindowTitle(QApplication.applicationName())
        self.setWindowIcon(QIcon("icon.png"))
        self.pillar = None
        self.room = None

        # set to True when any data is modified
        self.dirty = False

    def create_children(self):
        self.status_bar = self.statusBar()
        self.create_toolbars()
        self.canvas = QGraphicsView(self)
        self.setCentralWidget(self.canvas)

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
        wizard = ProjectWizard(self)
        wizard.exec_()
        project_name = wizard.projectNameLineEdit.text()
        # str_loc = wizard.locationComboBox.currentText()
        # location = text_to_enum(Countries, str_loc)
        # str_ore__type = wizard.oreTypeComboBox.currentText()
        # ore_type = text_to_enum(OreTypes, str_ore__type)
        min_extraction = wizard.minExtractionSpin.value()
        room_span = wizard.roomWidthSpin.value()
        drill_blast = wizard.drillBlastRadio.isChecked()
        # Page 2 Data
        sample_height = wizard.sampleHeightSpin.value()
        sample_diameter = wizard.sampleDiameterSpin.value()
        sample_strength = wizard.uniaxStrengthSpin.value()
        is_cylinder = wizard.cylindricalSampleRadio.isChecked()

        cohesion = wizard.cohesionSpin.value()
        rmr = wizard.rmrSpin.value()
        friction_angle = wizard.frictionAngleSpin.value()

        depth = wizard.oreDepthSpin.value()
        overburden_sg = wizard.overburdenDensitySpin.value()
        seam_dip = wizard.seamDipSpin.value()
        seam_height = wizard.seamHeightSpin.value()

        combo_data = wizard.get_dynamic_combo_data()

        sample = Sample(sample_strength, sample_height, sample_diameter, is_cylinder)
        pillar = Pillar(sample, seam_height, 0)

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
