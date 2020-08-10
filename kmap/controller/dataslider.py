# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.config.config import config
#from kmap.model.dataslider_model import DataSliderModel

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

        self._setup(data)

    def update_slice_label(self):

        index = self.slider.sliderPosition()
        value = '%.2f  %s' % (self.slice_keys[index], self.units)
        self.value_label.setText(value)

    def change_slice(self, index):

        self.update_slice_label()

        self.value_changed.emit(index)

    def _setup(self, data):

        # Slice Keys
        self.slice_keys = data.slice_keys
        # Slider
        maximum = len(self.slice_keys) - 1
        self.slider.setMaximum(maximum)

        # Key Labels
        if 'slice_key_label' in data.meta_data:
            key_label = data.meta_data['slice_key_label']

        else:
            key_label = config.get_key(
                'sliced_data', 'default_slice_keys')

        self.key_label.setText('%s:' % key_label)

        # Units
        if 'slice_unit' in data.meta_data:
            self.units = data.meta_data['slice_unit']

        else:
            self.units = config.get_key('sliced_data', 'default_slice_unit')

        self.update_slice_label()

    def _connect(self):

        self.slider.valueChanged.connect(self.change_slice)
