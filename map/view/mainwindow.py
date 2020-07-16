from PyQt5.QtWidgets import QMainWindow
from map.ui.mainwindow_ui import MainWindowUI


class MainWindow(QMainWindow, MainWindowUI):

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        self.show()
