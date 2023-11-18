from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from kmap.config.config import config
from kmap.ui.polarization import Ui_polarization as Polarization_UI


class Polarization(QWidget, Polarization_UI):
    polarization_changed = Signal()

    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(Polarization, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()
        self._connect()

    def change_polarization(self):
        _, polarization = self._get_polarization()
        self.s_share_label.setVisible(polarization == "unpolarized")
        self.s_share_spinbox.setVisible(polarization == "unpolarized")
        self.polarization_changed.emit()

    def get_parameters(self):
        Ak_type, polarization = self._get_polarization()
        factor = self._get_factor()
        Ak_type = factor if factor == "no" else factor + Ak_type
        angles = self._get_angles()
        s_share = self._get_s_share()

        return (Ak_type, polarization, *angles, s_share)

    def save_state(self):
        save = {
            "Ak": self.ak_combobox.currentIndex(),
            "polarization": self.polarization_combobox.currentIndex(),
            "angle": self.angle_spinbox.value(),
            "azimuth": self.azimuth_spinbox.value(),
            "s_share": self._get_s_share(),
        }

        return save

    def restore_state(self, save):
        self.ak_combobox.setCurrentIndex(save["Ak"])
        self.polarization_combobox.setCurrentIndex(save["polarization"])
        self.angle_spinbox.setValue(save["angle"])
        self.azimuth_spinbox.setValue(save["azimuth"])
        self.s_share_spinbox.setValue(save["s_share"])

        self.polarization_changed.emit()

    def _get_factor(self):
        Ak_index = self.ak_combobox.currentIndex()

        if Ak_index == 0:
            Ak_type = "no"

        elif Ak_index == 1:
            Ak_type = "only-"

        else:
            Ak_type = ""

        return Ak_type

    def _get_polarization(self):
        Ak_index = self.polarization_combobox.currentIndex()

        if Ak_index == 0:
            Ak_type = "toroid"
            polarization = "p"

        else:
            Ak_type = "NanoESCA"

            if Ak_index == 1:
                polarization = "p"

            elif Ak_index == 2:
                polarization = "s"

            elif Ak_index == 3:
                polarization = "unpolarized"

            elif Ak_index == 4:
                polarization = "C+"

            elif Ak_index == 5:
                polarization = "C-"

            elif Ak_index == 6:
                polarization = "CDAD"

        return Ak_type, polarization

    def _get_angles(self):
        alpha = self.angle_spinbox.value()
        beta = self.azimuth_spinbox.value()
        gamma = "auto"

        return alpha, beta, gamma

    def _get_s_share(self):
        return self.s_share_spinbox.value()

    def _setup(self):
        s_share = config.get_key("orbital", "s_share_default")
        self.s_share_spinbox.setValue(float(s_share))

        self.s_share_label.setVisible(False)
        self.s_share_spinbox.setVisible(False)

    def _connect(self):
        self.polarization_combobox.currentIndexChanged.connect(self.change_polarization)
        self.angle_spinbox.valueChanged.connect(self.change_polarization)
        self.azimuth_spinbox.valueChanged.connect(self.change_polarization)
        self.ak_combobox.currentIndexChanged.connect(self.change_polarization)
        self.s_share_spinbox.valueChanged.connect(self.change_polarization)
