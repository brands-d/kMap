"""Defines the LMFit tab and the LMFitResult tab.

This file defines two similar types of tabs: the LMFit and the
LMFitResult tab as well as a common base class LMFitBaseTab.
"""
# Python Imports
import logging

# Third Party Imports
import h5py
import numpy as np

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog

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
from kmap.controller.matplotlibwindow import MatplotlibImageWindow
from kmap.controller.lmfitresult import LMFitResult
from kmap.controller.lmfitoptions import LMFitOptions
from kmap.controller.lmfitorbitaloptions import LMFitOrbitalOptions
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ / 'ui/lmfittab.ui'
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

        return kmap

    def refresh_residual_plot(self, param=None, weight_sum_data=None):
        index = self.slider.get_index()
        residual = self.model.get_residual(index, param, weight_sum_data)

        level = np.nanmax(np.absolute(residual.data))

        if config.get_key('pyqtgraph', 'keep_max_level_residual') == 'True':
            old_level = np.nanmax(np.absolute(self.residual_plot.get_levels()))

            if old_level != 1 and old_level > level:
                level = old_level

        self.residual_plot.plot(residual)

        self.residual_plot.set_levels([-level, level])

        self.update_chi2_label(weight_sum_data)

    def refresh_all(self):

        self.refresh_sliced_plot()
        self.refresh_selected_plot()
        kmap = self.refresh_sum_plot()
        self.refresh_residual_plot(weight_sum_data=kmap)

    def update_chi2_label(self, weight_sum_data=None):
        slice_index = self.slider.get_index()
        reduced_chi2 = self.model.get_reduced_chi2(
            slice_index, weight_sum_data)
        self.residual_label.setText('Residual (red. Chi^2: %.3E)'
                                    % reduced_chi2)

    def display_in_matplotlib(self):
        windows = []

        for plot in [self.residual_plot, self.sum_plot, self.sliced_plot, self.selected_plot]:
            data = plot.model.plot_data
            LUT = plot.get_LUT()
            windows.append(MatplotlibImageWindow(data, LUT=LUT))

        return windows

    def transpose(self, constant_axis):
        self.model.transpose(constant_axis)
        self.refresh_sliced_plot()
        self.refresh_residual_plot()

    def change_symmetry(self, symmetry, mirror):
        self.model.set_sliced_symmetrization(symmetry, mirror)
        self.refresh_sliced_plot()
        self.refresh_residual_plot()

    def closeEvent(self, event):
        del self.model

        Tab.closeEvent(self, event)

    def _refresh_orbital_plots(self):
        self.refresh_selected_plot()
        kmap = self.refresh_sum_plot()
        self.refresh_residual_plot(weight_sum_data=kmap)

    def _setup(self):
        self.slider = DataSlider(self.model.sliced_data)
        self.crosshair = CrosshairAnnulus(self.residual_plot)
        self.colormap = Colormap(
            [self.sliced_plot, self.selected_plot, self.sum_plot])
        residual_colormap = Colormap(self.residual_plot)

        residual_colormap.set_colormap('blueAndRed')

    def _connect(self):
        self.crosshair.crosshair_changed.connect(self.crosshair.update_label)
        self.crosshair.crosshair_changed.connect(self.refresh_all)

        self.slider.slice_changed.connect(self.change_slice)
        self.slider.axis_changed.connect(self.change_slice)
        self.slider.tranpose_triggered.connect(self.transpose)
        self.slider.symmetry_changed.connect(self.change_symmetry)

        self.tree.item_selected.connect(self.refresh_selected_plot)


