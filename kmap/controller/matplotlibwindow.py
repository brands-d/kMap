# Python Imports
from math import ceil, floor

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import (FigureCanvas,
                                                NavigationToolbar2QT)
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
# Third party Imports
from matplotlib.ticker import AutoMinorLocator

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import AspectWidget
from kmap.model.matplotlibwindow_model import MatplotlibWindowModel

# Load .ui File
UI_file = __directory__ / 'ui/matplotlibwindow.ui'
MatplotlibWindow_UI, _ = uic.loadUiType(UI_file)


class MatplotlibWindow(QMainWindow, MatplotlibWindow_UI):

    def __init__(self, plot_data, LUT=None):

        self.model = MatplotlibWindowModel(plot_data)
        self.LUT = ListedColormap(LUT, 'cm_user')

        # Setup GUI
        super(MatplotlibWindow, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect()

        self.display_figure()

        self.update_canvas()
        self.fit_axis()

        self.show()
        self.options.show()

    def display_figure(self):

        x, y, image = self.model.x, self.model.y, self.model.image

        self.plot = self.axes.pcolormesh(x, y, image, cmap=self.LUT)

    def update_x_range(self, range_):

        self.axes.set_xlim(range_)

        self.update_canvas()

    def update_y_range(self, range_):

        self.axes.set_ylim(range_)

        self.update_canvas()

    def update_canvas(self):

        self.figure.canvas.draw()

    def add_minor_ticks(self, num):

        # Is off by one, no idea why
        self.axes.xaxis.set_minor_locator(AutoMinorLocator(num + 1))
        self.axes.yaxis.set_minor_locator(AutoMinorLocator(num + 1))

        self.update_canvas()

    def add_grid(self, which='No Grid'):

        if which == 'No Grid':
            self.axes.grid(False, which='both')

        elif which == 'Major Only':
            self.axes.grid(True, which='major')
            self.axes.grid(False, which='minor')

        elif which == 'Major and Minor':
            self.axes.grid(True, which='both')

        self.update_canvas()

    def fit_axis(self):

        # New Limits. Round to second decimal place to always fit entire
        # image
        x, y = self.model.x, self.model.y
        x_limit = [floor(min(x) * 100) / 100,
                   ceil(max(x) * 100) / 100]
        y_limit = [floor(min(y) * 100) / 100,
                   ceil(max(y) * 100) / 100]

        self.options.set_x_range(x_limit)
        self.options.set_y_range(y_limit)

        self.update_x_range(x_limit)
        self.update_y_range(y_limit)

        self.update_canvas()

    def closeEvent(self, event):

        # Catch closing to close options window as well
        try:
            self.options.close()
            del self.options

        except:
            pass

        finally:
            event.accept()

    def add_colorbar(self, enable):

        if enable:
            self.colorbar = self.figure.colorbar(self.plot, ax=self.axes)

        else:
            self.colorbar.remove()

        self.update_canvas()

    def add_x_label(self, label):

        self.axes.set_xlabel(label)

        self.update_canvas()

    def add_y_label(self, label):

        self.axes.set_ylabel(label)

        self.update_canvas()

    def add_title(self, title):

        self.axes.set_title(title)

        self.update_canvas()

    def _setup(self):

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        # Canvas
        canvas = FigureCanvas(self.figure)
        self.addToolBar(NavigationToolbar2QT(canvas, self))

        # Main Layout
        layout = QHBoxLayout()
        layout.addWidget(canvas)

        self.central_widget = AspectWidget()
        self.central_widget.setLayout(layout)

        self.setCentralWidget(self.central_widget)

        self.options = MatplotlibOptions()

    # noinspection PyUnresolvedReferences
    def _connect(self):

        self.options.colorbar_changed.connect(self.add_colorbar)
        self.options.grid_changed.connect(self.add_grid)
        self.options.ticks_changed.connect(self.add_minor_ticks)
        self.options.title_changed.connect(self.add_title)
        self.options.x_label_changed.connect(self.add_x_label)
        self.options.y_label_changed.connect(self.add_y_label)
        self.options.x_range_changed.connect(self.update_x_range)
        self.options.y_range_changed.connect(self.update_y_range)
        self.options.fit_axis_triggered.connect(self.fit_axis)


# Load .ui File
UI_file = __directory__ / 'ui/matplotliboptions.ui'
MatplotlibOptions_UI, _ = uic.loadUiType(UI_file)


class MatplotlibOptions(QWidget, MatplotlibOptions_UI):
    colorbar_changed = pyqtSignal(int)
    grid_changed = pyqtSignal(str)
    ticks_changed = pyqtSignal(int)
    title_changed = pyqtSignal(str)
    x_label_changed = pyqtSignal(str)
    y_label_changed = pyqtSignal(str)
    x_range_changed = pyqtSignal(list)
    y_range_changed = pyqtSignal(list)
    fit_axis_triggered = pyqtSignal()

    def __init__(self):
        # Setup GUI
        super(MatplotlibOptions, self).__init__()
        self.setupUi(self)
        self._connect()

    def get_x_range(self):
        min_ = self.x_min_spinbox.value()
        max_ = self.x_max_spinbox.value()

        return [min_, max_]

    def get_y_range(self):
        min_ = self.y_min_spinbox.value()
        max_ = self.y_max_spinbox.value()

        return [min_, max_]

    def set_x_range(self, range_):
        min_, max_ = range_

        self.x_min_spinbox.blockSignals(True)
        self.x_max_spinbox.blockSignals(True)

        self.x_min_spinbox.setMaximum(min_ + 1)
        self.x_min_spinbox.setValue(min_)

        self.x_max_spinbox.setMinimum(max_ - 1)
        self.x_max_spinbox.setValue(max_)

        self.x_min_spinbox.blockSignals(False)
        self.x_max_spinbox.blockSignals(False)

        self._update_boundaries()

    def set_y_range(self, range_):
        min_, max_ = range_

        self.y_min_spinbox.blockSignals(True)
        self.y_max_spinbox.blockSignals(True)

        self.y_min_spinbox.setMaximum(min_ + 1)
        self.y_min_spinbox.setValue(min_)

        self.y_max_spinbox.setMinimum(max_ - 1)
        self.y_max_spinbox.setValue(max_)

        self.y_min_spinbox.blockSignals(False)
        self.y_max_spinbox.blockSignals(False)

        self._update_boundaries()

    def add_colorbar(self, state):
        enable = True if state != 0 else False
        self.colorbar_changed.emit(enable)

    def add_grid(self, which):
        self.grid_changed.emit(which)

    def add_ticks(self, num):
        self.ticks_changed.emit(num)

    def add_title(self, text):
        self.title_changed.emit(text)

    def add_x_label(self, text):
        self.x_label_changed.emit(text)

    def add_y_label(self, text):
        self.y_label_changed.emit(text)

    def change_x_range(self):
        range_ = self.get_x_range()

        self._update_boundaries()

        self.x_range_changed.emit(range_)

    def change_y_range(self):
        range_ = self.get_y_range()

        self._update_boundaries()

        self.y_range_changed.emit(range_)

    def fit_axis(self):
        self.fit_axis_triggered.emit()

    def _update_boundaries(self):
        self.x_min_spinbox.setMaximum(self.x_max_spinbox.value() - 0.01)
        self.x_max_spinbox.setMinimum(self.x_min_spinbox.value() + 0.01)
        self.y_min_spinbox.setMaximum(self.y_max_spinbox.value() - 0.01)
        self.y_max_spinbox.setMinimum(self.y_min_spinbox.value() + 0.01)

    def _connect(self):
        self.colorbar_checkbox.stateChanged.connect(self.add_colorbar)
        self.grid_combobox.currentTextChanged.connect(self.add_grid)
        self.ticks_spinbox.valueChanged.connect(self.add_ticks)
        self.title_line_edit.textChanged.connect(self.add_title)
        self.x_line_edit.textChanged.connect(self.add_x_label)
        self.y_line_edit.textChanged.connect(self.add_y_label)
        self.x_min_spinbox.valueChanged.connect(self.change_x_range)
        self.x_max_spinbox.valueChanged.connect(self.change_x_range)
        self.y_min_spinbox.valueChanged.connect(self.change_y_range)
        self.y_max_spinbox.valueChanged.connect(self.change_y_range)
        self.fit_button.clicked.connect(self.fit_axis)
