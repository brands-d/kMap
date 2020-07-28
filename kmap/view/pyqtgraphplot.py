import pyqtgraph as pg
from kmap.ui.pyqtgraphplot_ui import PyQtGraphPlotUI


class PyQtGraphPlot(pg.ImageView, PyQtGraphPlotUI):

    def __init__(self):

        self.displayed_plot_data = None

        super().__init__(view=pg.PlotItem())

        self.setupUI()

    def plot(self, plotdata, pixel_center=True):

        self.displayed_plot_data = plotdata
        image = plotdata.data
        scale = plotdata.step_size
        '''Move image position by half a step to make center of pixel
        the point specified by axis'''
        if pixel_center:
            pos = plotdata.range[:, 0] - scale / 2

        else:
            pos = plotdata.range[:, 0]

        self.clear()

        self.setImage(image, autoRange=True,
                      autoLevels=True, pos=pos, scale=scale)
