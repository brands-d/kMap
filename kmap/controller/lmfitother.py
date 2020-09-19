# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfitother.ui')
LMFitOther_UI, _ = uic.loadUiType(UI_file)


class LMFitOther(QWidget, LMFitOther_UI):

    value_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):

        # Setup GUI
        super(LMFitOther, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def get_parameters(self):

        Ak_type, polarization = self._get_polarization()
        factor = self._get_factor()
        Ak_type = factor if factor == 'no' else factor + Ak_type
        symmetry = self._get_symmetry()
        dk = float(config.get_key('orbital', 'dk'))

        return Ak_type, polarization, symmetry, dk

    def _get_symmetry(self):

        index = self.symmetrize_combobox.currentIndex()
        available_symmetries = ['no', '2-fold', '2-fold+mirror',
                                '3-fold', '3-fold+mirror', '4-fold',
                                '4-fold+mirror']

        return available_symmetries[index]

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
                polarization = 'C+'

            elif Ak_index == 4:
                polarization = 'C-'

            elif Ak_index == 5:
                polarization = 'CDAD'

        return Ak_type, polarization

    def _connect(self):

        self.polarization_combobox.currentIndexChanged.connect(
            self.value_changed.emit)
        self.ak_combobox.currentIndexChanged.connect(self.value_changed.emit)
        self.symmetrize_combobox.currentIndexChanged.connect(
            self.value_changed.emit)
