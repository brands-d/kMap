from kmap.ui.abstract_ui import AbstractUI
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QSpinBox, QLineEdit,
    QPushButton, QWidget, QLabel)


class DatabaseWindowUI(AbstractUI, QMainWindow):

    def _initialize_misc(self):

        self.setGeometry(200, 300, 500, 550)
        self.setWindowTitle('Database')
        self.setWindowModality(Qt.WindowModal)

    def _initialize_content(self):

        self.lineedit = QLineEdit()

        self.button = QPushButton('Load Direct')

        self.label1 = QLabel('Molecule Number:')
        self.molecule = QSpinBox()
        self.label2 = QLabel('Orbital Number:')
        self.orbital = QSpinBox()

        self.button2 = QPushButton('Load Indirect')

        layout = QVBoxLayout()
        layout.addWidget(self.lineedit)
        layout.addWidget(self.button)
        layout.addWidget(self.label1)
        layout.addWidget(self.molecule)
        layout.addWidget(self.label2)
        layout.addWidget(self.orbital)
        layout.addWidget(self.button2)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def _initialize_connections(self):

        self.button.clicked.connect(self.load_online)
        self.button2.clicked.connect(self.load_database)
