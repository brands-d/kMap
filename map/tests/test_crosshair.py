import unittest
import numpy as np
import numpy.testing as npt
from map.model.crosshair import Crosshair, CrosshairWithROI
from map.model.plotdata import PlotData


class TestCrosshair(unittest.TestCase):

    def setUp(self):
        self.x = 0
        self.y = 0
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


class TestCrosshairWithROI(unittest.TestCase):

    def setUp(self):
        self.x = 0
        self.y = 0
        self.radius = 1
        self.plotdata = PlotData(
            np.arange(25).reshape(5, 5), [[-2, 2], [-2, 2]])

    def test_correct_initialization(self):

        crosshair = CrosshairWithROI(self.x, self.y, self.radius)

        self.assertEqual(crosshair.radius, self.radius)
        self.assertEqual(crosshair.x, self.x)
        self.assertEqual(crosshair.y, self.y)

    def test_incorrect_initialization(self):

        self.assertRaises(ValueError, CrosshairWithROI, self.x, self.y, -1)

    def test_set_radius(self):

        crosshair = CrosshairWithROI(self.x, self.y, self.radius)

        new_radius = 2
        crosshair.set_radius(new_radius)
        self.assertEqual(crosshair.radius, new_radius)

        new_radius = 0
        crosshair.set_radius(new_radius)
        self.assertEqual(crosshair.radius, new_radius)

        new_radius = -1
        self.assertRaises(ValueError, crosshair.set_radius, new_radius)

    def test_basic_mask(self):

        crosshair = CrosshairWithROI(self.x, self.y, 0)
        mask = crosshair.mask(self.plotdata, region='roi', inverted=False)
        expected = np.zeros((5, 5), dtype=np.bool)
        npt.assert_equal(mask, expected)

        crosshair = CrosshairWithROI(self.x, self.y, self.radius)
        mask = crosshair.mask(self.plotdata, region='roi', inverted=False)
        expected = np.zeros((5, 5), dtype=np.bool)
        expected[2, 2] = True
        npt.assert_equal(mask, expected)

        crosshair = CrosshairWithROI(self.x, self.y, 1.5)
        mask = crosshair.mask(self.plotdata, region='roi', inverted=False)
        expected = np.zeros((5, 5), dtype=np.bool)
        expected[1:4, 1:4] = True
        npt.assert_equal(mask, expected)

        crosshair = CrosshairWithROI(self.x, self.y, 1.5)
        mask = crosshair.mask(self.plotdata, region='roi', inverted=True)
        expected = np.zeros((5, 5), dtype=np.bool)
        expected[[0, 4], :] = True
        expected[:, [0, 4]] = True
        npt.assert_equal(mask, expected)

    def test_override_mask(self):

        crosshair = CrosshairWithROI(self.x, self.y, 1.5)
        mask = crosshair.mask(self.plotdata, region='x', inverted=False)
        expected = np.zeros((5, 5), dtype=np.bool)
        expected[2, :] = True
        npt.assert_equal(mask, expected)

    def test_border_mask(self):

        crosshair = CrosshairWithROI(self.x, self.y, 1.5)
        mask = crosshair.mask(self.plotdata, region='border', inverted=False)
        expected = np.zeros((5, 5), dtype=np.bool)
        expected[1:4, 1:4] = True
        expected[2, 2] = False
        npt.assert_equal(mask, expected)

        crosshair = CrosshairWithROI(self.x, self.y, 0)
        mask = crosshair.mask(self.plotdata, region='border', inverted=False)
        expected = np.zeros((5, 5), dtype=np.bool)
        npt.assert_equal(mask, expected)

        crosshair = CrosshairWithROI(1, 1, 0.5)
        mask = crosshair.mask(self.plotdata, region='border', inverted=False)
        expected = np.zeros((5, 5), dtype=np.bool)
        expected[3, 3] = True
        npt.assert_equal(mask, expected)

        crosshair = CrosshairWithROI(1, 1, 0.5)
        mask = crosshair.mask(self.plotdata, region='border', inverted=True)
        expected = np.ones((5, 5), dtype=np.bool)
        expected[3, 3] = False
        npt.assert_equal(mask, expected)

        crosshair = CrosshairWithROI(1, 1, 10)
        mask = crosshair.mask(self.plotdata, region='border', inverted=False)
        expected = np.zeros((5, 5), dtype=np.bool)
        npt.assert_equal(mask, expected)


if __name__ == '__main__':
    unittest.main()
