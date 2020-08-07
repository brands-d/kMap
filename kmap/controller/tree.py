from abc import abstractmethod
from PyQt5.QtCore import pyqtSignal
from kmap.ui.tree_ui import DatabaseTreeUI
from kmap.controller.treeitem import MoleculeTreeItem, OrbitalTreeItem


class DatabaseTree(DatabaseTreeUI):

    def add_molecule(self, molecule):

        molecule_item = MoleculeTreeItem(molecule)
        self.addTopLevelItem(molecule_item)

        for orbital in molecule.orbitals:
            orbital_item = OrbitalTreeItem(orbital)
            molecule_item.addChild(orbital_item)

    def get_chosen_items(self):

        orbitals = []

        selected_items = self.selectedItems()

        for selected_item in selected_items:
            if isinstance(selected_item, MoleculeTreeItem):
                molecule = selected_item.molecule

                for orbital in molecule.orbitals:
                    orbitals.append(orbital)

            else:
                orbital = selected_item.orbital
                orbitals.append(orbital)

        return set(orbitals)
