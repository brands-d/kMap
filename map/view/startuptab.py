from map.ui.sliceddatatab_ui import StartUpTabUI
from PyQt5.QtWidgets import QWidget


class StartUpTab(QWidget, StartUpTabUI):

    def __init__(self):

        super().__init__()

        self.setupUi()
