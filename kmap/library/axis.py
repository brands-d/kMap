import numpy as np

from kmap.library.misc import axis_from_range


class Axis:
    def __init__(self, label, units, range_, num):
        self.label = label
        self.units = units
        self.range = range_
        self.axis = axis_from_range(range_, num)
        self.stepsize = abs(self.axis[1] - self.axis[0])
        self.num = len(self.axis)

    @classmethod
    def init_from_hdf_list(cls, axis, num):
        if Axis._is_correct_axis(axis):
            return cls(*axis, num)

    @classmethod
    def _is_correct_axis(self, axis):
        if not isinstance(axis, list) or len(axis) != 3:
            raise ValueError("axis has to be a list of length 3")

        label, units, range_ = axis
        if not isinstance(label, str) or not label:
            raise ValueError("axis label has to be a non empty string")

        if not isinstance(units, str) or not units:
            raise ValueError("axis units has to be a non empty string")

        if len(range_) != 2:
            raise ValueError("axis range has to be list of length 2")

        minimum, maximum = range_
        if not np.isfinite(minimum) or not np.isfinite(maximum):
            raise ValueError("axis range can not contain inf or nan values")

        if not minimum < maximum:
            raise ValueError("axis minimum has to strictly smaller than maxmimum")

        return True

    def __str__(self):
        rep = f"Label:\t{self.label}\nUnits:\t{self.units}\nRange:\t[{self.range[0]:.3f}, {self.range[1]:.3f}]"
        return rep

    def sublist(self, indices):
        num = len(indices)
        units = self.units
        label = self.label
        range_ = [self.axis[indices[0]], self.axis[indices[-1]]]

        subaxis = Axis(label, units, range_, num)

        return subaxis