class LMFitTab(LMFitBaseTab, LMFitTab_UI):
    fit_finished = pyqtSignal(list, dict)

    def __init__(self, sliced_tab, orbital_tab):
        self.sliced_tab = sliced_tab
        self.orbital_tab = orbital_tab
        self.model = LMFitModel(sliced_tab.get_data(),
                                orbital_tab.get_orbitals())
        s_share = float(config.get_key('orbital', 's_share'))
        self.model.set_s_share(s_share)

        # Setup GUI
        super(LMFitTab, self).__init__()
        self.setupUi(self)

        self._setup()
        self._connect()

        self.refresh_all()

    @classmethod
    def init_from_save(cls, save, sliced_data, orbitals):
        tab = LMFitTab(sliced_data, orbitals)
        tab.title = save['title']

        tab.slider.restore_state(save['slider']),
        tab.crosshair.restore_state(save['crosshair']),
        tab.orbital_options.restore_state(save['orbital_options']),
        tab.interpolation.restore_state(save['interpolation']),
        tab.lmfit_options.restore_state(save['lmfit_options'])
        tab.tree.restore_state(save['tree'])

        return tab

    def get_title(self):
        return self.title

    def get_data(self):
        return [self.model.sliced_data, self.model.orbitals]

    def trigger_fit(self):
        try:
            results = self.model.fit()

        except ValueError as e:
            logging.getLogger('kmap').warning(str(e))
            self.lmfit_options.update_fit_button()

            return

        settings = self.model.get_settings()

        self.fit_finished.emit(results, settings)

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

        self.refresh_all()

    def save_state(self):
        save = {'title': self.title,
                'slider': self.slider.save_state(),
                'crosshair': self.crosshair.save_state(),
                'orbital_options': self.orbital_options.save_state(),
                'interpolation': self.interpolation.save_state(),
                'lmfit_options': self.lmfit_options.save_state(),
                'tree': self.tree.save_state()}

        return save, [self.sliced_tab, self.orbital_tab]

    def _change_slice_policy(self, slice_policy):
        axis = self.slider.get_axis()

        if slice_policy == 'all':
            self.model.set_slices('all', axis_index=axis, combined=False)

        elif slice_policy == 'only one':
            index = self.slider.get_index()
            self.model.set_slices([index], axis_index=axis, combined=False)

        else:
            self.model.set_slices('all', axis_index=axis, combined=True)

    def _change_method(self, method):

        self._change_to_matrix_state(method == 'matrix_inversion')

        self.model.set_fit_method(method)

    def _change_to_matrix_state(self, state):

        if state:
            variables = self.model.background_equation[1]
            if 'c' not in variables:
                self.lmfit_options._pre_factor_background()

        self.tree._change_to_matrix_state(state)

    def _change_region(self, *args):
        self.model.set_region(*args)

        self.refresh_all()

    def _change_background(self, *args):

        new_variables = self.model.set_background_equation(*args)
        for variable in new_variables:
            self.tree.add_equation_parameter(variable)

        self.refresh_sum_plot()
        self.refresh_residual_plot()

    def _setup(self):
        LMFitBaseTab._setup(self)

        self.orbital_options = LMFitOrbitalOptions()
        self.tree = LMFitTree(self.model.orbitals, self.model.parameters)
        self.interpolation = LMFitInterpolation()
        self.lmfit_options = LMFitOptions(self)

        self.change_axis()
        self.model.set_crosshair(self.crosshair.model)
        self._change_background(self.lmfit_options.get_background())

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
        self.lmfit_options.method_changed.connect(self._change_method)
        self.lmfit_options.slice_policy_changed.connect(
            self._change_slice_policy)
        self.lmfit_options.region_changed.connect(self._change_region)

        self.orbital_options.symmetrization_changed.connect(
            self.model.set_symmetrization)
        self.orbital_options.symmetrization_changed.connect(
            self._refresh_orbital_plots)
        self.orbital_options.polarization_changed.connect(
            self.model.set_polarization)
        self.orbital_options.polarization_changed.connect(
            self._refresh_orbital_plots)


