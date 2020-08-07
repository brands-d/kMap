from abc import abstractmethod
from kmap.ui.abstract_ui import AbstractUI
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QSpinBox, QPlainTextEdit, QComboBox,
    QPushButton, QWidget, QLabel, QHBoxLayout, QSpacerItem,
    QGroupBox)
from kmap.controller.tree import DatabaseTree


class DatabaseWindowUI(AbstractUI, QMainWindow):

    def _initialize_misc(self):

        self.setGeometry(200, 100, 1100, 700)
        self.setWindowTitle('Database')
        self.setWindowModality(Qt.WindowModal)

    def _initialize_content(self):

        # Database Widget
        self.tree = DatabaseTree()

        # Filter Combobox
        self.combobox = QComboBox()
        self.combobox.addItem('No Filter')
        self.combobox.addItem('B3LYP')
        self.combobox.addItem('HSE')
        self.combobox.addItem('OT-RSH')
        self.combobox.addItem('PBE')

        # Filter Button
        self.filter_button = QPushButton('Filter')

        # Spacer
        database_spacer = QSpacerItem(0, 0,
                             hPolicy=QSP.Policy.Expanding,
                             vPolicy=QSP.Policy.Fixed)

        # Load Button
        self.database_button = QPushButton('Load')

        # Layout at the Bottom of the Database
        database_load_layout = QHBoxLayout()
        database_load_layout.addWidget(self.combobox)
        database_load_layout.addWidget(self.filter_button)
        database_load_layout.addItem(database_spacer)
        database_load_layout.addWidget(self.database_button)

        # Database Layout
        database_layout = QVBoxLayout()
        database_layout.addWidget(self.tree)
        database_layout.addLayout(database_load_layout)

        # Database Groupbox
        database_group_box = QGroupBox('Database')
        database_group_box.setStyleSheet('QGroupBox { font-weight: ' +
                                         'bold; } ')
        database_group_box.setLayout(database_layout)

        # URL Lineedit
        self.line_edit = QPlainTextEdit()
        self.line_edit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.line_edit.setPlaceholderText('Please enter URLs to be ' +
                                          'loaded\ndirectly here. To ' +
                                          'load multiple orbitals, ' +
                                          'enter each URL on a new ' +
                                          'line.')

        # URL Spacer
        url_spacer = QSpacerItem(0, 0,
                                 hPolicy=QSP.Policy.Expanding,
                                 vPolicy=QSP.Policy.Fixed)

        # URL Load Button
        self.url_button = QPushButton('Load')

        # URL Load Layout
        url_load_layout = QHBoxLayout()
        url_load_layout.addItem(url_spacer)
        url_load_layout.addWidget(self.url_button)

        # URL Layout
        url_layout = QVBoxLayout()
        url_layout.addWidget(self.line_edit)
        url_layout.addLayout(url_load_layout)

        # URL Groupbox
        url_group_box = QGroupBox('Load by URL')
        url_group_box.setStyleSheet('QGroupBox { font-weight: ' +
                                    'bold; } ')
        url_group_box.setLayout(url_layout)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(database_group_box)
        main_layout.addWidget(url_group_box)
        main_layout.setStretch(0, 3)
        main_layout.setStretch(1, 1)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _initialize_connections(self):

        self.url_button.clicked.connect(self.load_urls)
        self.database_button.clicked.connect(self.load_database)

        self.filter_button.clicked.connect(self.filter_tree)

    @abstractmethod
    def load_urls(self):
        pass

    @abstractmethod
    def load_database(self):
        pass

    @abstractmethod
    def filter(self):
        pass
