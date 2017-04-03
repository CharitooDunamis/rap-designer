from __future__ import division
from __future__ import unicode_literals

# from pprint import pprint
from collections import namedtuple
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import qtawesome as qta
import sys

converter = namedtuple('ConverterTuple', ['from_si', 'to_si'])
# app = QApplication(sys.argv)


def createLabelledSpin(label, double=False, suffix=None, prefix=None, default=None, max_=None, min_=None,
                       icon_names=None, icon_options=None, parent=None):
    # global app
    spin = QSpinBox(parent)
    if double:
        spin = QDoubleSpinBox(parent)
    if suffix:
        spin.setSuffix(suffix)
    if prefix:
        spin.setPrefix(prefix)
    if max_ and min_:
        spin.setRange(min_, max_)
        spin.setValue(min_)
    if default:
        spin.setValue(default)
    if icon_names:
        icon = qta.icon(*icon_names, **icon_options)
    lbl = QLabel(label, parent)
    return lbl, spin


class Quantity:
    """Descriptor for an imperial unit"""

    def set_to_si(self, fxn):
        self._to = fxn

    def set_from(self, fxn):
        self._from = fxn

    def __set__(self, instance, value):
        instance.value = self._from(value)

    def __get__(self, instance, owner):
        return self._from(instance.value)


class ConverterSpin(QWidget):
    def __init__(self, label, default_unit, units, double=True, parent=None):
        super(ConverterSpin, self).__init__(parent)
        self.units = units
        self.default_unit = default_unit
        if double:
            self.spin = QDoubleSpinBox()
        else:
            self.spin = QSpinBox()
        self.spin.setMaximum(1000)
        self.unitsCombo = QComboBox()
        all_units = [default_unit] + list(units.keys())
        self.unitsCombo.addItems(all_units)
        self._layout(label=label)
        self.value = self.spin.value()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def _layout(self, label):
        horiz = QHBoxLayout()
        horiz.addWidget(QLabel(label))
        horiz.addWidget(self.spin)
        horiz.addWidget(self.unitsCombo)
        self.setLayout(horiz)
        self._connections()

    def _connections(self):
        self.connect(self.unitsCombo, SIGNAL('currentIndexChanged(int)'), self.unitsChanged)
        self.connect(self.spin, SIGNAL('editingFinished()'), self.valueChanged)

    def value(self, unit='default'):
        if unit != 'default':
            unit_data = self.units.get(unit)
            from_si = unit_data.from_si
        else:
            from_si = lambda x: x
        return from_si(self.value)

    def get_unit_function(self, direction='to'):
        current_unit = self.unitsCombo.currentText()
        if current_unit == self.default_unit:
            fxn = lambda x: x
        else:
            formulas = self.units[current_unit]
            if direction == 'to':
                fxn = formulas.to_si
            else:
                fxn = formulas.from_si
        return fxn

    def valueChanged(self):
        fxn = self.get_unit_function()
        self.value = fxn(self.spin.value())

    def unitsChanged(self):
        # print('Units have been changed')
        fxn = self.get_unit_function('from')
        value = fxn(self.value)
        if isinstance(self.spin, QDoubleSpinBox):
            # print('Spin box is double')
            value = round(value, 2)
        else:
            # print('Spin box is not double')
            value = round(value, 0)
        # print(value)
        self.spin.setValue(value)
