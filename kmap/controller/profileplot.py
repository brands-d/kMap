import numpy as np
from pyqtgraph import PlotWidget, mkPen, mkBrush
from kmap.model.profileplot_model import ProfilePlotModel
from kmap.config.config import config


class ProfilePlot(PlotWidget):

    def __init__(self, *args, **kwargs):

        super(ProfilePlot, self).__init__(*args, **kwargs)
        self._setup()

        self.plot_item = self.getPlotItem()
        self.model = ProfilePlotModel()
        self.title_suffixes = {'x': ' - Vertical Line',
                               'y': ' - Horizontal Line',
                               'roi': ' - Region of Interest',
                               'border': ' - Border of ROI',
                               'ring': ' - Annulus'}

    def clear(self):

        self.plot_item.clear()

    def plot(self, data, title, crosshair, region, phi_sample=720,
             line_sample=500, normalized=False):

        index = len(self.plot_item.listDataItems())
        colors = config.get_key('profile_plot', 'colors')
        color = colors.split(',')[index % len(colors)]
        line_width = int(config.get_key('profile_plot', 'line_width'))
        symbols = config.get_key('profile_plot', 'symbols')
        symbol = symbols.split(',')[index % len(symbols)]
        symbol_size = int(config.get_key('profile_plot', 'symbol_size'))

        x, y = self.model.get_plot_data(
            data, crosshair, region, phi_sample, line_sample)

        if normalized:
            y = y / max(y)

        self.plot_item.plot(x, y,
                            name=title + self.title_suffixes[region],
                            pen=mkPen(color, width=line_width),
                            symbol=symbol,
                            symbolPen=mkPen(color, width=symbol_size),
                            symbolBrush=mkBrush(color))

    def set_label(self, x, y):

        self.setLabel('left', text=y[0], units=y[1])
        self.setLabel('bottom', text=x[0], units=x[1])

    def _setup(self):

        self.addLegend()
