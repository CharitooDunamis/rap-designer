from qtpy.QtWidgets import (QDialog, QFileDialog, QApplication)
from qtpy.QtGui import QPixmap
from qtpy.QtCore import SIGNAL
from os.path import join

from . import (about_ui, export_ui)
from . import GUI_DIR


class AboutDialog(QDialog, about_ui.Ui_Dialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        logo = QPixmap(join(GUI_DIR, "icon.png"))
        self.iconLabel.setPixmap(logo)


class ExportDialog(QDialog, export_ui.Ui_Dialog):

    def __init__(self, parent=None):
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
        self.connect(self.browseButton, SIGNAL("clicked()"), self.ask_dir)

    def ask_dir(self):
        dir = QFileDialog.getExistingDirectory(parent=self, caption="Export Results to",
                                               filter=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.folderLineEdit.setText(dir)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    top = ExportDialog()
    top.show()
    sys.exit(app.exec_())
