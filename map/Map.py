import os
import logging
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from map.view.mainwindow import MainWindow
from map import __version__, __project__, __directory__
from map.model.model import Model
from map.config.config import config


class Map(QApplication):

    def __init__(self, sysarg):

        # Apply various configurations
        self.load_settings(startup=True)

        logging.getLogger('root').debug(
            'Initializing Map v' + __version__ + '.')

        # Initialize application
        super().__init__(sysarg)
        self.setApplicationVersion(__version__)
        self.setApplicationName(__project__)
        self.setDesktopFileName(__project__)

    def run(self):

        logging.getLogger('root').info('Starting up Map.')

        # Creating model
        model = Model(self)

        # Creating mainwindow
        self.main_window = MainWindow(model)

        super().exec_()

    def load_settings(self, startup=False):

        # Load config
        config.setup()

        # Logging
        # Delete old log files if user set to do so
        if startup and config.get_key('logging', 'persistent') == 'False':
            log_file = __directory__ + '/../default.log'
            if os.path.exists(log_file):
                os.remove(log_file)

        logging.config.fileConfig(config.get_config(
            'logging'), disable_existing_loggers=False)

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

        value = config.get_key('pyqtgraph', 'imageAxisOrder')
        pg.setConfigOption('imageAxisOrder', value)

        logging.getLogger('root').debug('Settings loaded successfully.')
