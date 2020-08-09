# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.model.dataslider_model import DataSliderModel

# Load .ui File
UI_file = __directory__ + '/ui/dataslider.ui'
DataSlider_UI, _ = uic.loadUiType(UI_file)


class DataSlider(QWidget, DataSlider_UI):

    value_changed = pyqtSignal(int)

    def __init__(self, data):

        # Setup GUI
        super(DataSlider, self).__init__()
        self.setupUi(self)
        self._connect()

        self.model = DataSliderModel(data)

        self._setup()

    def _setup(self):

        maximum = len(self.model.slice_keys) - 1
        self.slider.setMaximum(maximum)

        key_label, units = self.model.key_label, self.model.units
        self.key_label.setText('%s [%s]:' % (key_label, units))

        self.update_slice_label()

    def update_slice_label(self):

        index = self.slider.sliderPosition()
        value = str(self.model.slice_keys[index])
        self.value_label.setText(value)

    def change_slice(self, index):

        self.update_slice_label()

        self.value_changed.emit(index)

    def _connect(self):

        self.slider.valueChanged.connect(self.change_slice)
