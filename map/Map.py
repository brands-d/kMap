import logging.config
from PyQt5.QtWidgets import QApplication, QMainWindow
from map import __directory__, __version__, __project__


class Map(QApplication):

    def __init__(self, sysarg):

        # Initialize logging
        logging.config.fileConfig(__directory__ +
                                  '/config/logging.ini')
        root_logger = logging.getLogger('root')
        root_logger.info('Initializing Map')

        # Initialize settings

        # Initialize application
        super().__init__(sysarg)
        self.setApplicationVersion(__version__)
        self.setApplicationName(__project__)
