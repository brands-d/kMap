import unittest
import numpy as np
from map.model.sliceddata import SlicedData


class TestSlicedData(unittest.TestCase):
    def test_initialization(self):

        slices = np.arange(27).reshape(3, 3, 3)
        range_ = [[1, 2], [-1, 1]]
        slice_axis = [1, 2, 3]

        sliced_data = SlicedData(slices, range_, slice_axis)

        np.testing.assert_equal(
            sliced_data.slice_from_idx(1).data, slices[1])
        np.testing.assert_equal(
            sliced_data.slice_from_value(1).data, slices[0])

        range_ = [[[1, 2], [-1, 1]], [[3, 2], [-4, 3]], [[1, 3], [0, 1]]]

        sliced_data = SlicedData(slices, range_, slice_axis)

        np.testing.assert_equal(
            sliced_data.slice_from_idx(0).data, slices[0])
        np.testing.assert_equal(
            sliced_data.slice_from_value(3).data, slices[2])
        np.testing.assert_equal(
            sliced_data.slice_from_value(1).range, [[1, 2], [-1, 1]])
        np.testing.assert_equal(
            sliced_data.slice_from_value(3).range, [[1, 3], [0, 1]])


if __name__ == '__main__':
    unittest.main()
