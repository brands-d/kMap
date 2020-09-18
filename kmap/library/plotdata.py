"""Defines the PlotData class.

This file defines a class named PlotData designed to be plotted in
arbitrary situations. For this purpose it holds a data matrix and axes
data as well as some other useful properties. It also comes with
interpolations methods.
"""

from numbers import Number
import numpy as np
from scipy.ndimage import gaussian_filter
import itertools as it
from scipy.interpolate import RegularGridInterpolator as RGI
from kmap.library.misc import axis_from_range


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
        self.x_axis = axis_from_range(self.range[0], self.data.shape[1])
        self.y_axis = axis_from_range(self.range[1], self.data.shape[0])

        # Set step_size
        self.step_size = np.array([self.x_axis[1] - self.x_axis[0],
                                   self.y_axis[1] - self.y_axis[0]],
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
            points = list(it.product(y_axis, x_axis))
            rgi = RGI((self.y_axis, self.x_axis), self.data,
                      bounds_error=bounds_error, *args, **kwargs)

            new_data = np.array(rgi(points), dtype=np.float64).reshape(
                len(y_axis), len(x_axis))

        else:
            NotImplementedError('Chosen interpolator is unknown')

        if update:
            self.data = new_data
            self.x_axis = x_axis
            self.y_axis = y_axis
            self.range = np.array(
                [[x_axis[0], x_axis[-1]], [y_axis[0], y_axis[-1]]])
            self.step_size = np.array(
                [abs(x_axis[1] - x_axis[0]), abs(y_axis[1] - y_axis[0])])

        return new_data

    def interpolate_points(self, x, y, interpolator='rgi',
                           bounds_error=False, *args, **kwargs):

        if interpolator == 'rgi':
            points = np.transpose([y, x])
            rgi = RGI((self.y_axis, self.x_axis), self.data,
                      bounds_error=bounds_error, *args, **kwargs)

            intensities = np.array(rgi(points), dtype=np.float64)

        else:
            NotImplementedError('Chosen interpolator is unknown')

        return intensities

    def smoothing(self, sigma_x, sigma_y, *args, mode='nearest',
                  update=False, fill_value=np.nan, **kwargs):

        # gaussian filter needs number of pixel
        sigma_x = round(sigma_x / self.step_size[0])
        sigma_y = round(sigma_y / self.step_size[1])

        fill_mask = np.zeros(self.data.shape, dtype=bool)
        fill_mask[np.isnan(self.data)] = True
        self.data[fill_mask] = fill_value

        if update:
            gaussian_filter(
                self.data, [sigma_x, sigma_y], mode=mode,
                output=self.data, **kwargs)
            self.data[fill_mask] = np.nan

            return self

        else:
            smoothed = gaussian_filter(
                self.data, [sigma_y, sigma_x], mode=mode, **kwargs)
            new_plot_data = PlotData(smoothed, self.range)
            self.data[fill_mask] = np.nan

            return new_plot_data

    def __add__(self, other):

        if isinstance(other, self.__class__):

            if ((self.x_axis == other.x_axis).all() and
                    (self.y_axis == other.y_axis).all()):
                return PlotData(self.data + other.data, self.range)

    def __sub__(self, other):

        if isinstance(other, self.__class__):
            if ((self.x_axis == other.x_axis).all() and
                    (self.y_axis == other.y_axis).all()):
                return PlotData(self.data - other.data, self.range)

        elif isinstance(other, float):

            return PlotData(self.data - other, self.range)

    def __mul__(self, other):

        if isinstance(other, float) or isinstance(other, int):

            return PlotData(self.data * other, self.range)

    def __rmul__(self, other):

        if isinstance(other, float) or isinstance(other, int):

            return PlotData(self.data * other, self.range)

    def __pow__(self):

        if isinstance(other, float) or isinstance(other, int):

            return PlotData(self.data ** 2, self.range)
