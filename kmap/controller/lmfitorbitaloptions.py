# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ / 'ui/lmfitorbitaloptions.ui'
LMFitOrbitalOptions_UI, _ = uic.loadUiType(UI_file)


class LMFitOrbitalOptions(QWidget, LMFitOrbitalOptions_UI):
    symmetrization_changed = pyqtSignal(str)
    polarization_changed = pyqtSignal(str, str)

    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(LMFitOrbitalOptions, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def save_state(self):
        save = {'factor': self.ak_combobox.currentIndex(),
                'polarization': self.polarization_combobox.currentIndex(),
                'symmetry': self.symmetrize_combobox.currentIndex()}

        return save

    def restore_state(self, save):
        self.ak_combobox.setCurrentIndex(save['factor'])
        self.polarization_combobox.setCurrentIndex(save['polarization'])
        self.symmetrize_combobox.setCurrentIndex(save['symmetry'])

    def get_symmetrization(self):
        index = self.symmetrize_combobox.currentIndex()
        available_symmetries = ['no', '2-fold', '2-fold+mirror',
                                '3-fold', '3-fold+mirror', '4-fold',
                                '4-fold+mirror']

        return available_symmetries[index]

    def get_polarization(self):
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

        factor = self._get_factor()
        Ak_type = factor if factor == 'no' else factor + Ak_type

        return Ak_type, polarization

    def _get_factor(self):
        Ak_index = self.ak_combobox.currentIndex()

        if Ak_index == 0:
            Ak_type = 'no'

        elif Ak_index == 1:
            Ak_type = 'only-'

        else:
            Ak_type = ''

        return Ak_type

    def _change_symmetrization(self):
        symmetrization = self.get_symmetrization()

        self.symmetrization_changed.emit(symmetrization)

    def _change_polarization(self):
        Ak_type, polarization = self.get_polarization()
        self.polarization_changed.emit(Ak_type, polarization)

    def _connect(self):
        self.polarization_combobox.currentIndexChanged.connect(
            self._change_polarization)
        self.ak_combobox.currentIndexChanged.connect(self._change_polarization)
        self.symmetrize_combobox.currentIndexChanged.connect(
            self._change_symmetrization)
