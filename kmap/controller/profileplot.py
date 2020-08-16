from pyqtgraph import PlotWidget


class ProfilePlot(PlotWidget):

    def __init__(self, *args, **kwargs):

        super(ProfilePlot, self).__init__(*args, **kwargs)
        self._setup()

    def plot(self, x, y):

        self.clear()

        super().plot(x, y)

    def _setup(self):

        pass
        #self.profilePlot.setLabel('left', text='Intensity (arbitrary units)')
        #self.profilePlot.setLabel('bottom', text='k_x / k_y', units='A^-1')
        # self.profilePlot.addLegend()
