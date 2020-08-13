# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ + '/ui/polarization.ui'
Polarization_UI, _ = uic.loadUiType(UI_file)


class Polarization(QWidget, Polarization_UI):

    polarization_changed = pyqtSignal()
    symmetrization_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):

        # Setup GUI
        super(Polarization, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()
        self._connect()

    def change_polarization(self):

        self.polarization_changed.emit()

    def change_symmetrization(self):

        self.symmetrization_changed.emit()

    def get_parameters(self):

        Ak_type, polarization = self._get_polarization()
        symmetry = self._get_symmetry()
        angles = self._get_angles()

        return (Ak_type, polarization, *angles, symmetry)

    def _get_polarization(self):

        Ak_index = self.polarization_combobox.currentIndex()
        polarization = 'p'
        if Ak_index == 0:
            Ak_type = 'no'

        elif Ak_index == 1:
            Ak_type = 'toroid'

        else:
            Ak_type = 'NanoESCA'

            if Ak_index == 3:
                polarization = 's'

            elif Ak_index == 4:
                polarization = 'C+'

            elif Ak_index == 5:
                polarization = 'C-'

            elif Ak_index == 6:
                polarization = 'CDAD'

        return Ak_type, polarization

    def _get_symmetry(self):

        index = self.symmetrize_combobox.currentIndex()
        available_symmetries = ['no', '2-fold', '2-fold+mirror',
                                '3-fold', '3-fold+mirror', '4-fold',
                                '4-fold+mirror']

        return available_symmetries[index]

    def _get_angles(self):

        alpha = self.angle_spinbox.value()
        beta = self.azimuth_spinbox.value()
        gamma = 'auto'

        return alpha, beta, gamma

    def _setup(self):

        # Can't add sub and superscript text in QtCreator
        self.polarization_combobox.setItemText(0, 'no |A\u2096|\u00B2')

    def _connect(self):

        self.polarization_combobox.currentIndexChanged.connect(
            self.change_polarization)
        self.angle_spinbox.valueChanged.connect(self.change_polarization)
        self.azimuth_spinbox.valueChanged.connect(self.change_polarization)
        self.symmetrize_combobox.currentIndexChanged.connect(
            self.change_symmetrization)
