"""Defines the crosshair class.

This file defines a class named crosshair to be the model side of the
crosshair. Addtitionally to a bare bones crosshair class, there is also
a corsshair class including a ROI and a ROI-annulus.
"""

import numpy as np
from map.library.library import idx_closest_value


class Crosshair():

    def __init__(self, x=0, y=0):

        self.x = x
        self.y = y

    def set_position(self, x=None, y=None):

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

    def mask(self, plotdata, region='center', inverted=False):

        mask = np.zeros(plotdata.data.shape)
        x_idx = idx_closest_value(plotdata.x_axis, self.x)
        y_idx = idx_closest_value(plotdata.y_axis, self.y)

        if region == 'center':
            if x_idx is not None and y_idx is not None:
                mask[x_idx, y_idx] = 1

        elif region == 'x':
            if x_idx is not None:
                mask[x_idx, :] = 1

        elif region == 'y':
            if y_idx is not None:
                mask[:, y_idx] = 1

        mask = mask.astype(np.bool, copy=False)

        if inverted:
            return ~mask

        else:
            return mask

    def cut_from_data(self, plotdata, region='center', inverted=False,
                      fill=np.nan):

        mask = self.mask(plotdata, region=region, inverted=inverted)
        cut_data = np.copy(plotdata.data)
        cut_data[~mask] = fill

        return cut_data
