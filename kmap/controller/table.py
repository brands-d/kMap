from abc import abstractmethod
from PyQt5.QtCore import pyqtSignal
from kmap.ui.table_ui import TableUI, OrbitalTableUI
from kmap.controller.tablerow import OrbitalTableRow


class Table(TableUI):

    item_changed = pyqtSignal(int)
    item_removed = pyqtSignal(int)

    def __init__(self):

        self.rows = []

        TableUI.__init__(self)

    def remove_item(self, ID):

        index = self._ID_to_row_index(ID)

        self._remove_row(index)
        self.item_removed.emit(ID)

    def get_parameters_by_ID(self, ID):

        index = self._ID_to_row_index(ID)

        return self.rows[index].get_parameters()

    def parameters_changed(self, ID, parameter, value):

        self._update_selected_rows(parameter, value)

        self.item_changed.emit(ID)

    def _ID_to_row_index(self, ID):

        for index, row in enumerate(self.rows):
            if row.ID == ID:
                return index

        raise IndexError('No data with this ID')

    def _add_row(self, row):

        self.rows.append(row)
        self._connet_row(row)

    def _remove_row(self, index):

        self.table.removeRow(index)
        del self.rows[index]

    def _update_selected_rows(self, parameter, value):

        selected_rows = self.table.selectionModel().selectedIndexes()
        for selected_row in selected_rows:
            row = self.rows[selected_row.row()]
            row.update_parameter_silently(parameter, value)

    @abstractmethod
    def add_item(self, data):
        pass

    @abstractmethod
    def _connet_row(self, row):
        pass


class OrbitalTable(Table, OrbitalTableUI):

    def add_item(self, orbital):

        ID, name = orbital.ID, orbital.name
        new_row = OrbitalTableRow(self.table, ID, name)

        self._add_row(new_row)

    def _connet_row(self, row):
        
        row.row_removed.connect(self.remove_item)
        row.parameter_changed.connect(self.parameters_changed)