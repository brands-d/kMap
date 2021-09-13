# Python Imports
import os
import unittest

# Third Party Imports
import numpy as np
import numpy.testing as npt

# Own Imports
from kmap.model.lmfit_model import LMFitModel
from kmap.model.crosshair_model import CrosshairAnnulusModel
from kmap.library.sliceddata import SlicedData
from kmap.library.orbitaldata import OrbitalData
from kmap.library.misc import step_size_to_num
from kmap.config.config import config


class TestLMFitModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        file_path = os.path.dirname(os.path.realpath(
            __file__))
        input_path = file_path + '/../../example/data/'

        sliced_path = input_path + 'example5_6584.hdf5'
        cls.sliced_data = SlicedData.init_from_hdf5(sliced_path)

        orbital_paths = ['PTCDA_C.cube', 'PTCDA_D.cube',
                         'PTCDA_E.cube', 'PTCDA_F.cube']
        cls.orbitals = [OrbitalData.init_from_file(
            input_path + path, ID) for ID, path in enumerate(orbital_paths)]

        cls.expected = np.loadtxt(file_path + '/output/weights_PTCDA')
        cls.background_expected = np.loadtxt(
            file_path + '/output/background_expected')

    def setUp(self):

        self.lmfit = LMFitModel(
            TestLMFitModel.sliced_data, TestLMFitModel.orbitals)
        self.crosshair = CrosshairAnnulusModel()

    def test_set_crosshair(self):

        self.lmfit.set_crosshair(self.crosshair)

        self.assertEqual(self.lmfit.crosshair, self.crosshair)

    def test_set_axis(self):

        step_size = 0.24
        range_ = [-3, 3]
        axis = np.linspace(
            *range_, num=step_size_to_num(range_, step_size), endpoint=True)

        self.lmfit.set_axis_by_step_size(range_, step_size)
        npt.assert_almost_equal(self.lmfit.get_sliced_kmap(0).x_axis, axis)

    def test_set_slices(self):

        self.lmfit.set_slices([1, 2, 3])
        self.lmfit.set_slices([0, 1, 2, 3], combined=True)

    def test_set_background_equation(self):

        self.lmfit.set_background_equation('np.exp(a)')
        npt.assert_equal(self.lmfit.background_equation, ['np.exp(a)', ['a']])

        self.assertRaises(
            ValueError, self.lmfit.set_background_equation, 'np.exp(a')

    def test_parameters(self):

        self.lmfit.set_background_equation('np.exp(a)')

        self.assertEqual(self.lmfit.parameters['w_1'].min, 0)
        self.assertEqual(self.lmfit.parameters['a'].value, 0)
        self.assertEqual(self.lmfit.parameters['E_kin'].max, 150)

    def test_edit_parameter(self):

        self.lmfit.edit_parameter('w_1', value=1.5)
        self.assertEqual(self.lmfit.parameters['w_1'].value, 1.5)

    def test_background(self):

        range_, dk = [-3.0, 3.0], 0.025
        self.lmfit.set_axis_by_step_size(range_, dk)

        self.lmfit.set_background_equation(
            '(np.exp(-x**2-y**2)-np.exp(-(x-1)**2-(y-1)**2))/2')

        background = self.lmfit._get_background(param=[])

        npt.assert_almost_equal(background, TestLMFitModel.background_expected)

    def test_settings(self):

        lmfit_new = LMFitModel(
            TestLMFitModel.sliced_data, TestLMFitModel.orbitals)

        lmfit_new.set_settings(self.lmfit.get_settings())

    def test_PTCDA(self):

        if float(config.get_key('orbital', 'dk3D')) != 0.12:
            print(
                'WARNING: Test \'test_PTCDA\' from the ' +
                '\'test_lmfit\' module has not been run. It requires ' +
                '\'dk3D\' setting from the \'cube\' category to be ' +
                'to 0.12.')
            return

        # Set certain parameters not being fitted but desired to be changed
        range_, dk = [-3.0, 3.0], 0.04
        self.lmfit.set_axis_by_step_size(range_, dk)
        self.lmfit.set_polarization('toroid', 'p')
        self.lmfit.set_background_equation('c')

        # Set certain fit parameter to desired value
        self.lmfit.edit_parameter('E_kin', value=27.2)
        self.lmfit.edit_parameter('alpha', value=40)
        self.lmfit.edit_parameter('c', value=1, vary=True)

        # Activate fitting for all weights (i is a dummy ID used in setUpClass)
        for i in [0, 1, 2, 3]:
            self.lmfit.edit_parameter('w_' + str(i), vary=True)

        # Set slices to be used
        self.lmfit.set_slices('all', combined=False)

        results = self.lmfit.fit()

        # Test results
        weights = np.array([[result[1].params['w_0'].value,
                             result[1].params['w_1'].value,
                             result[1].params['w_2'].value,
                             result[1].params['w_3'].value]
                            for result in results]).T

        npt.assert_almost_equal(weights, TestLMFitModel.expected, decimal=5)
