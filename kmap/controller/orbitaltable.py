from kmap.ui.orbitaltable_ui import OrbitalTableUI
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class OrbitalTable(OrbitalTableUI):

    def __init__(self):

        OrbitalTableUI.__init__(self)

    def add_orbital(self, orbital):

        self._add_table_row(orbital.ID, orbital.name)

    def _add_table_row(self, ID, name):

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        # Remove
        label = QLabel('X')
        label.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row_count, 0, label)

        # ID
        label = QLabel(str(ID))
        label.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row_count, 1, label)

        # Name
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row_count, 2, label)
