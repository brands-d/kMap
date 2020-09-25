# Python Modules
from itertools import chain

# Third Party Imports
from lmfit import minimize, Parameters
import numpy as np

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir, pyqtSignal

# Own Imports
from kmap import __directory__
from kmap.library.plotdata import PlotData
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfit.ui')
LMFit_UI, _ = uic.loadUiType(UI_file)


class LMFit(QWidget, LMFit_UI):

    fit_triggered = pyqtSignal()
    region_changed = pyqtSignal()
    background_changed = pyqtSignal()

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
            type_ = 'Only One Slice'

        elif type_ == 1:
            for index in range(self.sliced.axes[axis_index].num):
                sliced_data = self.sliced.slice_from_index(index,
                                                           axis_index)
                results.append(self.fit_single_slice(variables,
                                                     parameters,
                                                     interpolator,
                                                     sliced_data,
                                                     region, crosshair))
            type_ = 'All Slices Individually'

        else:
            data = np.nansum(self.sliced.data, axis=axis_index)
            range_ = [axis.range for i, axis in enumerate(
                self.sliced.axes) if i != axis_index]
            sliced_data = PlotData(data, range_)
            results.append(self.fit_single_slice(variables, parameters,
                                                 interpolator,
                                                 sliced_data,
                                                 region, crosshair))
            type_ = 'All Slices Combined'

        return results, type_

    def fit_single_slice(self, variables, parameters, interpolator,
                         sliced_data, region='all',
                         crosshair=None):

        sliced_data = interpolator.interpolate(sliced_data)

        lmfit_param = Parameters()

        for parameter in chain(*variables):
            name, vary, value, min_, max_, expr = parameter

            if expr == '':
                expr = None

            lmfit_param.add(name, value=value, min=min_,
                            max=max_, vary=vary, expr=expr)

        method = self._get_method()
        xtol = float(config.get_key('lmfit', 'xtol'))
        background = self.get_background(
            sliced_data.x_axis, sliced_data.y_axis)

        result = minimize(self.chi2, lmfit_param,
                          args=(sliced_data, parameters,
                                interpolator, crosshair, background),
                          nan_policy='omit',
                          method=method,
                          xtol=xtol)

        return result

    def chi2(self, param, sliced_data, other_params, interpolator, crosshair, background=1):

        orbital_kmaps = []
        axes = interpolator.get_axes()

        for orbital in self.orbitals:
            ID = orbital.ID

            kmap = orbital.get_kmap(E_kin=param['E_kin'].value,
                                    dk=tuple(axes),
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

        difference = sliced_data - background * param['c'].value - orbital_kmap

        difference = self.cut_region(difference, crosshair)

        return difference.data

    def cut_region(self, data, crosshair):

        region, inverted = self.get_region()

        if region == 'all':
            return data

        else:
            cut_data = crosshair.model.cut_from_data(
                data, region=region, inverted=inverted)

            return cut_data

    def get_background(self, x, y):

        equation = self.line_edit.text()

        # Set empty equation to constant background
        if not equation:
            equation = '1'

        try:
            # Wrap y-axis to transpose -> meshgrid like multiplicaltion
            local = {'x': x, 'y': np.array([y]).T}
            background = eval(equation, None, local)

            return background

        except Exception as e:
            print(e)

    def get_background_raw(self):

        return self.line_edit.text()

    def set_background(self, equation):

        self.line_edit.blockSignals(True)
        self.line_edit.setText(equation)
        self.line_edit.blockSignals(False)

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
        self.line_edit.returnPressed.connect(self.background_changed.emit)
