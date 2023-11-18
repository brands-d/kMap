import numpy as np
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from kmap.library.misc import transpose_axis_order
from kmap.ui.dataslider import Ui_dataslider as DataSlider_UI
from kmap.ui.dataslidernotranspose import Ui_dataslider as DataSliderNoTranspose_UI


class DataSliderBase(QWidget):
    slice_changed = Signal(int)
    axis_changed = Signal(int)
    symmetry_changed = Signal(str, bool)

    def __init__(self, data, *args, **kwargs):
        self.data = data

        # Setup GUI
        super(DataSliderBase, self).__init__(*args, **kwargs)

    def change_slice(self, index):
        sender = self.sender().objectName()

        # If spinbox or slider called, index will be the slice index
        # and the other widget has to be updated. As default use slider
        # position as index
        if sender == "spinbox":
            self._update_slider_silently(index)

        elif sender == "slider":
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

    def change_symmetry(self, index):
        symmetries = ("no", "2-fold", "3-fold", "4-fold")
        symmetry = symmetries[int(np.ceil(index / 2))]
        mirror = True if index in (2, 4, 6) else False
        self.symmetry_changed.emit(symmetry, mirror)

    def get_index(self):
        index = self.slider.sliderPosition()

        return index

    def get_axis(self):
        axis = self.combobox.currentIndex()

        return axis

    def save_state(self):
        save = {
            "slice": self.get_index(),
            "axis": self.get_axis(),
            "symmetry": self.symmetrize_combobox.currentIndex(),
        }

        return save

    def restore_state(self, save):
        self.combobox.setCurrentIndex(save["axis"])
        self.slider.setValue(save["slice"])
        self.symmetrize_combobox.setCurrentIndex(save["symmetry"])

    def _update_slice_label(self):
        index = self.slider.sliderPosition()
        axis = self.data.axes[self.combobox.currentIndex()]
        value = axis.axis[index]

        text = "%.2f  %s" % (value, axis.units)
        self.value_label.setText(text)

    def _update_slider_silently(self, index):
        self.slider.blockSignals(True)

        axis = self.data.axes[self.combobox.currentIndex()]
        maximum = len(axis.axis) - 1
        self.slider.setMaximum(maximum)
        self.slider.setSliderPosition(index)

        self.slider.blockSignals(False)

    def _update_spinbox_silently(self, index):
        self.spinbox.blockSignals(True)

        axis = self.data.axes[self.combobox.currentIndex()]
        maximum = len(axis.axis) - 1
        self.spinbox.setMaximum(maximum)
        self.spinbox.setValue(index)

        self.spinbox.blockSignals(False)

    def _setup_combobox(self):
        for index in range(3):
            axis_label = self.data.axes[index].label
            self.combobox.addItem(str(axis_label))

    def _setup(self):
        self._setup_combobox()
        self._update_slice_label()
        self.change_axis(0)

    def _connect(self):
        self.slider.valueChanged.connect(self.change_slice)
        self.spinbox.valueChanged.connect(self.change_slice)
        self.combobox.currentIndexChanged.connect(self.change_axis)
        self.symmetrize_combobox.currentIndexChanged.connect(self.change_symmetry)


class DataSliderNoTranspose(DataSliderBase, DataSliderNoTranspose_UI):
    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(DataSliderNoTranspose, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()
        self._connect()


class DataSlider(DataSliderBase, DataSlider_UI):
    tranpose_triggered = Signal(tuple)
    symmetry_changed = Signal(str, bool)

    def __init__(self, *args, **kwargs):
        self.axis_order = (0, 1, 2)

        # Setup GUI
        super(DataSlider, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()
        self._connect()

    def trigger_transpose(self, axis_order=None):
        index = self.slider.sliderPosition()

        if axis_order and axis_order is not None:
            self.axis_order = axis_order
        else:
            self.axis_order = transpose_axis_order(self.get_axis())

        self.tranpose_triggered.emit(self.axis_order)

        for i in range(3):
            self.combobox.setItemText(i, self.data.axes[i].label)

        self._update_slice_label()
        self._update_slider_silently(index)
        self._update_spinbox_silently(index)

    def save_state(self):
        save_ = {"transpose": self.axis_order}
        save = super().save_state()
        save.update(save_)

        return save

    def restore_state(self, save):
        super().restore_state(save)
        if self.axis_order == save["transpose"]:
            return
        else:
            self.trigger_transpose(save["transpose"])

    def _connect(self):
        super()._connect()
        self.transpose_button.clicked.connect(self.trigger_transpose)
