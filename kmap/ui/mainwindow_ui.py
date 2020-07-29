from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTabWidget
from kmap.config.config import config
from kmap.ui.abstract_ui import AbstractUI
from kmap import __directory__


class MainWindowUI(AbstractUI):

    def _initialize_misc(self):

        x = int(config.get_key('app', 'x'))
        y = int(config.get_key('app', 'y'))
        w = int(config.get_key('app', 'w'))
        h = int(config.get_key('app', 'h'))
        self.setGeometry(x, y, h, w)
        self.setWindowTitle('kMap')
        self.setWindowIcon(
            QIcon(__directory__ + '/resources/images/icon.png'))

    def _initialize_content(self):

        # Central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.menubar = self.menuBar()
        # File menu
        file_menu = self.menubar.addMenu('File')
        self.load_slice_action = file_menu.addAction('Open .hdf5 File...')
        self.load_slice_action.setShortcut(QKeySequence('Ctrl+f'))
        self.load_orbital_action = file_menu.addAction('Open .cube File...')
        self.load_orbital_action.setShortcut(QKeySequence('Ctrl+o'))
        file_menu.addSeparator()
        export = file_menu.addMenu('Export')
        self.show_matplotlib = export.addAction('Matplotlib')
        self.show_matplotlib.setShortcut(QKeySequence('Ctrl+m'))
        file_menu.addSeparator()
        log_menu = file_menu.addMenu('Open .log Files...')
        self.log_file_action = log_menu.addAction('default.log...')
        self.log_file_action.setShortcut(QKeySequence('Ctrl+l'))
        self.mod_log_file_action = log_menu.addAction('module.log...')
        # Preferences menu
        settings_menu = self.menubar.addMenu('Preferences')
        general_menu = settings_menu.addMenu('General Settings')
        self.general_action = general_menu.addAction('Edit User')
        self.general_default_action = general_menu.addAction('Show Default')
        logging_menu = settings_menu.addMenu('Logging Settings')
        self.logging_action = logging_menu.addAction('Edit User')
        self.logging_default_action = logging_menu.addAction('Show Default')
        self.settings_action = settings_menu.addAction('Reload Settings')
        # Help menu
        help_menu = self.menubar.addMenu('Help')
        self.readme_action = help_menu.addAction('Open README')
        self.about_action = help_menu.addAction('About kMap')

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setUsesScrollButtons(True)
        layout.addWidget(self.tab_widget)

    def _initialize_connections(self):

        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # File menu
        self.load_slice_action.triggered.connect(self.open_hdf5_file)
        self.load_orbital_action.triggered.connect(self.open_cube_file)
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
        self.about_action.triggered.connect(self.open_about)
