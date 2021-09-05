# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHeaderView, QHBoxLayout, QSizePolicy

# Own Imports
from kmap import __directory__
from kmap.controller.orbitaltablerow import OrbitalTableRow
from kmap.controller.lmfittreeitems import (
    OrbitalTreeItem, OrbitalOptionsTreeItem, LMFitDataTreeItem,
    OrbitalOptionsResultTreeItem, OrbitalResultTreeItem,
    DataResultTreeItem, BackgroundOptionsTreeItem,
    BackgroundOptionsResultTreeItem)

# Load .ui File
UI_file = __directory__ / 'ui/lmfittree.ui'
LMFitTree_UI, _ = uic.loadUiType(UI_file)


class LMFitBaseTree(QWidget):
    item_selected = pyqtSignal()

    def get_selected_orbital_ID(self):

        selected_items = self.tree.selectedItems()

        for item in selected_items:
            if (isinstance(item, OrbitalTreeItem) or
                    isinstance(item, OrbitalResultTreeItem)):
                return item.ID

            elif ((isinstance(item, LMFitDataTreeItem) or
                   isinstance(item, DataResultTreeItem)) and
                  (isinstance(item.parent(), OrbitalTreeItem) or
                   isinstance(item.parent(), OrbitalResultTreeItem))):
                return item.parent().ID

        return -1

    def _connect(self):

        self.tree.itemSelectionChanged.connect(self.item_selected.emit)


class LMFitTree(LMFitBaseTree, LMFitTree_UI):
    value_changed = pyqtSignal()
    vary_changed = pyqtSignal()

    def __init__(self, orbitals, parameters, *args, **kwargs):

        # Setup GUI
        super(LMFitTree, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup(orbitals, parameters)
        self._connect()

    def save_state(self):

        save = [self.tree.topLevelItem(i).save_state()
                for i in range(self.tree.topLevelItemCount())]

        return save

    def restore_state(self, save):

        for i in range(self.tree.topLevelItemCount()):
            self.tree.topLevelItem(i).restore_state(save[i])

    def add_equation_parameter(self, parameter):

        self.background_item.add_equation_parameter(self.tree, parameter)

    def _change_to_matrix_state(self, state):

        for i in range(self.tree.topLevelItemCount()):
            self.tree.topLevelItem(i)._change_to_matrix_state(state)

    def _setup(self, orbitals, parameters):

        widths = [60, 0, 100, 80, 130, 130, 130, 200]

        for col, width in enumerate(widths):
            self.tree.setColumnWidth(col, width)

        self.tree.header().setResizeMode(1, QHeaderView.Stretch)
        self.tree.header().setDefaultAlignment(Qt.AlignCenter)

        # Add TreeItems
        self.orbital_options_item = OrbitalOptionsTreeItem(
            self.tree, parameters)
        self.background_item = BackgroundOptionsTreeItem(self.tree, parameters)
        self.tree.addTopLevelItem(self.orbital_options_item)
        for orbital in orbitals:
            self.tree.addTopLevelItem(
                OrbitalTreeItem(self.tree, orbital, parameters))

    def _connect(self):

        LMFitBaseTree._connect(self)

        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            item.signals.value_changed.connect(self.value_changed.emit)
            item.signals.vary_changed.connect(self.vary_changed.emit)


# Load .ui File
UI_file = __directory__ / 'ui/lmfitresulttree.ui'
LMFitResultTree_UI, _ = uic.loadUiType(UI_file)


class LMFitResultTree(LMFitBaseTree, LMFitResultTree_UI):

    def __init__(self, orbitals, result, background_variables=[]):

        # Setup GUI
        super(LMFitResultTree, self).__init__()
        self.setupUi(self)
        self._setup(orbitals, result, background_variables)
        self._connect()

    def update_result(self, result):

        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            item.update_result(result)

    def _setup(self, orbitals, result, background_variables):

        widths = [60, 0, 100, 150, 150]

        for col, width in enumerate(widths):
            self.tree.setColumnWidth(col, width)

        self.tree.header().setResizeMode(1, QHeaderView.Stretch)
        self.tree.header().setDefaultAlignment(Qt.AlignCenter)

        # Add TreeItems
        self.tree.addTopLevelItem(OrbitalOptionsResultTreeItem(
            self.tree, result))
        self.tree.addTopLevelItem(BackgroundOptionsResultTreeItem(
            self.tree, result, background_variables))
        for orbital in orbitals:
            self.tree.addTopLevelItem(
                OrbitalResultTreeItem(self.tree, orbital, result))