class LMFitResultTab(LMFitBaseTab, LMFitTab_UI):
    open_plot_tab = pyqtSignal(list, list, Axis, list, list)

    def __init__(self, lmfit_tab, results, settings):
        self.results = results
        self.lmfit_tab = lmfit_tab
        self.current_result = self.results[0]
        self.settings = settings

        self.model = LMFitModel(*self.lmfit_tab.get_data())
        self.model.set_settings(settings)

        # Setup GUI
        super(LMFitResultTab, self).__init__()
        self.setupUi(self)

        self._setup()
        self._connect()

        self.refresh_all()

    @classmethod
    def init_from_save(cls, save, tab, ID_map=None):
        results = save['results']

        if ID_map is not None:
            for result in results:
                result = LMFitResultTab._apply_ID_map(result[1], ID_map)

        settings = save['settings']

        tab = LMFitResultTab(tab, results, settings)

        return tab

    @classmethod
    def _apply_ID_map(cls, result, ID_map):
        params = result.params
        new_params = params.copy()

        for map_ in ID_map:
            for parameter in params.items():
                old_name, parameter = parameter

                if old_name.endswith(str(map_[0])):
                    new_name = '_'.join(old_name.split(
                        '_')[:-1]) + '_' + str(map_[1])
                    new_params[new_name] = new_params[old_name]

                    if old_name != new_name:
                        del new_params[old_name]

        result.params = new_params
        return result

    def save_state(self):
        save = {'title': self.title,
                'results': self.results,
                'settings': self.settings}

        return save, [self.lmfit_tab]

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
        return super().refresh_sum_plot(params)

    def refresh_residual_plot(self, weight_sum_data=None):
        params = self.current_result[1].params
        super().refresh_residual_plot(params, weight_sum_data)

    def update_tree(self):
        params = self.current_result[1].params
        self.tree.update_result(params)

    def print_result(self):
        report = self.result.get_fit_report()

        print(report)

    def print_covariance_matrix(self):
        cov_matrix = self.result.get_covariance_matrix()

        print(cov_matrix)

    def get_orbitals(self):
        return self.model.orbitals

    def plot(self):
        results = [result[1] for result in self.results]
        orbitals = self.model.orbitals
        axis = self.model.sliced_data.axes[self.model.slice_policy[0]]
        kmaps = abs(self.get_residual_kmaps())
        residuals = list(np.nansum(np.nansum(kmaps, axis=1), axis=1))

        self.open_plot_tab.emit(results, orbitals, axis, residuals,
                                self.model.background_equation[1])

    def export_to_hdf5(self):
        path = config.get_key('paths', 'hdf5_export_start')
        if path == 'None':
            file_name, _ = QFileDialog.getSaveFileName(
                None, 'Save .hdf5 File (*.hdf5)')
        else:
            start_path = str(__directory__ / path)
            file_name, _ = QFileDialog.getSaveFileName(
                None, 'Save .hdf5 File (*.hdf5)', str(start_path))

        if not file_name:
            return
        else:
            h5file = h5py.File(file_name, 'w')

        kmaps = self.get_residual_kmaps()

        slice_axis = self.slider.data.axes[0]
        x_axis = self.slider.data.axes[1]
        y_axis = self.slider.data.axes[2]

        h5file.create_dataset('name', data='Residual')
        h5file.create_dataset('axis_1_label', data=slice_axis.label)
        h5file.create_dataset('axis_2_label', data=x_axis.label)
        h5file.create_dataset('axis_3_label', data=y_axis.label)
        h5file.create_dataset('axis_1_units', data=slice_axis.units)
        h5file.create_dataset('axis_2_units', data=x_axis.units)
        h5file.create_dataset('axis_3_units', data=y_axis.units)
        h5file.create_dataset('axis_1_range', data=slice_axis.range)
        h5file.create_dataset('axis_2_range', data=x_axis.range)
        h5file.create_dataset('axis_3_range', data=y_axis.range)
        h5file.create_dataset('data', data=kmaps, dtype='f8',
                              compression='gzip', compression_opts=9)
        h5file.close()

    def get_residual_kmaps(self):
        kmaps = []
        for i, result in enumerate(self.results):
            residual = self.model.get_residual(i, result[1].params)
            kmaps.append(residual.data)
        kmaps = np.array(kmaps)

        return kmaps

    def _setup(self):
        LMFitBaseTab._setup(self)

        self.result = LMFitResult(self.current_result[1], self.model)
        self.tree = LMFitResultTree(
            self.model.orbitals, self.current_result[1].params,
            self.model.background_equation[1])
        self.crosshair._set_model(self.model.crosshair)

        layout = QVBoxLayout()
        self.scroll_area.widget().setLayout(layout)
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.result)
        layout.insertWidget(3, self.colormap)
        layout.insertWidget(4, self.crosshair)

        self.layout.insertWidget(1, self.tree)

    def _connect(self):
        self.result.print_triggered.connect(self.print_result)
        self.result.cov_matrix_requested.connect(self.print_covariance_matrix)
        self.result.plot_requested.connect(self.plot)

        LMFitBaseTab._connect(self)
