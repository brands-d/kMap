import os
import unittest
import numpy.testing as npt
import numpy as np
from kmap.library.orbital import Orbital


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestOrbital(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        with open(dir_path + '/input/pentacene_HOMO.cube') as file:
            cls.cubefile = file.read()

        cls.orbital = Orbital(cls.cubefile, dk3D=0.15, E_kin_max=50)

    def test_init_kaxis(self):

        # check kx, ky and kz axis
        axes = ('kx', 'ky', 'kz')
        shape_expected = (49, 49, 47)
        endpoints_expected = [[-3.6049414968815316, 3.604941496881459],
                              [-3.60333247262221, 3.603332472622217],
                              [-3.4738792493962727, 3.4738792493963437]]

        for axis, shape, endpoint in zip(axes, shape_expected,
                                         endpoints_expected):
            k = self.orbital.psik[axis]
            self.assertEqual(len(k), shape)  # length of axis
            npt.assert_almost_equal(
                k[0], endpoint[0], decimal=14)  # first value
            npt.assert_almost_equal(
                k[-1], endpoint[-1], decimal=14)  # last value

    def test_init_3DFT(self):

        # check 3D Fourier transform
        data = self.orbital.psik['data']
        shape_expected = (49, 49, 47)
        sum_expected = 261.80992432542286
        arbitrary_element_expected = 4.352036114737106e-05  # data[11, 34, 27]

        self.assertEqual(data.shape, shape_expected)
        npt.assert_almost_equal(np.sum(data), sum_expected, decimal=14)
        npt.assert_almost_equal(
            data[11, 34, 27], arbitrary_element_expected, decimal=14)


if __name__ == '__main__':
    unittest.main()
