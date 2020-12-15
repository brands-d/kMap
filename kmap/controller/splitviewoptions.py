# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ / 'ui/splitviewoptions.ui'
SplitViewOptions_UI, _ = uic.loadUiType(UI_file)


class SplitViewOptions(QWidget, SplitViewOptions_UI):
    values_changed = pyqtSignal(float, str)

    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(SplitViewOptions, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def save_state(self):
        scale = self.scale_spinbox.value()
        type_ = self.type_combobox.currentIndex()

        save = {'Scale': scale, 'Type': type_}

        return save

    def restore_state(self, save):
        scale = save['Scale']
        type_ = save['Type']

        self.scale_spinbox.setValue(scale)
        self.type_combobox.setCurrentIndex(type_)

    def get_parameters(self):
        scale = self.scale_spinbox.value()
        type_ = self.type_combobox.currentText()

        return scale, type_

    def emit_values(self):
        scale, type_ = self.get_parameters()
        self.values_changed.emit(scale, type_)

    def _connect(self):
        self.scale_spinbox.valueChanged.connect(self.emit_values)
        self.type_combobox.currentIndexChanged.connect(self.emit_values)
