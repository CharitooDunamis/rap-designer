gi# import sys

# from qtpy.QtGui import *
# from qtpy.QtCore import *
from qtpy.QtWidgets import *

try:
    from . import about_ui
except (SystemError, ImportError) as e:
    import about_ui


class AboutDialog(QDialog, about_ui.Ui_Dialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
