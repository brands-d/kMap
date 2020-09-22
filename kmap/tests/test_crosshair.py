import os
import unittest
import numpy as np
import numpy.testing as npt
from kmap.library.plotdata import PlotData
from kmap.model.crosshair_model import *


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestCrosshair(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.expected = np.load(
            dir_path + '/output/test_crosshair_expected.npy',
            allow_pickle=True).item()

    def setUp(self):

        self.x = 0
        self.y = 0
        self.radius = 1.5
        self.width = 1.5
        self.crosshair = CrosshairAnnulusModel(x=self.x, y=self.y,
                                               radius=self.radius,
                                               width=self.width)

        self.data = PlotData(np.reshape(np.array(range(99)), (9, 11)),
                             [[-5, 5], [-4, 4]])

    def test_correct_initialization(self):

        self.assertEqual(self.crosshair.x, self.x)
        self.assertEqual(self.crosshair.y, self.y)
        self.assertEqual(self.crosshair.radius, self.radius)
        self.assertEqual(self.crosshair.width, self.width)

    def test_incorrect_initialization(self):

        self.assertRaises(ValueError, CrosshairROIModel, radius=-1)
        self.assertRaises(ValueError, CrosshairAnnulusModel, width=-1)

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

    def test_set_radius(self):

        new_radius = 2
        self.crosshair.set_radius(new_radius)
        self.assertEqual(self.crosshair.radius, new_radius)

        new_radius = 0
        self.crosshair.set_radius(new_radius)
        self.assertEqual(self.crosshair.radius, new_radius)

        new_radius = -1
        self.assertRaises(ValueError, self.crosshair.set_radius, new_radius)

    def test_set_width(self):

        new_width = 2
        self.crosshair.set_width(new_width)
        self.assertEqual(self.crosshair.width, new_width)

        new_width = 0
        self.crosshair.set_width(new_width)
        self.assertEqual(self.crosshair.width, new_width)

        new_width = -1
        self.assertRaises(ValueError, self.crosshair.set_width, new_width)

    def test_point_mask(self):

        # Standard
        title = 'Center Cut'
        self.mask(1, 1, 2, 1.5, 'center', False, title)

        # Edge Case
        title = 'Center Edge Case'
        self.mask(0.5, 0.5, 1.5, 1.5, 'center', False, title)

    def test_line_mask(self):

        # x-Line
        title = 'x-Line'
        self.mask(0, 0, 1.5, 1.5, 'x', False, title)

        # y-Line
        title = 'y-Line'
        self.mask(0, 0, 1.5, 1.5, 'y', False, title)

        # x-Line Inverted
        title = 'x-Line Inverted'
        self.mask(0, 0, 1.5, 1.5, 'x', True, title)

        # x-Line 2
        title = 'x-Line 2'
        self.mask(1, 0, 1.5, 1.5, 'x', False, title)

        # y-Line Edge Case
        title = 'y-Line Edge Case 2'
        self.mask(0, 0.5, 1.5, 1.5, 'y', False, title)

    def test_roi_mask(self):

        # ROI Cut
        title = 'ROI Cut'
        self.mask(0, 0, 1.5, 1.5, 'roi', False, title)

        # ROI Cut Inverted
        title = 'ROI Cut Inverted'
        self.mask(0, 0, 1.5, 1.5, 'roi', True, title)

        # Moved ROI
        title = 'Moved ROI'
        self.mask(1, 1, 3, 1.5, 'roi', False, title)

        # ROI Cut Edge Case
        title = 'ROI Edge Case'
        self.mask(0, 0, 2, 1.5, 'roi', False, title)

        # ROI Cut Edge Case 2
        title = 'ROI Edge Case 2'
        self.mask(0, 0, 2.01, 1.5, 'roi', False, title)

    def test_border_mask(self):

        # Border Cut
        title = 'Border Cut'
        self.mask(0, 0, 1.5, 1.5, 'border', False, title)

        # Moved Border Cut
        title = 'Moved Border Cut'
        self.mask(1, 1, 2, 1.5, 'border', False, title)

        # Inverted Border Cut
        title = 'Inverted Border Cut'
        self.mask(0, 0, 1.5, 1.5, 'border', True, title)

        # Border Cut Edge Case
        title = 'Border Edge Case'
        self.mask(0, 0, 0.70, 1.5, 'border', False, title)

        # Border Cut Edge Case 2
        title = 'Border Edge Case 2'
        self.mask(0, 0, 2.13, 1.5, 'border', False, title)

    def test_outer_border_mask(self):

        # Outer Border Cut
        title = 'Outer Border Cut'
        self.mask(0, 0, 1.5, 1.5, 'outer_border', False, title)

        # Outer Border Edge Case
        title = 'Outer Border Edge Case'
        self.mask(0, 0, 0.00, 0.7, 'outer_border', False, title)

        # Outer Border Edge Case 2
        title = 'Outer Border Edge Case 2'
        self.mask(0, 0, 0.00, 2.13, 'outer_border', False, title)

    def test_ring_mask(self):

        # Ring Cut
        title = 'Ring Cut'
        self.mask(0, 0, 1.5, 1.5, 'ring', False, title)

        # Moved Ring Cut
        title = 'Moved Ring Cut'
        self.mask(1, 1, 2, 1.5, 'ring', False, title)

        # Inverted Ring Cut
        title = 'Inverted Ring Cut'
        self.mask(0, 0, 1.5, 1.5, 'ring', True, title)

        # Ring Edge Case 2
        title = 'Ring Edge Case'
        self.mask(0, 0, 1, 2.00, 'ring', False, title)

        # Ring Edge Case 2
        title = 'Ring Edge Case 2'
        self.mask(0, 0, 2.01, 1.5, 'ring', False, title)

    def mask(self, x, y, r, w, region, inverted, title):

        self.crosshair.set_position(x, y)
        self.crosshair.set_radius(r)
        self.crosshair.set_width(w)

        cut = self.crosshair.cut_from_data(
            self.data, region=region, inverted=inverted)

        expected_output = self.expected[title]

        npt.assert_equal(expected_output, cut.data)


if __name__ == '__main__':
    unittest.main()
