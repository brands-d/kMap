# Python Imports
import numpy as np

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# Third Party Imports
from pyqtgraph import ImageView, PlotItem

# Own Imports
from kmap.model.pyqtgraphplot_model import PyQtGraphPlotModel


class PyQtGraphPlot(ImageView):

    def __init__(self, plot_data=None):

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

    def _setup(self):

        self.view.invertY(False)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
