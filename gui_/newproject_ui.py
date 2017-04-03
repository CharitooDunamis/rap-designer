# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/newproject.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_NewProjectWizard(object):
    def setupUi(self, NewProjectWizard):
        NewProjectWizard.setObjectName(_fromUtf8("NewProjectWizard"))
        NewProjectWizard.resize(400, 300)
        NewProjectWizard.setWizardStyle(QtGui.QWizard.ClassicStyle)
        NewProjectWizard.setOptions(QtGui.QWizard.ExtendedWatermarkPixmap|QtGui.QWizard.HaveFinishButtonOnEarlyPages)
        self.wizardPage1 = QtGui.QWizardPage()
        self.wizardPage1.setObjectName(_fromUtf8("wizardPage1"))
        NewProjectWizard.addPage(self.wizardPage1)
        self.wizardPage2 = QtGui.QWizardPage()
        self.wizardPage2.setObjectName(_fromUtf8("wizardPage2"))
        self.comboBox = QtGui.QComboBox(self.wizardPage2)
        self.comboBox.setGeometry(QtCore.QRect(180, 60, 69, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.label = QtGui.QLabel(self.wizardPage2)
        self.label.setGeometry(QtCore.QRect(120, 20, 46, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        NewProjectWizard.addPage(self.wizardPage2)
        self.wizardPage = QtGui.QWizardPage()
        self.wizardPage.setObjectName(_fromUtf8("wizardPage"))
        NewProjectWizard.addPage(self.wizardPage)

        self.retranslateUi(NewProjectWizard)
        QtCore.QMetaObject.connectSlotsByName(NewProjectWizard)

    def retranslateUi(self, NewProjectWizard):
        NewProjectWizard.setWindowTitle(_translate("NewProjectWizard", "Wizard", None))
        self.label.setText(_translate("NewProjectWizard", "Page 2", None))

import mainresource_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NewProjectWizard = QtGui.QWizard()
    ui = Ui_NewProjectWizard()
    ui.setupUi(NewProjectWizard)
    NewProjectWizard.show()
    sys.exit(app.exec_())

