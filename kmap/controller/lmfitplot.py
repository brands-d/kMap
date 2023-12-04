from numpy import array
from pyqtgraph import FillBetweenItem, PlotDataItem, PlotWidget, mkBrush, mkPen

from kmap.config.config import config


class LMFitPlot(PlotWidget):
    def __init__(self, *args, **kwargs):
        super(LMFitPlot, self).__init__(*args, **kwargs)
        self._setup()

        self.plot_item = self.getPlotItem()

    def clear(self):
        self.plot_item.clear()

    def get_data(self):
        data_sets = []

        for item in self.plot_item.listDataItems():
            name = item.name()
            x, y = item.getData()
            color = item.opts["pen"].color().getRgb()
            marker_size = item.opts["symbolSize"]
            marker = item.opts["symbol"]
            linewidth = item.opts["pen"].width()
            data_sets.append(
                {
                    "name": name,
                    "x": x,
                    "y": y,
                    "color": color,
                    "marker": marker,
                    "line width": linewidth,
                    "marker size": marker_size,
                }
            )

        return data_sets

    def plot(self, x, y, title):
        index = len(self.plot_item.listDataItems())
        colors = config.get_key("profile_plot", "colors")
        transparency = config.get_key("profile_plot", "transparency")
        colors = colors.split(",")
        color = colors[index % len(colors)]
        line_width = int(config.get_key("profile_plot", "line_width"))
        symbols = config.get_key("profile_plot", "symbols")
        symbols = symbols.split(",")
        symbol = symbols[index % len(symbols)]
        symbol_size = int(config.get_key("profile_plot", "symbol_size"))

        stderr = array([aux.stderr for aux in y])
        y = array([aux.value for aux in y])

        band = FillBetweenItem(
            PlotDataItem(x, y + stderr),
            PlotDataItem(x, y - stderr),
            brush=mkBrush(color + transparency),
        )
        self.plot_item.addItem(band)
        self.plot_item.plot(
            x,
            y,
            name=title,
            pen=mkPen(color, width=line_width),
            symbol=symbol,
            symbolPen=mkPen(color, width=symbol_size),
            symbolBrush=mkBrush(color),
        )

    def set_label(self, x, y):
        self.setLabel("left", text=y)
        self.setLabel("bottom", text=x)

    def _setup(self):
        pass
        self.addLegend()
