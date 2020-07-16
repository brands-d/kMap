from map.ui.sliceddatatab_ui import SlicedDataTabUI
from PyQt5.QtWidgets import QWidget


class SlicedDataTab(QWidget, SlicedDataTabUI):

    def __init__(self, model, data):

        super().__init__()

        self.setupUi(model)
