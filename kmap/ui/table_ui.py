from PyQt5.QtWidgets import QGroupBox, QTableWidget, QVBoxLayout, QHeaderView
from PyQt5.QtWidgets import QSizePolicy as QSP
from kmap.ui.abstract_ui import AbstractUI


class TableUI(AbstractUI, QGroupBox):

    def _initialize_misc(self):

        self.setStyleSheet('QGroupBox { font-weight: bold; } ')

    def _initialize_content(self):

        # Table Label
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setMinimumSectionSize(10)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)


class OrbitalTableUI(TableUI):

    def _initialize_misc(self):

        super()._initialize_misc()

        self.setTitle('Loaded Orbitals')

    def _initialize_content(self):

        super()._initialize_content()

        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['', 'ID', 'Name', 'Deconv.', 'Phi', 'Theta', 'Psi'])
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 40)
        self.table.setColumnWidth(3, 90)
        self.table.setColumnWidth(4, 75)
        self.table.setColumnWidth(5, 75)
        self.table.setColumnWidth(6, 75)
        self.table.horizontalHeader().setResizeMode(2, QHeaderView.Stretch)
