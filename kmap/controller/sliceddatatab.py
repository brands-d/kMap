# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import QDir

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.model.sliceddatatab_model import SlicedDataTabModel
from kmap.controller.matplotlibwindow import MatplotlibWindow
from kmap.controller.interpolation import Interpolation
from kmap.controller.dataslider import DataSlider
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.controller.colormap import Colormap


# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/sliceddatatab.ui')
SlicedDataTab_UI, _ = uic.loadUiType(UI_file)


class SlicedDataTab(Tab, SlicedDataTab_UI):

    def __init__(self, model):

        self.model = model

        # Setup GUI
        super(SlicedDataTab, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect()

        self.change_axis(0)
        self.change_slice(0)

    @classmethod
    def init_from_URLs(cls, URLs):

        model = SlicedDataTabModel()
        model.load_data_from_URLs(URLs)

        return cls(model)

    @classmethod
    def init_from_URL(cls, URL):

        model = SlicedDataTabModel()
        model.load_data_from_URL(URL)

        return cls(model)

    @classmethod
    def init_from_cube(cls, URL):

        model = SlicedDataTabModel()
        model.load_data_from_cube(URL)

        return cls(model)
        
    @classmethod
    def init_from_path(cls, path):

        model = SlicedDataTabModel()
        model.load_data_from_path(path)

        return cls(model)

    def get_data(self):

        return self.model.data

    def change_slice(self, index=-1):

        axis = self.slider.get_axis()
        slice_index = index if index != -1 else self.slider.get_index()
        data = self.model.change_slice(slice_index, axis)

        data = self.interpolation.interpolate(data)
        data = self.interpolation.smooth(data)

        self.plot_item.plot(data)
        self.crosshair.update_label()

    def change_axis(self, axis):

        # 'axes' is a copy of all axes except the one with index 'axis'
        axes = [a for i, a in enumerate(self.model.data.axes) if i != axis]

        index = self.slider.get_index()
        data = self.model.change_slice(index, axis)

        self.plot_item.set_labels(axes[1], axes[0])
        self.interpolation.set_label(axes[1], axes[0])
        self.plot_item.plot(data)

    def crosshair_changed(self):

        self.crosshair.update_label()

    def display_in_matplotlib(self):

        data = self.model.displayed_plot_data
        LUT = self.plot_item.get_LUT()

        window = MatplotlibWindow(data, LUT=LUT)

        return window

    def closeEvent(self, event):

        del self.model

        Tab.closeEvent(self, event)

    def to_string(self):

        text = self.model.to_string()

        return text

    def get_displayed_plot_data(self):

        return self.model.displayed_plot_data

    def get_crosshair(self):

        return self.crosshair

    def get_plot_labels(self):

        bottom = self.plot_item.get_label('bottom')
        left = self.plot_item.get_label('left')
        return bottom, left

    def transpose(self, constant_axis):

        self.model.transpose(constant_axis)
        self.change_axis(self.slider.get_axis())

    def _setup(self):

        self.slider = DataSlider(self.model.data)
        self.crosshair = CrosshairAnnulus(self.plot_item)
        self.colormap = Colormap(self.plot_item)
        self.interpolation = Interpolation()

        layout = self.scroll_area.widget().layout()
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.colormap)
        layout.insertWidget(2, self.crosshair)
        layout.insertWidget(3, self.interpolation)

        # Set Title
        data = self.model.data

        if data:
            id_ = data.ID

            if 'alias' in data.meta_data:
                text = data.meta_data['alias']
            else:
                text = data.name

            self.title = '%s (%i)' % (text, id_)

        else:
            self.title = 'NO DATA'

    def _connect(self):

        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.slider.slice_changed.connect(self.change_slice)
        self.slider.axis_changed.connect(self.change_axis)
        self.slider.tranpose_triggered.connect(self.transpose)
        self.interpolation.smoothing_changed.connect(self.change_slice)
        self.interpolation.interpolation_changed.connect(self.change_slice)
