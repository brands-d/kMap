"""Defines the PlotData class.

This file defines a class named PlotData designed to hold arbitrary
image-like. For this purpose it holds a data matrix and axes data as
well as some other useful properties. It also comes with interpolations 
and Gaussian filter methods.
"""

import itertools as it
from numbers import Number

import numpy as np
from scipy.interpolate import RegularGridInterpolator as RGI
from scipy.ndimage import gaussian_filter, rotate

from kmap.library.misc import axis_from_range, range_from_axes


class PlotData:
    """
    Basic data class holding necessary information for plotting.

    Defines a data class for data designed to be plotted, including
    interpolation and smoothing.
    """

    def __init__(self, data, range_):
        """
        Args:
            data (float): 2D array of numbers with at least 2 elements
                in each dimension. Can contain NaN values.
            range_ (float): List of two lists containing the min and max
                value of x_axis and y_axis respectively. Can not contain
                NaN values and min value as to be strictly smaller than
                max value. (e.g. [[x_min, x_max], [y_min, y_max]])

        Public Attributes:
            data (float): See args.
            range (float): See args.
            x_axis (float): 1D array for the first axis of the data.
            y_axis (float): 1D array for the second axis of the data.
            step_size (float) : List of step sizes for each axes.
        """

        # Set data
        self.data = np.array(data, dtype=np.float64)

        if self.data.ndim != 2 or len(self.data) < 2 or len(self.data[0]) < 2:
            raise TypeError(
                "data has to be 2D array with at least 2 "
                + "elements in each dimension"
            )

        else:
            self.data[~np.isfinite(self.data)] = np.nan

        # Set range
        self.range = np.array(range_, dtype=np.float64)

        if self.range.shape != (2, 2):
            raise TypeError("range has to be of shape (2, 2)")

        if not np.isfinite(self.range).all():
            raise ValueError("range can only have finite values")

        # Set axes
        self.x_axis = axis_from_range(self.range[0], self.data.shape[1])
        self.y_axis = axis_from_range(self.range[1], self.data.shape[0])

        # Set step_size
        _, self.step_size = range_from_axes(self.x_axis, self.y_axis)

    def interpolate(self, x_axis, y_axis, update=False, **kwargs):
        """Wrapper method to interpolate data at entire grid specified
            by the axes passed.

        Args:
            x_axis (float): Same es as constructor.
            y_axis (float): Same es as constructor.
            update (bool): If True data and axis saved in this instance
                will be overriden with interpolation result. If False
                interpolate will only return the result but data will
                stay unchanged.
            **kwargs: See interpolate_points.

        Returns:
            (PlotData): PlotData object with the interpolated data.
        """

        points = np.array(list(it.product(y_axis, x_axis)))
        new_data = self.interpolate_points(points[:, 1], points[:, 0], **kwargs)
        new_data = np.array(new_data, dtype=np.float64).reshape(
            len(y_axis), len(x_axis)
        )

        if update:
            self.data, self.x_axis, self.y_axis = new_data, x_axis, y_axis
            self.range, self.step_size = range_from_axes(x_axis, y_axis)

            return self

        else:
            range_, _ = range_from_axes(x_axis, y_axis)
            new_plot_data = PlotData(new_data, range_)

            return new_plot_data

    def interpolate_points(
        self, x, y, interpolator="rgi", bounds_error=False, **kwargs
    ):
        """Interpolates the current data at the points
            [(x_1,y_1), (x_2,y_2),...].

        Args:
            x_axis (float): Same es as constructor.
            y_axis (float): Same es as constructor.
            interpolator (string): Specifies the underlying
                interpolation method to be used. Currently available:
                    rgi - RegularGridInterpolator from SciPy
            bounds_error (bool): If True interpolating outside current
                range will result in an error. If False data points
                outside will be filled with np.nan.
            **kwargs: Will be passed to the interpolation
                method, thus pass any arguments the chosen interpolation
                accepts.

        Returns:
            (float): List of data interpolated at the specified points.

        """

        if interpolator == "rgi":
            points = np.transpose([y, x])
            rgi = RGI(
                (self.y_axis, self.x_axis),
                self.data,
                bounds_error=bounds_error,
                **kwargs
            )

            intensities = np.array(rgi(points), dtype=np.float64)

        else:
            NotImplementedError("Chosen interpolator is unknown")

        return intensities

    def symmetrise(self, symmetry="no", mirror=False, update=False):
        """Symmetrises the data set. Optional mirroring available.

        Args:
            symmetry (str): '2-fold', '3-fold', '4-fold' or 'no'.
            mirror (bool): Whether the data gets mirrored as well. Along first
                axis for 2- and 3-fold and along first and second axis for 4-
                fold symmetry.
            update (bool): If True data in this instance
                will be overriden with symmetrised result. If False
                this function will only return the result but data will
                stay unchanged.

        Returns:
            (PlotData): PlotData object with the symmetrised data.

        """

        new_data = self.data

        if symmetry == "2-fold":
            new_data += rotate(np.nan_to_num(new_data), 180, reshape=False)

            if mirror:
                new_data += np.flip(new_data, 0)
                new_data /= 2

            new_data /= 2

        elif symmetry == "3-fold":
            aux_1 = rotate(np.nan_to_num(new_data), 120, reshape=False)
            aux_2 = rotate(np.nan_to_num(new_data), 240, reshape=False)
            new_data += aux_1 + aux_2

            if mirror:
                new_data += np.flip(new_data, 0)
                new_data /= 2

            new_data /= 3

        elif symmetry == "4-fold":
            aux_1 = rotate(np.nan_to_num(new_data), 90, reshape=False)
            aux_2 = rotate(np.nan_to_num(new_data), 180, reshape=False)
            aux_3 = rotate(np.nan_to_num(new_data), 270, reshape=False)
            new_data += aux_1 + aux_2 + aux_3

            if mirror:
                new_data += np.flip(new_data, 0)
                new_data += np.flip(new_data, 1)
                new_data /= 2

            new_data /= 4

        if update:
            self.data = new_data

            return self

        else:
            new_plot_data = PlotData(new_data, self.range)

            return new_plot_data

    def smooth(
        self,
        sigma_x,
        sigma_y,
        mode="nearest",
        update=False,
        fill_value=np.nan,
        **kwargs
    ):
        """Applies a 2D Gaussian filter to the current data. Wrapper
            method for the "gaussian_filter" method from them
            "scipy.ndimage" module.

        Args:
            sigma_x (float): See scipy.ndimage.gaussian_filter
                documentation.
            sigma_y (float): See scipy.ndimage.gaussian_filter
                documentation.
            mode (string): See scipy.ndimage.gaussian_filter
                documentation. Changed default to "nearest".
            update (bool): If True data and axis saved in this instance
                will be overriden with smoothing result. If False
                smoothing will only return the result but data will
                stay unchanged.
            fill_value (float): All NaN values in the data will be
                temporarily filled with value specified in "fill_value"
                for the smoothing procedure. (This can be necessary
                since NaN values will "infect" other values around it
                during smoothing)
            **kwargs: See scipy.ndimage.gaussian_filter

        Returns:
            (PlotData): PlotData object with the smoothed data.

        """

        # Gaussian filter needs number of pixel
        sigma_x = round(sigma_x / self.step_size[0])
        sigma_y = round(sigma_y / self.step_size[1])

        fill_mask = np.zeros(self.data.shape, dtype=bool)
        fill_mask[np.isnan(self.data)] = True
        self.data[fill_mask] = fill_value

        new_data = gaussian_filter(self.data, [sigma_y, sigma_x], mode=mode, **kwargs)
        new_data[fill_mask] = np.nan

        if update:
            self.data = new_data

            return self

        else:
            new_plot_data = PlotData(new_data, self.range)

            return new_plot_data

    def copy(self):
        data = self.data.copy()
        range_ = self.range.copy()
        return PlotData(data, range_)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if (self.x_axis == other.x_axis).all() and (
                self.y_axis == other.y_axis
            ).all():
                return PlotData(self.data + other.data, self.range)

            else:
                raise ValueError("Axes need to be equal")

        elif isinstance(other, np.ndarray):
            return PlotData(self.data + other, self.range)

        elif isinstance(other, float) or isinstance(other, int):
            return PlotData(self.data + other, self.range)

        else:
            raise TypeError("Can not add '%s' to PlotData" % other.__class__)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            if (self.x_axis == other.x_axis).all() and (
                self.y_axis == other.y_axis
            ).all():
                return PlotData(self.data - other.data, self.range)

            else:
                raise ValueError("Axes need to be equal")

        elif isinstance(other, np.ndarray):
            return PlotData(self.data - other, self.range)

        elif isinstance(other, float) or isinstance(other, int):
            return PlotData(self.data - other, self.range)

        else:
            raise TypeError("Can not subtract '%s' to PlotData" % other.__class__)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            if (self.x_axis == other.x_axis).all() and (
                self.y_axis == other.y_axis
            ).all():
                return PlotData(self.data * other.data, self.range)

            else:
                raise ValueError("Axes need to be equal")

        elif isinstance(other, float) or isinstance(other, int):
            return PlotData(self.data * other, self.range)

        else:
            raise TypeError("Can not multiply '%s' to PlotData" % other.__class__)

    def __rmul__(self, other):
        if isinstance(other, self.__class__):
            if (self.x_axis == other.x_axis).all() and (
                self.y_axis == other.y_axis
            ).all():
                return PlotData(self.data * other.data, self.range)

            else:
                raise ValueError("Axes need to be equal")

        elif isinstance(other, float) or isinstance(other, int):
            return PlotData(self.data * other, self.range)

        else:
            raise TypeError("Can not multiply '%s' to PlotData" % other.__class__)

    def __pow__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return PlotData(self.data * self.data, self.range)

        else:
            raise TypeError("Can take PlotData to the power of '%s'" % other.__class__)
