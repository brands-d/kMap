# Python Imports
import numpy as np

# Own Imports
from kmap.config.config import config


class PyQtGraphPlotModel():

    def __init__(self, plot_data):

        self.plot_data = plot_data

    def get_plot(self):

        image = self.plot_data.data
        scale = self.plot_data.step_size
        pos = self._calculate_pos(scale)
        range_ = self._calculate_range(scale)

        return image, pos, scale, range_

    def _calculate_pos(self, scale):

        pixel_center = config.get_key('pyqtgraph', 'pixel_center') == 'True'

        if pixel_center:
            pos = self.plot_data.range[:, 0] - scale / 2
        else:
            pos = self.plot_data.range[:, 0]

        return pos

    def _calculate_range(self, scale):

        pixel_center = config.get_key('pyqtgraph', 'pixel_center') == 'True'

        if pixel_center:
            old_x_range = self.plot_data.range[0, [0, -1]]
            old_y_range = self.plot_data.range[1, [0, -1]]
            x_range = old_x_range + np.array([-1, 1]) * scale[0] / 2
            y_range = old_y_range + np.array([-1, 1]) * scale[1] / 2

        else:
            x_range = self.plot_data.range[0, [0, -1]]
            y_range = self.plot_data.range[1, [0, -1]]

        return [x_range, y_range]
