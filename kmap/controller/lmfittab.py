# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QDir

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.controller.dataslider import DataSlider
from kmap.model.lmfittab_model import LMFitTabModel
from kmap.controller.colormap import Colormap
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.interpolation import Interpolation

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

        self.change_slice()
        self.orbital_selected_changed(0)
        self.refresh_sum_plot()

    def change_slice(self, index=-1):

        axis = self.slider.get_axis()
        slice_index = index if index != -1 else self.slider.get_index()
        data = self.model.change_slice(slice_index, axis)

        self.sliced_plot.plot(data)

    def change_axis(self, axis):

        # 'axes' is a copy of all axes except the one with index 'axis'
        axes = [a for i, a in enumerate(self.model.sliced.axes) if i != axis]

        index = self.slider.get_index()
        data = self.model.change_slice(index, axis)

        self.sliced_plot.set_labels(axes[1], axes[0])

        self.sliced_plot.plot(data)

    def orbital_selected_changed(self, index):

        data = self.model.get_selected_orbital_plot(index)

        self.selected_plot.plot(data)

    def get_parameters(self, ID):

        return (1, 30, 0.03,
                0, 0, 0, 'no', 'p', 0, 0, 'auto', 'no')

    def refresh_sum_plot(self):

        data = self.model.get_sum_plot()

        data = self.interpolation.interpolate(data)
        data = self.interpolation.smooth(data)

        self.sum_plot.plot(data)


    def get_title(self):

        return 'LM-Fit'

    def closeEvent(self, event):

        #del self.model

        Tab.closeEvent(self, event)

    def _setup(self):

        self.slider = DataSlider(self.model.sliced)
        self.crosshair = CrosshairAnnulus(self.residual_plot)
        self.colormap = Colormap(
            [self.sliced_plot, self.selected_plot, self.sum_plot])
        self.interpolation = Interpolation()

        layout = QVBoxLayout()
        self.scroll_area.widget().setLayout(layout)
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.colormap)
        layout.insertWidget(2, self.crosshair)
        layout.insertWidget(3, self.interpolation)

    def _connect(self):

        #self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.slider.slice_changed.connect(self.change_slice)
        self.slider.axis_changed.connect(self.change_axis)
        self.interpolation.smoothing_changed.connect(self.change_slice)
        self.interpolation.interpolation_changed.connect(self.change_slice)
