# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ / 'ui/cubeoptions.ui'
CubeOptions_UI, _ = uic.loadUiType(UI_file)


class CubeOptions(QWidget, CubeOptions_UI):
    energy_changed = pyqtSignal()
    resolution_changed = pyqtSignal()
    symmetrization_changed = pyqtSignal()
    get_match_energy = pyqtSignal()

    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(CubeOptions, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def save_state(self):
        E_kin = self.energy_spinbox.value()
        resolution = self.resolution_spinbox.value()
        symmetry = self.symmetrize_combobox.currentIndex()

        save = {'E_kin': E_kin, 'resolution': resolution, 'symmetry': symmetry}

        return save

    def restore_state(self, save):
        E_kin = save['E_kin']
        resolution = save['resolution']
        symmetry = save['symmetry']

        self.energy_spinbox.setValue(E_kin)
        self.resolution_spinbox.setValue(resolution)
        self.symmetrize_combobox.setCurrentIndex(symmetry)

    def set_kinetic_energy(self, energy):
        if energy is not None:
            self.energy_spinbox.setValue(energy)

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
        self.energy_spinbox.valueChanged.connect(self.energy_changed.emit)
        self.resolution_spinbox.valueChanged.connect(
            self.resolution_changed.emit)
        self.symmetrize_combobox.currentIndexChanged.connect(
            self.symmetrization_changed.emit)
        self.match_button.clicked.connect(self.get_match_energy.emit)
