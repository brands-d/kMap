import logging
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from map.view.mainwindow import MainWindow
from map import __version__, __project__
from map.model.model import Model
from map.config.config import config


class Map(QApplication):

    def __init__(self, sysarg):

        # Load config
        config.setup()

        logging.config.fileConfig(config.get_config('logging'))
        self.root_log = logging.getLogger('root')
        self.root_log.debug('Initializing Map')

        # Initialize application
        super().__init__(sysarg)
        self.setApplicationVersion(__version__)
        self.setApplicationName(__project__)
        self.setDesktopFileName(__project__)

        # Apply various configurations
        self._setup()

    def run(self):

        self.root_log.info('Starting up Map')

        # Creating model
        self.model = Model()

        # Creating mainwindow
        self.main_window = MainWindow(self.model)

        super().exec_()

    def _setup(self):

        # PyQtGraph
        value = config.get_key('pyqtgraph', 'background')
        if value == 'None':
            pg.setConfigOption('background', None)

        else:
            pg.setConfigOption('background', value)

        value = config.get_key('pyqtgraph', 'foreground')
        if value == 'None':
            pg.setConfigOption('foreground', None)

        else:
            pg.setConfigOption('foreground', value)

        value = config.get_key('pyqtgraph', 'antialias')
        if value == 'True':
            pg.setConfigOption('antialias', True)

        else:
            pg.setConfigOption('antialias', False)
