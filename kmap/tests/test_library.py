import unittest
from kmap.library.library import *


class TestLibrary(unittest.TestCase):

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

        value = -2.5
        self.assertEqual(idx_closest_value(axis, value), None)

        value = -1.23
        self.assertEqual(idx_closest_value(axis, value), 1)

    def test_normalize(self):

        data = [1,2,3]

        self.assertEqual(normalize(data), 2)