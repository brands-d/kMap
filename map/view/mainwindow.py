from PyQt5.QtWidgets import QMainWindow
from map.ui.mainwindow_ui import MainWindowUI


class MainWindow(QMainWindow, MainWindowUI):

    def __init__(self):

        super().__init__()
        self.setupUi()

        self.show()

    def open_about(self):
        ''' UNDER CONSTRUCTION '''
        print('Open About')

    def open_general_settings(self):
        ''' UNDER CONSTRUCTION '''
        print('Open General Settings')

    def open_logging_settings(self):
        ''' UNDER CONSTRUCTION '''
        print('Open Logging Settings')

    def open_file(self):
        ''' UNDER CONSTRUCTION '''
        print('Open File')
