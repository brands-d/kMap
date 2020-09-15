# Python Modules
from itertools import chain

# Third Party Imports
from lmfit import minimize, Parameters
import numpy as np
import timeit

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir, pyqtSignal

# Own Imports
from kmap import __directory__
from kmap.library.plotdata import PlotData

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfit.ui')
LMFit_UI, _ = uic.loadUiType(UI_file)


class LMFit(QWidget, LMFit_UI):

    fit_triggered = pyqtSignal()
    region_changed = pyqtSignal()

    def __init__(self, sliced, orbitals):

        self.sliced = sliced
        self.orbitals = orbitals

        # Setup GUI
        super(LMFit, self).__init__()
        self.setupUi(self)
        self._connect()

    def fit(self, variables, parameters, interpolator,
            axis_index=0, slice_index=0, region='all', crosshair=None):

        type_ = self.slice_combobox.currentIndex()
        results = []

        if type_ == 0:
            sliced_data = self.sliced.slice_from_index(slice_index,
                                                       axis_index)
            results.append(self.fit_single_slice(variables, parameters,
                                                 interpolator,
                                                 sliced_data,
                                                 region, crosshair))

        elif type_ == 1:
            for index in range(self.sliced.axes[axis_index].num):
                sliced_data = self.sliced.slice_from_index(index,
                                                           axis_index)
                results.append(self.fit_single_slice(variables,
                                                     parameters,
                                                     interpolator,
                                                     sliced_data,
                                                     region, crosshair))

        else:
            data = np.nansum(self.sliced.data, axis=axis_index)
            range_ = [axis.range for i, axis in enumerate(self.sliced.axes) if i != axis_index]
            sliced_data=PlotData(data, range_)
            results.append(self.fit_single_slice(variables, parameters,
                                                 interpolator,
                                                 sliced_data,
                                                 region, crosshair))

        return results

    def fit_single_slice(self, variables, parameters, interpolator,
                         sliced_data, region = 'all',
                         crosshair = None):

        sliced_data=interpolator.interpolate(sliced_data)
        sliced_data=interpolator.smooth(sliced_data)

        lmfit_param=Parameters()

        for parameter in chain(*variables):
            name, vary, value, min_, max_, expr=parameter

            if expr == '':
                expr=None

            lmfit_param.add(name, value = value, min = min_,
                            max = max_, vary = vary, expr = expr)

        method=self._get_method()

        start_time = timeit.default_timer()

        result=minimize(self.chi2, lmfit_param,
                          args=(sliced_data, parameters,
                                interpolator, crosshair),
                          nan_policy='omit',
                          method=method,
                          xtol=1e-11)

        end_time = timeit.default_timer()
        print('minimize = ',end_time - start_time)

        return result

    def chi2(self, param, sliced_data, other_params, interpolator, crosshair):

        orbital_kmaps = []

        start_time = timeit.default_timer()
        for orbital in self.orbitals:
            ID = orbital.ID

            kmap = orbital.get_kmap(E_kin=param['E_kin'].value,
                                    dk=other_params[3],
                                    phi=param['phi_' + str(ID)].value,
                                    theta=param['theta_' + str(ID)].value,
                                    psi=param['psi_' + str(ID)].value,
                                    alpha=param['alpha_'].value,
                                    beta=param['beta_'].value,
                                    Ak_type=other_params[0],
                                    polarization=other_params[1],
                                    symmetrization=other_params[2])

            orbital_kmaps.append(param['w_' + str(ID)].value * kmap)

        orbital_kmap = np.sum(orbital_kmaps)

        end_time = timeit.default_timer()
        print('get_kmap = ',end_time - start_time)

        orbital_kmap = interpolator.interpolate(orbital_kmap)

        start_time = timeit.default_timer()
        print('interpolate = ',start_time - end_time)

        orbital_kmap = interpolator.smooth(orbital_kmap)

        end_time = timeit.default_timer()
        print('smooth = ',end_time - start_time)


        difference = sliced_data - param['c'].value - orbital_kmap

        difference = self.cut_region(difference, crosshair)

        start_time = timeit.default_timer()
        print('difference = ',start_time - end_time)

        return difference.data

    def cut_region(self, data, crosshair):

        region, inverted = self.get_region()

        if region == 'all':
            return data

        else:
            cut_data = crosshair.model.cut_from_data(
                data, region=region, inverted=inverted)

            return cut_data

    def set_region(self, region, inverted):

        if inverted:
            if region == 'roi':
                index = 3

            elif region == 'ring':
                index = 4

        else:
            if region == 'roi':
                index = 1

            elif region == 'ring':
                index = 2

            else:
                index = 0

        self.region_comboBox.setCurrentIndex(index)

    def get_region(self):

        text = self.region_comboBox.currentText()

        if text == 'Entire kMap':
            region = 'all'
            inverted = False

        elif text == 'Only ROI':
            region = 'roi'
            inverted = False

        elif text == 'Only Annulus':
            region = 'ring'
            inverted = False

        elif text == 'Except ROI':
            region = 'roi'
            inverted = True

        elif text == 'Except Annulus':
            region = 'ring'
            inverted = True

        return region, inverted

    def _get_method(self):

        text = self.method_combobox.currentText()

        return text[text.find("(") + 1:text.find(")")]

    def _connect(self):

        self.fit_button.clicked.connect(self.fit_triggered.emit)
        self.region_comboBox.currentIndexChanged.connect(
            self.region_changed.emit)
