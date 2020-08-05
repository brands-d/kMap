from PyQt5.QtCore import pyqtSignal
from kmap.ui.orbitaltablerow_ui import OrbitalTableRowUI


class OrbitalTableRow(OrbitalTableRowUI):

    orbital_removed = pyqtSignal(int)
    parameters_changed = pyqtSignal(int, str, float)

    def __init__(self, parent, data_ID, data_name):

        self.table = parent.table
        self.data_ID = data_ID
        self.data_name = data_name

        OrbitalTableRowUI.__init__(self)

    def _remove_orbital(self):

        self.orbital_removed.emit(self.data_ID)

    def _parameters_changed(self):

        id_ = self.data_ID

        if self.sender() is self.deconvolution:
            type_ = 'deconvolution'
        elif self.sender() is self.phi:
            type_ = 'phi'
        elif self.sender() is self.theta:
            type_ = 'theta'
        elif self.sender() is self.psi:
            type_ = 'psi'

        value = self.sender().value()

        self.parameters_changed.emit(id_, type_, value)
