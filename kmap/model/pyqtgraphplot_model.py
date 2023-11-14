import numpy as np

from kmap.config.config import config


class PyQtGraphPlotModel:
    def __init__(self, plot_data):
        self.plot_data = plot_data

    def get_plot(self):
        image = self.plot_data.data
        scale = self.plot_data.step_size
        pixel_center = config.get_key("pyqtgraph", "pixel_center") == "True"
        pos = self._calculate_pos(scale, pixel_center=pixel_center)
        range_ = self._calculate_range(scale, pixel_center=pixel_center)

        return image, pos, scale, range_

    def _calculate_pos(self, scale, pixel_center=True):
        if pixel_center:
            pos = self.plot_data.range[:, 0] - scale / 2
        else:
            pos = self.plot_data.range[:, 0]

        return pos

    def _calculate_range(self, scale, pixel_center=True):
        old_range = self.plot_data.range

        if pixel_center:
            shift = np.array([[-1, 1], [-1, 1]]) * scale / 2
            new_range = old_range + shift

        else:
            new_range = old_range

        return new_range
