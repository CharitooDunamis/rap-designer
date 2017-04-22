# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export.ui'
#
# Created: Sat Apr 22 09:16:19 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(253, 144)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setVerticalSpacing(17)
        self.formLayout.setObjectName("formLayout")
        self.fileNameLabel = QtGui.QLabel(Dialog)
        self.fileNameLabel.setObjectName("fileNameLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.fileNameLabel)
        self.fileNameLineEdit = QtGui.QLineEdit(Dialog)
        self.fileNameLineEdit.setObjectName("fileNameLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.fileNameLineEdit)
        self.fileTypeLabel = QtGui.QLabel(Dialog)
        self.fileTypeLabel.setObjectName("fileTypeLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.fileTypeLabel)
        self.fileTypeCombo = QtGui.QComboBox(Dialog)
        self.fileTypeCombo.setObjectName("fileTypeCombo")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.fileTypeCombo)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.fileNameLabel.setBuddy(self.fileNameLineEdit)
        self.fileTypeLabel.setBuddy(self.fileTypeCombo)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Export As", None, QtGui.QApplication.UnicodeUTF8))
        self.fileNameLabel.setText(QtGui.QApplication.translate("Dialog", "&File Name", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTypeLabel.setText(QtGui.QApplication.translate("Dialog", "File &Type", None, QtGui.QApplication.UnicodeUTF8))

