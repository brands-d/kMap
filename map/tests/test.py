import unittest
import numpy.testing
from map.model.data import PlotData


class TestPlotData(unittest.TestCase):
    def test_initialization(self):

        data = [[1, 2, 3], [4, 5, 6]]
        range_ = [[1, 2], [-1, 1]]

        plotdata = PlotData(data, range_)

        numpy.testing.assert_equal(plotdata.data, data)
        numpy.testing.assert_equal(plotdata.range, range_)
        numpy.testing.assert_equal(plotdata.shape, (2, 3))
        numpy.testing.assert_equal(plotdata.x_axis, [1, 2])
        numpy.testing.assert_equal(plotdata.y_axis, [-1, 0, 1])
        numpy.testing.assert_equal(plotdata.step_size, [1, 1])


if __name__ == '__main__':
    unittest.main()
