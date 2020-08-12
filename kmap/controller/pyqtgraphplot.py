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
        self.plt = PlotItem()       
        super(PyQtGraphPlot, self).__init__(view=self.plt)
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

        image, pos, scale = self.model.get_plot()

        if np.all(np.isnan(image)) == True:
            return

        self.setImage(image, autoRange=True,
                      autoLevels=True, pos=pos, scale=scale)

        self.plt.setAspectLocked(False)   # pep: for testing only !!!

    def get_plot_data(self):

        return self.model.plot_data

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

    def _setup(self):

        self.view.invertY(False)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
