from map.ui.abstract_ui import AbstractUI
from PyQt5.QtWidgets import QPushButton


class MainWindowUI(AbstractUI):

    def _initialize_geometry(self, window):

        window.setGeometry(100, 100, 800, 600)
        window.setWindowTitle('Map')

    def _initialize_sub_content(self, window):

        test_button = QPushButton('Test')
        window.setCentralWidget(test_button)
