# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget, QHeaderView, QHBoxLayout

# Own Imports
from kmap import __directory__
from kmap.controller.orbitaltablerow import OrbitalTableRow
from kmap.controller.lmfittreeitems import (
    OrbitalTreeItem, OtherTreeItem, DataTreeItem)

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfittree.ui')
LMFitTree_UI, _ = uic.loadUiType(UI_file)


class LMFitTree(QWidget, LMFitTree_UI):

    item_selected = pyqtSignal()

    def __init__(self, orbitals, *args, **kwargs):

        # Setup GUI
        super(LMFitTree, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup(orbitals)
        self._connect()

    '''
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

        raise IndexError('No data with this ID')

    def _update_selected_rows(self, parameter, value):

        selected_rows = self.table.selectionModel().selectedIndexes()
        for selected_row in selected_rows:
            row = self.rows[selected_row.row()]
            row.update_parameter_silently(parameter, value)
    '''

    def get_selected_orbital_ID(self):

        selected_items = self.tree.selectedItems()

        for item in selected_items:
            if isinstance(item, OrbitalTreeItem):
                return item.ID

            elif (isinstance(item, DataTreeItem) and
                  isinstance(item.parent(), OrbitalTreeItem)):
                return item.parent().ID

        return -1

    def _setup(self, orbitals):

        widths = [60, 0, 100, 80, 130, 130, 130, 200]

        for col, width in enumerate(widths):
            self.tree.setColumnWidth(col, width)

        self.tree.header().setResizeMode(1, QHeaderView.Stretch)
        self.tree.header().setDefaultAlignment(Qt.AlignCenter)

        # Add TreeItems
        self.tree.addTopLevelItem(OtherTreeItem(self.tree))
        for orbital in orbitals:
            self.tree.addTopLevelItem(OrbitalTreeItem(self.tree, orbital))

    def _item_selected(self):

        self.item_selected.emit()

    def _connect(self):

        self.tree.itemSelectionChanged.connect(self._item_selected)
