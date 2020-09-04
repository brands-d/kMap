# Python Modules
from itertools import chain

# Third Party Imports
from lmfit import minimize, Parameters, fit_report
import numpy as np

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir, pyqtSignal

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfit.ui')
LMFit_UI, _ = uic.loadUiType(UI_file)


class LMFit(QWidget, LMFit_UI):

    fit_triggered = pyqtSignal()

    def __init__(self, sliced, orbitals):

        self.sliced = sliced
        self.orbitals = orbitals

        # Setup GUI
        super(LMFit, self).__init__()
        self.setupUi(self)
        self._connect()

    def fit(self, variables, parameters, interpolator, axis_index=0, slice_index=0, region='all', crosshair=None):

        if slice_index == -1:
            print('NOT IMPLEMENTED YET')
        else:
            sliced_data = self.sliced.slice_from_index(slice_index,
                                                       axis_index)

        sliced_data = interpolator.interpolate(sliced_data)
        sliced_data = interpolator.smooth(sliced_data)

        lmfit_param = Parameters()

        for parameter in chain(*variables):
            name, vary, value, min_, max_, expr = parameter

            if expr == '':
                expr = None

            lmfit_param.add(name, value=value, min=min_,
                            max=max_, vary=vary, expr=expr)

        method = self._get_method()

        result = minimize(self.chi2, lmfit_param,
                          args=(sliced_data, parameters,
                                interpolator, crosshair),
                          nan_policy='omit',
                          method=method)

        return fit_report(result)

    def chi2(self, param, sliced_data, other_params, interpolator, crosshair):

        orbital_kmaps = []

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

        orbital_kmap = interpolator.interpolate(orbital_kmap)
        orbital_kmap = interpolator.smooth(orbital_kmap)

        difference = sliced_data - param['c'].value - orbital_kmap

        difference = self._cut_region(difference, crosshair)

        return difference.data

    def _cut_region(self, data, crosshair):

        region, inverted = self._get_region()

        if region == 'all':
            return data

        else:
            cut_data = crosshair.cut_from_data(
                data, region=region, inverted=inverted)

            return cut_data

    def _get_region(self):

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
