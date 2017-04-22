from qtpy.QtWidgets import QDialog

from . import (about_ui, export_ui)


class AboutDialog(QDialog, about_ui.Ui_Dialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)


class ExportDialog(QDialog, export_ui.Ui_Dialog):

    FILETYPES = ("pdf", "txt", "xlsx", "csv")

    def __init__(self, parent=None):
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
        self.fileTypeCombo.addItem("All")
        self.fileTypeCombo.addItems(list(self.FILETYPES))
