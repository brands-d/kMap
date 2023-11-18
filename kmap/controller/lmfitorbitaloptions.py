from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from kmap.config.config import config
from kmap.ui.lmfitorbitaloptions import Ui_lmfitother as LMFitOrbitalOptions_UI


class LMFitOrbitalOptions(QWidget, LMFitOrbitalOptions_UI):
    symmetrization_changed = Signal(str)
    polarization_changed = Signal(str, str, float)

    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(LMFitOrbitalOptions, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()
        self._connect()

    def save_state(self):
        save = {
            "Ak": self.ak_combobox.currentIndex(),
            "polarization": self.polarization_combobox.currentIndex(),
            "symmetry": self.symmetrize_combobox.currentIndex(),
            "s_share": self.get_s_share(),
        }

        return save

    def restore_state(self, save):
        self.ak_combobox.setCurrentIndex(save["Ak"])
        self.polarization_combobox.setCurrentIndex(save["polarization"])
        self.symmetrize_combobox.setCurrentIndex(save["symmetry"])
        self.s_share_spinbox.setValue(save["s_share"])

    def get_symmetrization(self):
        index = self.symmetrize_combobox.currentIndex()
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

    def get_polarization(self):
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

        factor = self._get_factor()
        Ak_type = factor if factor == "no" else factor + Ak_type

        return Ak_type, polarization

    def _get_factor(self):
        Ak_index = self.ak_combobox.currentIndex()

        if Ak_index == 0:
            Ak_type = "no"

        elif Ak_index == 1:
            Ak_type = "only-"

        else:
            Ak_type = ""

        return Ak_type

    def _change_symmetrization(self):
        symmetrization = self.get_symmetrization()

        self.symmetrization_changed.emit(symmetrization)

    def _change_polarization(self):
        Ak_type, polarization = self.get_polarization()
        s_share = self.get_s_share()

        self.s_share_label.setVisible(polarization == "unpolarized")
        self.s_share_spinbox.setVisible(polarization == "unpolarized")

        self.polarization_changed.emit(Ak_type, polarization, s_share)

    def get_s_share(self):
        return self.s_share_spinbox.value()

    def _setup(self):
        s_share = config.get_key("orbital", "s_share_default")
        self.s_share_spinbox.setValue(float(s_share))

        self.s_share_label.setVisible(False)
        self.s_share_spinbox.setVisible(False)

    def _connect(self):
        self.polarization_combobox.currentIndexChanged.connect(
            self._change_polarization
        )
        self.ak_combobox.currentIndexChanged.connect(self._change_polarization)
        self.symmetrize_combobox.currentIndexChanged.connect(
            self._change_symmetrization
        )
        self.s_share_spinbox.valueChanged.connect(self._change_polarization)
