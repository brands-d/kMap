# The file has to be in the folder kmap/tests
# The file name has to start with "test_"

# Has to have unittest import
import unittest
# Useful for tests involving numpy arrays
import numpy.testing as npt
import numpy as np
# Import modules necessary for testing here
from kmap.library.orbital import Orbital

# Class has to be named TestXXX (for exmaple TestOrbital)
# Class has to inherit from unittest.TestCase
class TestOrbital(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('input/pentacene_HOMO.cube') as file:
            cls.cubefile = file.read()
        cls.orbital = Orbital(cls.cubefile,dk3D=0.15, E_kin_max=50) 


    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass     
        # Code run before each test comes here
        # For example reading data from files or construct objects
        # (Tests can never depend on each other, only on setUp and tearDown
        # as the order in which they are run is not fixed)
        # Use setUpClass and tearDownClass for methods run once and only once
        # before/after all tests (for exmaple downloading a file)
        
    def tearDown(self):
        pass
        # Code run after each test comes here
        # For exmaple correct destruction or deletion of files

    def test_init_kaxis(self):
        # check kx, ky and kz axis
        axes = ('kx', 'ky', 'kz')
        shape_expected = (49, 49, 47)
        endpoints_expected = [ [-3.6049414968815316,3.604941496881459],
                               [-3.60333247262221,  3.603332472622217],
                               [-3.4738792493962727,3.4738792493963437]]

        for axis, shape, endpoint in zip(axes, shape_expected,endpoints_expected):
            k = self.orbital.psik[axis]
            self.assertEqual(len(k), shape)  # length of axis
            npt.assert_almost_equal(k[0],  endpoint[0], decimal=14)  # first value
            npt.assert_almost_equal(k[-1], endpoint[-1],decimal=14)  # last value
 
    def test_init_3DFT(self):
        # check 3D Fourier transform
        data = self.orbital.psik['data']
        shape_expected = (49, 49, 47)   
        sum_expected = 261.80992432542286
        arbitrary_element_expected = 4.352036114737106e-05  # data[11, 34, 27]
        
        self.assertEqual(data.shape, shape_expected)
        npt.assert_almost_equal(np.sum(data), sum_expected, decimal=14)
        npt.assert_almost_equal(data[11,34,27], arbitrary_element_expected, decimal=14)


if __name__ == '__main__':
    unittest.main()