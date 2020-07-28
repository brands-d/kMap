from math import ceil, floor
from PyQt5.QtWidgets import QMainWindow
from matplotlib.ticker import AutoMinorLocator
from kmap.ui.matplotlibwindow_ui import MatplotlibWindowUI


class MatplotlibWindow(QMainWindow, MatplotlibWindowUI):

    def __init__(self, plot_data, name='Matplotlib'):

        super().__init__()

        self.name = name
        self.plot_data = plot_data

        self.setupUI()

        self._calc_centered_axes()
        self.fit_axis_limit()

        self.display_figure()

        self.show()
        self.options.show()

    def display_figure(self):

        self.plot = self.axes.pcolormesh(self.x, self.y, self.plot_data.data)

    def _calc_centered_axes(self):

        x_step_size = self.plot_data.step_size[0]
        centered_range = self.plot_data.range[0] + \
            [-x_step_size / 2, x_step_size / 2]
        self.x = self.plot_data.axis_from_range(
            centered_range, len(self.plot_data.x_axis) + 1)

        y_step_size = self.plot_data.step_size[1]
        centered_range = self.plot_data.range[1] + \
            [-y_step_size / 2, y_step_size / 2]
        self.y = self.plot_data.axis_from_range(
            centered_range, len(self.plot_data.y_axis) + 1)

    def update_axes(self):

        # Update Axis Limit
        x_limit = [self.x_min_spinbox.value(), self.x_max_spinbox.value()]
        y_limit = [self.y_min_spinbox.value(), self.y_max_spinbox.value()]
        self.axes.set_xlim(x_limit)
        self.axes.set_ylim(y_limit)

        # Update Ticks
        ticks_num = self.ticks_spinbox.value()
        # Is off by one, no idea why
        self.axes.xaxis.set_minor_locator(AutoMinorLocator(ticks_num + 1))
        self.axes.yaxis.set_minor_locator(AutoMinorLocator(ticks_num + 1))

        # Update Grid
        grid = self.grid_combobox.currentIndex()
        if grid == 0:
            self.axes.grid(False, which='both')

        elif grid == 1:
            self.axes.grid(True, which='major')
            self.axes.grid(False, which='minor')

        elif grid == 2:
            self.axes.grid(True, which='both')

        self.figure.canvas.draw()

    def fit_axis_limit(self):

        # New Limits. Round to second decimal place to always fit entire
        # image
        x_limit = [floor(min(self.x) * 100) / 100,
                   ceil(max(self.x) * 100) / 100]
        y_limit = [floor(min(self.y) * 100) / 100,
                   ceil(max(self.y) * 100) / 100]

        # Disable signals to not redraw everytime
        self.x_min_spinbox.blockSignals(True)
        self.x_max_spinbox.blockSignals(True)
        self.y_min_spinbox.blockSignals(True)
        self.y_max_spinbox.blockSignals(True)

        # "Disable" boundaries because new range might not fit
        self.x_min_spinbox.setMaximum(10)
        self.x_max_spinbox.setMinimum(-10)
        self.y_min_spinbox.setMaximum(10)
        self.y_max_spinbox.setMinimum(-10)

        # Update spinboxes
        self.x_min_spinbox.setValue(x_limit[0])
        self.x_max_spinbox.setValue(x_limit[1])
        self.y_min_spinbox.setValue(y_limit[0])
        self.y_max_spinbox.setValue(y_limit[1])

        # Reset boundaries
        self._update_boundaries()

        self.x_min_spinbox.blockSignals(False)
        self.x_max_spinbox.blockSignals(False)
        self.y_min_spinbox.blockSignals(False)
        self.y_max_spinbox.blockSignals(False)

        # Redraw
        self.update_axes()

    def _update_boundaries(self):

        self.x_min_spinbox.setMaximum(self.x_max_spinbox.value() - 0.1)
        self.x_max_spinbox.setMinimum(self.x_min_spinbox.value() + 0.1)
        self.y_min_spinbox.setMaximum(self.y_max_spinbox.value() - 0.1)
        self.y_max_spinbox.setMinimum(self.y_min_spinbox.value() + 0.1)

    def closeEvent(self, event):

        # Catch closing to close options window as well
        self.options.close()
        event.accept()

    def add_colorbar(self, enable):

        if enable:
            self.colorbar = self.figure.colorbar(self.plot, ax=self.axes)

        else:
            self.colorbar.remove()

        self.update_axes()