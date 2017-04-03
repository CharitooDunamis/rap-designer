import sys

from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

import qtawesome as qta

try:
    from .wizard import ProjectWizard
except (SystemError, ValueError) as e:
    from wizard import ProjectWizard


class MineRapper(QMainWindow):

    def __init__(self, parent=None):
        super(MineRapper, self).__init__(parent)
        self.createChildren()
        self.setMinimumSize(QSize(400, 300))
        self.setGeometry(QRect(100, 100, 800, 600))
        self.setWindowTitle(QApplication.applicationName())
        self.setWindowIcon(QIcon("icon.png"))

    def createChildren(self):
        self.statusBar = self.statusBar()
        self.createToolbars()
        self.canvas = QGraphicsView(self)
        self.setCentralWidget(self.canvas)

    def createAction(self, text, slot=None, icn=None, shortcut=None, tip=None, checkable=False, signal='triggered()',
                     icn_options=None):
        action = QAction(text, self)
        action.setCheckable(checkable)
        if slot:
            self.connect(action, SIGNAL(signal), slot)
        if icn:
            icon = qta.icon(icn, **icn_options)
            action.setIcon(icon)
        if shortcut:
            action.setShortcut(shortcut)
        if tip:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        return action

    def createToolbars(self):
        mainTools = self.addToolBar("Main")
        mainTools.setObjectName("MainToolbar")
        mainTools.setIconSize(QSize(32, 32))
        newAction = self.createAction("&New", icn='fa.file-text', shortcut=QKeySequence.New,
                                      tip="Create a new RAP project.", icn_options={"color": "black"},
                                      slot=self.newProject)
        infoAction = self.createAction("&About", icn="fa.info-circle", shortcut="Shift + A", tip="About Mine RAPPa",
                                       icn_options={"color": "black"})
        saveAction = self.createAction("&Save", icn="fa.save", shortcut=QKeySequence.Save, tip="Save RAP Project",
                                       icn_options={"color": "black"})
        graphAction = self.createAction("&Sensitivity", icn="fa.line-chart", tip="Sensitivity Analysis for current plan"
                                        , icn_options={})
        exportAction = self.createAction("&Export Results", icn="fa.file-pdf-o", tip="Export results", icn_options={})
        configAction = self.createAction("&Settings", icn="fa.cog", tip="Change settings", icn_options={})
        mainTools.addActions([newAction, saveAction])
        mainTools.addSeparator()
        mainTools.addActions([exportAction, graphAction])
        mainTools.addSeparator()
        mainTools.addActions([configAction, infoAction])

    def newProject(self):
        wizard = ProjectWizard(self)
        wizard.exec_()


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
