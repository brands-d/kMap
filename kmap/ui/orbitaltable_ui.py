from abc import abstractmethod
from PyQt5.QtWidgets import QGroupBox, QTableWidget, QVBoxLayout, QHeaderView
from kmap.ui.abstract_ui import AbstractUI


class OrbitalTableUI(AbstractUI, QGroupBox):

    def _initialize_misc(self):

        self.setTitle('Loaded Orbitals')
        self.setStyleSheet('QGroupBox { font-weight: bold; } ')

    def _initialize_content(self):

        # Table Label
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Remove', 'ID', 'Name'])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setResizeMode(
            QHeaderView.ResizeToContents)
        '''
        self.table.setColumnWidth(0, 75)
        self.table.setColumnWidth(1, 50)'''
        self.table.horizontalHeader().setResizeMode(2, QHeaderView.Stretch)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def _initialize_connections(self):
        pass
