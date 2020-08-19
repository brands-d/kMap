import numpy as np
from pyqtgraph import PlotWidget, mkPen, mkBrush
from kmap.model.profileplot_model import ProfilePlotModel


class ProfilePlot(PlotWidget):

    def __init__(self, *args, **kwargs):

        super(ProfilePlot, self).__init__(*args, **kwargs)
        self._setup()

        self.plot_item = self.getPlotItem()
        self.model = ProfilePlotModel()

    def clear(self):

        self.plot_item.clear()

    def plot(self, data, crosshair, region, phi_sample=720, line_sample=500):

        x, y = self.model.get_plot_data(
            data, crosshair, region, phi_sample, line_sample)

        self.plot_item.plot(x, y, name='Test',
                            pen=mkPen('r', width=3), symbol='+',
                            symbolPen=mkPen('r', width=1),
                            symbolBrush=mkBrush('r'))

    def _setup(self):

        # self.setLabel('left', text='Intensity (arbitrary units)')
        # self.setLabel('bottom', text='k_x / k_y', units='A^-1')
        self.addLegend()
