from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.library.qwidgetsub import FixedSizeWidget


class MiniKSpacePlot(FixedSizeWidget, PyQtGraphPlot):

    def __init__(self, *args, **kwargs):

        width = 300
        self.ratio = 1
        self.ID = None

        super(MiniKSpacePlot, self).__init__(300, 1, *args, **kwargs)

    def plot(self, plot_data, ID):

        self.ID = ID

        PyQtGraphPlot.plot(self, plot_data)

    def _setup(self):

        PyQtGraphPlot._setup(self)

        self.ui.histogram.hide()
        self.view.showAxis('bottom', show=True)
        self.view.showAxis('left', show=True)
        self.view.showAxis('top', show=True)
        self.view.showAxis('right', show=True)
        self.view.setAspectLocked(lock=True, ratio=self.ratio)
