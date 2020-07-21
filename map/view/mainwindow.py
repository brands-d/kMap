import logging
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from map.ui.mainwindow_ui import MainWindowUI
from map.view.sliceddatatab import SlicedDataTab
from map.view.orbitaldatatab import OrbitalDataTab
from map.view.fileviewertab import FileViewerTab
from map.view.fileeditortab import FileEditorTab
from map import __directory__, __version__


class MainWindow(QMainWindow, MainWindowUI):

    def __init__(self, model):

        super().__init__()

        self.setupUi()

        self.model = model

        self.open_welcome()

        self.show()

    def open_about(self):

        with open(__directory__ + '/resources/texts/about.txt', 'r') as f:
            QMessageBox.about(self, 'Map', f.read() % __version__)

    def open_readme(self):

        file_path = __directory__ + '/resources/texts/readme.txt'
        index = self.tab_widget.addTab(FileViewerTab(
            file_path, richText=True), 'README')
        self.tab_widget.setCurrentIndex(index)

    def open_general_settings(self):

        file_path = __directory__ + '/config/settings.ini'
        index = self.tab_widget.addTab(
            FileEditorTab(file_path), 'General Settings')
        self.tab_widget.setCurrentIndex(index)

    def open_logging_settings(self):

        file_path = __directory__ + '/config/logging.ini'
        index = self.tab_widget.addTab(
            FileEditorTab(file_path), 'Logging Settings')
        self.tab_widget.setCurrentIndex(index)

    def open_log_file(self):

        file_path = __directory__ + '/../default.log'
        index = self.tab_widget.addTab(FileViewerTab(file_path), 'Log File')
        self.tab_widget.setCurrentIndex(index)

    def open_welcome(self):

        file_path = __directory__ + '/resources/texts/welcome.txt'
        index = self.tab_widget.addTab(
            FileViewerTab(file_path, richText=True), 'Welcome')
        self.tab_widget.setCurrentIndex(index)

    def reload_settings(self):

        self.model.reload_settings()

    def open_sliced_tab(self, data):

        if 'alias' in data.meta_data:
            tab_title = data.meta_data['alias']

        else:
            tab_title = data.name

        tab_title = tab_title + ' (' + str(data.ID) + ')'
        index = self.tab_widget.addTab(
            SlicedDataTab(self.model, data), tab_title)
        self.tab_widget.setCurrentIndex(index)

    def open_orbital_tab(self, data):

        if 'alias' in data.meta_data:
            tab_title = data.meta_data['alias']

        else:
            tab_title = data.name

        tab_title = tab_title + ' (' + str(data.ID) + ')'
        index = self.tab_widget.addTab(
            OrbitalDataTab(self.model, data), tab_title)
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):

        self.tab_widget.widget(index).close()
        self.tab_widget.removeTab(index)

    def open_hdf5_file(self):

        file_paths, _ = QFileDialog.getOpenFileNames(
            None, 'Open file',
            __directory__ + '/resources/test_resources/',
            'hdf5 files (*.hdf5 *.h5);; All Files (*)')

        if file_paths:
            for file_path in file_paths:
                new_data = self.model.load_data_from_filepath(file_path,
                                                              'hdf5')

                if new_data:
                    self.open_sliced_tab(new_data)

        else:
            self.root_log.info('No file chosen')

    def open_cube_file(self):

        file_paths, _ = QFileDialog.getOpenFileNames(
            None, 'Open file',
            __directory__,
            'hdf5 files (*.cube);; All Files (*)')

        if file_paths:
            for file_path in file_paths:
                new_data = self.model.load_data_from_filepath(file_path,
                                                              'cube')

                if new_data:
                    self.open_orbital_tab(new_data)

        else:
            self.root_log.info('No file chosen')
