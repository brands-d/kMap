"""Defines classes related to holding data.

This file defines multiple classes related to data to be used in Map.py
of various sorts and origins. This includes basic PlotData as well as
higher-level ExpData.
"""

import numpy as np


class PlotData():
    """Basic data class holding necessary information for plotting.

    Defines a bare-bones data class for data designed to be plotted.

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

        self.data = np.array(data, dtype=np.float64)
        self.range = range_

        self.shape = self.data.shape

        self.x_axis = np.linspace(range_[0][0], range_[0][1],
                                  num=self.shape[0], endpoint=True,
                                  dtype=np.float64)
        self.y_axis = np.linspace(range_[1][0], range_[1][1],
                                  num=self.shape[1], endpoint=True,
                                  dtype=np.float64)
        self.step_size = [self.x_axis[1] - self.x_axis[0],
                          self.y_axis[1] - self.y_axis[0]]


class SlicedData():

    def __init__(self, slices, ranges, slice_axis):

        # Test for uniqueness in the slice_axis key list
        if len(slice_axis) > len(set(slice_axis)):
            raise ValueError('slice_axis has to have only unique values')

        # Test if slice_axis matches slices
        elif len(slice_axis) != len(slices):
            raise TypeError('slice_axis has to be the same length as slices')

        else:
            self.slice_axis = slice_axis

        # If only one range is supplied, it applies to all slices
        if len(np.array(ranges).shape) == 2:
            self._slices = [PlotData(slice_, ranges) for slice_ in slices]

        # Each slices has its own range
        elif len(ranges) == len(slices):
            self._slices = [PlotData(slice_, range_)
                            for slice_, range_ in zip(slices, ranges)]
        else:
            raise TypeError(
                'range_ needs to be specified either once for all or for all \
                slices individually')

    def slice_from_idx(self, idx):

        return self._slices[idx]

    def slice_from_value(self, value):

        for idx, key in enumerate(self.slice_axis):
            if key == value:
                return self._slices[idx]

        return None
