import unittest
import os
import numpy as np
import numpy.testing as npt
from kmap import __directory__
from kmap.library.sliceddata import SlicedData


class TestSlicedData(unittest.TestCase):

    def test_initialization_from_hdf5(self):
        sliced_data = SlicedData.init_from_hdf5(
            __directory__ / '../example/data/example5_6584.hdf5')

        npt.assert_almost_equal(
            sliced_data.slice_from_index(2).data[145, 235], 194.848388671875,
            decimal=14)

        (sliced_data.name, '6584estep0.0170213final.txt')
        npt.assert_equal(sliced_data.meta_data, {'alias': 'M3 PTCDA/Ag(110)',
                                                 'arcwidth': '0.7800000000000011',
                                                 'fermiLevel': '28.2',
                                                 'filenumber': '6584estep0.0170213final.txt',
                                                 'kStepSize': '0.02',
                                                 'negPolar_avgs': 'False',
                                                 'polarshift': '0.0',
                                                 'rotation': '-24.0',
                                                 'sym_anglemax': '180.0',
                                                 'sym_anglemin': '0.0',
                                                 'symmode': '2-fold'})


if __name__ == '__main__':
    unittest.main()
