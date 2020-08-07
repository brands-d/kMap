from abc import abstractmethod
from PyQt5.QtWidgets import QCheckBox
from kmap.ui.treeitem_ui import (
    TreeItemUI, MoleculeTreeItemUI, OrbitalTreeItemUI)


class TreeItem(TreeItemUI):

    def __init__(self):

        TreeItemUI.__init__(self)


class MoleculeTreeItem(TreeItem, MoleculeTreeItemUI):

    def __init__(self, molecule):

        self.molecule = molecule

        super().__init__()


class OrbitalTreeItem(TreeItem, OrbitalTreeItemUI):

    def __init__(self, orbital):

        self.orbital = orbital

        super().__init__()
