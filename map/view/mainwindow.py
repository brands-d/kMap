import logging
import re
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from map.ui.mainwindow_ui import MainWindowUI
from map.view.sliceddatatab import SlicedDataTab
from map import __directory__


class MainWindow(QMainWindow, MainWindowUI):

    def __init__(self, model):

        super().__init__()

        self.setupUi(model)

        self.root_log = logging.getLogger('root')

        self.show()

    def open_about(self):
        ''' UNDER CONSTRUCTION '''
        print('Open About')

    def open_readme(self):
        ''' UNDER CONSTRUCTION '''
        print('Open README')

    def open_general_settings(self):
        ''' UNDER CONSTRUCTION '''
        print('Open General Settings')

    def open_logging_settings(self):
        ''' UNDER CONSTRUCTION '''
        print('Open Logging Settings')

    def add_sliced_data_tab(self, data):

        if 'alias' in data.meta_data:
            tab_title = data.meta_data['alias']

        else:
            tab_title = data.name

        tab_title = tab_title + ' (' + str(data.ID) + ')'
        self.tab_widget.addTab(SlicedDataTab(self.model, data), tab_title)

    def close_tab(self, index):

        tab_text = self.tab_widget.tabText(index)
        ID = self._get_ID_from_tab_text(tab_text)

        try:
            self.root_log.info('Removing data with ID %i' % ID)

            self.model.remove_data_by_ID(ID)
            self.tab_widget.removeTab(index)

        except LookupError:
            self.root_log.exception('Removing of data with ID %i ' +
                                    'couldnt be removed. Traceback:'
                                    % ID)
            self.root_log.error('Error occured when trying to remove' +
                                'data. Correct behaviour from now on' +
                                'can\'t be guaranteed!')

    def open_file(self):

        self.root_log.info('Loading new file(s)...')

        file_paths, _ = QFileDialog.getOpenFileNames(
            None, 'Open file',
            __directory__,
            'hdf5 files (*.hdf5 *.h5);; All Files (*)')

        if file_paths:
            for file_path in file_paths:
                new_data = self.model.load_sliced_data_from_filepath(file_path)

                if new_data:
                    self.add_sliced_data_tab(new_data)

        else:
            self.root_log.info('No file chosen')

    def _get_ID_from_tab_text(self, tab_text):

        return int(re.search(r'\([0-9]+\)', tab_text).group(0)[1:-1])
