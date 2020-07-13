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

    def cut_from_data(self, plotdata, fill=np.nan, *args, **kwargs):

        mask = self.mask(plotdata, *args, **kwargs)
        cut_data = np.copy(plotdata.data)
        cut_data[~mask] = fill

        return cut_data


class CrosshairWithROI(Crosshair):

    def __init__(self, x=0, y=0, radius=0):

        if not np.isfinite(radius) or not radius >= 0:
            raise ValueError('radius has to be positive finite')
        else:
            self.radius = radius

        super().__init__(x, y)

    def set_radius(self, radius):

        if not np.isfinite(radius) or not radius >= 0:
            raise ValueError('radius has to be positive finite')
        else:
            self.radius = radius

    def mask(self, plotdata, region='center', inverted=False):

        if region in ['center', 'x', 'y']:
            mask = super().mask(plotdata, region=region, inverted=inverted)

        else:
            # Mesgrid of axis values shifted by center
            X = np.copy(plotdata.x_axis).reshape(
                len(plotdata.x_axis), 1) - self.x
            Y = np.copy(plotdata.y_axis).reshape(
                1, len(plotdata.y_axis)) - self.y

            # Calculate distance from center for all values
            dist_from_center = np.sqrt(X**2 + Y**2)
            if region == 'roi':
                mask = np.array(dist_from_center < self.radius, dtype=np.bool)

            # region == 'border'
            else:
                '''"Pixel" is on the border if the border radius lies
                inside (strictly) the pixels max and min radius'''

                epsilon = plotdata.step_size / 2

                sign_x = np.sign(X)
                sign_y = np.sign(Y)
                lower_bound = np.sqrt(
                    (X - sign_x * epsilon[0])**2 +
                    (Y - sign_y * epsilon[1])**2)

                sign_x[sign_x == 0] = 1
                sign_y[sign_y == 0] = 1
                upper_bound = np.sqrt(
                    (X + sign_x * epsilon[0])**2 +
                    (Y + sign_y * epsilon[1])**2)

                mask = np.array(
                    (lower_bound < self.radius) & (
                        self.radius < upper_bound),
                    dtype=np.bool)

            if inverted:
                mask = ~mask

        return mask
