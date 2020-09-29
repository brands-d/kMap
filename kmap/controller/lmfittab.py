"""Defines the LMFit tab and the LMFitResult tab.

This file defines two similar types of tabs: the LMFit and the
LMFitResult tab as well as a common base class LMFitBaseTab.
"""

# Third Party Imports
import numpy as np

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import QDir, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

# Own Imports
from kmap import __directory__
from kmap.library.axis import Axis
from kmap.library.qwidgetsub import Tab
from kmap.model.lmfit_model import LMFitModel
from kmap.controller.dataslider import DataSlider
from kmap.controller.colormap import Colormap
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.interpolation import LMFitInterpolation
from kmap.controller.lmfittree import LMFitTree, LMFitResultTree
from kmap.controller.lmfitresult import LMFitResult
from kmap.controller.lmfitoptions import LMFitOptions
from kmap.controller.lmfitorbitaloptions import LMFitOrbitalOptions

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfittab.ui')
LMFitTab_UI, _ = uic.loadUiType(UI_file)


class LMFitBaseTab(Tab):

    def refresh_sliced_plot(self):

        index = self.slider.get_index()
        kmap = self.model.get_sliced_kmap(index)

        self.sliced_plot.plot(kmap)

    def refresh_selected_plot(self, param=None):

        ID = self.tree.get_selected_orbital_ID()

        if ID == -1:
            self.selected_plot.plot(None)

        else:
            kmap = self.model.get_orbital_kmap(ID, param)
            self.selected_plot.plot(kmap)

    def refresh_sum_plot(self, param=None):

        kmap = self.model.get_weighted_sum_kmap(param)
        self.sum_plot.plot(kmap)

    def refresh_residual_plot(self, param=None):

        index = self.slider.get_index()
        residual = self.model.get_residual(index, param)

        self.residual_plot.plot(residual)

        level = np.nanmax(np.absolute(residual.data))
        self.residual_plot.set_levels([-level, level])

        self.update_chi2_label()

    def update_chi2_label(self):

        slice_index = self.slider.get_index()
        reduced_chi2 = self.model.get_reduced_chi2(slice_index)
        self.residual_label.setText('Residual (red. Chi^2: %.3E)'
                                    % reduced_chi2)

    def closeEvent(self, event):

        del self.model

        Tab.closeEvent(self, event)

    def _refresh_orbital_plots(self):

        self.refresh_selected_plot()
        self.refresh_sum_plot()
        self.refresh_residual_plot()

    def _setup(self):

        self.slider = DataSlider(self.model.sliced_data)
        self.crosshair = CrosshairAnnulus(self.residual_plot)
        self.colormap = Colormap(
            [self.sliced_plot, self.selected_plot, self.sum_plot])
        residual_colormap = Colormap(self.residual_plot)

        residual_colormap.set_colormap('blueAndRed')

    def _connect(self):

        self.crosshair.crosshair_changed.connect(self.crosshair.update_label)

        self.slider.slice_changed.connect(self.change_slice)
        self.slider.axis_changed.connect(self.change_slice)

        self.tree.item_selected.connect(self.refresh_selected_plot)


