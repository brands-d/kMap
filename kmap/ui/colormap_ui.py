from abc import abstractmethod
from PyQt5.QtWidgets import (
    QGridLayout, QComboBox, QPushButton, QLineEdit, QGroupBox)
from kmap.ui.abstract_ui import AbstractUI


class ColormapUI(AbstractUI, QGroupBox):

    def _initialize_misc(self):

        self.setTitle('Colormap')
        self.setStyleSheet('QGroupBox { font-weight: bold; } ')

    def _initialize_content(self):

        # Colormap Combobox
        self.combobox = QComboBox()
        self.combobox.setDuplicatesEnabled(False)

        # Reload Button
        self.reload_button = QPushButton('Reload')

        # LineEdit
        self.lineEdit = QLineEdit()
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('Enter new colormap\'s name...')

        # Add Button
        self.add_button = QPushButton('Add')

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.combobox, 0, 0)
        layout.addWidget(self.reload_button, 0, 1)
        layout.addWidget(self.lineEdit, 1, 0)
        layout.addWidget(self.add_button, 1, 1)

        self.setLayout(layout)

    def _initialize_connections(self):

        self.combobox.currentIndexChanged.connect(
            self.change_colormap_by_index)

        self.reload_button.clicked.connect(self.load_colormaps)
        self.add_button.clicked.connect(self.add_colormap)

    @abstractmethod
    def change_colormap(self, name):
        pass

    @abstractmethod
    def load_colormaps(self):
        pass

    @abstractmethod
    def add_colormap(self):
        pass
