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
        x_axis (float): 1D array of numbers. Cannot contain NaN values.
            Has to have the same length as the first dimension of data.
        y_axis (float): 1D array of numbers. Cannot contain NaN values.
            Has to have the same length as the second dimension of data.

    Attributes:
        data (float): See Args.
        x_axis (float): See Args.
        y_axis (float): See Args.
        range(float): List of two lists containing the min and max value
            of x_axis and y_axis. (E.g. [[x_min, x_max],[y_min, y_max]])
        step_size(float): Contains the 

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
