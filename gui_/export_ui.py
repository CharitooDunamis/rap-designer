# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export.ui'
#
# Created: Tue Apr 25 05:05:50 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(351, 165)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.folderLabel = QtGui.QLabel(Dialog)
        self.folderLabel.setObjectName("folderLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.folderLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.folderLineEdit = QtGui.QLineEdit(Dialog)
        self.folderLineEdit.setFrame(False)
        self.folderLineEdit.setReadOnly(True)
        self.folderLineEdit.setObjectName("folderLineEdit")
        self.horizontalLayout.addWidget(self.folderLineEdit)
        self.browseButton = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browseButton.sizePolicy().hasHeightForWidth())
        self.browseButton.setSizePolicy(sizePolicy)
        self.browseButton.setMinimumSize(QtCore.QSize(17, 0))
        self.browseButton.setMaximumSize(QtCore.QSize(50, 31))
        self.browseButton.setObjectName("browseButton")
        self.horizontalLayout.addWidget(self.browseButton)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.fileTypeLabel = QtGui.QLabel(Dialog)
        self.fileTypeLabel.setObjectName("fileTypeLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.fileTypeLabel)
        self.fileTypeCombo = QtGui.QComboBox(Dialog)
        self.fileTypeCombo.setObjectName("fileTypeCombo")
        self.fileTypeCombo.addItem("")
        self.fileTypeCombo.addItem("")
        self.fileTypeCombo.addItem("")
        self.fileTypeCombo.addItem("")
        self.fileTypeCombo.addItem("")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.fileTypeCombo)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.folderLabel.setBuddy(self.folderLineEdit)
        self.fileTypeLabel.setBuddy(self.fileTypeCombo)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Export As", None, QtGui.QApplication.UnicodeUTF8))
        self.folderLabel.setText(QtGui.QApplication.translate("Dialog", "&Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("Dialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTypeLabel.setText(QtGui.QApplication.translate("Dialog", "File &Type", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTypeCombo.setItemText(0, QtGui.QApplication.translate("Dialog", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTypeCombo.setItemText(1, QtGui.QApplication.translate("Dialog", "PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTypeCombo.setItemText(2, QtGui.QApplication.translate("Dialog", "HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTypeCombo.setItemText(3, QtGui.QApplication.translate("Dialog", "CSV", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTypeCombo.setItemText(4, QtGui.QApplication.translate("Dialog", "Word Document", None, QtGui.QApplication.UnicodeUTF8))

