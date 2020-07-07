import unittest
import numpy as np
import numpy.testing
from map.model.data import PlotData, SlicedData


class TestPlotData(unittest.TestCase):
    def test_initialization(self):

        data = [[1, 2, 3], [4, 5, 6]]
        range_ = [[1, 2], [-1, 1]]

        plot_data = PlotData(data, range_)

        numpy.testing.assert_equal(plot_data.data, data)
        numpy.testing.assert_equal(plot_data.range, range_)
        numpy.testing.assert_equal(plot_data.shape, (2, 3))
        numpy.testing.assert_equal(plot_data.x_axis, [1, 2])
        numpy.testing.assert_equal(plot_data.y_axis, [-1, 0, 1])
        numpy.testing.assert_equal(plot_data.step_size, [1, 1])


class TestSlicedData(unittest.TestCase):
    def test_initialization(self):

        slices = np.arange(27).reshape(3, 3, 3)
        range_ = [[1, 2], [-1, 1]]
        slice_axis = [1, 2, 3]

        sliced_data = SlicedData(slices, range_, slice_axis)

        numpy.testing.assert_equal(
            sliced_data.slice_from_idx(1).data, slices[1])
        numpy.testing.assert_equal(
            sliced_data.slice_from_value(1).data, slices[0])


if __name__ == '__main__':
    unittest.main()
