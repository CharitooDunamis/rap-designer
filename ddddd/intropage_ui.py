# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/intropage.ui'
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

class Ui_IntroPage(object):
    def setupUi(self, IntroPage):
        IntroPage.setObjectName(_fromUtf8("IntroPage"))
        IntroPage.resize(400, 300)

        self.retranslateUi(IntroPage)
        QtCore.QMetaObject.connectSlotsByName(IntroPage)

    def retranslateUi(self, IntroPage):
        IntroPage.setWindowTitle(_translate("IntroPage", "Introduction", None))
        IntroPage.setTitle(_translate("IntroPage", "New Project Wizard", None))
        IntroPage.setSubTitle(_translate("IntroPage", "This wizard will guide you through the steps to create a new room and pillar mining project.", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    IntroPage = QtGui.QWizardPage()
    ui = Ui_IntroPage()
    ui.setupUi(IntroPage)
    IntroPage.show()
    sys.exit(app.exec_())

