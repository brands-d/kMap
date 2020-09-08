# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget, QHeaderView, QHBoxLayout, QSizePolicy

# Own Imports
from kmap import __directory__
from kmap.controller.orbitaltablerow import OrbitalTableRow
from kmap.controller.lmfittreeitems import (
    OrbitalTreeItem, OtherTreeItem,
    DataTreeItem, OtherResultTreeItem, OrbitalResultTreeItem)

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfittree.ui')
LMFitTree_UI, _ = uic.loadUiType(UI_file)


class LMFitBaseTree(QWidget):

    item_selected = pyqtSignal()

    def get_selected_orbital_ID(self):

        selected_items = self.tree.selectedItems()

        for item in selected_items:
            if (isinstance(item, OrbitalTreeItem) or
                    isinstance(item, OrbitalResultTreeItem)):
                return item.ID

            elif ((isinstance(item, DataTreeItem) or
                   isinstance(item, DataResultTreeItem)) and
                  (isinstance(item.parent(), OrbitalTreeItem) or
                   isinstance(item.parent(), OrbitalResultTreeItem))):
                return item.parent().ID

        return -1

    def get_all_parameters(self):

        parameters = [self.tree.topLevelItem(i).get_parameters()
                      for i in
                      range(self.tree.topLevelItemCount())]

        return parameters

    def get_orbital_parameters(self, ID):

        parameters = []

        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)

            if i == 0:
                alpha, beta, _, E_kin = item.get_parameters()

            if ((isinstance(item, OrbitalTreeItem) or
                 isinstance(item, OrbitalResultTreeItem)) and
                    ID == item.ID):
                weight, *orientation = item.get_parameters()

        return [weight, E_kin, *orientation, alpha, beta]

    def _connect(self):

        self.tree.itemSelectionChanged.connect(self.item_selected.emit)


class LMFitTree(LMFitBaseTree, LMFitTree_UI):

    value_changed = pyqtSignal()

    def __init__(self, orbitals, *args, **kwargs):

        # Setup GUI
        super(LMFitTree, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup(orbitals)
        self._connect()

    def _get_background(self):

        return self.tree.topLevelItem(0).children[2].initial_spinbox.value()

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

    def _connect(self):

        LMFitBaseTree._connect(self)

        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)

            for child in item.children:
                child.initial_spinbox.valueChanged.connect(
                    self.value_changed.emit)


# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfitresulttree.ui')
LMFitResultTree_UI, _ = uic.loadUiType(UI_file)


class LMFitResultTree(LMFitBaseTree, LMFitResultTree_UI):

    def __init__(self, orbitals, result, *args, **kwargs):

        self.result = result

        # Setup GUI
        super(LMFitResultTree, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup(orbitals)
        self._connect()

    def _get_background(self):

        return self.tree.topLevelItem(0).children[2].get_parameters()

    def _setup(self, orbitals):

        widths = [60, 0, 100, 150, 150]

        for col, width in enumerate(widths):
            self.tree.setColumnWidth(col, width)

        self.tree.header().setResizeMode(1, QHeaderView.Stretch)
        self.tree.header().setDefaultAlignment(Qt.AlignCenter)

        # Add TreeItems
        self.tree.addTopLevelItem(OtherResultTreeItem(self.tree, self.result))
        for orbital in orbitals:
            self.tree.addTopLevelItem(
                OrbitalResultTreeItem(self.tree, orbital, self.result))

    def _connect(self):

        LMFitBaseTree._connect(self)
