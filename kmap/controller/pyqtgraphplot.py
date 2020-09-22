# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# Third Party Imports
import numpy as np
from pyqtgraph import ImageView, PlotItem, AxisItem

# Own Imports
from kmap.model.pyqtgraphplot_model import PyQtGraphPlotModel
from kmap.library.axis import Axis
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

        self.set_range(range_)
        ratio = (range_[1][1] - range_[1][0]) / (range_[0][1] - range_[0][0])

        if config.get_key('pyqtgraph', 'fixed_ratio') == 'True':
            self.set_aspect_ratio(ratio)

        else:
            self.set_aspect_ratio(None)

    def set_range(self, range_):

        padding = float(config.get_key('pyqtgraph', 'padding'))
        self.view.setRange(xRange=range_[0], yRange=range_[1],
                           update=True, padding=padding)

    def set_levels(self, levels):

        self.getHistogramWidget().setLevels(levels[0], levels[1])

    def set_aspect_ratio(self, ratio):

        if ratio is not None:
            self.plot_view.setAspectLocked(True, ratio=ratio)

        else:
            self.plot_view.setAspectLocked(False)

    def set_labels(self, x, y):

        color = config.get_key('pyqtgraph', 'axis_color')
        size = config.get_key('pyqtgraph', 'axis_size')

        if isinstance(x, list):
            self.set_label('bottom', x[0], x[1], color, size)

        elif isinstance(x, Axis):
            self.set_label('bottom', x.label, x.units, color, size)

        else:
            self.set_label('bottom', str(x), None, color, size)

        if isinstance(y, list):
            self.set_label('left', y[0], y[1], color, size)

        elif isinstance(y, Axis):
            self.set_label('left', y.label, y.units, color, size)

        else:
            self.set_label('left', str(y), None, color, size)

    def set_label(self, side, label, units=None, color='k', size=1):

        axis = AxisItem(side, text=label, units=units,
                        **{'color': color, 'font-size': size})

        if config.get_key('pyqtgraph', 'show_axis_label') == 'True':
            axis.showLabel(True)

        else:
            axis.showLabel(False)

        self.view.setAxisItems({side: axis})

    def get_plot_data(self):

        return self.model.plot_data

    def get_LUT(self):

        colormap = self.getHistogramWidget().gradient.colorMap()
        LUT = colormap.getLookupTable(mode='float', alpha=False, nPts=100)

        return LUT[1:]

    def get_label(self, side):

        return self.plot_view.getAxis(side).label.toHtml()

    def _setup(self):

        self.view.invertY(False)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
