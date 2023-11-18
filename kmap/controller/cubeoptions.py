from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from kmap.ui.cubeoptions import Ui_cubeoptions as CubeOptions_UI


class CubeOptions(QWidget, CubeOptions_UI):
    energy_changed = Signal()
    V0_changed = Signal()
    resolution_changed = Signal()
    symmetrization_changed = Signal()
    get_match_energy = Signal()

    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(CubeOptions, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def save_state(self):
        E_kin = self.energy_spinbox.value()
        V0 = self.inner_potential_spinbox.value()
        resolution = self.resolution_spinbox.value()
        symmetry = self.symmetrize_combobox.currentIndex()

        save = {
            "E_kin": E_kin,
            "resolution": resolution,
            "symmetry": symmetry,
            "V0": V0,
        }

        return save

    def restore_state(self, save):
        E_kin = save["E_kin"]
        V0 = save["V0"]
        resolution = save["resolution"]
        symmetry = save["symmetry"]

        self.energy_spinbox.setValue(E_kin)
        self.inner_potential_spinbox.setValue(V0)
        self.resolution_spinbox.setValue(resolution)
        self.symmetrize_combobox.setCurrentIndex(symmetry)

    def set_kinetic_energy(self, energy):
        if energy is not None:
            self.energy_spinbox.setValue(energy)

    def set_inner_potential(self, V0):
        if V0 is not None:
            self.inner_potential_spinbox.setValue(V0)

    def get_parameters(self):
        energy = self.energy_spinbox.value()
        resolution = self.resolution_spinbox.value()
        symmetry = self._get_symmetry()
        V0 = self.inner_potential_spinbox.value()

        return energy, resolution, symmetry, V0

    def _get_symmetry(self):
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

    def _connect(self):
        self.energy_spinbox.valueChanged.connect(self.energy_changed.emit)
        self.inner_potential_spinbox.valueChanged.connect(self.V0_changed.emit)
        self.resolution_spinbox.valueChanged.connect(self.resolution_changed.emit)
        self.symmetrize_combobox.currentIndexChanged.connect(
            self.symmetrization_changed.emit
        )
        self.match_button.clicked.connect(self.get_match_energy.emit)
