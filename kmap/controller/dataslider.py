from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGroupBox
from kmap.ui.dataslider_ui import DataSliderUI
from kmap.model.dataslider_model import DataSliderModel

class DataSlider(DataSliderUI):

    value_changed = pyqtSignal(int)

    def __init__(self, data):

        self.model = DataSliderModel(data)

        DataSliderUI.__init__(self)

        self._setup()

    def _setup(self):

        self.slider.setMaximum(len(self.model.slice_keys) - 1)
        self.key_label.setText('%s [%s]:' % (
            self.model.key_label, self.model.unit))

        self.update_slice_label()

    def update_slice_label(self):

        index = self.slider.sliderPosition()
        self.value_label.setText(str(self.model.slice_keys[index]))

    def change_slice(self, index):

        self.update_slice_label()

        self.value_changed.emit(index)
