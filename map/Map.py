import logging.config
from configparser import ConfigParser
from PyQt5.QtWidgets import QApplication
from map.gui.mainwindow import MainWindow
from map import __directory__, __version__, __project__


class Map(QApplication):

    def __init__(self, sysarg):

        # Initialize logging
        logging.config.fileConfig(__directory__ +
                                  '/config/logging.ini')
        self.root_log = logging.getLogger('root')
        self.root_log.debug('Initializing Map')

        # Initialize settings
        self.cfg = ConfigParser()
        self.cfg.read(__directory__ + '/config/settings.ini')

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