class LMFitTab(LMFitBaseTab, LMFitTab_UI):

    fit_finished = pyqtSignal(list, list, dict)

    def __init__(self, sliced_data, orbitals):

        self.model = LMFitModel(sliced_data, orbitals)

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

        results = self.model.fit()
        settings = self.model.get_settings()
        data = [self.model.sliced_data, self.model.orbitals]
        self.fit_finished.emit(data, results, settings)

    def change_slice(self):

        axis_index = self.slider.get_axis()
        slice_policy = self.lmfit_options.get_slice_policy()
        combined = True if slice_policy == 'all combined' else False
        slice_indices = (self.slider.get_index()
                         if slice_policy == 'only one' else 'all')

        self.model.set_slices(
            slice_indices, axis_index=axis_index, combined=combined)

        self.refresh_sliced_plot()
        self.refresh_residual_plot()

    def change_axis(self):

        axis = self.interpolation.get_axis()
        self.model.set_axis(axis)

        self.refresh_sliced_plot()
        self.refresh_selected_plot()
        self.refresh_sum_plot()
        self.refresh_residual_plot()

    def _change_slice_policy(self, slice_policy):

        axis = self.slider.get_axis()

        if slice_policy == 'all':
            self.model.set_slices('all', axis_index=axis, combined=False)

        elif slice_policy == 'only one':
            index = self.slider.get_index()
            self.model.set_slices([index], axis_index=axis, combined=False)

        else:
            self.model.set_slices('all', axis_index=axis, combined=True)

    def _change_region(self, *args):

        self.model.set_region(*args)
        self.refresh_residual_plot()

    def _change_background(self, *args):

        self.model.set_background_equation(*args)
        self.refresh_sum_plot()
        self.refresh_residual_plot()

    def _setup(self):

        LMFitBaseTab._setup(self)

        self.orbital_options = LMFitOrbitalOptions()
        self.tree = LMFitTree(self.model.orbitals, self.model.parameters)
        self.interpolation = LMFitInterpolation()
        self.lmfit_options = LMFitOptions()

        self.model.set_crosshair(self.crosshair.model)

        layout = QVBoxLayout()
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(3)
        self.scroll_area.widget().setLayout(layout)
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.orbital_options)
        layout.insertWidget(2, self.interpolation)
        layout.insertWidget(3, self.lmfit_options)
        layout.insertWidget(4, self.colormap)
        layout.insertWidget(5, self.crosshair)

        self.layout.insertWidget(1, self.tree)

    def _connect(self):

        LMFitBaseTab._connect(self)

        self.interpolation.interpolation_changed.connect(self.change_axis)

        self.tree.value_changed.connect(self._refresh_orbital_plots)
        self.tree.vary_changed.connect(self.update_chi2_label)
        self.lmfit_options.background_changed.connect(self._change_background)
        self.lmfit_options.fit_triggered.connect(self.trigger_fit)
        self.lmfit_options.method_changed.connect(self.model.set_fit_method)
        self.lmfit_options.slice_policy_changed.connect(
            self._change_slice_policy)

        self.orbital_options.symmetrization_changed.connect(
            self.model.set_symmetrization)
        self.orbital_options.symmetrization_changed.connect(
            self._refresh_orbital_plots)
        self.orbital_options.polarization_changed.connect(
            self.model.set_polarization)
        self.orbital_options.polarization_changed.connect(
            self._refresh_orbital_plots)


class LMFitResultTab(LMFitBaseTab, LMFitTab_UI):

    open_plot_tab = pyqtSignal(list, list, Axis)

    def __init__(self, data, results, settings):

        self.results = results
        self.current_result = self.results[0]

        self.model = LMFitModel(*data)
        self.model.set_settings(settings)

        # Setup GUI
        super(LMFitResultTab, self).__init__()
        self.setupUi(self)

        self._setup()
        self._connect()

        self.refresh_sliced_plot()
        self.refresh_selected_plot()
        self.refresh_sum_plot()
        self.refresh_residual_plot()

    def get_title(self):

        return 'Results'

    def change_slice(self):

        index = self.slider.get_index()

        self.current_result = self.results[0] if len(
            self.results) == 1 else self.results[index]

        self.update_tree()
        self.result.result = self.current_result[1]
        self.refresh_sliced_plot()
        self._refresh_orbital_plots()

    def refresh_selected_plot(self):

        params = self.current_result[1].params
        super().refresh_selected_plot(params)

    def refresh_sum_plot(self):

        params = self.current_result[1].params
        super().refresh_sum_plot(params)

    def refresh_residual_plot(self):

        params = self.current_result[1].params
        super().refresh_residual_plot(params)

    def update_tree(self):

        params = self.current_result[1].params
        self.tree.update_result(params)

    def print_result(self):

        report = self.result.get_fit_report()

        print(report)

    def print_covariance_matrix(self):

        cov_matrix = self.result.get_covariance_matrix()

        print(cov_matrix)

    def plot(self):

        results = [result[1] for result in self.results]
        orbitals = self.model.orbitals
        axis = self.model.sliced_data.axes[self.model.slice_policy[0]]
        self.open_plot_tab.emit(results, orbitals, axis)

    def _setup(self):

        LMFitBaseTab._setup(self)

        self.result = LMFitResult(self.current_result[1], self.model)
        self.tree = LMFitResultTree(
            self.model.orbitals, self.current_result[1].params)
        self.crosshair._set_model(self.model.crosshair)

        layout = QVBoxLayout()
        self.scroll_area.widget().setLayout(layout)
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.result)
        layout.insertWidget(3, self.colormap)
        layout.insertWidget(4, self.crosshair)

        self.layout.insertWidget(1, self.tree)

    def _connect(self):

        self.slider.slice_changed.connect(self.change_slice)
        self.result.print_triggered.connect(self.print_result)
        self.result.cov_matrix_requested.connect(self.print_covariance_matrix)
        self.result.plot_requested.connect(self.plot)

        LMFitBaseTab._connect(self)
