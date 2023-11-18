from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QHeaderView, QWidget

from kmap.controller.orbitaltablerow import OrbitalTableRow
from kmap.ui.orbitaltable import Ui_orbitaltable as OrbitalTable_UI


class OrbitalTable(QWidget, OrbitalTable_UI):
    orbital_changed = Signal(int)
    orbital_removed = Signal(int)
    orbital_selected = Signal(int)

    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(OrbitalTable, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()

        self.rows = []

    def add_orbital(self, orbital, orientation):
        new_row = OrbitalTableRow(orbital, orientation)

        self._add_row(new_row)

    def remove_orbital_by_ID(self, ID):
        index = self._ID_to_row_index(ID)

        self.table.removeRow(index)
        del self.rows[index]

        self.orbital_removed.emit(ID)

    def get_parameters_by_ID(self, ID):
        index = self._ID_to_row_index(ID)

        return self.rows[index].get_parameters()

    def get_use_by_ID(self, ID):
        index = self._ID_to_row_index(ID)

        return self.rows[index].get_use()

    def change_parameter(self, ID, parameter, value):
        self._update_selected_rows(parameter, value)

        self.orbital_changed.emit(ID)

    def update_orbital_parameters(self, ID, values):
        row_index = self._ID_to_row_index(ID)
        row = self.rows[row_index]

        for i, parameter in enumerate(["weight", "phi", "theta", "psi"]):
            row.update_parameter_silently(parameter, values[i])

        self.orbital_changed.emit(ID)

    def update_orbital_use(self, ID, state):
        row_index = self._ID_to_row_index(ID)
        row = self.rows[row_index]
        row.update_use(state)

        self.change_use(ID)

    def save_state(self):
        save = {}
        for row in self.rows:
            save.update({f"{row.ID}": row.save_state()})

        return save

    def restore_state(self, save):
        for ID, row_save in save.items():
            index = self._ID_to_row_index(int(ID))
            self.rows[index].restore_state(row_save)

    def change_use(self, ID):
        self.orbital_changed.emit(ID)

    def _add_row(self, new_row):
        row_index = len(self.rows)

        self.rows.append(new_row)

        self.table.insertRow(row_index)
        self._embed_row(new_row, row_index)
        self._connet_row(new_row)
        # "Select" newly added row to trigger miniplots
        self.table.cellClicked.emit(row_index, 2)

    def _ID_to_row_index(self, ID):
        for index, row in enumerate(self.rows):
            if row.ID == ID:
                return index

        raise IndexError("No data with this ID")

    def _update_selected_rows(self, parameter, value):
        selected_rows = self.table.selectionModel().selectedIndexes()
        for selected_row in selected_rows:
            row = self.rows[selected_row.row()]
            row.update_parameter_silently(parameter, value)

    def _setup(self):
        widths = [40, 40, 0, 90, 80, 80, 80, 45]

        for col, width in enumerate(widths):
            self.table.setColumnWidth(col, width)

        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

    def _embed_row(self, row, row_index):
        # To center checkbox, embed it inside a layout inside a widget
        layout = QHBoxLayout()
        layout.addWidget(row.use)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        center_widget = QWidget()
        center_widget.setLayout(layout)

        widgets = [
            row.button,
            row.ID_label,
            row.name_label,
            row.weight,
            row.phi,
            row.theta,
            row.psi,
            center_widget,
        ]

        for col, widget in enumerate(widgets):
            self.table.setCellWidget(row_index, col, widget)

    def _row_selected(self, row):
        self.orbital_selected.emit(self.rows[row].ID)

    def _connet_row(self, row):
        row.row_removed.connect(self.remove_orbital_by_ID)
        row.parameter_changed.connect(self.change_parameter)
        row.use_changed.connect(self.change_use)

        self.table.cellClicked.connect(self._row_selected)
