import unittest
import numpy as np
import numpy.testing as npt
from map import __directory__
from map.model.sliceddata import SlicedData


class TestSlicedData(unittest.TestCase):

    def setUp(self):
        self.slices = np.arange(27).reshape(3, 3, 3)
        self.range = [[1, 2], [-1, 1]]
        self.slice_keys = [1, 2, 3]

    def test_initialization(self):

        name = 'Test Data'
        meta_data = {'Test Key': 'Test Value'}
        sliced_data = SlicedData(self.slices, self.range,
                                 self.slice_keys, name=name,
                                 meta_data=meta_data)

        npt.assert_equal(sliced_data.slice_from_idx(1).data, self.slices[1])
        npt.assert_equal(sliced_data.slice_from_key(1).data, self.slices[0])
        npt.assert_equal(sliced_data.slice_from_idx(1).range, self.range)
        npt.assert_equal(sliced_data.name, name)
        npt.assert_equal(sliced_data.meta_data, meta_data)

        range_ = [[[-1, 2], [-1, -1.5]],
                  [[33, 2], [1, 2]], [[19, 24], [1, 10]]]
        sliced_data = SlicedData(self.slices, range_, self.slice_keys)
        npt.assert_equal(sliced_data.slice_from_idx(1).range, range_[1])
        npt.assert_equal(sliced_data.slice_from_key(1).range, range_[0])

    def test_initialization_from_hdf5(self):

        sliced_data = SlicedData.init_from_hdf5(
            __directory__ + '/resources/test_resources/basic.hdf5')

        npt.assert_equal(sliced_data.name, 'basic')
        npt.assert_equal(sliced_data.slice_from_idx(1).data, self.slices[1])
        npt.assert_equal(sliced_data.slice_from_idx(2).range, self.range)
        npt.assert_equal(sliced_data.meta_data, {'date': '2020/07/12'})

    def test_initialization_from_hdf5_with_new_keys(self):

        self.assertRaises(AttributeError, SlicedData.init_from_hdf5,
                          __directory__ +
                          '/resources/test_resources/basic_new_keys.hdf5')

        new_keys = {'name': 'new_name', 'slice_keys': 'new_slice_keys'}
        sliced_data = SlicedData.init_from_hdf5(
            __directory__ + '/resources/test_resources/basic_new_keys.hdf5',
            new_keys)

        npt.assert_equal(sliced_data.name, 'basic')
        npt.assert_equal(sliced_data.slice_from_idx(1).data, self.slices[1])
        npt.assert_equal(sliced_data.slice_from_idx(2).range, self.range)
        npt.assert_equal(sliced_data.meta_data, {'date': '2020/07/12'})


if __name__ == '__main__':
    unittest.main()
