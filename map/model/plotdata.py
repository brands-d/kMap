"""Define the PlotData class.

This file defines a class named PlotData designed to be ploted in
arbitrary situations. For this purpose it holds a data matrix and axes
data as well as some other useful properties. It also comes with
interpolations methods.
"""

import numpy as np
import itertools as it
from scipy.interpolate import RegularGridInterpolator as RGI


class PlotData():
    """Basic data class holding necessary information for plotting.

    Defines a data class for data designed to be plotted, including
    interpolation.

    Args:
        data (float): 2D array of numbers with at least 2 elements in
            each dimension. Can contain NaN values.
        range(float): List of two lists containing the min and max value
            of x_axis and y_axis. (E.g. [[x_min, x_max],[y_min, y_max]])

    Attributes:
        data (float): See args.
        range (float): See args.
        x_axis (float): 1D array for the first axis of data.
        y_axis (float): 1D array for the first axis of data.
    """

    def __init__(self, data, range_):

        # Set data
        self.data = np.array(data, dtype=np.float64)
        if (self.data.ndim != 2 or len(self.data) < 2 or
                len(self.data[0]) < 2):
            raise TypeError('data has to be 2D array with at least 2 ' +
                            'elements in each dimension')

        else:
            self.data[~ np.isfinite(self.data)] = np.nan

        # Set range
        self.range = np.array(range_, dtype=np.float64)
        if self.range.shape != (2, 2):
            raise TypeError('range_ has to be of shape (2, 2)')

        elif not np.isfinite(range_).all():
            raise ValueError('range_ can only have finite values')

        # Set axes
        self.x_axis = self.axis_from_range(self.range[0], self.data.shape[0])
        self.y_axis = self.axis_from_range(self.range[1], self.data.shape[1])

        # Set step_size
        self.step_size = [self.x_axis[1] - self.x_axis[0],
                          self.y_axis[1] - self.y_axis[0]]

    def axis_from_range(self, range_, num):

        return np.linspace(range_[0], range_[1],
                           num=num, endpoint=True,
                           dtype=np.float64)


'''UNDER CONSTRUCTION
    def interpolate(self, x_axis, y_axis, interpolator='rgi',
                    bounds_error=False, *args, **kwargs):

        if interpolator == 'rgi':
            points = it.product(x_axis, y_axis)
            rgi = RGI((self.x_axis, self.y_axis), self.data,
                      bounds_error=bounds_error, *args, **kwargs)

            self.data = rgi(points)
            self.x_axis = x_axis
            self.y_axis = y_axis

        else:
            ValueError('Chosen interpolator is unknown')'''
