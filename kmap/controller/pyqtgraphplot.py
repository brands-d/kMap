import numpy as np

from kmap.ui.pyqtgraphplot_ui import PyQtGraphPlotUI
from kmap.model.pyqtgraphplot_model import PyQtGraphPlotModel

class PyQtGraphPlot(PyQtGraphPlotUI):

    def __init__(self, plot_data=None):

        self.model = PyQtGraphPlotModel(plot_data)

        PyQtGraphPlotUI.__init__(self)

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