from kmap.config.config import config


class PyQtGraphPlotModel():

    def __init__(self, plot_data):

        self.plot_data = plot_data

    def get_plot(self):

        image = self.plot_data.data
        scale = self.plot_data.step_size
        pos = self._calculate_pos(scale)

        return image, pos, scale

    def _calculate_pos(self, scale):

        pixel_center = config.get_key('pyqtgraph', 'pixel_center') == 'True'

        if pixel_center:
            pos = self.plot_data.range[:, 0] - scale / 2
        else:
            pos = self.plot_data.range[:, 0]
