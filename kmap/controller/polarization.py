from PyQt5.QtCore import pyqtSignal
from kmap.model.polarization_model import PolarizationModel
from kmap.ui.polarization_ui import PolarizationUI


class Polarization(PolarizationUI):

    polarization_changed = pyqtSignal()

    def __init__(self):

        self.model = PolarizationModel()

        PolarizationUI.__init__(self)

    def change_polarization(self):

        self.polarization_changed.emit()

    def get_parameters(self):

        Ak_index = self.combobox.currentIndex()
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

        alpha = self.angle_spinbox.value()
        beta = self.azimuth_spinbox.value()
        gamma = 0

        return Ak_type, polarization, alpha, beta, gamma
