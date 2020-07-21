from map.ui.dataslider_ui import DataSliderUI
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal


class DataSlider(QWidget, DataSliderUI):

    value_changed = pyqtSignal(int)

    def __init__(self, data):

        super().__init__()

        self.data = data

        self.setupUi()

        self.load_data()

    def load_data(self):

        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.data.slice_keys) - 1)
        self.slider.setSingleStep(1)

    def change_slice(self, index):

        self.value_changed.emit(index)
