import numpy as np
from pyqtgraph import PlotWidget, mkBrush, mkPen

from kmap.config.config import config
from kmap.library.misc import normalize
from kmap.library.plotdata import PlotData
from kmap.model.profileplot_model import ProfilePlotModel


class ProfilePlot(PlotWidget):
    def __init__(self, *args, **kwargs):
        super(ProfilePlot, self).__init__(*args, **kwargs)
        self._setup()

        self.plot_item = self.getPlotItem()
        self.model = ProfilePlotModel()
        self.title_suffixes = {
            "center": " - Center Point",
            "x": " - Vertical Line",
            "y": " - Horizontal Line",
            "roi": " - Region of Interest",
            "border": " - Border of ROI",
            "ring": " - Annulus",
        }

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

    def plot(
        self,
        data,
        title,
        crosshair,
        region,
        phi_sample=720,
        line_sample=500,
        normalized=False,
    ):
        index = len(self.plot_item.listDataItems())
        colors = config.get_key("profile_plot", "colors")
        color = colors.split(",")[index % len(colors)]
        line_width = int(config.get_key("profile_plot", "line_width"))
        symbols = config.get_key("profile_plot", "symbols")
        symbol = symbols.split(",")[index % len(symbols)]
        symbol_size = int(config.get_key("profile_plot", "symbol_size"))

        if data is None:
            return

        elif isinstance(data, PlotData):
            x, y = self.model.get_plot_data(
                data, crosshair, region, phi_sample, line_sample
            )
        else:
            data, axis = data
            x = np.array(data.axes[axis].axis)
            y = []
            for i in range(len(x)):
                slice_ = data.slice_from_index(i, axis=axis)
                plot_data = crosshair.cut_from_data(slice_, region=region).data

                if np.isnan(plot_data).all():
                    y.append(np.nan)

                else:
                    if config.get_key("crosshair", "normalized_intensity") == "True":
                        y.append(normalize(plot_data))

                    else:
                        y.append(np.nansum(plot_data))

            y = np.array(y)

        x = x[~np.isnan(y)]
        y = y[~np.isnan(y)]

        if normalized:
            y = y / max(y)

        self.plot_item.plot(
            x,
            y,
            name=title + self.title_suffixes[region],
            pen=mkPen(color, width=line_width),
            symbol=symbol,
            symbolPen=mkPen(color, width=symbol_size),
            symbolBrush=mkBrush(color),
        )

    def set_label(self, x, y):
        self.setLabel("left", text=y)
        self.setLabel("bottom", text=x)

    def _setup(self):
        self.addLegend()
