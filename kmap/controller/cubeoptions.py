# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/cubeoptions.ui')
CubeOptions_UI, _ = uic.loadUiType(UI_file)


class CubeOptions(QWidget, CubeOptions_UI):

    energy_changed = pyqtSignal()
    resolution_changed = pyqtSignal()
    symmetrization_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):

        # Setup GUI
        super(CubeOptions, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def change_energy(self):

        self.energy_changed.emit()

    def change_symmetrization(self):

        self.symmetrization_changed.emit()

    def change_resolution(self):

        self.resolution_changed.emit()

    def get_parameters(self):

        energy = self.energy_spinbox.value()
        resolution = self.resolution_spinbox.value()
        symmetry = self._get_symmetry()

        return energy, resolution, symmetry

    def _get_symmetry(self):

        index = self.symmetrize_combobox.currentIndex()
        available_symmetries = ['no', '2-fold', '2-fold+mirror',
                                '3-fold', '3-fold+mirror', '4-fold',
                                '4-fold+mirror']

        return available_symmetries[index]

    def _connect(self):

        self.energy_spinbox.valueChanged.connect(self.change_energy)
        self.resolution_spinbox.valueChanged.connect(self.change_resolution)
        self.symmetrize_combobox.currentIndexChanged.connect(
            self.change_symmetrization)
