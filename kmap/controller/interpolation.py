# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.library.misc import (
    resolution_to_num, num_to_resolution, axis_from_range)

# Load .ui File
UI_file = __directory__ + '/ui/interpolation.ui'
Interpolation_UI, _ = uic.loadUiType(UI_file)


class Interpolation(QWidget, Interpolation_UI):

    def __init__(self):

        # Setup GUI
        super(Interpolation, self).__init__()
        self.setupUi(self)

    def interpolate(self, data):

        if self.interpolation_checkbox.isChecked():
            axes = self.get_axes()
            data.interpolate(*axes, update=True)
            
        return data

    def smooth(self, data):

        if self.smoothing_checkbox.isChecked():
            sigma = self.get_sigma()
            data.smoothing(*sigma, update=True)

        return data

    def get_sigma(self):

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

    def get_order(self):

        return self.order_spinbox.value()

    def get_axes(self):

        range_ = self.get_range()
        resolution = self.get_resolution()
        num = [resolution_to_num(range_[0], resolution[0]),
               resolution_to_num(range_[1], resolution[1])]

        axes = [axis_from_range(range_[0], num[0]),
                axis_from_range(range_[1], num[1])]

        return axes
