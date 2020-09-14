# Third Party Imports
import numpy as np
from pyqtgraph import ColorMap
from lmfit import Parameters
from lmfit.minimizer import MinimizerResult

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QDir, pyqtSignal, Qt

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.library.misc import get_reduced_chi2
from kmap.controller.dataslider import DataSlider
from kmap.model.lmfittab_model import LMFitTabModel
from kmap.controller.colormap import Colormap
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.interpolation import Interpolation
from kmap.controller.lmfittree import LMFitTree
from kmap.controller.lmfit import LMFit
from kmap.controller.lmfitother import LMFitOther
from kmap.library.qwidgetsub import CenteredLabel

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfittab.ui')
LMFitTab_UI, _ = uic.loadUiType(UI_file)


class LMFitBaseTab(Tab):

    def get_title(self):

        return self.title

    def set_title(self, title):

        self.title = title

    def change_axis(self, axis):

        # 'axes' is a copy of all axes except the one with index 'axis'
        axes = [a for i, a in enumerate(self.model.sliced.axes) if i != axis]

        self.sliced_plot.set_labels(axes[1], axes[0])

        self.refresh_sliced_plot()

    def refresh_sliced_plot(self):

        index = self.slider.get_index()
        axis = self.slider.get_axis()

        data = self.model.get_sliced_plot(index, axis)

        data = self.interpolation.interpolate(data)
        data = self.interpolation.smooth(data)

        self.sliced_plot.plot(data)

        self.refresh_residual_plot()

    def refresh_selected_plot(self):

        ID = self.tree.get_selected_orbital_ID()

        if ID == -1:
            self.selected_plot.plot(None)

        else:

            parameters = self._get_parameters(ID)
            data = self.model.get_selected_orbital_plot(ID, parameters)

            data = self.interpolation.interpolate(data)
            data = self.interpolation.smooth(data)

            self.selected_plot.plot(data)

    def refresh_sum_plot(self):

        parameters = []

        for orbital in self.model.orbitals:
            parameters.append(self._get_parameters(orbital.ID))

        data = self.model.get_sum_plot(parameters)

        data = self.interpolation.interpolate(data)
        data = self.interpolation.smooth(data)

        self.sum_plot.plot(data)

        self.refresh_residual_plot()

    def refresh_residual_plot(self):

        sliced_data = self.model.displayed_slice_data
        sum_data = self.model.displayed_sum_data

        if sliced_data is None or sum_data is None:
            data = None
            level = 1

        else:
            data = sliced_data - sum_data - self.tree._get_background()
            data = self.lmfit.cut_region(data, self.crosshair)
            level = np.nanmax(np.absolute(data.data))

        self.residual_plot.plot(data)
        self.residual_plot.set_levels([-level, level])

        self.update_chi2_label()

    def update_chi2_label(self):

        residual = self.residual_plot.get_plot_data()

        if residual is None:
            self.chi2_value.setText('')

        else:
            n = self.tree.get_number_variables()
            reduced_chi2 = get_reduced_chi2(residual.data, n)

            self.chi2_value.setText('%.3f' % reduced_chi2)

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
        self.interpolation = Interpolation(force_interpolation=True)
        self.lmfit = LMFit(self.model.sliced, self.model.orbitals)
        self.chi2_value = CenteredLabel('')
        self.chi2_label = CenteredLabel('Reduced Chi^2:')
        self.chi2_widget = QWidget()
        layout = QHBoxLayout()
        self.chi2_widget.setLayout(layout)
        layout.addWidget(self.chi2_label)
        layout.addWidget(self.chi2_value)

        colormap = ColorMap(
            [0, 0.5, 1],
            [[255, 0, 0, 255], [255, 255, 255, 255], [0, 0, 255, 255]])
        self.residual_plot.setColorMap(colormap)

    def _connect(self):

        self.crosshair.crosshair_changed.connect(self.crosshair_changed)

        self.slider.slice_changed.connect(self.refresh_sliced_plot)
        self.slider.axis_changed.connect(self.change_axis)

        self.tree.item_selected.connect(self.refresh_selected_plot)


class LMFitTab(LMFitBaseTab, LMFitTab_UI):

    fit_finished = pyqtSignal(MinimizerResult, tuple, tuple)

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

    def get_title(self):

        return 'LM-Fit'

    def trigger_fit(self):

        variables = self.tree.get_all_parameters()
        parameters = self.lmfitother.get_parameters()
        axis_index = self.slider.get_axis()
        slice_index = self.slider.get_index()
        other_parameter = self.lmfitother.get_parameters()
        region = self.lmfit.get_region()

        result = self.lmfit.fit(variables, parameters,
                                self.interpolation,
                                axis_index=axis_index,
                                slice_index=slice_index,
                                crosshair=self.crosshair)

        self.fit_finished.emit(result, other_parameter, region)

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

        layout = QVBoxLayout()
        self.scroll_area.widget().setLayout(layout)
        layout.insertWidget(0, self.lmfit)
        layout.insertWidget(1, self.slider)
        layout.insertWidget(2, self.chi2_widget)
        layout.insertWidget(3, self.lmfitother)
        layout.insertWidget(4, self.colormap)
        layout.insertWidget(5, self.crosshair)
        layout.insertWidget(6, self.interpolation)

        self.layout.insertWidget(1, self.tree)

    def _connect(self):

        LMFitBaseTab._connect(self)

        self.interpolation.smoothing_changed.connect(self.refresh_sliced_plot)
        self.interpolation.interpolation_changed.connect(
            self.refresh_sliced_plot)

        self.interpolation.smoothing_changed.connect(
            self.refresh_selected_plot)
        self.interpolation.interpolation_changed.connect(
            self.refresh_selected_plot)

        self.interpolation.smoothing_changed.connect(self.refresh_sum_plot)
        self.interpolation.interpolation_changed.connect(self.refresh_sum_plot)

        self.tree.value_changed.connect(self.refresh_selected_plot)
        self.tree.value_changed.connect(self.refresh_sum_plot)
        self.tree.value_changed.connect(self.refresh_residual_plot)
        self.tree.vary_changed.connect(self.update_chi2_label)

        self.lmfit.fit_triggered.connect(self.trigger_fit)

        self.lmfitother.value_changed.connect(self.refresh_selected_plot)
        self.lmfitother.value_changed.connect(self.refresh_sum_plot)
        self.lmfitother.value_changed.connect(self.refresh_residual_plot)
