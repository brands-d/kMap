# Python Imports
import numpy as np

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# Third Party Imports
from pyqtgraph import ImageView, PlotItem, AxisItem

# Own Imports
from kmap.model.pyqtgraphplot_model import PyQtGraphPlotModel
from kmap.config.config import config


class PyQtGraphPlot(ImageView):

    def __init__(self, *args, plot_data=None, **kwargs):

        # Setup GUI
        self.plot_view = PlotItem()
        super(PyQtGraphPlot, self).__init__(
            *args, view=self.plot_view, **kwargs)
        self._setup()

        self.model = PyQtGraphPlotModel(plot_data)

        self.refresh_plot()

    def plot(self, plot_data):

        self.model.plot_data = plot_data

        self.refresh_plot()

    def refresh_plot(self):

        self.clear()

        if self.model.plot_data is None:
            return

        image, pos, scale, range_ = self.model.get_plot()

        if np.all(np.isnan(image)) == True:
            return

        # Plot
        self.setImage(image, autoRange=True,
                      autoLevels=True, pos=pos, scale=scale)

        # Fit Range
        padding = float(config.get_key('pyqtgraph', 'padding'))
        x_range, y_range = range_
        self.view.setRange(xRange=x_range, yRange=y_range,
                           update=True, padding=padding)

        # set AspectRatio
        self.plot_view.setAspectLocked(True, ratio=(
            y_range[1] - y_range[0]) / (x_range[1] - x_range[0]))

    def get_plot_data(self):

        return self.model.plot_data

    def get_LUT(self):

        colormap = self.getHistogramWidget().gradient.colorMap()
        LUT = colormap.getLookupTable(mode='float', alpha=False, nPts=20)

        return LUT

    def set_label(self, x, y):

        color = config.get_key('pyqtgraph', 'axis_color')
        size = config.get_key('pyqtgraph', 'axis_size')

        x_axis = AxisItem('bottom', text=x.label, units=x.units,
                          **{'color': color, 'font-size': size})
        y_axis = AxisItem('left', text=y.label, units=y.units,
                          **{'color': color, 'font-size': size})

        if config.get_key('pyqtgraph', 'show_axis_label') != 'True':
            x_axis.showLabel(True)
            y_axis.showLabel(True)

        else:
            x_axis.showLabel(True)
            y_axis.showLabel(True)

        self.view.setAxisItems({'bottom': x_axis, 'left': y_axis})

    def get_label(self, side):

        return self.plot_view.getAxis(side).label.toHtml()

    def _setup(self):

        self.view.invertY(False)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
