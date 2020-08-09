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
        fullscreen = bool(config.get_key('logging', 'persistent'))
        if fullscreen:
            self.showMaximized()
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

        # Load cube
        cube_menu = file_menu.addMenu('Open .cube File(s)...')
        self.load_cube_file_action = cube_menu.addAction('Locally...')
        self.load_cube_online_action = cube_menu.addAction('Online...')

        # Separator
        file_menu.addSeparator()

        # Export
        export = file_menu.addMenu('Export')

        # Matplotlib
        self.show_matplotlib = export.addAction('Matplotlib')

        # Separator
        file_menu.addSeparator()

        # Log Menu
        log_menu = file_menu.addMenu('Open .log Files...')

        # Open Log File
        self.log_file_action = log_menu.addAction('default.log...')

        # Open Module Log File
        self.mod_log_file_action = log_menu.addAction('module.log...')

        # Edit menu
        edit_menu = self.menubar.addMenu('Edit')
        self.open_sim_tab_action = edit_menu.addAction('Open new SimTab')

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

        self._initialize_shortcuts()

    def _initialize_shortcuts(self):

        actions = [self.load_hdf5_action, self.show_matplotlib,
                   self.log_file_action, self.load_cube_online_action,
                   self.load_cube_file_action]

        alias = ['load_hdf5', 'show_matplotlib', 'open_log',
                 'load_cube_online', 'load_cube_file']

        for action, alias in zip(actions, alias):
            shortcut = config.get_key('shortcut', alias, file='shortcut')
            action.setShortcut(QKeySequence(shortcut))

    def _initialize_connections(self):

        # Tab closed
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # File menu
        self.load_hdf5_action.triggered.connect(self.load_hdf5_files)
        self.load_cube_file_action.triggered.connect(
            self.load_cube_files_locally)
        self.load_cube_online_action.triggered.connect(
            self.open_database_browser)
        self.log_file_action.triggered.connect(self.open_log_file)
        self.mod_log_file_action.triggered.connect(self.open_mod_log_file)
        self.show_matplotlib.triggered.connect(self.open_in_matplotlib)

        # Edit menu
        self.open_sim_tab_action.triggered.connect(self.open_orbital_data_tab)

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
