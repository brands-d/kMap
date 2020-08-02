from pyqtgraph import ImageView, PlotItem
from kmap.ui.abstract_ui import AbstractUI


class PyQtGraphPlotUI(AbstractUI, ImageView):

    def __init__(self):

        super().__init__(view=PlotItem())
        '''
        ImageView.__init__(self, view=PlotItem())
        AbstractUI.__init__(self)
        '''

    def _initialize_misc(self):

        self.view.invertY(False)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
