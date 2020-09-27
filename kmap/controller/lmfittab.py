"""Defines the LMFit tab and the LMFitResult tab.

This file defines two similar types of tabs: the LMFit and the
LMFitResult tab as well as a common base class LMFitBaseTab.
"""

# Third Party Imports
import numpy as np
from lmfit import Parameters
from pyqtgraph import ColorMap

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import QDir, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

# Own Imports
from kmap import __directory__
from kmap.library.axis import Axis
from kmap.library.qwidgetsub import Tab
from kmap.library.qwidgetsub import CenteredLabel
from kmap.library.misc import get_reduced_chi2
from kmap.model.lmfittab_model import LMFitTabModel
from kmap.controller.dataslider import DataSlider
from kmap.controller.colormap import Colormap
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.interpolation import LMFitInterpolation
from kmap.controller.lmfittree import LMFitTree, LMFitResultTree
from kmap.controller.lmfitresult import LMFitResult
from kmap.controller.lmfit import LMFit
from kmap.controller.lmfitother import LMFitOther


# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfittab.ui')
LMFitTab_UI, _ = uic.loadUiType(UI_file)


class LMFitBaseTab(Tab):
    """
    Base class for LMFit-like tabs.

    Defines a common base class for all LMFit-like tabs. Handles mostly
    the updating of plots.
    """

    def change_axis(self, axis):
        """Changes the axis denoting the slices for the entire tab.

        Args:
            axis (int): Index of the axis to be used as slice values.
                Possible values: 0-2
        """

        # 'axes' is a copy of all axes except the one with index 'axis'
        axes = [a for i, a in enumerate(self.model.sliced.axes) if i != axis]

        self.sliced_plot.set_labels(axes[1], axes[0])

    def refresh_sliced_plot(self):
        print('refresh_sliced_plot')
        index = self.slider.get_index()
        axis = self.slider.get_axis()

        data = self.model.get_sliced_plot(index, axis)

        data = self.interpolation.interpolate(data)

        self.sliced_plot.plot(data)

    def refresh_selected_plot(self):
        print('refresh_selected_plot')
        ID = self.tree.get_selected_orbital_ID()

        if ID == -1:
            self.selected_plot.plot(None)

        else:

            parameters = self._get_parameters(ID)
            data = self.model.get_selected_orbital_plot(ID, parameters)

            data = self.interpolation.interpolate(data)

            self.selected_plot.plot(data)

    def refresh_sum_plot(self):
        print('refresh_sum_plot')
        parameters = []

        for orbital in self.model.orbitals:
            parameters.append(self._get_parameters(orbital.ID))

        data = self.model.get_sum_plot(parameters)

        data = self.interpolation.interpolate(data)

        self.sum_plot.plot(data)

    def refresh_residual_plot(self):

        print('refresh_residual_plot')
        sliced_data = self.model.displayed_slice_data
        sum_data = self.model.displayed_sum_data

        if sliced_data is None or sum_data is None:
            data = None
            level = 1

        else:
            background = self.lmfit.get_background(
                sliced_data.x_axis,
                sliced_data.y_axis) * self.tree._get_background()
            data = sliced_data - sum_data - background
            data = self.lmfit.cut_region(data, self.crosshair)
            level = np.nanmax(np.absolute(data.data))

        self.residual_plot.plot(data)
        self.residual_plot.set_levels([-level, level])

        self.update_chi2_label()

    def update_chi2_label(self):

        residual = self.residual_plot.get_plot_data()

        if residual is None:
            self.residual_label.setText('Residual')

        else:
            n = self.tree.get_number_variables()
            reduced_chi2 = get_reduced_chi2(residual.data, n)
            self.residual_label.setText('Residual (red. Chi^2: %.3E)'
                                        % reduced_chi2)

    def crosshair_changed(self):

        self.crosshair.update_label()

    def closeEvent(self, event):

        del self.model

        Tab.closeEvent(self, event)

    def _setup(self):

        self.slider = DataSlider(self.model.sliced)
        self.crosshair = CrosshairAnnulus(self.residual_plot)
        self.colormap = Colormap(
            [self.sliced_plot, self.selected_plot, self.sum_plot])
        self.lmfit = LMFit(self.model.sliced, self.model.orbitals)

        colormap = ColorMap(
            [0, 0.5, 1],
            [[255, 0, 0, 255], [255, 255, 255, 255], [0, 0, 255, 255]])
        self.residual_plot.setColorMap(colormap)

    def _connect(self):

        self.crosshair.crosshair_changed.connect(self.crosshair_changed)

        self.lmfit.region_changed.connect(self.refresh_residual_plot)

        self.slider.slice_changed.connect(self.refresh_sliced_plot)
        self.slider.slice_changed.connect(self.refresh_selected_plot)
        self.slider.slice_changed.connect(self.refresh_sum_plot)
        self.slider.slice_changed.connect(self.refresh_residual_plot)

        self.slider.axis_changed.connect(self.change_axis)
        self.slider.axis_changed.connect(self.refresh_sliced_plot)
        self.slider.axis_changed.connect(self.refresh_residual_plot)

        self.tree.item_selected.connect(self.refresh_selected_plot)


