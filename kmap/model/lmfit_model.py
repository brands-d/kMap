"""Defines the LMFitModel class.

This file defines a class named LMFitModel designed encapsulate the
LMFit process. As such it can be understood as a wrapper class for the
lmfit package, both wrapping it's methods into a more useful form and
extending the feature-set. This class is can be used as a module inside
scripts without the GUI part.
"""

# Python Imports
import copy
import re
import builtins

# Third Party Imports
import numpy as np
from lmfit import minimize, Parameters

# Own Imports
from kmap.model.crosshair_model import CrosshairModel, CrosshairAnnulusModel
from kmap.library.orbitaldata import OrbitalData
from kmap.library.sliceddata import SlicedData
from kmap.library.misc import (
    axis_from_range, step_size_to_num, get_reduced_chi2, transpose_axis_order)
from kmap.config.config import config


class LMFitModel():
    """
    Wrapper class for the lmfit package. Acts both as module usable in
    scripts as well as core logic class for the lmfit part in kMap.py.

    For an example on how to use it please see the 'test_PTCDA' test in
    the 'kmap.tests.test_lmfit' file.

    ATTENTION: Please do not set any attributes manually. Instead use
    the appropriate "set_xxx" method instead.
    """

    def __init__(self, sliced_data, orbitals):
        """
        Args:
            sliced_data (SlicedData): A single SlicedData object.
            orbitals (OrbitalData or list): A single OrbitalData object
                or a list of OrbitalData objects.
                ATTENTION: An Orbital object is NOT sufficient. Please
                use the OrbitalData wrapping class instead.
        """

        self.axis = None
        self.crosshair = None
        self.symmetrization = 'no'
        self.background_equation = ['0', []]
        self.Ak_type = 'no'
        self.polarization = 'p'
        self.slice_policy = [0, [0], False]
        self.method = {'method': 'leastsq', 'xtol': 1e-12}
        self.region = ['all', False]

        self._set_sliced_data(sliced_data)
        self._add_orbitals(orbitals)

        self._set_parameters()

    def set_crosshair(self, crosshair):
        """A setter method to set a custom crosshair. If none is set
        when a region restriction is applied, a CrosshairAnnulusModel
        will be created.

        Args:
            crosshair (CrosshairModel): A crosshair model for cutting
                the data for any region-restriction.
                ATTENTION: The passed CrosshairModel has to support the
                region restriction you want to use.
        """

        if crosshair is None or isinstance(crosshair, CrosshairModel):
            self.crosshair = crosshair

        else:
            raise TypeError(
                'crosshair has to be of type %s (is %s)' % (
                    type(CrosshairModel), type(crosshair)))

    def set_axis(self, axis):
        """A setter method to set an axis for the interpolation onto a
        common grid. Default is the x-axis of the first slice in the
        list of slices chosen to be fitted.

        Args:
            axis (np.array): 1D array defining the common axis (and grid
            as only square kmaps are supported) for the subtraction.
        """

        self.axis = axis

    def set_axis_by_step_size(self, range_, step_size):
        """A convenience setter method to set an axis by defining the
        range and the step size.

        Args:
            range_ (list): A list of min and max value.
            step_size (float): A number denoting the step size.
        """

        num = step_size_to_num(range_, step_size)
        self.set_axis(axis_from_range(range_, num))

    def set_axis_by_num(self, range_, num):
        """A convenience setter method to set an axis by defining the
        range and the number of grid points.

        Args:
            range_ (list): A list of min and max value.
            num (int): An integer denoting the number of grid points.
        """

        self.set_axis(axis_from_range(range_, num))

    def set_symmetrization(self, symmetrization):
        """A setter method to set the type of symmetrization for the
        orbital kmaps. Default is 'no'.

        Args:
            symmetrization (str): See 'get_kmap' from
            'kmap.library.orbital.py' for information.
        """

        self.symmetrization = symmetrization

    def set_region(self, region, inverted=False):
        """A setter method to set the region restriction for the lmfit
        process. Default is no region restriction ('all').

        Args:
            region (str): Supports all regions the crosshair model you
            supplied supports. See there for documentation. (default
            is a CrosshairAnnulusModel).
            inverted (bool): See your CrosshairModel for documentation.
        """

        self.region = [region, inverted]

        if region != 'all' and self.crosshair is None:
            self.crosshair = CrosshairAnnulusModel()

    def set_polarization(self, Ak_type, polarization):
        """A setter method to set the type of polarization for the
        orbital kmaps. Default is 'toroid' and 'p'.

        Args:
            Ak_type (str): See 'get_kmap' from
            'kmap.library.orbital.py' for information.
            polarization (str): See 'get_kmap' from
            'kmap.library.orbital.py' for information.
        """

        self.Ak_type = Ak_type
        self.polarization = polarization

    def set_slices(self, slice_indices, axis_index=0, combined=False):
        """A setter method to chose the slices to be fitted next time
        'fit()' is called. Default is [0], 0 and False.

        Args:
            slice_indices (int or list or str): Either one or more
            indices for the slices to be fitted next. Pass 'all' to use
            all slices in this axis.
            axis_index (int): Which axis in the SlicedData is used as
            slice axis.
            combined (bool): Whether to fit all slices individually or
            add all the slices for one fit instead.
        """

        if isinstance(slice_indices, str) and slice_indices == 'all':
            self.slice_policy = [axis_index,
                                 range(self.sliced_data.axes[axis_index].num),
                                 combined]

        elif isinstance(slice_indices, list):
            self.slice_policy = [axis_index, slice_indices, combined]

        elif isinstance(slice_indices, range):
            self.slice_policy = [axis_index, list(slice_indices), combined]

        else:
            self.slice_policy = [axis_index, [slice_indices], combined]

    def set_fit_method(self, method, xtol=1e-7):
        """A setter method to set the method and the tolerance for the
        fitting process. Default is 'leastsq' and 1e-7.

        Args:
            method (str): See the documentation for the lmfit module.
            xtol (str): Only available for one of the following methods:
                        'leastsq', 'least_squares', 'powell'
        """

        xtol_capable_methods = ['leastsq', 'least_squares']
        if method in xtol_capable_methods:
            self.method = {'method': method, 'xtol': xtol}

        else:
            self.method = {'method': method}

    def set_background_equation(self, equation):
        """A setter method to set an custom background equation.
        Default is '1'.

        Args:
            equation (str): An equation used to calculate the background
            profile. Can use python function (e.g. abs()) and basics
            methods from the numpy module (prefix by 'np.';
            e.g. np.sqrt()). Can contain variables to be fitted.
            Variables have can only contain lower or upper case letters,
            underscores and numbers. They cannot start with numbers.
            The variables 'x' and 'y' are special and denote the x and
            y axis respectively. No variables already used outside the
            background equation (like phi) can be used.
            Here are some examples of valid variable names:
            x_s, x2, x_2, foo, this_is_a_valid_variable.
            Each variables starts with following default values:
            value=0, min=-99999.9, max=99999.9, vary=False, expr=None

            The equation will be parsed by eval. Please don't injected
            any code as it would be really easy to do so. There are no
            safeguards in place whatsoever so we (have to) trust you.
            Thanks, D.B.
        """

        try:
            compile(equation, '', 'exec')

        except:
            raise ValueError(
                'Equation is not parseable. Check for syntax errors.')

        # Pattern matches all numpy, math and builtin methods
        clean_pattern = 'np\\.[a-z1-9\\_]+|math\\.[a-z1-9\\_]+'
        for builtin in dir(builtins):
            clean_pattern += '|' + str(builtin)

        cleaned_equation = re.sub(clean_pattern, '', equation)
        # Pattern matches all text including optional underscore with
        # numbers.
        variable_pattern = '[a-zA-Z\\_]+[0-9]*'
        variables = list(set(re.findall(variable_pattern, cleaned_equation)))

        # x and y need special treatment
        if 'x' in variables:
            variables.remove('x')

        if 'y' in variables:
            variables.remove('y')

        new_variables = np.setdiff1d(variables, self.background_equation[1])
        self.background_equation = [equation, variables]
        for variable in new_variables:
            self.parameters.add(variable, value=0, min=-99999.9,
                                max=99999.9, vary=False, expr=None)

        return [self.parameters[variable] for variable in new_variables]

    def edit_parameter(self, parameter, *args, **kwargs):
        """A setter method to edit fitting settings for one parameter.
        Use this method to enable a parameter for fitting (vary=True)

        Args:
            parameter (str): Name of the parameter to be editted.
            *args & **kwargs (): Are being passed to the
            'parameter.set' method of the lmfit module. See there
            for more documentation.
        """

        self.parameters[parameter].set(*args, **kwargs)

    def fit(self):
        """Calling this method will trigger a lmfit with the current
        settings.

        Returns:
            (list): A list of MinimizerResults. One for each slice
            fitted.
        """

        lmfit_padding = float(config.get_key('lmfit', 'padding'))

        any_parameter_vary = False
        for parameter in self.parameters.values():
            if parameter.vary:
                any_parameter_vary = True
                break

        if not any_parameter_vary and self.method['method'] not in ['leastsq', 'least_squares']:
            raise ValueError(
                'Only leastsq and least_squares can fit if no parameter is set to vary.')

        for parameter in self.parameters.values():
            if parameter.vary and parameter.value <= parameter.min:
                padded_value = parameter.min + lmfit_padding
                print('WARNING: Initial value for parameter \'%s\' had to be corrected to %f (was %f)' % (
                    parameter.name, padded_value, parameter.value))
                parameter.value = padded_value

        results = []
        for index in self.slice_policy[1]:
            slice_ = self.get_sliced_kmap(index)
            result = minimize(self._chi2,
                              copy.deepcopy(self.parameters),
                              kws={'slice_': slice_},
                              nan_policy='omit',
                              **self.method)

            results.append([index, result])

        return results

    def transpose(self, constant_axis):

        axis_order = transpose_axis_order(constant_axis)

        self.sliced_data.transpose(axis_order)

    def get_settings(self):

        settings = {'crosshair': self.crosshair,
                    'background': self.background_equation,
                    'symmetrization': self.symmetrization,
                    'polarization': [self.Ak_type, self.polarization],
                    'slice_policy': self.slice_policy,
                    'method': self.method,
                    'region': self.region,
                    'axis': self.axis}

        return copy.deepcopy(settings)

    def set_settings(self, settings):

        self.set_crosshair(settings['crosshair'])
        self.set_background_equation(settings['background'][0])
        self.set_polarization(*settings['polarization'])
        slice_policy = settings['slice_policy']
        self.set_slices(slice_policy[1], slice_policy[0], slice_policy[2])
        self.set_region(*settings['region'])
        self.set_symmetrization(settings['symmetrization'])
        self.set_fit_method(*settings['method'])
        self.set_axis(settings['axis'])

    def get_sliced_kmap(self, slice_index):

        axis_index, slice_indices, is_combined = self.slice_policy

        if is_combined:
            kmaps = []
            for slice_index in slice_indices:
                kmaps.append(self.sliced_data.slice_from_index(slice_index,
                                                               axis_index))

            kmap = np.nansum(kmaps, axis=axis_index)

        else:
            kmap = self.sliced_data.slice_from_index(slice_index,
                                                     axis_index)

        if self.axis is not None:
            kmap = kmap.interpolate(self.axis, self.axis)

        else:
            self.axis = kmap.x_axis

        return kmap

    def get_orbital_kmap(self, ID, param=None):

        if param is None:
            param = self.parameters

        orbital = self.ID_to_orbital(ID)
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

        return kmap

    def get_weighted_sum_kmap(self, param=None, with_background=True):

        if param is None:
            param = self.parameters

        orbital_kmaps = []
        for orbital in self.orbitals:
            ID = orbital.ID

            weight = param['w_' + str(ID)].value

            kmap = weight * self.get_orbital_kmap(ID, param)

            orbital_kmaps.append(kmap)

        orbital_kmap = np.nansum(orbital_kmaps)

        if with_background:
            variables = {}
            for variable in self.background_equation[1]:
                variables.update({variable: param[variable].value})

            background = self._get_background(variables)

            return orbital_kmap + background

        else:
            return orbital_kmap

    def get_residual(self, slice_, param=None, weight_sum_data=None):

        if param is None:
            param = self.parameters

        if weight_sum_data is None:
            orbital_kmap = self.get_weighted_sum_kmap(param)

        else:
            orbital_kmap = weight_sum_data

        if isinstance(slice_, int):
            sliced_kmap = self.get_sliced_kmap(slice_)
            residual = sliced_kmap - orbital_kmap

        else:
            residual = slice_ - orbital_kmap

        residual = self._cut_region(residual)

        return residual

    def get_reduced_chi2(self, slice_index, weight_sum_data=None):

        n = self._get_degrees_of_freedom()
        residual = self.get_residual(
            slice_index, weight_sum_data=weight_sum_data)
        reduced_chi2 = get_reduced_chi2(residual.data, n)

        return reduced_chi2

    def ID_to_orbital(self, ID):

        for orbital in self.orbitals:
            if orbital.ID == ID:
                return orbital

        return None

    def _chi2(self, param=None, slice_=0):

        if param is None:
            param = self.parameters

        residual = self.get_residual(slice_, param)

        return residual.data

    def _get_degrees_of_freedom(self):

        n = 0
        for parameter in self.parameters.values():
            if parameter.vary:
                n += 1

        return n

    def _get_background(self, variables=[]):

        variables.update({'x': self.axis, 'y': np.array([self.axis]).T})
        background = eval(self.background_equation[0], None, variables)

        return background

    def _cut_region(self, data):

        if self.crosshair is None or self.region[0] == 'all':
            return data

        else:
            return self.crosshair.cut_from_data(
                data, region=self.region[0], inverted=self.region[1])

    def _set_sliced_data(self, sliced_data):

        if isinstance(sliced_data, SlicedData):
            self.sliced_data = sliced_data

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

        # LMFit doesn't work when the initial value is exactly the same
        # as the minimum value. For this reason the initial value will
        # be set ever so slightly above 0 to circumvent this problem.
        self.parameters.add('c', value=0,
                            min=0, vary=False, expr=None)
        self.parameters.add('E_kin', value=30,
                            min=5, max=150, vary=False, expr=None)
        for angle in ['alpha', 'beta']:
            self.parameters.add(angle, value=0,
                                min=90, max=-90, vary=False, expr=None)
