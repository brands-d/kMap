from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGroupBox
from map.ui.dataslider_ui import DataSliderUI


class DataSlider(QGroupBox, DataSliderUI):

    value_changed = pyqtSignal(int)

    def __init__(self, slice_keys, key_label='', unit='[a.u.]'):

        super().__init__()

        self.slice_keys = slice_keys
        self.key_label_text = key_label
        self.unit_text = unit

        self.setupUi()

        self._load()

    def _load(self):

        self.slider.setMaximum(len(self.slice_keys) - 1)
        self.key_label.setText(self.key_label_text +
                               ' [' + self.unit_text + ']:')
        self.update_slice_label()

    def update_slice_label(self):

        index = self.slider.sliderPosition()
        self.value_label.setText(str(self.slice_keys[index]))

    def change_slice(self, index):

        self.update_slice_label()

        self.value_changed.emit(index)
