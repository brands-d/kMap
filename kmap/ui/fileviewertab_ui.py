from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel)
from kmap.ui.abstract_ui import AbstractUI


class FileViewerTabUI(AbstractUI):

    def _initialize_content(self):

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        self.title_layout = QHBoxLayout()
        main_layout.addLayout(self.title_layout)
        # Label
        self.title = QLabel('Path: ' + self.file_path)
        self.title_layout.addWidget(self.title)
        # Reload Button
        self.reload_button = QPushButton('Reload')
        self.title_layout.addWidget(self.reload_button)

        # Text display
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        main_layout.addWidget(self.display)

        # Search
        search_layout = QHBoxLayout()
        main_layout.addLayout(search_layout)
        # Search bar
        self.line_edit = QLineEdit()
        self.line_edit.setClearButtonEnabled(True)
        self.line_edit.setPlaceholderText('Enter search term here...')
        search_layout.addWidget(self.line_edit)
        # Find button
        self.find_next_button = QPushButton('Find')
        search_layout.addWidget(self.find_next_button)
        # Find Prev button
        self.find_prev_button = QPushButton('Find Prev')
        search_layout.addWidget(self.find_prev_button)

    def _initialize_connections(self):

        # Search
        self.find_next_button.clicked.connect(self.find_next)
        self.find_prev_button.clicked.connect(self.find_prev)

        # Reload
        self.reload_button.clicked.connect(self.open_file)
