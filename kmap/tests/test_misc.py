"""Unittests for the methods in the misc.py file.
"""

# Python Imports
import unittest

# Third Party Imports
import numpy.testing as npt

# Own Imports
from kmap.library.misc import *


class TestMisc(unittest.TestCase):

    def test_round_to(self):

        self.assertEqual(round_to(2, 0.25), 2)
        self.assertEqual(round_to(2.2, 0.25), 2.25)
        self.assertEqual(round_to(-1.1, 0.25), -1)

    def test_idx_closest_value(self):

        axis = [-1.73, -1.33, -0.93]

        value = -1.73
        self.assertEqual(idx_closest_value(axis, value), 0)

        value = -1.63
        self.assertEqual(idx_closest_value(axis, value), 0)

        value = 1.73
        self.assertEqual(idx_closest_value(axis, value), None)

        value = 1.73
        self.assertEqual(idx_closest_value(axis, value, bounds_error=False), 2)

        value = -1.94
        self.assertEqual(idx_closest_value(axis, value), None)

        value = -1.94
        self.assertEqual(idx_closest_value(axis, value, bounds_error=False), 0)

        value = -1.23
        self.assertEqual(idx_closest_value(axis, value), 1)

    def test_centered_meshgrid(self):

        x = np.array([1, 2, 3])
        y = np.array([-1, 0, 1])
        expected = ([[-1, 0, 1]], [[-1], [0], [1]])

        npt.assert_equal(centered_meshgrid(x, 2, y, 0), expected)

    def distance_in_meshgrid(self):

        X, Y = [[-1, 0, 1]], [[-1], [0], [1]]
        sqrt2 = np.sqrt(2)
        expected = [[sqrt2, 1, sqrt2], [1, 0, 1], [sqrt2, 1, sqrt2]]

        npt.assert_almost_equal(distance_in_meshgrid(X, Y), expected)

    def test_normalize(self):

        data = [1, 2, 3]

        self.assertEqual(normalize(data), 2)

    def test_axis_from_range(self):

        npt.assert_equal(axis_from_range([1, 2], 3), [1, 1.5, 2])

    def test_range_from_axes(self):

        x = [-1, 0, 1]
        y = [0, 2, 4]
        expected_ranges = [[-1, 1], [0, 4]]
        expected_step_sizes = [1, 2]

        npt.assert_equal(range_from_axes(x, y), (
                         expected_ranges, expected_step_sizes))

    def test_step_size_to_num(self):

        npt.assert_equal(step_size_to_num([1, 6], 2), 3)
        npt.assert_equal(step_size_to_num([-1, 1], 1), 3)

    def test_get_rotation_axes(self):

        sqrt1_2 = 1 / np.sqrt(2)
        expected = [[0, 0, 1], [sqrt1_2, sqrt1_2, 0], [sqrt1_2, -sqrt1_2, 0]]

        npt.assert_almost_equal(get_rotation_axes(45, 90), expected)

    def test_get_reduced_chi2(self):

        npt.assert_almost_equal(get_reduced_chi2([1, 2, 3], 2), 14)
