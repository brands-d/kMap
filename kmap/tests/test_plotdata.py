"""Unittests for the PlotData class.
"""

# Python Imports
import unittest

# Third Party Imports
import numpy as np
import numpy.testing as npt

# Own Imports
from kmap.library.plotdata import PlotData


class TestPlotData(unittest.TestCase):

    def setUp(self):

        self.data = [[1, 2, 3], [4, 5, 6]]
        self.range_ = [[1, 2], [-1, 1]]
        self.plot_data = PlotData(self.data, self.range_)

    def test_correct_initialization(self):

        npt.assert_equal(self.plot_data.data, self.data)
        npt.assert_equal(self.plot_data.range, self.range_)
        npt.assert_equal(self.plot_data.data.shape, (2, 3))
        npt.assert_equal(self.plot_data.x_axis, [1., 1.5, 2.])
        npt.assert_equal(self.plot_data.y_axis, [-1., 1.])
        npt.assert_equal(self.plot_data.step_size, [0.5, 2.])

        self.data = [[1, 2, np.nan], [4, np.inf, 6]]
        plot_data = PlotData(self.data, self.range_)

        npt.assert_equal(
            plot_data.data, [[1, 2, np.nan], [4, np.nan, 6]])

    def test_incorrect_data_shape(self):

        self.data = [1, 2, 3, 4, 5, 6]
        self.assertRaises(TypeError, PlotData, self.data, self.range_)

    def test_too_small_data(self):

        self.data = [[1], [2]]
        self.assertRaises(TypeError, PlotData, self.data, self.range_)

    def test_incorrect_range_shape(self):

        self.range_ = [[1, 2]]
        self.assertRaises(TypeError, PlotData, self.data, self.range_)

    def test_incorrect_range_values(self):

        self.range_ = [[1, 2], [np.nan, 1]]
        self.assertRaises(ValueError, PlotData, self.data, self.range_)

        self.range_ = [[1, 2], [np.inf, 1]]
        self.assertRaises(ValueError, PlotData, self.data, self.range_)

    def test_basic_interpolation(self):

        new_x_axis = [1.5, 2]
        new_y_axis = [-0.5, 0, 0.5]
        new_data = self.plot_data.interpolate(new_x_axis, new_y_axis)
        npt.assert_equal(
            new_data.data, [[2.75, 3.75], [3.5, 4.5], [4.25, 5.25]])
        npt.assert_equal(self.plot_data.data, self.data)

        new_x_axis = [-2, 1]
        new_y_axis = [0, -0.5, -10]
        new_data = self.plot_data.interpolate(new_x_axis, new_y_axis)
        npt.assert_equal(
            new_data.data, [[np.nan, 2.5], [np.nan, 1.75], [np.nan, np.nan]])

        new_x_axis = [1, 1.25, 1.5, 2]
        new_y_axis = [-1, -0.25, 0.5, 1]
        new_data = self.plot_data.interpolate(new_x_axis, new_y_axis)
        npt.assert_equal(
            new_data.data, [[1., 1.5, 2., 3.],
                            [2.125, 2.625, 3.125, 4.125],
                            [3.25, 3.75, 4.25, 5.25],
                            [4., 4.5, 5., 6.]])

    def test_update_interpolation(self):

        new_x_axis = [1.5, 2]
        new_y_axis = [-0.5, 0, 0.5]
        new_data = self.plot_data.interpolate(
            new_x_axis, new_y_axis, update=True)
        npt.assert_equal(
            new_data.data, [[2.75, 3.75], [3.5, 4.5], [4.25, 5.25]])
        npt.assert_equal(self.plot_data.data, [
                         [2.75, 3.75], [3.5, 4.5], [4.25, 5.25]])

    def test_increase_range(self):

        new_x_axis = [0, 1, 2, 3]
        new_y_axis = [-1, 0, 1, 2]
        new_data = self.plot_data.interpolate(
            new_x_axis, new_y_axis, update=True)
        npt.assert_equal(new_data.data, [[np.nan, 1., 3., np.nan],
                                         [np.nan, 2.5, 4.5, np.nan],
                                         [np.nan, 4., 6., np.nan],
                                         [np.nan, np.nan, np.nan, np.nan]])
        npt.assert_equal(self.plot_data.x_axis, [0, 1, 2, 3])
        npt.assert_equal(self.plot_data.y_axis, [-1, 0, 1, 2])

    def test_add(self):

        data = [[7, 8, 9], [10, 11, 12]]
        range_ = [[1, 2], [-1, 1]]

        second_plot_data = PlotData(data, range_)

        added_plot_data = self.plot_data + second_plot_data
        npt.assert_equal(added_plot_data.data, [[8, 10, 12], [14, 16, 18]])

        added_plot_data = self.plot_data + 4
        npt.assert_equal(added_plot_data.data, [[5, 6, 7], [8, 9, 10]])

    def test_incorrect_add(self):

        data = [[7, 8, 9], [10, 11, 12]]
        range_ = [[1, 3], [-1, 1]]

        second_plot_data = PlotData(data, range_)

        self.assertRaises(ValueError, self.plot_data.__add__, second_plot_data)
        self.assertRaises(TypeError, self.plot_data.__add__, 'string')

    def test_sub(self):

        data = [[7, 8, 9], [10, 11, 12]]
        range_ = [[1, 2], [-1, 1]]

        second_plot_data = PlotData(data, range_)

        subed_plot_data = self.plot_data - second_plot_data
        npt.assert_equal(subed_plot_data.data, [[-6, -6, -6], [-6, -6, -6]])

        subed_plot_data = self.plot_data - np.array(data)
        npt.assert_equal(subed_plot_data.data, [[-6, -6, -6], [-6, -6, -6]])

        subed_plot_data = self.plot_data - 4
        npt.assert_equal(subed_plot_data.data, [[-3, -2, -1], [0, 1, 2]])

    def test_incorrect_sub(self):

        data = [[7, 8, 9], [10, 11, 12]]
        range_ = [[1, 3], [-1, 1]]

        second_plot_data = PlotData(data, range_)

        self.assertRaises(ValueError, self.plot_data.__sub__, second_plot_data)
        self.assertRaises(TypeError, self.plot_data.__sub__, 'string')

    def test_mul(self):

        data = [[2, 2, 2], [3, 3, 3]]
        range_ = [[1, 2], [-1, 1]]

        second_plot_data = PlotData(data, range_)

        mul_plot_data = self.plot_data * second_plot_data
        npt.assert_equal(mul_plot_data.data, [[2, 4, 6], [12, 15, 18]])

        mul_plot_data = second_plot_data * self.plot_data
        npt.assert_equal(mul_plot_data.data, [[2, 4, 6], [12, 15, 18]])

        mul_plot_data = self.plot_data * 4
        npt.assert_equal(mul_plot_data.data, [[4, 8, 12], [16, 20, 24]])

    def test_incorrect_mul(self):

        data = [[7, 8, 9], [10, 11, 12]]
        range_ = [[1, 3], [-1, 1]]

        second_plot_data = PlotData(data, range_)

        self.assertRaises(ValueError, self.plot_data.__mul__, second_plot_data)
        self.assertRaises(TypeError, self.plot_data.__mul__, 'string')
        self.assertRaises(
            ValueError, self.plot_data.__rmul__, second_plot_data)
        self.assertRaises(TypeError, self.plot_data.__rmul__, 'string')

    def test_pow(self):

        pow_plot_data = self.plot_data ** 2
        npt.assert_equal(pow_plot_data.data, [[1, 4, 9], [16, 25, 36]])


if __name__ == '__main__':
    unittest.main()
