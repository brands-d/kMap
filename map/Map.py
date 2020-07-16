import logging.config
from PyQt5.QtWidgets import QApplication
from map.view.mainwindow import MainWindow
from map import __version__, __project__
from map.config.config import config


class Map(QApplication):

    def __init__(self, sysarg):

        # Initialize logging

        logging.config.fileConfig(config.get_config('logging'))
        self.root_log = logging.getLogger('root')
        self.root_log.debug('Initializing Map')

        # Initialize application
        super().__init__(sysarg)
        self.setApplicationVersion(__version__)
        self.setApplicationName(__project__)
        self.setDesktopFileName(__project__)

    def run(self):

        self.root_log.info('Starting up Map')

        # Creating MainWindow()
        self.main_window = MainWindow()

        super().exec_()
