from abc import abstractmethod
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget
from kmap.config.config import config
from kmap.ui.abstract_ui import AbstractUI
from kmap import __directory__


class MainWindowUI(AbstractUI, QMainWindow):

    def _initialize_misc(self):

        x = int(config.get_key('app', 'x'))
        y = int(config.get_key('app', 'y'))
        w = int(config.get_key('app', 'w'))
        h = int(config.get_key('app', 'h'))
        self.setGeometry(x, y, h, w)
        self.setWindowTitle('kMap')
        self.setWindowIcon(
            QIcon(__directory__ + '/resources/images/icon.png'))
        self.show()

    def _initialize_content(self):

        # Menubar
        self.menubar = self.menuBar()

        # File menu
        file_menu = self.menubar.addMenu('File')

        # Load hdf5
        self.load_hdf5_action = file_menu.addAction('Open .hdf5 File(s)...')
        self.load_hdf5_action.setShortcut(QKeySequence('Ctrl+f'))

        # Load cube
        self.load_cube_action = file_menu.addAction('Open .cube File(s)...')
        self.load_cube_action.setShortcut(QKeySequence('Ctrl+o'))

        # Separator
        file_menu.addSeparator()

        # Export
        export = file_menu.addMenu('Export')

        # Matplotlib
        self.show_matplotlib = export.addAction('Matplotlib')
        self.show_matplotlib.setShortcut(QKeySequence('Ctrl+m'))

        # Separator
        file_menu.addSeparator()

        # Log Menu
        log_menu = file_menu.addMenu('Open .log Files...')

        # Open Log File
        self.log_file_action = log_menu.addAction('default.log...')
        self.log_file_action.setShortcut(QKeySequence('Ctrl+l'))

        # Open Module Log File
        self.mod_log_file_action = log_menu.addAction('module.log...')

        # Preferences menu
        settings_menu = self.menubar.addMenu('Preferences')

        # General settings
        general_menu = settings_menu.addMenu('General Settings')
        self.general_action = general_menu.addAction('Edit User')
        self.general_default_action = general_menu.addAction('Show Default')

        # Logging settings
        logging_menu = settings_menu.addMenu('Logging Settings')
        self.logging_action = logging_menu.addAction('Edit User')
        self.logging_default_action = logging_menu.addAction('Show Default')

        # Reload settings
        self.settings_action = settings_menu.addAction('Reload Settings')

        # Help menu
        help_menu = self.menubar.addMenu('Help')
        self.readme_action = help_menu.addAction('Open README')
        self.welcome_action = help_menu.addAction('Open Welcome')
        self.about_action = help_menu.addAction('About kMap')

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setUsesScrollButtons(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _initialize_connections(self):

        # Tab closed
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # File menu
        self.load_hdf5_action.triggered.connect(self.load_hdf5_files)
        self.load_cube_action.triggered.connect(self.load_cube_files)
        self.log_file_action.triggered.connect(self.open_log_file)
        self.mod_log_file_action.triggered.connect(self.open_mod_log_file)

        # Edit menu
        self.show_matplotlib.triggered.connect(self.open_in_matplotlib)

        # Preferences menu
        self.general_action.triggered.connect(self.open_general_settings)
        self.logging_action.triggered.connect(self.open_logging_settings)
        self.general_default_action.triggered.connect(
            self.open_general_default_settings)
        self.logging_default_action.triggered.connect(
            self.open_logging_default_settings)
        self.settings_action.triggered.connect(self.reload_settings)

        # Help menu
        self.readme_action.triggered.connect(self.open_readme)
        self.welcome_action.triggered.connect(self.open_welcome)
        self.about_action.triggered.connect(self.open_about)

    @abstractmethod
    def close_tab(self, index):
        pass

    @abstractmethod
    def load_hdf5_files(self):
        pass

    @abstractmethod
    def load_cube_files(self):
        pass

    @abstractmethod
    def open_log_file(self):
        pass

    @abstractmethod
    def open_mod_log_file(self):
        pass

    @abstractmethod
    def open_in_matplotlib(self):
        pass

    @abstractmethod
    def open_general_settings(self):
        pass

    @abstractmethod
    def open_logging_settings(self):
        pass

    @abstractmethod
    def open_general_default_settings(self):
        pass

    @abstractmethod
    def open_logging_default_settings(self):
        pass

    @abstractmethod
    def reload_settings(self):
        pass

    @abstractmethod
    def open_readme(self):
        pass

    @abstractmethod
    def open_welcome(self):
        pass

    @abstractmethod
    def open_about(self):
        pass
