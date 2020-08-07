from abc import abstractmethod
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QCheckBox, QHBoxLayout, QWidget
from kmap.ui.abstract_ui import AbstractUI


class TreeItemUI(AbstractUI, QTreeWidgetItem):

    pass


class MoleculeTreeItemUI(AbstractUI, QTreeWidgetItem):

    def _initialize_content(self):

        self.setText(0, self.molecule.full_name)
        self.setText(1, self.molecule.formula)
        self.setText(2, '%i' % self.molecule.charge)
        self.setText(3, '%.3f' % self.molecule.magnetic_moment)
        self.setText(4, self.molecule.XC_functional)
        self.setText(5, '')

        self.setTextAlignment(0, Qt.AlignCenter)
        self.setTextAlignment(1, Qt.AlignCenter)
        self.setTextAlignment(2, Qt.AlignCenter)
        self.setTextAlignment(3, Qt.AlignCenter)
        self.setTextAlignment(4, Qt.AlignCenter)
        self.setTextAlignment(5, Qt.AlignCenter)


class OrbitalTreeItemUI(TreeItemUI):

    def _initialize_content(self):

        self.setText(0, self.orbital.name)
        self.setText(1, '')
        self.setText(2, '')
        self.setText(3, '')
        self.setText(4, '')
        self.setText(5, '%.3f' % self.orbital.energy)

        self.setTextAlignment(0, Qt.AlignCenter)
        self.setTextAlignment(1, Qt.AlignCenter)
        self.setTextAlignment(2, Qt.AlignCenter)
        self.setTextAlignment(3, Qt.AlignCenter)
        self.setTextAlignment(4, Qt.AlignCenter)
        self.setTextAlignment(5, Qt.AlignCenter)
