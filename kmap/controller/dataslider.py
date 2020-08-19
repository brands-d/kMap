# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/dataslider.ui')
DataSlider_UI, _ = uic.loadUiType(UI_file)


class DataSlider(QWidget, DataSlider_UI):

    slice_changed = pyqtSignal(int)
    axis_changed = pyqtSignal(int)

    def __init__(self, data, *args, **kwargs):

        self.axes = data.axes

        # Setup GUI
        super(DataSlider, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()
        self._connect()

    def change_slice(self, index):

        sender = self.sender().objectName()

        # If spinbox or slider called, index will be the slice index
        # and the other widget has to be updated. As default use slider
        # position as index
        if sender == 'spinbox':
            self._update_slider_silently(index)

        elif sender == 'slider':
            self._update_spinbox_silently(index)

        else:
            index = self.slider.sliderPosition()

        self._update_slice_label()

        self.slice_changed.emit(index)

    def change_axis(self, axis):

        index = self.slider.sliderPosition()

        self._update_slider_silently(index)
        self._update_spinbox_silently(index)
        self._update_slice_label()

        self.axis_changed.emit(axis)

    def get_index(self):

        index = self.slider.sliderPosition()

        return index

    def get_axis(self):

        axis = self.combobox.currentIndex()

        return axis

    def _update_slice_label(self):

        index = self.slider.sliderPosition()
        axis = self.axes[self.combobox.currentIndex()]
        value = axis.axis[index]

        text = '%.2f  %s' % (value, axis.units)
        self.value_label.setText(text)

    def _update_slider_silently(self, index):

        self.slider.blockSignals(True)

        axis = self.axes[self.combobox.currentIndex()]
        maximum = len(axis.axis) - 1
        self.slider.setMaximum(maximum)
        self.slider.setSliderPosition(index)

        self.slider.blockSignals(False)

    def _update_spinbox_silently(self, index):

        self.spinbox.blockSignals(True)

        axis = self.axes[self.combobox.currentIndex()]
        maximum = len(axis.axis) - 1
        self.spinbox.setMaximum(maximum)
        self.spinbox.setValue(index)

        self.spinbox.blockSignals(False)

    def _setup_combobox(self):

        for index in range(3):
            axis_label = self.axes[index].label
            self.combobox.addItem(str(axis_label))

    def _setup(self):

        self._setup_combobox()
        self._update_slice_label()
        self.change_axis(0)

    def _connect(self):

        self.slider.valueChanged.connect(self.change_slice)
        self.spinbox.valueChanged.connect(self.change_slice)
        self.combobox.currentIndexChanged.connect(self.change_axis)
