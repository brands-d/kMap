from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from kmap.ui.sliceddatabaseoptions import Ui_window as SlicedDataBaseOptions_UI


class SlicedDataBaseOptions(QWidget, SlicedDataBaseOptions_UI):
    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(SlicedDataBaseOptions, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()

    def get_parameters(self):
        name = self.line_edit.text()
        name = name if name else "no name given"
        polarization = self._get_polarization()
        symmetry = self._get_symmetry()
        orientation = self._get_orientation()
        other = self._get_other()

        return (name, *other, *orientation, *polarization, symmetry)

    def _get_orientation(self):
        phi = self.phi_spinbox.value()
        theta = self.theta_spinbox.value()
        psi = self.psi_spinbox.value()

        return phi, theta, psi

    def _get_other(self):
        photon = self.photon_spinbox.value()
        fermi = self.fermi_spinbox.value()
        broadening = self.broadening_spinbox.value()
        dk = self.dk_spinbox.value()

        return photon, fermi, broadening, dk

    def _get_polarization(self):
        Ak_index = self.polarization_combobox.currentIndex()
        polarization = "p"
        if Ak_index == 0:
            Ak_type = "no"

        elif Ak_index == 1:
            Ak_type = "toroid"

        else:
            Ak_type = "NanoESCA"

            if Ak_index == 3:
                polarization = "s"

            elif Ak_index == 4:
                polarization = "unpolarized"

            elif Ak_index == 5:
                polarization = "C+"

            elif Ak_index == 6:
                polarization = "C-"

            elif Ak_index == 7:
                polarization = "CDAD"

        alpha = self.alpha_spinbox.value()
        beta = self.beta_spinbox.value()
        gamma = "auto"

        return Ak_type, polarization, alpha, beta, gamma

    def closeEvent(self, event):
        self.deleteLater()
        event.accept()

    def _get_symmetry(self):
        index = self.symmetrization_combobox.currentIndex()
        available_symmetries = [
            "no",
            "2-fold",
            "2-fold+mirror",
            "3-fold",
            "3-fold+mirror",
            "4-fold",
            "4-fold+mirror",
        ]

        return available_symmetries[index]

    def _setup(self):
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
