from PyQt5.QtCore import pyqtSignal
from kmap.ui.orbitaltable_ui import OrbitalTableUI
from kmap.controller.orbitaltablerow import OrbitalTableRow


class OrbitalTable(OrbitalTableUI):

    orbitals_changed = pyqtSignal()
    orbital_removed = pyqtSignal(int)

    def __init__(self):

        self.rows = []

        OrbitalTableUI.__init__(self)

    def add_orbital(self, orbital):

        self._add_table_row(orbital.ID, orbital.name)

    def _add_table_row(self, ID, name):

        new_row = OrbitalTableRow(self, ID, name)
        new_row.orbital_removed.connect(self.remove_orbital_by_ID)
        new_row.parameters_changed.connect(self.parameters_changed)

        self.rows.append(new_row)

    def get_parameters_by_ID(self, ID):

        for row in self.rows:
            if row.data_ID == ID:
                deconvolution = row.deconvolution.value()
                phi = row.phi.value()
                theta = row.theta.value()
                psi = row.psi.value()

                return deconvolution, phi, theta, psi

        return None

    def remove_orbital_by_ID(self, ID):

        for index, row in enumerate(self.rows):
            if row.data_ID == ID:
                self.table.removeRow(index)
                self.rows.remove(row)

        self.orbital_removed.emit(ID)

    def parameters_changed(self, ID, type_, value):

        self._update_seleted_rows(type_, value)

        self.orbitals_changed.emit()

    def _update_seleted_rows(self, type_, value):

        selected_rows = self.table.selectionModel().selectedIndexes()
        for selected_row in selected_rows:
            row = self.rows[selected_row.row()]

            if type_ == 'deconvolution':
                row.deconvolution.blockSignals(True)
                row.deconvolution.setValue(value)
                row.deconvolution.blockSignals(False)

            if type_ == 'phi':
                row.phi.blockSignals(True)
                row.phi.setValue(value)
                row.phi.blockSignals(False)

            elif type_ == 'theta':
                row.theta.blockSignals(True)
                row.theta.setValue(value)
                row.theta.blockSignals(False)

            elif type_ == 'psi':
                row.psi.blockSignals(True)
                row.psi.setValue(value)
                row.psi.blockSignals(False)
