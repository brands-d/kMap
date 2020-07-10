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
