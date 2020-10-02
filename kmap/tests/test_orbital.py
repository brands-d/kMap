import os
import unittest
import numpy.testing as npt
import numpy as np
from kmap.library.orbital import Orbital



class TestOrbital(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = dir_path + '/input/pentacene_HOMO.cube'
        with open(filepath) as file:
            cls.cubefile = file.read()
        cls.orbital = Orbital(cls.cubefile,dk3D=0.15, E_kin_max=50) 


    def setUp(self):
        pass     
        # Code run before each test comes here
        
    def tearDown(self):
        pass
        # Code run after each test comes here


    def test_init_kaxis(self):

        # check kx, ky and kz axis
        axes = ('kx', 'ky', 'kz')
        shape_expected = (49, 49, 47)
        endpoints_expected = [ [-3.6049414968815032,3.604941496881459],
                               [-3.60333247262221,  3.603332472622217],
                               [-3.4738792493962727,3.4738792493963437]]


        for axis, shape, endpoint in zip(axes, shape_expected,
                                         endpoints_expected):
            k = self.orbital.psik[axis]
            self.assertEqual(len(k), shape)  # length of axis
            npt.assert_almost_equal(k[0],  endpoint[0], decimal=13)  # first value
            npt.assert_almost_equal(k[-1], endpoint[-1],decimal=13)  # last value
 

    def test_init_3DFT(self):

        # check 3D Fourier transform
        data = self.orbital.psik['data']
        shape_expected = (49, 49, 47)
        sum_expected = 261.80992432542286
        arbitrary_element_expected = 4.352036114737106e-05  # data[11, 34, 27]

        self.assertEqual(data.shape, shape_expected)
        npt.assert_almost_equal(np.sum(data), sum_expected, decimal=13)
        npt.assert_almost_equal(data[11,34,27], arbitrary_element_expected, decimal=13)

    def test_get_kmap_basic(self):
    
        kmap = self.orbital.get_kmap(
                     E_kin=30, dk=0.10, 
                     phi=0, theta=0, psi=0,
                     Ak_type='no', polarization='p', alpha=60, beta=90,
                     gamma=0,symmetrization='no') 

        shape_expected = (56, 56)
        endpoints_expected = [-2.8060742649871617,2.8060742649871617]
        sum_expected = 11.748706872541481  

        self.assertEqual(kmap.data.shape, shape_expected)
        self.assertEqual(len(kmap.x_axis), shape_expected[0])
        self.assertEqual(len(kmap.y_axis), shape_expected[1])
        npt.assert_almost_equal(kmap.x_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.x_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(kmap.y_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.y_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(np.nansum(kmap.data), sum_expected, decimal=13)

    def test_get_kmap_orientation(self):
    
        kmap = self.orbital.get_kmap(
                     E_kin=30, dk=0.15, 
                     phi=27, theta=38, psi=-11,
                     Ak_type='no', polarization='p', alpha=60, beta=90,
                     gamma=0,symmetrization='no') 

        shape_expected = (37, 37)
        endpoints_expected = [-2.8060742649871617,2.8060742649871617]
        sum_expected = 3.9675298372410364   

        self.assertEqual(kmap.data.shape, shape_expected)
        self.assertEqual(len(kmap.x_axis), shape_expected[0])
        self.assertEqual(len(kmap.y_axis), shape_expected[1])
        npt.assert_almost_equal(kmap.x_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.x_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(kmap.y_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.y_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(np.nansum(kmap.data), sum_expected, decimal=13)


    def test_get_kmap_toroid(self):
    
        kmap = self.orbital.get_kmap(
                     E_kin=25, dk=0.20, 
                     phi=0, theta=0, psi=0,
                     Ak_type='toroid', polarization='p', alpha=60, beta=47,
                     gamma=0,symmetrization='no') 

        shape_expected = (25, 25)
        endpoints_expected = [-2.5615836216136625, 2.5615836216136625]
        sum_expected = 21.626385200246624    

        self.assertEqual(kmap.data.shape, shape_expected)
        self.assertEqual(len(kmap.x_axis), shape_expected[0])
        self.assertEqual(len(kmap.y_axis), shape_expected[1])
        npt.assert_almost_equal(kmap.x_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.x_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(kmap.y_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.y_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(np.nansum(kmap.data), sum_expected, decimal=13)

    def test_get_kmap_NanoESCA(self):
    
        kmap = self.orbital.get_kmap(
                     E_kin=25, dk=0.20, 
                     phi=0, theta=0, psi=0,
                     Ak_type='NanoESCA', polarization='p', alpha=47, beta=123,
                     gamma=0,symmetrization='no') 

        shape_expected = (25, 25)
        endpoints_expected = [-2.5615836216136625, 2.5615836216136625]
        sum_expected = 9.364599942353433   

        self.assertEqual(kmap.data.shape, shape_expected)
        self.assertEqual(len(kmap.x_axis), shape_expected[0])
        self.assertEqual(len(kmap.y_axis), shape_expected[1])
        npt.assert_almost_equal(kmap.x_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.x_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(kmap.y_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.y_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(np.nansum(kmap.data), sum_expected, decimal=13)

    def test_get_kmap_symmetry(self):
    
        kmap = self.orbital.get_kmap(
                     E_kin=25, dk=0.20, 
                     phi=12, theta=-21, psi=17,
                     Ak_type='no', polarization='p', alpha=0, beta=0,
                     gamma=0,symmetrization='3-fold+mirror') 

        shape_expected = (25, 25)
        endpoints_expected = [-2.5615836216136625, 2.5615836216136625]
        sum_expected = 3.1856202463487717   

        self.assertEqual(kmap.data.shape, shape_expected)
        self.assertEqual(len(kmap.x_axis), shape_expected[0])
        self.assertEqual(len(kmap.y_axis), shape_expected[1])
        npt.assert_almost_equal(kmap.x_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.x_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(kmap.y_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.y_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(np.nansum(kmap.data), sum_expected, decimal=13)


    def test_get_kmap_kgrid(self):
    
        kx = np.linspace(-2,2,10)
        ky = np.linspace(-2,2,12)

        kmap = self.orbital.get_kmap(
                     E_kin=25, dk=(kx,ky), 
                     phi=17, theta=-23, psi=-17,
                     Ak_type='no', polarization='p', alpha=0, beta=0,
                     gamma=0,symmetrization='no') 

        shape_expected = (10, 12)
        endpoints_expected = [-2, 2]
        sum_expected = 0.8832029249194455  

        self.assertEqual(kmap.data.T.shape, shape_expected)
        self.assertEqual(len(kmap.x_axis), shape_expected[0])
        self.assertEqual(len(kmap.y_axis), shape_expected[1])
        npt.assert_almost_equal(kmap.x_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.x_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(kmap.y_axis[0],  endpoints_expected[0], decimal=13)   
        npt.assert_almost_equal(kmap.y_axis[-1], endpoints_expected[-1],decimal=13)    
        npt.assert_almost_equal(np.nansum(kmap.data), sum_expected, decimal=13)


    def test_check_new_cut(self):

        sums_expected = [202.12975607342722, 17.171157851335725,
                            3.8929271845777813,17.9086022363552,
                            27.839419217261188,1.855922052900676]

        kmaps = []
        kmaps.append(self.orbital.get_kmap(E_kin=20)) 
        kmaps.append(self.orbital.get_kmap(E_kin=20,dk=0.1))
        kmaps.append(self.orbital.get_kmap(E_kin=20,dk=0.2))
        kx = np.linspace(-2,2,50)
        ky = np.linspace(-2,2,50)
        kmaps.append(self.orbital.get_kmap(E_kin=30,dk=(kx,ky)))
        kmaps.append(self.orbital.get_kmap(E_kin=20,dk=(kx,ky)))
        kx = np.linspace(-3,3,20)
        ky = np.linspace(-3,3,20)
        kmaps.append(self.orbital.get_kmap(E_kin=20,dk=(kx,ky)))

        for kmap, sum_expected in zip(kmaps, sums_expected):
            npt.assert_almost_equal(np.nansum(kmap.data), sum_expected, decimal=13)

if __name__ == '__main__':
    unittest.main()
