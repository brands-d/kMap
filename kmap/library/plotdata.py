"""Defines the PlotData class.

This file defines a class named PlotData designed to be plotted in
arbitrary situations. For this purpose it holds a data matrix and axes
data as well as some other useful properties. It also comes with
interpolations methods.
"""

from numbers import Number
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
        range_ (float): List of two lists containing the min and max
            value of x_axis and y_axis.

    Attributes:
        data (float): See args.
        range (float): See args.
        x_axis (float): 1D array for the first axis of the data.
        y_axis (float): 1D array for the second axis of the data.
        step_size (float) : List of step sizes for each axes.
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
        self.step_size = np.array([self.x_axis[1] - self.x_axis[0],
                                   self.y_axis[1] - self.y_axis[0]],
                                  dtype=np.float64)

    def axis_from_range(self, range_, num):
        """Calculates a full 1D axis from range values and number of
        elements. Result can be used for interpolation method.

        Args:
            range_ (float): 1D list with min and max value (inclusive).
            num (int): Number of points.

        Returns:
            (float): 1D np.array containing the resulting axis.

        """

        return np.linspace(range_[0], range_[1],
                           num=num, endpoint=True,
                           dtype=np.float64)

    def interpolate(self, x_axis, y_axis, interpolator='rgi',
                    bounds_error=False, update=False, *args, **kwargs):
        """Interpolates the current data to the new axes specificied.

        Args:
            x_axis (float): Same es as constructor.
            y_axis (float): Same es as constructor.
            interpolator (string): Specifies the underlying
                interpolation method to be used. Currently available:
                    rgi - RegularGridInterpolator from SciPy
            bounds_error (bool): If True interpolating outside current
                range will result in an error. If False data points
                outside will be filled with np.nan.
            update (bool): If True data and axis saved in this instance
                will be overriden with interpolation result. If False
                interpolate will only return the result but data will
                stay unchanged.
            *args & **kwargs: Will be passed to the interpolation
                method, thus pass any arguments the chosen interpolation
                accepts.

        Returns:
            (float): 2D np.array containing the result of the
                interpolation.

        """
        if interpolator == 'rgi':
            points = list(it.product(x_axis, y_axis))
            rgi = RGI((self.x_axis, self.y_axis), self.data,
                      bounds_error=bounds_error, *args, **kwargs)

            new_data = np.array(rgi(points), dtype=np.float64).reshape(
                len(x_axis), len(y_axis))

        else:
            ValueError('Chosen interpolator is unknown')

        if update:
            self.data = new_data
            self.x_axis = x_axis
            self.y_axis = y_axis

        return new_data

    def __add__(self, other):

        if isinstance(other, self.__class__):

            if ((self.x_axis == other.x_axis).all() and
                    (self.y_axis == other.y_axis).all()):
                return PlotData(self.data + other.data, self.range)

    def __mul__(self, other):

        if isinstance(other, float) or isinstance(other, int):

            return PlotData(self.data * other, self.range)

    def __rmul__(self, other):

        if isinstance(other, float) or isinstance(other, int):

            return PlotData(self.data * other, self.range)

    def __pow__(self):

        if isinstance(other, float) or isinstance(other, int):

            return PlotData(self.data ** 2, self.range)
