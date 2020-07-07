import unittest
import numpy as np
from map.model.data import PlotData, SlicedData


class TestPlotData(unittest.TestCase):
    def test_initialization(self):

        data = [[1, 2, 3], [4, 5, 6]]
        range_ = [[1, 2], [-1, 1]]

        plot_data = PlotData(data, range_)

        np.testing.assert_equal(plot_data.data, data)
        np.testing.assert_equal(plot_data.range, range_)
        np.testing.assert_equal(plot_data.shape, (2, 3))
        np.testing.assert_equal(plot_data.x_axis, [1, 2])
        np.testing.assert_equal(plot_data.y_axis, [-1, 0, 1])
        np.testing.assert_equal(plot_data.step_size, [1, 1])


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
