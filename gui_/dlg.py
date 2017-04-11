# import sys

# from qtpy.QtGui import *
# from qtpy.QtCore import *
from qtpy.QtWidgets import *

if __name__ == "__main__":
    import about_ui
else:
    from . import about_ui


class AboutDialog(QDialog, about_ui.Ui_Dialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
