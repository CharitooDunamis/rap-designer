import sys

from qtpy.QtCore import (SIGNAL, QSize, QRect)
from qtpy.QtGui import QKeySequence, QIcon
from qtpy.QtWidgets import (QAction, QApplication, QDesktopWidget, QGraphicsView, QMainWindow)
import qtawesome as qta

from .dialogs import AboutDialog
from .wizard import (text_to_enum, ProjectWizard, name_to_formula)
from rpm import (ZERO_LENGTH, DimensionalityError, unit_reg, Q_)
from rpm.rpm_oop import (RoomAndPillar, Sample, Pillar, StrengthFormula)
from rpm.constants import (Countries, ALL_FORMULA, OreTypes)


UNICODE_UNITS = {
    "°": "degree",
    "lb/ft³": "pound per foot ** 3",
}


def quantity_from_spin(spin_widget):
    magnitude = spin_widget.value()
    unit = spin_widget.suffix().strip()
    # pint does not support unicode units
    unit = UNICODE_UNITS.get(unit, None) or unit
    try:
        unit = unit_reg(unit)
    # AttributeError for when unit is None or NoneType
    except (DimensionalityError, AttributeError) as e:
        # print(e)
        unit = None
    quantity = Q_(magnitude)
    if unit:
        quantity *= unit
    # print(quantity)
    return quantity


class MineRapper(QMainWindow):

    def __init__(self, parent=None):
        super(MineRapper, self).__init__(parent)
        self.setMinimumSize(QSize(400, 300))
        self.setGeometry(QRect(100, 100, 800, 600))
        self.setWindowTitle(QApplication.applicationName())
        self.setWindowIcon(QIcon("gui_/icon.png"))

        # Children
        self.wiz = ProjectWizard(self)
        self.status_bar = self.statusBar()
        self.create_toolbars()
        self.canvas = QGraphicsView(self)
        self.setCentralWidget(self.canvas)

        self.rpm = None
        # set to True when any data is modified
        self.dirty = False
        self.bindings()
        self.center_on_screen()
        self.update_interface()

    @property
    def has_data(self):
        """Does the system has any data to work with"""
        return self.rpm is not None

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
        self.new_action = self.create_action("&New", icon='fa.file-text', shortcut=QKeySequence.New,
                                        tip="Create a new RAP project.", icn_options={"color": "black"},
                                        slot=self.new_project)
        self.info_action = self.create_action("&About", icon="fa.info-circle", shortcut="Shift + A", tip="About Mine RAPPa",
                                         slot=self.about, icn_options={"color": "black"})
        self.save_action = self.create_action("&Save", icon="fa.save", shortcut=QKeySequence.Save, tip="Save RAP Project",
                                         slot=self.save, icn_options={"color": "black"})
        self.graph_action = self.create_action("&Sensitivity", icon="fa.line-chart",
                                          tip="Sensitivity Analysis for current plan", icn_options={})
        self.export_action = self.create_action("&Export Results", icon="fa.file-pdf-o", tip="Export results",
                                           slot=self.export, icn_options={})
        self.config_action = self.create_action("&Settings", icon="fa.cog", tip="Change settings", icn_options={})
        all_tools.addActions([self.new_action, self.save_action])
        all_tools.addSeparator()
        all_tools.addActions([self.export_action, self.graph_action])
        all_tools.addSeparator()
        all_tools.addActions([self.config_action, self.info_action])

    def update_interface(self):
        has_data = self.has_data
        data_dependent_ui = [self.save_action, self.graph_action, self.export_action, self.graph_action]
        for component in data_dependent_ui:
            component.setEnabled(has_data)

    def new_project(self):
        self.wiz.exec_()

    def get_wiz_data(self):
        rpm = RoomAndPillar()
        rpm.project_name = self.wiz.projectNameLineEdit.text()
        str_loc = self.wiz.locationCombo.currentText()
        str_ore_type = self.wiz.oreTypeCombo.currentText()
        rpm.location = text_to_enum(Countries, str_loc)
        rpm.ore_type = text_to_enum(OreTypes, str_ore_type)

        rpm.room_span = quantity_from_spin(self.wiz.roomWidthSpin)
        rpm.min_extraction = self.wiz.minExtractionSpin.value()

        rpm.fragment_method = RoomAndPillar.DRILL_BLAST if self.wiz.drillBlastRadio.isChecked() \
            else RoomAndPillar.CONTINUOUS_MINER

        rpm.design_type = RoomAndPillar.REDESIGN if self.wiz.redesignRadio.isChecked() else RoomAndPillar.INITIAL

        # Page 2 Data
        sample_height = quantity_from_spin(self.wiz.sampleHeightSpin)
        sample_diameter = quantity_from_spin(self.wiz.sampleDiameterSpin)
        sample_strength = quantity_from_spin(self.wiz.uniaxStrengthSpin)
        is_cylinder = self.wiz.cylindricalSampleRadio.isChecked()

        rpm.friction_angle = quantity_from_spin(self.wiz.frictionAngleSpin)
        rpm.cohesion = quantity_from_spin(self.wiz.cohesionSpin)
        rpm.rmr = self.wiz.rmrSpin.value()

        rpm.seam_height = quantity_from_spin(self.wiz.seamHeightSpin)
        rpm.seam_dip = quantity_from_spin(self.wiz.seamDipSpin)
        rpm.mine_depth = quantity_from_spin(self.wiz.oreDepthSpin)

        rpm.overburden_density = self.wiz.overburdenDensitySpin.value()
        rpm.floor_density = self.wiz.floorDensitySpin.value()

        sample = Sample(sample_strength, sample_height, sample_diameter, is_cylinder)
        pillar_length = ZERO_LENGTH
        rpm.pillar = Pillar(sample, rpm.seam_height, pillar_length)

        if rpm.design_type == RoomAndPillar.REDESIGN:
            formula = name_to_formula(self.wiz.pillarFormulaCombo.currentText())
            formula.alpha = self.wiz.constantASpin.value()
            formula.beta = self.wiz.constantBSpin.value()
            if formula.k_type == StrengthFormula.OTHER:
                formula.k = self.wiz.constantKSpin.value()
            rpm.pillar_formula = formula

        self.rpm = rpm
        self.rpm.print_data()
        self.update_interface()

    def save(self):
        if not self.dirty:
            return
        pass

    def export(self, ext=None):
        pass

    def about(self):
        about_dlg = AboutDialog(self)
        about_dlg.show()

    def center_on_screen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


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
