import logging
from PyQt5.QtWidgets import QApplication
from map.view.mainwindow import MainWindow
from map import __version__, __project__
from map.model.model import Model
from map.config.config import config


class Map(QApplication):

    def __init__(self, sysarg):

        # Create config
        config.setup()

        self.root_log = logging.getLogger('root')
        self.root_log.debug('Initializing Map')

        # Initialize application
        super().__init__(sysarg)
        self.setApplicationVersion(__version__)
        self.setApplicationName(__project__)
        self.setDesktopFileName(__project__)

    def run(self):

        self.root_log.info('Starting up Map')

        # Creating model
        self.model = Model()

        # Creating mainwindow
        self.main_window = MainWindow(self.model)

        super().exec_()
