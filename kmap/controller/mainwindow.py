import logging
import traceback
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from kmap.ui.mainwindow_ui import MainWindowUI
from kmap.controller.sliceddatatab import SlicedDataTab
from kmap.controller.orbitaldatatab import OrbitalDataTab
from kmap.controller.filetab import FileViewerTab, FileEditorTab
from kmap.model.mainwindow_model import MainWindowModel
from kmap import __directory__, __version__


class MainWindow(MainWindowUI):

    def __init__(self):

        self.model = MainWindowModel(self)

        MainWindowUI.__init__(self)

        self.open_welcome()

    def close_tab(self, index):
        # Close tab specified with index

        self.tab_widget.removeTab(index)

    def load_hdf5_files(self):
        # Load one or more new hdf5 files

        log = logging.getLogger('kmap')
        log.info('Loading .hdf5 file(s)...')

        start_path = __directory__ + '/resources/test_resources/'
        extensions = 'hdf5 files (*.hdf5 *.h5);; All Files (*)'
        paths, _ = QFileDialog.getOpenFileNames(
            None, 'Open file(s)', start_path, extensions)

        if not paths:
            # No file chosen
            log.info('No file chosen')
            return

        for path in paths:

            self.open_sliced_data_tab(path)

    def open_sliced_data_tab(self, path):
        # Opens a new sliced data tab

        log = logging.getLogger('kmap')
        log.info('Trying to load %s' % path)

        try:
            tab = SlicedDataTab(path)
            title = tab.get_title()

            index = self.tab_widget.addTab(tab, title)
            self.tab_widget.setCurrentIndex(index)

        except Exception as e:

            log.error('Couldn\'t load %s' % path)
            log.error(traceback.format_exc())

    def load_cube_files_online(self):
        pass

    def load_cube_files_locally(self):
        # Load one or more new cube files

        start_path = __directory__ + '/resources/test_resources/'
        extensions = 'cube files (*.cube);; All Files (*)'
        paths, _ = QFileDialog.getOpenFileNames(
            None, 'Open file(s)', start_path, extensions)

        if not paths:
            # No file chosen
            logging.getLogger('kmap').info('No file chosen')
            return

        # Get Tab to load to
        tab = self._get_orbital_tab_to_load_to()

        # Load Data to Tab
        for path in paths:
            tab.add_orbital_from_filepath(path)

    def _get_orbital_tab_to_load_to(self):

        tab = None
        aux = self.tab_widget.currentWidget()
        if type(aux) == OrbitalDataTab:
            tab = aux

        else:
            for index in range(self.tab_widget.count()):
                aux = self.tab_widget.widget(index)

                if type(aux) == OrbitalDataTab:
                    tab = aux
                    break

        if tab is None:
            tab = self.open_orbital_data_tab()

        return tab

    def open_orbital_data_tab(self):
        # Opens a new orbital data tab

        tab = OrbitalDataTab()
        title = tab.get_title()

        index = self.tab_widget.addTab(tab, title)
        self.tab_widget.setCurrentIndex(index)

        return tab

    def open_log_file(self):
        # Open log file

        path = __directory__ + '/../default.log'
        title = 'Log File'

        self._open_file_tab(path, title, editable=False, richText=False)

    def open_mod_log_file(self):
        # Open module log file

        path = __directory__ + '/../modules.log'
        title = 'Modules Log File'

        self._open_file_tab(path, title, editable=False, richText=False)

    def open_general_settings(self):
        # Open general user settings

        path = __directory__ + '/config/settings_user.ini'
        title = 'General Settings'

        self._open_file_tab(path, title, editable=True, richText=False)

    def open_logging_settings(self):
        # Open logging user settings

        path = __directory__ + '/config/logging_user.ini'
        title = 'Logging Settings'

        self._open_file_tab(path, title, editable=True, richText=False)

    def open_general_default_settings(self):
        # Open general default settings

        path = __directory__ + '/config/settings_default.ini'
        title = 'General Settings (Default)'

        self._open_file_tab(path, title, editable=False, richText=False)

    def open_logging_default_settings(self):
        # Open logging default settings

        path = __directory__ + '/config/logging_default.ini'
        title = 'Logging Settings (Default)'

        self._open_file_tab(path, title, editable=False, richText=False)

    def reload_settings(self):
        # Reload the settings

        self.model.reload_settings()

    def open_readme(self):
        # Open a README page

        path = __directory__ + '/resources/texts/readme.txt'
        title = 'README'

        self._open_file_tab(path, title, editable=False, richText=True)

    def open_welcome(self):
        # Open a welcome page

        path = __directory__ + '/resources/texts/welcome.txt'
        title = 'Welcome'

        self._open_file_tab(path, title, editable=False, richText=True)

    def open_about(self):
        # Open an about window

        path = __directory__ + '/resources/texts/about.txt'
        title, text = self.model.get_about_text(path)
        QMessageBox.about(self, title, text)

    def open_in_matplotlib(self):

        current_tab = self.tab_widget.currentWidget()
        if (type(current_tab) is OrbitalDataTab or
                type(current_tab) is SlicedDataTab):

            current_tab.display_in_matplotlib()

    def _open_file_tab(self, path, title, editable=False, richText=False):

        if editable:
            tab = FileEditorTab(path)
        else:
            tab = FileViewerTab(path, richText=richText)

        index = self.tab_widget.addTab(tab, title)
        self.tab_widget.setCurrentIndex(index)
