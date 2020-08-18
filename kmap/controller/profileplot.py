import numpy as np
from pyqtgraph import PlotWidget, mkPen, mkBrush
from skimage.measure import profile_line
from kmap.library.misc import profile_line_phi


class ProfilePlot(PlotWidget):

    def __init__(self, *args, **kwargs):

        super(ProfilePlot, self).__init__(*args, **kwargs)
        self._setup()

        self.plot_item = self.getPlotItem()

    def clear(self):

        self.plot_item.clear()

    def plot(self, data, crosshair, region):

        if region == 'x' or region == 'y':
            mask = crosshair.mask(data, region=region)
            x = np.flip(data.y_axis) if region == 'x' else data.x_axis
            y = data.data.flatten()[mask.flatten()]

        elif region == 'roi' or region == 'border' or region == 'ring':
            # Circular parametrization starting at top going counter
            # clockwise
            angles = np.linspace(np.pi / 2, -3 / 2 * np.pi,
                                 num=180, endpoint=False)
            x = np.linspace(0, 360, num=180, endpoint=False)
            y = []
            x_center = crosshair.x
            y_center = crosshair.y
            data = crosshair.cut_from_data(data, fill=np.nan, region=region)

            for phi in angles:
                start, end = profile_line_phi(data, phi, x_center, y_center)
                intensities = profile_line(
                    data.data, start, end, mode='nearest')
                y.append(np.nanmean(intensities))

        x, y = self._filter_nan(np.array(x), np.array(y))
        self.plot_item.plot(x, y, name='Test',
                            pen=mkPen('r', width=3), symbol='+',
                            symbolPen=mkPen('r', width=1),
                            symbolBrush=mkBrush('r'))

    def _filter_nan(self, x, y):

        mask = np.ones(x.shape, dtype=bool)

        mask[np.isnan(x)] = False
        mask[np.isnan(y)] = False

        return x[mask], y[mask]

    def _setup(self):

        # self.setLabel('left', text='Intensity (arbitrary units)')
        # self.setLabel('bottom', text='k_x / k_y', units='A^-1')
        self.addLegend()
