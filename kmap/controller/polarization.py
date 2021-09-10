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
UI_file = __directory__ / 'ui/polarization.ui'
Polarization_UI, _ = uic.loadUiType(UI_file)


class Polarization(QWidget, Polarization_UI):
    polarization_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):

        # Setup GUI
        super(Polarization, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()
        self._connect()

    def change_polarization(self):

        _, polarization = self._get_polarization()
        self.s_share_label.setVisible(polarization == 'unpolarized')
        self.s_share_spinbox.setVisible(polarization == 'unpolarized')
        self.polarization_changed.emit()

    def get_parameters(self):

        Ak_type, polarization = self._get_polarization()
        factor = self._get_factor()
        Ak_type = factor if factor == 'no' else factor + Ak_type
        angles = self._get_angles()
        s_share = self._get_s_share()

        return (Ak_type, polarization, *angles, s_share)

    def save_state(self):

        Ak = self.ak_combobox.currentIndex()
        polarization = self.polarization_combobox.currentIndex()
        angle = self.angle_spinbox.value()
        azimuth = self.azimuth_spinbox.value()
        s_share = self._get_s_share()

        save = {'Ak': Ak, 'polarization': polarization,
                'angle': angle, 'azimuth': azimuth, 's_share': s_share}

        return save

    def restore_state(self, save):

        Ak = save['Ak']
        polarization = save['polarization']
        angle = save['angle']
        azimuth = save['azimuth']
        if 's_share' in save:
            s_share = save['s_share']
        else:
            # For backwards compatability
            print(
                'WARNING: s_share setting not found in save file. Using default of 0.694.')
            s_share = config.get_key('orbital', 's_share_default')

        self.ak_combobox.setCurrentIndex(Ak)
        self.polarization_combobox.setCurrentIndex(polarization)
        self.angle_spinbox.setValue(angle)
        self.azimuth_spinbox.setValue(azimuth)
        self.s_share_spinbox.setValue(s_share)

    def _get_factor(self):

        Ak_index = self.ak_combobox.currentIndex()

        if Ak_index == 0:
            Ak_type = 'no'

        elif Ak_index == 1:
            Ak_type = 'only-'

        else:
            Ak_type = ''

        return Ak_type

    def _get_polarization(self):

        Ak_index = self.polarization_combobox.currentIndex()

        if Ak_index == 0:
            Ak_type = 'toroid'
            polarization = 'p'

        else:
            Ak_type = 'NanoESCA'

            if Ak_index == 1:
                polarization = 'p'

            elif Ak_index == 2:
                polarization = 's'

            elif Ak_index == 3:
                polarization = 'unpolarized'

            elif Ak_index == 4:
                polarization = 'C+'

            elif Ak_index == 5:
                polarization = 'C-'

            elif Ak_index == 6:
                polarization = 'CDAD'

        return Ak_type, polarization

    def _get_angles(self):

        alpha = self.angle_spinbox.value()
        beta = self.azimuth_spinbox.value()
        gamma = 'auto'

        return alpha, beta, gamma

    def _get_s_share(self):

        return self.s_share_spinbox.value()

    def _setup(self):

        s_share = config.get_key('orbital', 's_share_default')
        self.s_share_spinbox.setValue(float(s_share))

        self.s_share_label.setVisible(False)
        self.s_share_spinbox.setVisible(False)

    def _connect(self):

        self.polarization_combobox.currentIndexChanged.connect(
            self.change_polarization)
        self.angle_spinbox.valueChanged.connect(self.change_polarization)
        self.azimuth_spinbox.valueChanged.connect(self.change_polarization)
        self.ak_combobox.currentIndexChanged.connect(self.change_polarization)
        self.s_share_spinbox.valueChanged.connect(self.change_polarization)
