from PyQt5.QtWidgets import QTreeWidget, QHeaderView, QAbstractItemView
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtCore import Qt
from kmap.ui.abstract_ui import AbstractUI


class TreeUI(AbstractUI, QTreeWidget):

    def _initialize_misc(self):

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.header().setMinimumSectionSize(10)


class DatabaseTreeUI(TreeUI):

    def _initialize_content(self):

        self.setColumnCount(6)
        self.setHeaderLabels(['Name', 'Formula', 'Charge',
                              'Mag. Moment', 'XC-Funktional', 'Energy'])
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 150)
        self.setColumnWidth(4, 150)
        self.setColumnWidth(5, 150)
        self.header().setStretchLastSection(False)
        self.header().setDefaultAlignment(Qt.AlignCenter)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        ''' Takes way too long
        self.setSortingEnabled(True)
        self.header().setSortIndicatorShown(True)'''
