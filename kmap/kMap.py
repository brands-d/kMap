import logging
import logging.config

import matplotlib as plt
import pyqtgraph as pg
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from kmap import __directory__, __project__, __version__
from kmap.config.config import config
from kmap.controller.mainwindow import MainWindow


class kMap(QApplication):
    def __init__(self, sysarg):
        # Apply various configurations
        self.load_settings(startup=True)

        logging.getLogger("kmap").debug(f"Initializing kMap.py v{__version__}.")

        # Initialize application
        super().__init__(sysarg)
        self.setApplicationVersion(__version__)
        self.setApplicationName(__project__)
        self.setDesktopFileName(__project__)

    def run(self):
        logging.getLogger("kmap").info("Starting up kMap.")

        # Creating mainwindow
        self.main_window = MainWindow()

        super().exec()

    def test(self):
        pass

    def load_settings(self, startup=False):
        logging.config.fileConfig(
            config.get_config("logging"), disable_existing_loggers=False
        )

        # PyQtGraph
        value = config.get_key("pyqtgraph", "background")
        if value == "None":
            pg.setConfigOption("background", None)

        else:
            pg.setConfigOption("background", value)

        value = config.get_key("pyqtgraph", "foreground")
        if value == "None":
            pg.setConfigOption("foreground", None)

        else:
            pg.setConfigOption("foreground", value)

        value = config.get_key("pyqtgraph", "antialias")
        if value == "True":
            pg.setConfigOption("antialias", True)

        else:
            pg.setConfigOption("antialias", False)

        value = config.get_key("pyqtgraph", "imageAxisOrder")
        pg.setConfigOption("imageAxisOrder", value)

        self.setFont(
            QFont(
                config.get_key("font", "font"),
                int(config.get_key("font", "size")),
                QFont.Normal,
            )
        )

        logging.getLogger("kmap").debug("Settings loaded successfully.")

        # MatPlotlib
        path = config.get_key("paths", "matplotlib")
        if path != "None":
            path = __directory__ / path
            plt.rcParams["savefig.directory"] = str(path)
