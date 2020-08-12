from kmap.config.config import config


class PyQtGraphPlotModel():

    def __init__(self, plot_data):

        self.plot_data = plot_data

    def get_plot(self):

        image = self.plot_data.data
        scale = self.plot_data.step_size
        pos = self._calculate_pos(scale)
        x_range = [self.plot_data.x_axis[0], self.plot_data.x_axis[-1]]
        y_range = [self.plot_data.y_axis[0], self.plot_data.y_axis[-1]]
        range_ = [x_range, y_range]
        
        return image, pos, scale, range_

    def _calculate_pos(self, scale):

        pixel_center = config.get_key('pyqtgraph', 'pixel_center') == 'True'

        if pixel_center:
            pos = self.plot_data.range[:, 0] - scale / 2
        else:
            pos = self.plot_data.range[:, 0]

        return pos
