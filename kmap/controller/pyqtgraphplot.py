import numpy as np
from pyqtgraph import AxisItem, ImageView, PlotItem

from kmap.config.config import config
from kmap.library.axis import Axis
from kmap.model.pyqtgraphplot_model import PyQtGraphPlotModel


class PyQtGraphPlot(ImageView):
    def __init__(self, *args, plot_data=None, **kwargs):
        # Setup GUI
        self.plot_view = PlotItem()
        super(PyQtGraphPlot, self).__init__(*args, view=self.plot_view, **kwargs)
        self._setup()

        self.model = PyQtGraphPlotModel(plot_data)

        self.refresh_plot()

    def plot(self, plot_data):
        self.model.plot_data = plot_data

        self.refresh_plot()

    def refresh_plot(self, keep_max_level=False):
        self.clear()

        if self.model.plot_data is None:
            return

        image, pos, scale, range_ = self.model.get_plot()

        if np.all(np.isnan(image)) == True:
            return

        old_level = self.get_levels()

        # Plot
        self.setImage(image, autoRange=True, autoLevels=True, pos=pos, scale=scale)

        self.set_range(range_)
        ratio = (range_[1][1] - range_[1][0]) / (range_[0][1] - range_[0][0])

        if config.get_key("pyqtgraph", "fixed_ratio") == "True":
            self.set_aspect_ratio(ratio)

        else:
            self.set_aspect_ratio(None)

        if keep_max_level or config.get_key("pyqtgraph", "keep_max_level") == "True":
            levels = [np.nanmin(image.data), np.nanmax(image.data)]

            # Catch empty plots
            if old_level != (0, 1):
                levels[0] = old_level[0] if old_level[0] < levels[0] else levels[0]
                levels[1] = old_level[1] if old_level[1] > levels[1] else levels[1]

            self.set_levels(levels)

    def set_range(self, range_):
        padding = float(config.get_key("pyqtgraph", "padding"))
        self.view.setRange(
            xRange=range_[0], yRange=range_[1], update=True, padding=padding
        )

    def set_levels(self, levels):
        self.getHistogramWidget().setLevels(*levels)
        self.setHistogramRange(*levels)

    def get_levels(self):
        return self.getHistogramWidget().getLevels()

    def set_aspect_ratio(self, ratio):
        if ratio is not None:
            self.plot_view.setAspectLocked(True, ratio=ratio)

        else:
            self.plot_view.setAspectLocked(False)

    def set_labels(self, x, y):
        color = config.get_key("pyqtgraph", "axis_color")
        size = config.get_key("pyqtgraph", "axis_size")

        if isinstance(x, list):
            self.set_label("bottom", x[0], x[1], color, size)

        elif isinstance(x, Axis):
            self.set_label("bottom", x.label, x.units, color, size)

        else:
            self.set_label("bottom", str(x), None, color, size)

        if isinstance(y, list):
            self.set_label("left", y[0], y[1], color, size)

        elif isinstance(y, Axis):
            self.set_label("left", y.label, y.units, color, size)

        else:
            self.set_label("left", str(y), None, color, size)

    def set_label(self, side, label, units=None, color="k", size=1):
        axis = AxisItem(
            side, text=label, units=units, **{"color": color, "font-size": size}
        )

        if config.get_key("pyqtgraph", "show_axis_label") == "True":
            axis.showLabel(True)

        else:
            axis.showLabel(False)

        self.view.setAxisItems({side: axis})

    def get_plot_data(self):
        return self.model.plot_data

    def get_LUT(self):
        colormap = self.getHistogramWidget().gradient.colorMap()
        nPts = int(config.get_key("pyqtgraph", "nPts"))
        LUT = colormap.getLookupTable(mode="float", alpha=True, nPts=nPts)

        return LUT

    def get_colormap(self):
        return self.getHistogramWidget().gradient.colorMap()

    def set_colormap(self, colormap):
        self.getHistogramWidget().gradient.setColorMap(colormap)

    def get_label(self, side):
        return self.plot_view.getAxis(side).label.toHtml()

    def _setup(self):
        self.view.invertY(False)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
