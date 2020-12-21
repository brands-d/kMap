# Third Party Imports
import numpy as np

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.library.misc import step_size_to_num, axis_from_range


class InterpolationBase(QWidget):
    interpolation_changed = pyqtSignal()

    def __init__(self):
        # Setup GUI
        super(InterpolationBase, self).__init__()

    def interpolate(self, data):
        if self.interpolation_checkbox.isChecked():
            axes = self.get_axes()
            data.interpolate(*axes, update=True)

        return data

    def get_order(self):
        return self.order_spinbox.value()

    def get_axes(self):
        range_ = self.get_range()
        resolution = self.get_resolution()
        num = [step_size_to_num(range_[0], resolution[0]),
               step_size_to_num(range_[1], resolution[1])]

        axes = [axis_from_range(range_[0], num[0]),
                axis_from_range(range_[1], num[1])]

        return axes

    def _change_interpolation(self):
        self.interpolation_changed.emit()


# Load .ui File
UI_file = __directory__ / 'ui/interpolation.ui'
Interpolation_UI, _ = uic.loadUiType(UI_file)


class Interpolation(InterpolationBase, Interpolation_UI):
    smoothing_changed = pyqtSignal()

    def __init__(self):
        # Setup GUI
        super(Interpolation, self).__init__()
        self.setupUi(self)
        self._connect()

    def set_force_interpolation(self, bool):
        self.interpolation_checkbox.setChecked(bool)
        self.interpolation_checkbox.setEnabled(not bool)

    def smooth(self, data):
        if self.smoothing_checkbox.isChecked():
            sigma = self.get_sigma()

            if self.fill_combobox.currentIndex() == 0:
                fill_value = np.nanmean(data.data)

            elif self.fill_combobox.currentIndex() == 1:
                fill_value = 0

            else:
                fill_value = np.nan

            data.smooth(*sigma, update=True, fill_value=fill_value)

        return data

    def get_sigma(self, pixel=True):
        sigma_x = self.sigma_x_spinbox.value()
        sigma_y = self.sigma_y_spinbox.value()

        return [sigma_x, sigma_y]

    def get_range(self):
        x_min = self.x_min_spinbox.value()
        x_max = self.x_max_spinbox.value()
        y_min = self.y_min_spinbox.value()
        y_max = self.y_max_spinbox.value()

        return [[x_min, x_max], [y_min, y_max]]

    def get_resolution(self):
        x_resolution = self.x_resolution_spinbox.value()
        y_resolution = self.y_resolution_spinbox.value()

        return [x_resolution, y_resolution]

    def set_label(self, x, y):
        # Set Label
        self.x_label.setText('%s:' % x.label)
        self.y_label.setText('%s:' % y.label)

        # Set Unit
        self.x_resolution_spinbox.setSuffix('  %s' % x.units)
        self.sigma_x_spinbox.setSuffix('  %s' % x.units)
        self.y_resolution_spinbox.setSuffix('  %s' % y.units)
        self.sigma_y_spinbox.setSuffix('  %s' % y.units)
        self.x_min_spinbox.setSuffix('  %s' % x.units)
        self.x_max_spinbox.setSuffix('  %s' % x.units)
        self.y_min_spinbox.setSuffix('  %s' % y.units)
        self.y_max_spinbox.setSuffix('  %s' % y.units)

        # Set Range
        self.sigma_x_spinbox.setMinimum(0)
        self.sigma_x_spinbox.setMaximum(15 * x.stepsize)
        self.sigma_y_spinbox.setMinimum(0)
        self.sigma_y_spinbox.setMaximum(15 * y.stepsize)
        # Set min/max of min/max spinbox to twice the range
        self.x_min_spinbox.setMinimum(x.range[0] - abs(x.range[0]))
        self.y_min_spinbox.setMinimum(y.range[0] - abs(y.range[0]))
        self.x_max_spinbox.setMaximum(x.range[1] + abs(x.range[1]))
        self.y_max_spinbox.setMaximum(y.range[1] + abs(y.range[1]))

        # Set Value
        self.sigma_x_spinbox.setValue(3 * x.stepsize)
        self.x_min_spinbox.setValue(x.range[0])
        self.x_max_spinbox.setValue(x.range[-1])
        self.sigma_y_spinbox.setValue(3 * y.stepsize)
        self.y_min_spinbox.setValue(y.range[0])
        self.y_max_spinbox.setValue(y.range[-1])

        self._update_dynamic_range_spinboxes()

    def save_state(self):
        save = {'sigma': self.get_sigma(),
                'range': self.get_range(),
                'force_interpolation':
                    not self.interpolation_checkbox.isEnabled(),
                'resolution': self.get_resolution(),
                'enable_smoothing': self.smoothing_checkbox.checkState(),
                'enable_interpolation': self.interpolation_checkbox.checkState(),
                'fill_value': self.fill_combobox.currentIndex()}

        return save

    def restore_state(self, save):
        self.set_sigma(save['sigma'])
        self.set_range(save['range'])
        self.set_resolution(save['resolution'])
        self.fill_combobox.setCurrentIndex(save['fill_value'])
        self.interpolation_checkbox.setCheckState(save['enable_interpolation'])
        self.smoothing_checkbox.setCheckState(save['enable_smoothing'])
        self.set_force_interpolation(save['force_interpolation'])

    def set_sigma(self, sigma):
        self.sigma_x_spinbox.setValue(sigma[0])
        self.sigma_y_spinbox.setValue(sigma[1])

    def set_range(self, range_):
        self.x_min_spinbox.setValue(range_[0][0])
        self.x_max_spinbox.setValue(range_[0][1])
        self.y_min_spinbox.setValue(range_[1][0])
        self.y_max_spinbox.setValue(range_[1][1])

    def set_resolution(self, resolution):
        self.x_resolution_spinbox.setValue(resolution[0])
        self.y_resolution_spinbox.setValue(resolution[1])

    def _update_dynamic_range_spinboxes(self):
        # Set max/min of min/max spinbox to value of other spinbox
        self.x_min_spinbox.setMaximum(self.x_max_spinbox.value() - 1)
        self.y_min_spinbox.setMaximum(self.y_max_spinbox.value() - 1)
        self.x_max_spinbox.setMinimum(self.x_min_spinbox.value() + 1)
        self.y_max_spinbox.setMinimum(self.y_min_spinbox.value() + 1)

    def _change_smoothing(self):
        self.smoothing_changed.emit()

    def _connect(self):
        self.sigma_x_spinbox.valueChanged.connect(self._change_smoothing)
        self.sigma_y_spinbox.valueChanged.connect(self._change_smoothing)
        self.smoothing_checkbox.stateChanged.connect(
            self._change_smoothing)

        self.x_min_spinbox.valueChanged.connect(
            self._update_dynamic_range_spinboxes)
        self.x_max_spinbox.valueChanged.connect(
            self._update_dynamic_range_spinboxes)
        self.y_min_spinbox.valueChanged.connect(
            self._update_dynamic_range_spinboxes)
        self.y_max_spinbox.valueChanged.connect(
            self._update_dynamic_range_spinboxes)

        self.x_min_spinbox.valueChanged.connect(self._change_interpolation)
        self.x_max_spinbox.valueChanged.connect(self._change_interpolation)
        self.y_min_spinbox.valueChanged.connect(self._change_interpolation)
        self.y_max_spinbox.valueChanged.connect(self._change_interpolation)
        self.interpolation_checkbox.stateChanged.connect(
            self._change_interpolation)

        self.x_resolution_spinbox.valueChanged.connect(
            self._change_interpolation)
        self.y_resolution_spinbox.valueChanged.connect(
            self._change_interpolation)