class LMFitTab(LMFitBaseTab, LMFitTab_UI):

    fit_finished = pyqtSignal(list, tuple, tuple, LMFitInterpolation, tuple)

    def __init__(self, sliced_data, orbitals):

        self.model = LMFitTabModel(sliced_data, orbitals)

        # Setup GUI
        super(LMFitTab, self).__init__()
        self.setupUi(self)

        self._setup()
        self._connect()

        self.refresh_sliced_plot()
        self.refresh_selected_plot()
        self.refresh_sum_plot()
        self.refresh_residual_plot()

    def get_title(self):

        return 'LM-Fit'

    def trigger_fit(self):

        variables = self.tree.get_all_parameters()
        parameters = self.lmfitother.get_parameters()
        axis_index = self.slider.get_axis()
        slice_index = self.slider.get_index()
        other_parameter = self.lmfitother.get_parameters()
        lmfit_parameter = (*self.lmfit.get_region(),
                           self.lmfit.get_background_raw())

        result, type_ = self.lmfit.fit(variables, parameters,
                                       self.interpolation,
                                       axis_index=axis_index,
                                       slice_index=slice_index,
                                       crosshair=self.crosshair)

        meta_parameter = (type_, slice_index, axis_index)

        self.fit_finished.emit(result, other_parameter,
                               meta_parameter, self.interpolation,
                               lmfit_parameter)

    def _get_parameters(self, ID):

        orbital_param = self.tree.get_orbital_parameters(ID)

        orbital_param = [param[2] for param in orbital_param]
        weight, E_kin, *orientation, alpha, beta = orbital_param
        Ak_type, polarization, symmetry, dk = self.lmfitother.get_parameters()
        parameters = [weight, E_kin, dk, *orientation, Ak_type,
                      polarization, alpha, beta, 0, symmetry]

        return parameters

    def _setup(self):

        LMFitBaseTab._setup(self)

        self.lmfitother = LMFitOther()
        self.tree = LMFitTree(self.model.orbitals)
        self.interpolation = LMFitInterpolation()

        layout = QVBoxLayout()
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(3)
        self.scroll_area.widget().setLayout(layout)
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.lmfitother)
        layout.insertWidget(2, self.interpolation)
        layout.insertWidget(3, self.lmfit)
        layout.insertWidget(4, self.colormap)
        layout.insertWidget(5, self.crosshair)

        self.layout.insertWidget(1, self.tree)

    def _connect(self):

        LMFitBaseTab._connect(self)

        plots = [self.refresh_sliced_plot, self.refresh_selected_plot,
                 self.refresh_sum_plot, self.refresh_residual_plot]

        for plot in plots:
            self.interpolation.interpolation_changed.connect(plot)

        self.tree.value_changed.connect(self.refresh_selected_plot)
        self.tree.value_changed.connect(self.refresh_sum_plot)
        self.tree.value_changed.connect(self.refresh_residual_plot)

        self.tree.vary_changed.connect(self.update_chi2_label)

        self.lmfit.fit_triggered.connect(self.trigger_fit)
        self.lmfit.background_changed.connect(self.refresh_residual_plot)

        self.lmfitother.value_changed.connect(self.refresh_selected_plot)
        self.lmfitother.value_changed.connect(self.refresh_sum_plot)
        self.lmfitother.value_changed.connect(self.refresh_residual_plot)


class LMFitResultTab(LMFitBaseTab, LMFitTab_UI):

    open_plot_tab = pyqtSignal(list, list, Axis)

    def __init__(self, results, other_parameter, meta_parameter, sliced_data,
                 orbitals, interpolator, background, region='all', inverted=False):

        self.model = LMFitTabModel(sliced_data, orbitals)
        self.other_parameter = other_parameter
        self.meta_parameter = meta_parameter
        self.title = 'Results'

        # Setup GUI
        super(LMFitResultTab, self).__init__()
        self.setupUi(self)

        self._setup(results, interpolator, background, region, inverted)
        self._connect()

        self.refresh_sliced_plot()
        self.refresh_selected_plot()
        self.refresh_sum_plot()
        self.refresh_residual_plot()

    def update_result_tree(self):

        index = self.slider.get_index()

        self.tree.update_result(self.result.get_index(index))

    def print_result(self):

        index = self.slider.get_index()
        report = self.result.get_fit_report(index)

        print(report)

    def print_covariance_matrix(self):

        index = self.slider.get_index()
        cov_matrix = self.result.get_covariance_matrix(index)

        print(cov_matrix)

    def plot(self):

        self.open_plot_tab.emit(self.result.results, self.model.orbitals,
                                self.model.sliced.axes[self.meta_parameter[2]])

    def _get_parameters(self, ID):

        orbital_param = self.tree.get_orbital_parameters(ID)

        weight, E_kin, *orientation, alpha, beta = orbital_param
        Ak_type, polarization, symmetry, dk = self.other_parameter
        parameters = [weight, E_kin, dk, *orientation, Ak_type,
                      polarization, alpha, beta, 0, symmetry]

        return parameters

    def _setup(self, results, interpolator, background, region, inverted):

        LMFitBaseTab._setup(self)

        self.result = LMFitResult(results, *self.meta_parameter[:2])
        self.tree = LMFitResultTree(
            self.model.orbitals, self.result.get_index(0))
        self.interpolation = interpolator

        layout = QVBoxLayout()
        self.scroll_area.widget().setLayout(layout)
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.result)
        layout.insertWidget(3, self.colormap)
        layout.insertWidget(4, self.crosshair)

        self.layout.insertWidget(1, self.tree)

        self.lmfit.set_region(region, inverted)
        self.lmfit.set_background(background)

    def _connect(self):

        self.slider.slice_changed.connect(self.update_result_tree)
        self.result.print_triggered.connect(self.print_result)
        self.result.cov_matrix_requested.connect(self.print_covariance_matrix)
        self.result.plot_requested.connect(self.plot)

        LMFitBaseTab._connect(self)
