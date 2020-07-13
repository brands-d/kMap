import unittest
import numpy as np
import numpy.testing as npt
from map.model.crosshair import Crosshair
from map.model.plotdata import PlotData


class TestCrosshair(unittest.TestCase):

    def setUp(self):
        self.x = 0
        self.y = 0
        self.radius = 1
        self.width = 1
        self.crosshair = Crosshair(self.x, self.y)
        self.plotdata = PlotData(
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[-1, 1], [-1, 1]])

    def test_correct_initialization(self):

        self.assertEqual(self.crosshair.x, self.x)
        self.assertEqual(self.crosshair.y, self.y)

    def test_set_position(self):

        new_x = 1
        new_y = -1

        self.crosshair.set_position()
        self.assertEqual(self.crosshair.x, self.x)
        self.assertEqual(self.crosshair.y, self.y)

        self.crosshair.set_position(y=new_y)
        self.assertEqual(self.crosshair.x, self.x)
        self.assertEqual(self.crosshair.y, new_y)

        self.crosshair.set_position(new_x)
        self.assertEqual(self.crosshair.x, new_x)
        self.assertEqual(self.crosshair.y, new_y)

    def test_point_mask(self):

        mask = self.crosshair.mask(
            self.plotdata, region='center', inverted=False)
        expected = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.bool)
        npt.assert_equal(mask, expected)

        mask = self.crosshair.mask(
            self.plotdata, region='center', inverted=True)
        expected = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.bool)
        npt.assert_equal(mask, expected)

    def test_line_mask(self):

        mask = self.crosshair.mask(self.plotdata, region='x', inverted=False)
        expected = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]], dtype=np.bool)
        npt.assert_equal(mask, expected)

        mask = self.crosshair.mask(self.plotdata, region='x', inverted=True)
        expected = np.array([[1, 1, 1], [0, 0, 0], [1, 1, 1]], dtype=np.bool)
        npt.assert_equal(mask, expected)

        mask = self.crosshair.mask(self.plotdata, region='y', inverted=False)
        expected = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]], dtype=np.bool)
        npt.assert_equal(mask, expected)

        mask = self.crosshair.mask(self.plotdata, region='y', inverted=True)
        expected = np.array([[1, 0, 1], [1, 0, 1], [1, 0, 1]], dtype=np.bool)
        npt.assert_equal(mask, expected)

    def test_outside_mask(self):

        expected = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=np.bool)

        self.crosshair.set_position(-3, 0)
        expected = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]], dtype=np.bool)
        mask = self.crosshair.mask(self.plotdata, region='y', inverted=False)
        npt.assert_equal(mask, expected)

        self.crosshair.set_position(0, -3)
        expected = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=np.bool)
        mask = self.crosshair.mask(self.plotdata, region='y', inverted=False)
        npt.assert_equal(mask, expected)

        self.crosshair.set_position(-3, -3)
        expected = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=np.bool)
        mask = self.crosshair.mask(self.plotdata, region='y', inverted=False)
        npt.assert_equal(mask, expected)

    def test_cut_from_data(self):

        data = self.crosshair.cut_from_data(
            self.plotdata, region='x', inverted=False)
        npt.assert_equal(
            data, [[np.nan, np.nan, np.nan], [4, 5, 6],
                   [np.nan, np.nan, np.nan]])
        npt.assert_equal(self.plotdata.data, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        data = self.crosshair.cut_from_data(
            self.plotdata, region='center', inverted=True, fill=-1)
        npt.assert_equal(
            data, [[1, 2, 3], [4, -1, 6], [7, 8, 9]])


if __name__ == '__main__':
    unittest.main()
