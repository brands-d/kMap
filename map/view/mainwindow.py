import logging
import re
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from map.ui.mainwindow_ui import MainWindowUI
from map.view.sliceddatatab import SlicedDataTab
from map.view.orbitaldatatab import OrbitalDataTab
from map import __directory__, __version__


class MainWindow(QMainWindow, MainWindowUI):

    def __init__(self, model):

        super().__init__()

        self.setupUi(model)

        self.show()

    def open_about(self):

        QMessageBox.about(self, 'Map', r'<h2 id="map"><center>Map' +
                          '</center></h2>' +
                          '<p> Map is a utility project to display, ' +
                          'modify and compare momentum maps of ' +
                          'orbitals from ARPES experiments and DFT ' +
                          'calculations. </p>\n <h4 id="version-s"> '
                          'Version: % s < /h4 >\n ' % __version__ +
                          '<h4 id="copyright-2020-"> Copyright 2020: ' +
                          '</h4><ul> <li> Dominik Brandstetter </li>' +
                          '<li> Peter Puschnig </li></ul>')

    def open_readme(self):
        ''' UNDER CONSTRUCTION '''
        print('Open README')

    def open_general_settings(self):
        ''' UNDER CONSTRUCTION '''
        print('Open General Settings')

    def open_logging_settings(self):
        ''' UNDER CONSTRUCTION '''
        print('Open Logging Settings')

    def reload_settings(self):

        self.model.reload_settings()

    def add_sliced_data_tab(self, data):

        if 'alias' in data.meta_data:
            tab_title = data.meta_data['alias']

        else:
            tab_title = data.name

        tab_title = tab_title + ' (' + str(data.ID) + ')'
        self.tab_widget.addTab(SlicedDataTab(self.model, data), tab_title)

    def add_orbital_data_tab(self, data):

        if 'alias' in data.meta_data:
            tab_title = data.meta_data['alias']

        else:
            tab_title = data.name

        tab_title = tab_title + ' (' + str(data.ID) + ')'
        self.tab_widget.addTab(OrbitalDataTab(self.model, data), tab_title)

    def close_tab(self, index):

        tab_text = self.tab_widget.tabText(index)
        ID = self._get_ID_from_tab_text(tab_text)

        try:
            self.model.remove_data_by_ID(ID)
            self.tab_widget.removeTab(index)

        except LookupError:
            log = logging.getLogger('root')
            log.exception('Removing of data with ID %i couldn\'t' % ID +
                          ' be removed. Traceback:')
            log.error('Error occured when trying to remove data. ' +
                      'Correct behaviour from now on can\'t be ' +
                      'guaranteed!')

    def open_hdf5_file(self):

        file_paths, _ = QFileDialog.getOpenFileNames(
            None, 'Open file',
            __directory__,
            'hdf5 files (*.hdf5 *.h5);; All Files (*)')

        if file_paths:
            for file_path in file_paths:
                new_data = self.model.load_data_from_filepath(file_path,
                                                              'hdf5')

                if new_data:
                    self.add_sliced_data_tab(new_data)

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
                    self.add_orbital_data_tab(new_data)

        else:
            self.root_log.info('No file chosen')

    def _get_ID_from_tab_text(self, tab_text):

        return int(re.search(r'\([0-9]+\)', tab_text).group(0)[1:-1])
