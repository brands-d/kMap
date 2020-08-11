# Python Imports
import numpy as np

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# Third Party Imports
from pyqtgraph import ImageView, PlotItem

# Own Imports
from kmap.model.pyqtgraphplot_model import PyQtGraphPlotModel
from kmap.config.config import config


class PyQtGraphPlot(ImageView):

    def __init__(self, *args, plot_data=None, **kwargs):

        # Setup GUI
        super(PyQtGraphPlot, self).__init__(view=PlotItem())
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

    def get_plot_data(self):

        return self.model.plot_data

    def set_label(self, x_label, x_units, y_label, y_units):

        color = config.get_key('pyqtgraph', 'axis_color')
        size = config.get_key('pyqtgraph', '14pt')

        x_axis = pg.AxisItem('bottom', text=x_label, units=x_units,
                             **{'color': color, 'font-size': size})
        y_axis = pg.AxisItem('left', text=y_label, units=y_units,
                             **{'color': color, 'font-size': size})

        if config.get_key('pyqtgraph', 'show_axis_label') != 'True':
            x_axis.showLabel(True)
            y_axis.showLabel(True)

        else:
            x_axis.showLabel(True)
            y_axis.showLabel(True)

        self.plot_item.view.setAxisItems({'bottom': x_axis, 'left': y_axis})

    def _setup(self):

        self.view.invertY(False)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
