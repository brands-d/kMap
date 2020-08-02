from abc import abstractmethod
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit,
    QPushButton, QLabel)
from kmap.ui.abstract_ui import AbstractUI


class FileViewerTabUI(AbstractUI, QWidget):

    def _initialize_content(self):

        # Label
        self.title = QLabel('Path: ' + self.path)

        # Reload Button
        self.reload_button = QPushButton('Reload')
        self.reload_button.setSizePolicy(
            QSP.Policy.Maximum, QSP.Policy.Preferred)

        # Title Layout
        self.title_layout = QHBoxLayout()
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.reload_button)

        # Text display
        self.display = QTextEdit()
        self.display.setReadOnly(True)

        # Search bar
        self.line_edit = QLineEdit()
        self.line_edit.setClearButtonEnabled(True)
        self.line_edit.setPlaceholderText('Enter search term here...')

        # Find button
        self.find_next_button = QPushButton('Find')

        # Find Prev button
        self.find_prev_button = QPushButton('Find Prev')

        # Search Layout
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.line_edit)
        search_layout.addWidget(self.find_next_button)
        search_layout.addWidget(self.find_prev_button)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.title_layout)
        main_layout.addWidget(self.display)
        main_layout.addLayout(search_layout)
        self.setLayout(main_layout)

    def _initialize_connections(self):

        # Search
        self.find_next_button.clicked.connect(self.find_next)
        self.find_prev_button.clicked.connect(self.find_prev)

        # Reload
        self.reload_button.clicked.connect(self.reload_text)
        self.reload_button.clicked.connect(self.refresh_display)

    @abstractmethod
    def find_next(self):
        pass

    @abstractmethod
    def find_prev(self):
        pass

    @abstractmethod
    def reload_text(self):
        pass

    @abstractmethod
    def refresh_display(self):
        pass


class FileEditorTabUI(FileViewerTabUI):

    def _initialize_content(self):

        super()._initialize_content()

        # Make Display Editable
        self.display.setReadOnly(False)

        # Save Button
        self.save_button = QPushButton('Save')
        self.save_button.setShortcut(QKeySequence('Ctrl+s'))
        self.save_button.setSizePolicy(
            QSP.Policy.Maximum, QSP.Policy.Preferred)

        # Title Layout
        self.title_layout.insertWidget(1, self.save_button)

    def _initialize_connections(self):

        super()._initialize_connections()

        # Search
        self.save_button.clicked.connect(self.save)

    @abstractmethod
    def save(self):
        pass
