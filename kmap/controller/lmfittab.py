# Third Party Imports
import numpy as np
from pyqtgraph import ColorMap

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHeaderView
from PyQt5.QtCore import QDir, Qt

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.controller.dataslider import DataSlider
from kmap.model.lmfittab_model import LMFitTabModel
from kmap.controller.colormap import Colormap
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.interpolation import Interpolation
from kmap.controller.lmfittree import LMFitTree

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfittab.ui')
LMFitTab_UI, _ = uic.loadUiType(UI_file)


class LMFitTab(Tab, LMFitTab_UI):

    def __init__(self, sliced_data, orbitals):

        self.model = LMFitTabModel(self, sliced_data, orbitals)

        # Setup GUI
        super(LMFitTab, self).__init__()
        self.setupUi(self)

        self._setup()
        self._connect()

        self.refresh_sliced_plot()
        self.refresh_selected_plot()
        self.refresh_sum_plot()

    def change_slice(self, index=-1):

        slice_index = index if index != -1 else self.slider.get_index()

        self.refresh_sliced_plot()

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
            data = self.model.get_selected_orbital_plot(ID)

            data = self.interpolation.interpolate(data)
            data = self.interpolation.smooth(data)

            self.selected_plot.plot(data)

    def refresh_sum_plot(self):

        data = self.model.get_sum_plot()

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
            data = sliced_data - sum_data
            level = np.nanmax(np.absolute(data.data))

        self.residual_plot.plot(data)
        self.residual_plot.set_levels([-level, level])

    def get_parameters(self, ID):

        return (1, 30, 0.03,
                0, 0, 0, 'no', 'p', 0, 0, 'auto', 'no')

    def get_title(self):

        return 'LM-Fit'

    def closeEvent(self, event):

        del self.model

        Tab.closeEvent(self, event)

    def _setup(self):

        self.slider = DataSlider(self.model.sliced)
        self.crosshair = CrosshairAnnulus(self.residual_plot)
        self.colormap = Colormap(
            [self.sliced_plot, self.selected_plot, self.sum_plot])
        self.interpolation = Interpolation(force_interpolation=True)
        self.tree = LMFitTree(self.model.orbitals)

        colormap = ColorMap(
            [0, 0.5, 1],
            [[255, 0, 0, 255], [255, 255, 255, 255], [0, 0, 255, 255]])
        self.residual_plot.setColorMap(colormap)

        layout = QVBoxLayout()
        self.scroll_area.widget().setLayout(layout)
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.colormap)
        layout.insertWidget(2, self.crosshair)
        layout.insertWidget(3, self.interpolation)

        self.layout.insertWidget(1, self.tree)

    def _connect(self):

        # self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.slider.slice_changed.connect(self.change_slice)
        self.slider.axis_changed.connect(self.change_axis)

        self.interpolation.smoothing_changed.connect(self.refresh_sliced_plot)
        self.interpolation.interpolation_changed.connect(
            self.refresh_sliced_plot)

        self.interpolation.smoothing_changed.connect(
            self.refresh_selected_plot)
        self.interpolation.interpolation_changed.connect(
            self.refresh_selected_plot)

        self.interpolation.smoothing_changed.connect(self.refresh_sum_plot)
        self.interpolation.interpolation_changed.connect(self.refresh_sum_plot)

        self.tree.item_selected.connect(self.refresh_selected_plot)
