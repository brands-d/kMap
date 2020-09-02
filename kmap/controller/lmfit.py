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

    def fit(self, parameters, interpolator, axis_index=0, slice_index=0):

        if slice_index == -1:
            print('NOT IMPLEMENTED YET')
        else:
            sliced_data = self.sliced.slice_from_index(slice_index,
                                                       axis_index)

        sliced_data = interpolator.interpolate(sliced_data)
        sliced_data = interpolator.smooth(sliced_data)

        lmfit_param = Parameters()

        for parameter in chain(*parameters):
            name, vary, value, min_, max_, expr = parameter

            if expr == '':
                expr = None

            lmfit_param.add(name, value=value, min=min_,
                            max=max_, vary=vary, expr=expr)

        result = minimize(self.chi2, lmfit_param,
                          args=(sliced_data, interpolator),
                          nan_policy='omit')

        return fit_report(result)

    def chi2(self, param, sliced_data, interpolator):

        orbital_kmaps = []

        for orbital in self.orbitals:
            ID = orbital.ID

            kmap = orbital.get_kmap(E_kin=param['E_kin'].value,
                                    phi=param['phi_' + str(ID)].value,
                                    theta=param['theta_' + str(ID)].value,
                                    psi=param['psi_' + str(ID)].value,
                                    alpha=param['alpha_'].value,
                                    beta=param['beta_'].value)

            orbital_kmaps.append(param['w_' + str(ID)].value * kmap)

        orbital_kmap = np.sum(orbital_kmaps)

        orbital_kmap = interpolator.interpolate(orbital_kmap)
        orbital_kmap = interpolator.smooth(orbital_kmap)

        difference = sliced_data - param['c'].value - orbital_kmap

        return difference.data

    def _connect(self):

        self.fit_button.clicked.connect(self.fit_triggered.emit)
