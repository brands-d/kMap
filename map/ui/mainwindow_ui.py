from map.ui.abstract_ui import AbstractUI
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon, QKeySequence
from map import __directory__


class MainWindowUI(AbstractUI):

    def _initialize_geometry(self):

        self.setGeometry(100, 100, 800, 600)

    def _initialize_misc(self):

        self.setWindowTitle('Map')
        self.setWindowIcon(
            QIcon(__directory__ + '/resources/images/icon.png'))

    def _initialize_content(self):

        self.setCentralWidget(QWidget())

        self.menubar = self.menuBar()
        # File menu
        file_menu = self.menubar.addMenu('File')
        open_file_action = file_menu.addAction('Open File...',
                                               self.open_file)
        open_file_action.setShortcut(QKeySequence('Ctrl+f'))
        # Help menu
        help_menu = self.menubar.addMenu('Help')
        help_menu.addAction('About Map', self.open_about)
        help_menu.addAction('Open README', self.open_about)
        # Settings sub-menu
        settings_menu = help_menu.addMenu('Open Settings')
        settings_menu.addAction('General', self.open_general_settings)
        settings_menu.addAction('Logging', self.open_logging_settings)