# Load .ui File
UI_file = __directory__ / 'ui/lmfitinterpolation.ui'
LMFitInterpolation_UI, _ = uic.loadUiType(UI_file)


class LMFitInterpolation(InterpolationBase, LMFitInterpolation_UI):

    def __init__(self):
        # Setup GUI
        super(LMFitInterpolation, self).__init__()
        self.setupUi(self)
        self._connect()

    def save_state(self):
        save = {'range': self.get_range(),
                'resolution': self.get_resolution()}

        return save

    def restore_state(self, save):
        self.set_range(save['range'])
        self.set_resolution(save['resolution'])

    def set_range(self, range_):
        self.min_spinbox.setValue(range_[0][0])
        self.max_spinbox.setValue(range_[0][1])

    def get_range(self):
        min_ = self.min_spinbox.value()
        max_ = self.max_spinbox.value()

        return [[min_, max_], [min_, max_]]

    def set_resolution(self, resolution):
        self.resolution_spinbox.setValue(resolution[0])

    def get_resolution(self):
        resolution = self.resolution_spinbox.value()

        return [resolution, resolution]

    def set_label(self, x, y):
        # Set Label
        self.label.setText('%s:' % x.label)

        # Set Unit
        self.resolution_spinbox.setSuffix('  %s' % x.units)
        self.min_spinbox.setSuffix('  %s' % x.units)
        self.max_spinbox.setSuffix('  %s' % x.units)

        # Set min/max of min/max spinbox to twice the range
        self.min_spinbox.setMinimum(x.range[0] - abs(x.range[0]))
        self.max_spinbox.setMaximum(x.range[1] + abs(x.range[1]))

        # Set Value
        self.min_spinbox.setValue(x.range[0])
        self.max_spinbox.setValue(x.range[-1])

        self._update_dynamic_range_spinboxes()

    def get_axis(self):
        axes = self.get_axes()

        return axes[0]

    def _update_dynamic_range_spinboxes(self):
        # Set max/min of min/max spinbox to value of other spinbox
        self.min_spinbox.setMaximum(self.max_spinbox.value() - 1)
        self.max_spinbox.setMinimum(self.min_spinbox.value() + 1)

    def _connect(self):
        self.min_spinbox.valueChanged.connect(
            self._update_dynamic_range_spinboxes)
        self.max_spinbox.valueChanged.connect(
            self._update_dynamic_range_spinboxes)

        self.min_spinbox.valueChanged.connect(self._change_interpolation)
        self.max_spinbox.valueChanged.connect(self._change_interpolation)

        self.resolution_spinbox.valueChanged.connect(
            self._change_interpolation)
