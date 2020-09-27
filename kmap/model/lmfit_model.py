import copy

import numpy as np
from lmfit import minimize, Parameters

from kmap.model.crosshair_model import CrosshairModel
from kmap.library.orbitaldata import OrbitalData
from kmap.library.sliceddata import SlicedData
from kmap.library.misc import axis_from_range, step_size_to_num


class LMFitModel():

    def __init__(self, sliced_data, orbitals):

        self.axis = None
        self.crosshair = None
        self.background_equation = ['1', []]
        self.symmetrization = 'no'
        self.Ak_type = 'toroid'
        self.polarization = 'p'
        self.slice_policy = [0, [0], False]
        self.method = ['leastsq', 1e-12]
        self.region = ['all', False]
        self.sliced_data_kmaps = []

        self._set_sliced_data(sliced_data)
        self._add_orbitals(orbitals)

        self._set_parameters()

    def set_crosshair(self, crosshair):

        if isinstance(crosshair, CrosshairModel):
            self.crosshair = crosshair

        else:
            raise TypeError(
                'crosshair has to be of type %s (is %s)' % (
                    type(CrosshairModel), type(crosshair)))

    def set_axis(self, axis):

        self.axis = axis

        self._set_sliced_data_map()

    def set_axis_by_step_size(self, range_, step_size):

        num = step_size_to_num(range_, step_size)
        self.set_axis(axis_from_range(range_, num))

    def set_axis_by_num(self, range_, num):

        self.set_axis(axis_from_range(range_, num))

    def set_symmetrization(self, symmetrization):

        self.symmetrization = symmetrization

    def set_region(self, region, inverted=False):

        self.region = [region, inverted]

    def set_polarization(self, Ak_type, polarization):

        self.Ak_type = Ak_type
        self.polarization = polarization

    def set_slices(self, slice_indices, axis_index=0, combined=False):

        if isinstance(slice_indices, str) and slice_indices == 'all':
            self.slice_policy = [axis_index,
                                 range(self.sliced_data.axes[axis_index].num),
                                 combined]

        elif isinstance(slice_indices, list):
            self.slice_policy = [axis_index, slice_indices, combined]

        else:
            self.slice_policy = [axis_index, [slice_indices], combined]

        self._set_sliced_data_map()

    def set_fit_method(self, method, xtol=1e-7):

        self.method = [method, xtol]

    def set_background_equation(self, equation, variables=[]):

        try:
            compile(equation, '', 'exec')
            self.background_equation = [equation, variables]

            for variable in variables:
                self.parameters.add(variable, value=0,
                                    min=-100, max=100, vary=False, expr=None)

        except:
            raise ValueError(
                'Equation is not parseable. Check for syntax errors.')

    def edit_parameter(self, parameter, *args, **kwargs):

        self.parameters[parameter].set(*args, **kwargs)

    def fit(self):

        results = []

        for index in range(len(self.sliced_data_kmaps)):
            result = minimize(self.chi2,
                              copy.deepcopy(self.parameters),
                              kws={'sliced_data_kmap_index': index},
                              nan_policy='omit',
                              method=self.method[0],
                              xtol=self.method[1])

            results.append(result)

        return results

    def chi2(self, param, sliced_data_kmap_index=0):

        orbital_kmaps = []

        for orbital in self.orbitals:
            ID = orbital.ID
            kmap = orbital.get_kmap(E_kin=param['E_kin'].value,
                                    dk=(self.axis, self.axis),
                                    phi=param['phi_' + str(ID)].value,
                                    theta=param['theta_' + str(ID)].value,
                                    psi=param['psi_' + str(ID)].value,
                                    alpha=param['alpha'].value,
                                    beta=param['beta'].value,
                                    Ak_type=self.Ak_type,
                                    polarization=self.polarization,
                                    symmetrization=self.symmetrization)
            orbital_kmaps.append(param['w_' + str(ID)].value * kmap)

        orbital_kmap = np.nansum(orbital_kmaps)

        variables = {}
        for variable in self.background_equation[1]:
            variables.update({variable: param[variable].value})

        background = param['c'].value * \
            eval(self.background_equation[0], None, variables)

        difference = self.sliced_data_kmaps[sliced_data_kmap_index] - \
            background - orbital_kmap

        difference = self._cut_region(difference)

        return difference.data

    def _set_sliced_data_map(self):

        axis_index, slice_indices, is_combined = self.slice_policy

        kmaps = []
        for slice_index in slice_indices:
            kmaps.append(self.sliced_data.slice_from_index(slice_index,
                                                           axis_index))

        if is_combined:
            kmaps = [np.nansum(kmaps, axis=axis_index)]

        if self.axis is not None:
            self.sliced_data_kmaps = [kmap_.interpolate(
                self.axis, self.axis) for kmap_ in kmaps]

        else:
            self.sliced_data_kmaps = kmaps
            self.axis = kmaps[0].x_axis

    def _cut_region(self, data):

        if self.crosshair is None or self.region[0] == 'all':
            return data

        else:
            return self.crosshair.cut_from_data(
                data, region=self.region[0], inverted=self.region[1])

    def _set_sliced_data(self, sliced_data):

        if isinstance(sliced_data, SlicedData):
            self.sliced_data = sliced_data
            self._set_sliced_data_map()

        else:
            raise TypeError(
                'sliced_data has to be of type %s (is %s)' % (
                    type(SlicedData), type(sliced_data)))

    def _add_orbitals(self, orbitals):

        if (isinstance(orbitals, list) and
                all(isinstance(element, OrbitalData)
                    for element in orbitals)):
            self.orbitals = orbitals

        elif isinstance(orbitals, OrbitalData):
            self.orbitals = [orbitals]

        else:
            raise TypeError(
                'orbital has to be of (or list of) type %s (is %s)' % (
                    type(OrbitalData), type(orbitals)))

    def _set_parameters(self):

        self.parameters = Parameters()

        for orbital in self.orbitals:
            ID = orbital.ID

            self.parameters.add('w_' + str(ID), value=1,
                                min=0, vary=False, expr=None)
            for angle in ['phi_', 'theta_', 'psi_']:
                self.parameters.add(angle + str(ID), value=0,
                                    min=90, max=-90, vary=False, expr=None)

        self.parameters.add('c', value=0,
                            min=0, vary=False, expr=None)
        self.parameters.add('E_kin', value=30,
                            min=5, max=150, vary=False, expr=None)
        for angle in ['alpha', 'beta']:
            self.parameters.add(angle, value=0,
                                min=90, max=-90, vary=False, expr=None)
