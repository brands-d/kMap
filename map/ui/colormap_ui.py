from PyQt5.QtWidgets import (
    QGridLayout, QComboBox, QPushButton, QLineEdit)
from map.ui.abstract_ui import AbstractUI


class ColormapUI(AbstractUI):

    def _initialize_content(self):

        self.setTitle('Colormap')
        self.setStyleSheet('QGroupBox { font-weight: bold; } ')

        # Colormap Combobox
        self.combobox = QComboBox()
        self.combobox.setDuplicatesEnabled(False)

        # Reload Button
        self.reload_button = QPushButton('Reload')

        # Add Edit
        self.add_lineEdit = QLineEdit()
        self.add_lineEdit.setClearButtonEnabled(True)
        self.add_lineEdit.setPlaceholderText('Enter new colormap\'s name...')

        # Add Button
        self.add_button = QPushButton('Add')

        # Main Layout
        main_layout = QGridLayout()
        main_layout.addWidget(self.combobox, 0, 0)
        main_layout.addWidget(self.reload_button, 0, 1)
        main_layout.addWidget(self.add_lineEdit, 1, 0)
        main_layout.addWidget(self.add_button, 1, 1)

        self.setLayout(main_layout)

    def _initialize_connections(self):

        self.combobox.currentTextChanged.connect(self.change_colormap)

        self.reload_button.clicked.connect(self.load_colormaps)
        self.add_button.clicked.connect(self.add_colormap)