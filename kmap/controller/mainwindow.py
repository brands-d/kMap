# Python Imports
import _pickle as pickle
import bz2
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

# Own Imports
from kmap import __directory__
from kmap.config.config import config
from kmap.controller.databasewindows import (
    OrbitalDatabase, SlicedDatabaseWindow)
from kmap.controller.orbitaldatatab import OrbitalDataTab
from kmap.controller.sliceddatatab import SlicedDataTab
from kmap.controller.tabchoosewindow import TabChooseWindow
from kmap.model.mainwindow_model import MainWindowModel

# Load .ui File
UI_file = __directory__ / 'ui/mainwindow.ui'
MainWindow_UI, _ = uic.loadUiType(UI_file)


class MainWindow(QMainWindow, MainWindow_UI):

    def __init__(self):
        # Setup GUI
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect()

        self.sub_windows = {}

        self.model = MainWindowModel(self)

        self.open_welcome()

    def load_hdf5_files(self):
        # Load one or more new hdf5 files

        log = logging.getLogger('kmap')
        log.info('Loading .hdf5 file(s)...')

        extensions = 'hdf5 files (*.hdf5 *.h5);; All Files (*)'

        path = config.get_key('paths', 'hdf5_start')
        if path == 'None':
            paths, _ = QFileDialog.getOpenFileNames(
                None, 'Open file(s)', filter=extensions)
        else:
            start_path = str(__directory__ / path)
            paths, _ = QFileDialog.getOpenFileNames(
                None, 'Open file(s)', str(start_path), extensions)

        if not paths:
            # No file chosen
            log.info('No file chosen')
            return

        for path in paths:
            self.tab_widget.open_sliced_data_tab(path)

    def open_orbitaldatabase_browser(self):
        database = OrbitalDatabase()
        database.files_chosen.connect(self.load_cube_files_online)

        self.sub_windows.update({str(id(database)): database})

    def open_binding_energy_sliceddatabase_browser(self):
        database = SlicedDatabaseWindow(mode='binding-energy')
        database.files_chosen.connect(self.load_sliced_files_online)

        self.sub_windows.update({str(id(database)): database})

    def open_photon_energy_sliceddatabase_browser(self):
        database = SlicedDatabaseWindow(mode='photon-energy')
        database.files_chosen.connect(self.load_sliced_file_online)

        self.sub_windows.update({str(id(database)): database})

    def open_cubefile_sliceddatabase_browser(self):
        database = SlicedDatabaseWindow(mode='cubefile')
        database.files_chosen.connect(self.load_cubefile_as_sliced_online)

        self.sub_windows.update({str(id(database)): database})

    def load_sliced_files_online(self, URLs):
        # Load one or more cube files as sliced data[BE, kx, ky]

        log = logging.getLogger('kmap')
        log.info('Loading .cube file(s) as sliced data[BE, kx, ky]...')

        self.tab_widget.open_sliced_data_tab_by_URLs(URLs)

    def load_sliced_file_online(self, URL):
        # Load one cube file as sliced data[photon_energy, kx, ky]

        log = logging.getLogger('kmap')
        log.info('Loading .cube file as sliced data[photon_energy, kx, ky]...')

        self.tab_widget.open_sliced_data_tab_by_URL(URL)

    def load_cubefile_as_sliced_online(self, URL):
        # Load one cube file as sliced psi[x,y,z] or psik[kx,ky,kz]

        log = logging.getLogger('kmap')
        log.info(
            'Loading .cube file as sliced psi[x,y,z] or psik[kx,ky,kz] ...')

        self.tab_widget.open_sliced_data_tab_by_cube(URL)

    def load_cube_files_online(self, URLs):
        if not URLs:
            # No file chosen
            logging.getLogger('kmap').info('No file chosen')
            return

        # Get Tab to load to
        tab = self.tab_widget.get_orbital_tab_to_load_to()

        # Load URL to Tab
        for URL in URLs:
            try:
                tab.add_orbital_from_online(URL[0], URL[1])

            except ValueError:
                logging.getLogger('kmap').error(
                    'URL "%s" is invalid. File could not be loaded.' % URL)

    def load_cube_files_locally(self):
        # Load one or more new cube files

        extensions = 'cube files (*.cube);; All Files (*)'

        path = config.get_key('paths', 'cube_start')
        if path == 'None':
            paths, _ = QFileDialog.getOpenFileNames(
                None, 'Open file(s)', filter=extensions)
        else:
            start_path = str(__directory__ / path)
            paths, _ = QFileDialog.getOpenFileNames(
                None, 'Open file(s)', str(start_path), extensions)

        if not paths:
            # No file chosen
            logging.getLogger('kmap').info('No file chosen')
            return

        # Get Tab to load to
        tab = self.tab_widget.get_orbital_tab_to_load_to()

        # Load Data to Tab
        for path in paths:
            tab.add_orbital_from_filepath(path)

    def open_log_file(self):
        # Open log file

        path = __directory__ / '../default.log'
        title = 'Log File'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=False)

    def open_mod_log_file(self):
        # Open module log file

        path = __directory__ / '../modules.log'
        title = 'Modules Log File'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=False)

    def open_general_settings(self):
        # Open general user settings

        path = __directory__ / 'config/settings_user.ini'
        title = 'General Settings'

        self.tab_widget.open_file_tab(
            path, title, editable=True, richText=False)

    def open_orbital_data_tab(self):
        self.tab_widget.open_orbital_data_tab()

    def open_profile_tab(self):
        self.tab_widget.open_profile_tab()

    def open_logging_settings(self):
        # Open logging user settings

        path = __directory__ / 'config/logging_user.ini'
        title = 'Logging Settings'

        self.tab_widget.open_file_tab(
            path, title, editable=True, richText=False)

    def open_shortcut_settings(self):
        # Open shortcut user settings

        path = __directory__ / 'config/shortcut_user.ini'
        title = 'Shortcut Settings'

        self.tab_widget.open_file_tab(
            path, title, editable=True, richText=False)

    def open_general_default_settings(self):
        # Open general default settings

        path = __directory__ / 'config/settings_default.ini'
        title = 'General Settings (Default)'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=False)

    def open_shortcut_default_settings(self):
        # Open general default settings

        path = __directory__ / 'config/shortcut_default.ini'
        title = 'Shortcut Settings (Default)'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=False)

    def open_logging_default_settings(self):
        # Open logging default settings

        path = __directory__ / 'config/logging_default.ini'
        title = 'Logging Settings (Default)'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=False)

    def open_readme(self):
        # Open a README page

        path = __directory__ / 'resources/texts/readme.txt'
        title = 'README'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=True)

    def open_welcome(self):
        # Open a welcome page

        path = __directory__ / 'resources/texts/welcome.txt'
        title = 'Welcome'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=True)

    def open_about(self):
        # Open an about window

        path = __directory__ / 'resources/texts/about.txt'
        title, text = self.model.get_about_text(path)
        QMessageBox.about(self, title, text)

    def open_lmfit_tab(self, tabs):
        if len(tabs) != 2 or tabs[0] is None or tabs[1] is None:
            return

        self.tab_widget.open_lmfit_tab(*tabs)

    def open_tab_choose_window(self):
        sliced_tabs = self.tab_widget.get_tabs_of_type(SlicedDataTab)
        orbital_tabs = self.tab_widget.get_tabs_of_type(OrbitalDataTab)

        if len(sliced_tabs) == 0 or len(orbital_tabs) == 0:
            return

        elif len(sliced_tabs) == 1 and len(orbital_tabs) == 1:
            tabs = [*sliced_tabs, *orbital_tabs]
            if self.sender() == self.open_splitview_tab_action:
                self.open_split_view_tab(tabs)
            else:
                self.open_lmfit_tab(tabs)

        else:
            self.tab_choose_window = TabChooseWindow(sliced_tabs,
                                                     orbital_tabs)
            if self.sender() == self.open_splitview_tab_action:
                self.tab_choose_window.tabs_chosen.connect(
                    self.open_split_view_tab)
            else:
                self.tab_choose_window.tabs_chosen.connect(self.open_lmfit_tab)

    def open_split_view_tab(self, tabs):
        if len(tabs) != 2 or tabs[0] is None or tabs[1] is None:
            return

        self.tab_widget.open_split_view_tab(*tabs)

    def open_in_matplotlib(self):
        current_tab = self.tab_widget.get_current_tab()

        if hasattr(current_tab, 'display_in_matplotlib'):
            window = current_tab.display_in_matplotlib()
            self.sub_windows.update({str(id(window)): window})

    def export_to_txt(self):
        current_tab = self.tab_widget.get_current_tab()

        if hasattr(current_tab, 'export_to_txt'):
            text = current_tab.export_to_txt()

            if type(text) is not str:
                return

            file_name, _ = QFileDialog.getSaveFileName(self, 'Save .txt File')

            with open(file_name, 'w') as file:
                file.write(text)

    def export_to_hdf5(self):
        current_tab = self.tab_widget.get_current_tab()

        if hasattr(current_tab, 'export_to_hdf5'):
            current_tab.export_to_hdf5()

    def reload_settings(self):
        # Reload the settings
        config.setup()

    def duplicate_tab(self):
        self.tab_widget.duplicate_tab()

    def save_project(self):
        tabs = self.tab_widget.get_all_tabs()
        tab_saves = []
        for i, tab in enumerate(tabs):
            save, dependencies = tab.save_state()
            dependencies = [self.tab_widget.get_index_of(
                tab) for tab in dependencies]
            tab_saves.append([i, [type(tab).__name__, save], dependencies])

        path = config.get_key('paths', 'project_start')
        if path == 'None':
            file_name, _ = QFileDialog.getSaveFileName(
                None, 'Save Project File (*.kmap)')
        else:
            start_path = str(__directory__ / path)
            file_name, _ = QFileDialog.getSaveFileName(
                None, 'Save Project File (*.kmap)', str(start_path))

        if not file_name.endswith('.kmap'):
            file_name += '.kmap'

        # pickle.dump(tab_saves, open(file_name, 'wb'))
        self.compress_pickle_dump(file_name, tab_saves)

    def compress_pickle_dump(self, title, data):
        with bz2.BZ2File(title, 'w') as f:
            pickle.dump(data, f)

    def decompress_pickle(self, file):
        data = bz2.BZ2File(file, 'rb')
        data = pickle.load(data)
        return data

    def load_project(self):
        path = config.get_key('paths', 'project_start')
        if path == 'None':
            file_names, _ = QFileDialog.getOpenFileNames(
                None, 'Load Project File (*.kmap)')
        else:
            start_path = str(__directory__ / path)
            file_names, _ = QFileDialog.getOpenFileNames(
                None, 'Load Project File (*.kmap)', str(start_path))

        if not file_names:
            return

        file_path = file_names[0]
        # save = pickle.load(open(file_path, 'rb'))
        save = self.decompress_pickle(file_path)

        data_tabs = [tab_save for tab_save in
                     save if tab_save[1][0] in ['SlicedDataTab',
                                                'OrbitalDataTab']]
        basic_tabs = [tab_save for tab_save in
                      save if tab_save[1][0] not in ['LMFitPlotTab',
                                                     'LMFitTab',
                                                     'LMFitResultTab',
                                                     'SlicedDataTab',
                                                     'OrbitalDataTab',
                                                     'SplitViewTab']]
        lmfit_tabs = [tab_save for tab_save in
                      save if tab_save[1][0] == 'LMFitTab']
        split_tabs = [tab_save for tab_save in save if tab_save[1][0] ==
                      'SplitViewTab']
        result_tabs = [tab_save for tab_save in
                       save if tab_save[1][0] == 'LMFitResultTab']
        plot_tabs = [tab_save for tab_save in
                     save if tab_save[1][0] == 'LMFitPlotTab']

        # Go through all non lmfit tabs first and replace the save
        # for a tab with the tab itself to be used for tabs that
        # depend on it
        for tab_save in basic_tabs:
            index, tab_save, _ = tab_save
            save[index] = self.tab_widget.open_tab_by_save(
                tab_save)

        ID_maps = []
        for tab_save in data_tabs:
            index, tab_save, _ = tab_save
            tab, ID_map = self.tab_widget.open_tab_by_save(
                tab_save)
            save[index] = tab
            ID_maps.append(ID_map)

        for tab_save in lmfit_tabs:
            index, tab_save, dependencies = tab_save
            sliced_idx, orbital_idx = dependencies
            sliced_tab = save[sliced_idx]
            orbital_tab = save[orbital_idx]

            tab = self.tab_widget.open_tab_by_save(tab_save,
                                                   sliced_tab,
                                                   orbital_tab)

            tab.sliced_data_tab_idx = sliced_idx
            tab.orbital_data_tab_idx = orbital_idx

            save[index] = tab

        for tab_save in split_tabs:
            index, tab_save, dependencies = tab_save
            sliced_idx, orbital_idx = dependencies
            sliced_tab = save[sliced_idx]
            orbital_tab = save[orbital_idx]

            tab = self.tab_widget.open_tab_by_save(tab_save,
                                                   sliced_tab,
                                                   orbital_tab)

            save[index] = tab

        for tab_save in result_tabs:
            index, tab_save, dependencies = tab_save
            lmfit_tab_idx = dependencies[0]
            lmfit_tab = save[lmfit_tab_idx]

            tab = self.tab_widget.open_tab_by_save(
                tab_save, lmfit_tab, ID_maps)

            save[index] = tab

        for tab_save in plot_tabs:
            index, tab_save, dependencies = tab_save
            result_tab_idx = dependencies[0]
            result_tab = save[result_tab_idx]

            self.tab_widget.open_tab_by_save(tab_save, result_tab)

    def closeEvent(self, event):
        for window in self.sub_windows.values():
            try:
                window.close()

            except Exception:
                pass

        event.accept()

    def close_current_tab(self):
        tab = self.tab_widget.get_current_tab()

        if tab is not None:
            tab.close()

    def _setup(self):
        self._set_misc()
        self._initialize_shortcuts()

    def _set_misc(self):
        x = int(config.get_key('app', 'x'))
        y = int(config.get_key('app', 'y'))
        w = int(config.get_key('app', 'w'))
        h = int(config.get_key('app', 'h'))
        self.setGeometry(x, y, h, w)
        if config.get_key('app', 'fullscreen') == 'True':
            self.showMaximized()
        self.setWindowTitle('kMap.py')
        self.setWindowIcon(QIcon(str(__directory__ /
                                     'resources/images/icon.png')))
        self.show()

    def _initialize_shortcuts(self):
        actions = [self.load_hdf5_action,
                   self.load_sliced_from_binding_energy_action,
                   self.load_sliced_from_photon_energy_action,
                   self.show_matplotlib,
                   self.log_file_action, self.load_cube_online_action,
                   self.load_cube_file_action,
                   self.open_lmfit_tab_action,
                   self.settings_action, self.duplicate_tab_action,
                   self.close_tab_action, self.save_project_action,
                   self.load_project_action,
                   self.general_default_action,
                   self.general_action,
                   self.logging_default_action,
                   self.logging_action, self.open_sim_tab_action,
                   self.open_profile_tab_action, self.mod_log_file_action,
                   self.export_txt, self.load_sliced_from_cubefile_action,
                   self.welcome_action, self.about_action, self.readme_action,
                   self.export_hdf5, self.open_splitview_tab_action]

        alias = ['load_hdf5', 'load_sliced_from_binding_energy_action',
                 'load_sliced_from_photon_energy_action',
                 'show_matplotlib', 'open_log',
                 'load_cube_online', 'load_cube_file',
                 'open_lmfit', 'reload_settings',
                 'duplicate_tab_action', 'close_tab_action',
                 'save_project_action', 'load_project_action',
                 'open_general_default', 'open_general_user',
                 'open_logging_default', 'open_logging_user',
                 'open_sim_tab_action', 'open_profile_tab_action',
                 'mod_log_file_action', 'export_txt',
                 'load_sliced_from_cubefile_action',
                 'welcome_action', 'about_action', 'readme_action',
                 'export_hdf5', 'split_view']

        for action, alias in zip(actions, alias):
            shortcut = config.get_key('shortcut', alias, file='shortcut')
            if shortcut != 'None':
                action.setShortcut(QKeySequence(shortcut))

        self.ref_action.setShortcut(QKeySequence('Ctrl+r'))

    def _connect(self):
        # File menu
        self.load_hdf5_action.triggered.connect(self.load_hdf5_files)
        self.load_sliced_from_binding_energy_action.triggered.connect(
            self.open_binding_energy_sliceddatabase_browser)
        self.load_sliced_from_photon_energy_action.triggered.connect(
            self.open_photon_energy_sliceddatabase_browser)
        self.load_sliced_from_cubefile_action.triggered.connect(
            self.open_cubefile_sliceddatabase_browser)
        self.load_cube_file_action.triggered.connect(
            self.load_cube_files_locally)
        self.load_cube_online_action.triggered.connect(
            self.open_orbitaldatabase_browser)
        self.log_file_action.triggered.connect(self.open_log_file)
        self.mod_log_file_action.triggered.connect(self.open_mod_log_file)
        self.show_matplotlib.triggered.connect(self.open_in_matplotlib)
        self.export_txt.triggered.connect(self.export_to_txt)
        self.export_hdf5.triggered.connect(self.export_to_hdf5)
        self.duplicate_tab_action.triggered.connect(self.duplicate_tab)
        self.close_tab_action.triggered.connect(self.close_current_tab)
        self.save_project_action.triggered.connect(self.save_project)
        self.load_project_action.triggered.connect(self.load_project)

        # Tabs menu
        self.open_sim_tab_action.triggered.connect(self.open_orbital_data_tab)
        self.open_profile_tab_action.triggered.connect(self.open_profile_tab)
        self.open_lmfit_tab_action.triggered.connect(
            self.open_tab_choose_window)
        self.open_splitview_tab_action.triggered.connect(
            self.open_tab_choose_window)

        # Preferences menu
        self.general_action.triggered.connect(self.open_general_settings)
        self.shortcut_action.triggered.connect(self.open_shortcut_settings)
        self.logging_action.triggered.connect(self.open_logging_settings)
        self.general_default_action.triggered.connect(
            self.open_general_default_settings)
        self.shortcut_default_action.triggered.connect(
            self.open_shortcut_default_settings)
        self.logging_default_action.triggered.connect(
            self.open_logging_default_settings)
        self.settings_action.triggered.connect(self.reload_settings)

        # Help menu
        self.readme_action.triggered.connect(self.open_readme)
        self.welcome_action.triggered.connect(self.open_welcome)
        self.about_action.triggered.connect(self.open_about)
